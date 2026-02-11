"""
agents/custom/sentiment_agent.py
SentimentAgent: CORE agent - Phân tích sentiment tin tức, xác thực chéo, tính impact, tạo recommendation.

LangGraph-ready:
- Node-hoá pipeline: mỗi bước là 1 hàm state in/out
- Có execute() legacy vẫn chạy tuần tự bằng các node functions
"""
from __future__ import annotations

import re
from typing import Optional, Dict, Any, List

from agents.base_agent import Agent
from memory.vector_memory import PortfolioItem


def _safe_lower(x: Any) -> str:
    return str(x or "").lower()


def _token_hits(text: str, keywords: List[str]) -> int:
    """
    Đếm keyword theo word-boundary để tránh lỗi kiểu 'up' khớp trong 'bankruptcy'.
    Với phrase (có space), vẫn dùng boundary ở 2 đầu.
    """
    if not text:
        return 0
    hits = 0
    for kw in keywords:
        kw = kw.strip().lower()
        if not kw:
            continue
        pattern = rf"\b{re.escape(kw)}\b"
        if re.search(pattern, text):
            hits += 1
    return hits


class SentimentAgent(Agent):
    """
    Pipeline:
    1) node_prepare_context
    2) node_sentiment_score
    3) node_cross_verify
    4) node_impact_calc
    5) node_recommend
    6) node_noise_filter
    7) node_build_alert (+ record cooldown)
    """

    def __init__(self, config_path: str = None, **kwargs):
        super().__init__(
            name="SentimentAgent",
            description="Phân tích sentiment tin tức tài chính và tạo recommendations.",
            config_path=config_path,
            **kwargs,
        )
        # Defaults (có thể override từ configs/model_config.yaml nếu bạn thêm AGENTS.SentimentAgent)
        self.sentiment_threshold = -0.5
        self.noise_filter_threshold = 0.60  # min verification confidence để coi là đáng tin
        self.verified_source_boost = 1.15
        self.rumor_penalty = 0.50
        self.high_urgency_threshold = 2.5  # theo % impact danh mục
        self.alert_cooldown_mins = 30
        self.dedup_window_mins = 60

        cfg = getattr(self.llm_service, "config", {}) or {}
        agent_cfg = (cfg.get("AGENTS", {}) or {}).get("SentimentAgent", {})
        for k in [
            "sentiment_threshold",
            "noise_filter_threshold",
            "verified_source_boost",
            "rumor_penalty",
            "high_urgency_threshold",
            "alert_cooldown_mins",
            "dedup_window_mins",
        ]:
            if k in agent_cfg:
                setattr(self, k, agent_cfg[k])

    # ----------------- Legacy execute (giữ tương thích) -----------------
    def execute(self, task: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        news = (task or {}).get("news")
        if not news:
            return {"error": "No news provided"}

        state: Dict[str, Any] = {
            "news": news,
        }
        if context:
            state.update(context)

        # chạy tuần tự bằng nodes
        state = self.node_prepare_context(state)
        state = self.node_sentiment_score(state)
        state = self.node_cross_verify(state)
        state = self.node_impact_calc(state)
        state = self.node_recommend(state)
        state = self.node_noise_filter(state)
        state = self.node_build_alert(state)

        # output theo format cũ
        result = {
            "news_id": getattr(news, "news_id", "unknown"),
            "headline": getattr(news, "headline", ""),
            "sentiment_score": state.get("sentiment_score", 0.0),
            "verification": state.get("verification", {}),
            "impact": state.get("impact", {}),
            "recommendation": state.get("recommendation", {}),
            "should_alert": bool(state.get("should_alert", False)),
            "alert_message": state.get("alert_message"),
        }
        return result

    def validate_output(self, output: Dict[str, Any]) -> bool:
        required_keys = ["sentiment_score", "verification", "impact", "recommendation", "should_alert"]
        return isinstance(output, dict) and all(k in output for k in required_keys)

    # ----------------- Node functions (LangGraph-ready) -----------------
    def node_prepare_context(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Chuẩn hoá state:
        - user_profile: fallback từ conversation_memory
        - portfolio: ưu tiên state['portfolio'], fallback vector_memory.get_portfolio()
        - news_key: phục vụ dedup
        """
        news = state.get("news")
        if not news and "task" in state:
            news = (state.get("task") or {}).get("news")
            state["news"] = news

        # profile
        if "user_profile" not in state or state["user_profile"] is None:
            try:
                state["user_profile"] = self.conversation_memory.get_user_profile()
            except Exception:
                state["user_profile"] = None

        # portfolio
        if "portfolio" not in state or state["portfolio"] is None:
            state["portfolio"] = self.vector_memory.get_portfolio()

        # news_key for dedup
        news_id = getattr(news, "news_id", None)
        headline = getattr(news, "headline", "")
        source = getattr(news, "source", "")
        if news_id:
            state["news_key"] = str(news_id)
        else:
            state["news_key"] = f"{source}:{headline}".strip()

        return state

    def node_sentiment_score(self, state: Dict[str, Any]) -> Dict[str, Any]:
        news = state.get("news")
        headline = _safe_lower(getattr(news, "headline", ""))
        content = _safe_lower(getattr(news, "content", ""))
        text_head = headline
        text_body = content

        negative_keywords = [
            "loss", "miss", "downgrade", "down", "weak", "bankruptcy", "fraud", "decline",
            "crisis", "concern", "lawsuit", "probe", "recall", "default",
        ]
        positive_keywords = [
            "profit", "beat", "upgrade", "up", "growth", "record", "surge", "strong",
            "buyback", "dividend",
        ]

        neg = _token_hits(text_head, negative_keywords) * 2 + _token_hits(text_body, negative_keywords)
        pos = _token_hits(text_head, positive_keywords) * 2 + _token_hits(text_body, positive_keywords)

        if neg + pos == 0:
            score = 0.0
        else:
            score = (pos - neg) / (pos + neg)
            score = max(-1.0, min(1.0, score))

        state["sentiment_score"] = round(score, 2)
        return state

    def node_cross_verify(self, state: Dict[str, Any]) -> Dict[str, Any]:
        news = state.get("news")
        source = _safe_lower(getattr(news, "source", "unknown"))

        trusted_sources = ["reuters", "bloomberg", "ap", "cnbc", "financial times", "wsj"]
        social_sources = ["twitter", "x", "reddit", "seeking alpha", "stocktwits"]

        cross_verified = bool(getattr(news, "cross_verified", False) or getattr(news, "is_verified", False))

        if any(s in source for s in trusted_sources):
            status = "Verified"
            confidence = 0.90
            multiplier = self.verified_source_boost
            tier = "trusted"
        elif any(s in source for s in social_sources):
            if cross_verified:
                status = "Social Confirmed"
                confidence = 0.75
                multiplier = 1.05
            else:
                status = "Unverified"
                confidence = 0.60
                multiplier = 1.00
            tier = "social"
        else:
            status = "Rumor"
            confidence = 0.35
            multiplier = self.rumor_penalty
            tier = "unknown"

        state["verification"] = {
            "status": status,
            "tier": tier,
            "source": source,
            "cross_verified": cross_verified,
            "confidence": confidence,
            "confidence_multiplier": multiplier,
        }
        return state

    def node_impact_calc(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ước tính impact lên danh mục (% portfolio).

        Lưu ý: allocation_pct trong portfolio là 0..100.
        expected_move_pct = 2..10 tuỳ |sentiment| (MVP heuristic).
        impact_pct = sign * expected_move_pct * (allocation_pct/100) * verification_confidence
        """
        news = state.get("news")
        sentiment = float(state.get("sentiment_score", 0.0) or 0.0)
        verification = state.get("verification", {}) or {}
        portfolio: Dict[str, PortfolioItem] = state.get("portfolio") or {}

        tickers = getattr(news, "tickers_mentioned", []) or []
        tickers = [str(t).upper() for t in tickers]

        affected: List[str] = []
        total_alloc_pct = 0.0
        for t in tickers:
            if t in portfolio:
                affected.append(t)
                total_alloc_pct += float(getattr(portfolio[t], "allocation_pct", 0.0) or 0.0)

        if not affected:
            impact = {
                "affected_tickers": [],
                "affected_allocation_pct": 0.0,
                "expected_price_move_pct": 0.0,
                "estimated_impact_pct": 0.0,
                "magnitude": "Low",
                "time_horizon": self._estimate_time_horizon(sentiment),
            }
            state["impact"] = impact
            return state

        expected_move_pct = 2.0 + (abs(sentiment) * 8.0)  # 2..10
        expected_move_pct = round(expected_move_pct, 2)

        alloc_frac = max(0.0, min(1.0, total_alloc_pct / 100.0))
        conf = float(verification.get("confidence", 0.5) or 0.5)
        sign = 1.0 if sentiment >= 0 else -1.0
        impact_pct = round(sign * expected_move_pct * alloc_frac * conf, 2)

        magnitude = "High" if abs(impact_pct) >= 2.5 else "Medium" if abs(impact_pct) >= 1.0 else "Low"

        state["impact"] = {
            "affected_tickers": affected,
            "affected_allocation_pct": round(total_alloc_pct, 2),
            "expected_price_move_pct": expected_move_pct,
            "estimated_impact_pct": impact_pct,
            "magnitude": magnitude,
            "time_horizon": self._estimate_time_horizon(sentiment),
        }
        return state

    def node_recommend(self, state: Dict[str, Any]) -> Dict[str, Any]:
        impact = state.get("impact", {}) or {}
        verification = state.get("verification", {}) or {}
        sentiment = float(state.get("sentiment_score", 0.0) or 0.0)
        user_profile = state.get("user_profile")
        portfolio: Dict[str, PortfolioItem] = state.get("portfolio") or {}

        affected = impact.get("affected_tickers", []) or []
        if not affected:
            state["recommendation"] = {
                "recommendation_id": self._recommendation_id(state.get("news_key", "unknown"), ["NONE"], "Hold"),
                "action": "Hold",
                "reasoning": "Tin tức không ảnh hưởng trực tiếp tới danh mục của bạn.",
                "urgency": "Low",
                "confidence": 0.8,
                "suggested_orders": [],
            }
            return state

        risk = getattr(user_profile, "risk_tolerance", "Moderate") if user_profile else "Moderate"
        preferred_actions = getattr(user_profile, "preferred_actions", ["Hold", "Sell", "BuyMore"]) if user_profile else ["Hold", "Sell", "BuyMore"]

        est_impact = float(impact.get("estimated_impact_pct", 0.0) or 0.0)
        urgency = "High" if abs(est_impact) >= self.high_urgency_threshold else "Medium" if abs(est_impact) >= 1.0 else "Low"

        action = "Hold"
        reasoning = "Giữ danh mục theo kế hoạch và theo dõi thêm dữ liệu."

        if est_impact <= -2.5:
            if risk == "Conservative":
                action = "Sell"
                reasoning = f"Tin có xu hướng tiêu cực (score {sentiment:.2f}) và ước tính ảnh hưởng ~{abs(est_impact):.1f}% danh mục. Bạn ưu tiên an toàn, nên cân nhắc giảm vị thế."
            elif risk == "Aggressive":
                action = "Hold"
                reasoning = f"Tin xấu có thể gây biến động ngắn hạn (~{abs(est_impact):.1f}% danh mục). Bạn mạo hiểm hơn, có thể giữ và chờ xác nhận thêm; tránh phản ứng vội nếu chưa có dữ liệu giá."
            else:
                action = "Hold"
                reasoning = f"Ảnh hưởng ước tính ~{abs(est_impact):.1f}% danh mục. Nên giữ và đặt ngưỡng quản trị rủi ro (stop-loss) thay vì bán gấp."
        elif est_impact >= 2.0:
            if risk == "Aggressive":
                action = "BuyMore"
                reasoning = f"Tin tích cực (score {sentiment:.2f}) có thể hỗ trợ giá. Nếu phù hợp chiến lược, bạn có thể mua tăng thêm có kiểm soát."
            else:
                action = "Hold"
                reasoning = "Tin tích cực, nhưng vẫn nên giữ theo kế hoạch và không đuổi giá."

        if action not in preferred_actions:
            action = "Hold"

        reco_id = self._recommendation_id(state.get("news_key", "unknown"), affected, action)
        if user_profile and self.conversation_memory.is_rejected_before(reco_id):
            action = "Hold"
            reco_id = self._recommendation_id(state.get("news_key", "unknown"), affected, action)
            reasoning = "Bạn từng không chọn khuyến nghị tương tự. Lần này mình đề xuất GIỮ và đặt ngưỡng bảo vệ rủi ro thay vì hành động mạnh."

        suggested_orders = self._suggest_orders(action, affected, portfolio, risk)

        conf = float(verification.get("confidence", 0.5) or 0.5)
        conf = min(0.95, max(0.2, conf + min(0.2, abs(est_impact) / 10)))

        state["recommendation"] = {
            "recommendation_id": reco_id,
            "action": action,
            "reasoning": reasoning,
            "urgency": urgency,
            "confidence": round(conf, 2),
            "suggested_orders": suggested_orders,
        }
        return state

    def node_noise_filter(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Quyết định should_alert dựa trên:
        - affected_tickers
        - verification confidence >= noise_filter_threshold
        - cooldown theo ticker
        - dedup theo news_key
        - sentiment <= threshold & impact >= min_impact theo risk
        """
        impact = state.get("impact", {}) or {}
        verification = state.get("verification", {}) or {}
        user_profile = state.get("user_profile")
        sentiment = float(state.get("sentiment_score", 0.0) or 0.0)

        affected = impact.get("affected_tickers", []) or []
        if not affected:
            state["should_alert"] = False
            return state

        confidence = float(verification.get("confidence", 0.0) or 0.0)
        if confidence < float(self.noise_filter_threshold):
            state["should_alert"] = False
            return state

        # cooldown
        if self.conversation_memory.is_in_alert_cooldown(affected, int(self.alert_cooldown_mins)):
            state["should_alert"] = False
            return state

        # dedup
        news_key = state.get("news_key", "")
        if news_key and self.conversation_memory.is_duplicate_news(news_key, window_mins=int(self.dedup_window_mins)):
            state["should_alert"] = False
            return state

        threshold = float(self.sentiment_threshold)
        if user_profile and hasattr(user_profile, "notification_threshold"):
            threshold = float(getattr(user_profile, "notification_threshold", threshold) or threshold)

        est_impact = abs(float(impact.get("estimated_impact_pct", 0.0) or 0.0))
        risk = getattr(user_profile, "risk_tolerance", "Moderate") if user_profile else "Moderate"
        min_impact = 0.7 if risk == "Conservative" else 1.0 if risk == "Moderate" else 1.3

        state["should_alert"] = (sentiment <= threshold) and (est_impact >= min_impact)
        return state

    def node_build_alert(self, state: Dict[str, Any]) -> Dict[str, Any]:
        if not state.get("should_alert"):
            state["alert_message"] = None
            return state

        impact = state.get("impact", {}) or {}
        reco = state.get("recommendation", {}) or {}
        news = state.get("news")

        tickers = ", ".join(impact.get("affected_tickers", []))
        impact_pct = float(impact.get("estimated_impact_pct", 0.0) or 0.0)

        msg = (
            "📊 SMART ALERT - SENTIMENT ADVISOR\n\n"
            f"Tickers ảnh hưởng: {tickers}\n"
            f"Dự báo impact lên danh mục: {impact_pct:.2f}%\n"
            f"Độ ưu tiên: {reco.get('urgency', 'Medium')}\n\n"
            "📝 Giải thích:\n"
            f"{reco.get('reasoning', '')}\n\n"
            f"💡 Đề xuất: {reco.get('action', 'Hold')}\n"
            f"Tin cậy: {float(reco.get('confidence', 0.7) or 0.7):.0%}\n"
        )
        state["alert_message"] = msg

        # Mark news seen (để dedup) + record cooldown
        news_key = state.get("news_key", "")
        if news_key:
            self.conversation_memory.mark_news_seen(news_key)

        try:
            self.conversation_memory.record_alert(
                tickers=impact.get("affected_tickers", []),
                news_id=getattr(news, "news_id", "unknown"),
                recommendation_id=reco.get("recommendation_id"),
                summary=msg,
                metadata={
                    "sentiment_score": state.get("sentiment_score"),
                    "estimated_impact_pct": impact.get("estimated_impact_pct"),
                    "verification_status": (state.get("verification") or {}).get("status"),
                },
            )
        except Exception:
            pass

        return state

    # ----------------- helpers -----------------
    def _estimate_time_horizon(self, sentiment_score: float) -> str:
        if abs(sentiment_score) >= 0.8:
            return "immediate"
        if abs(sentiment_score) >= 0.5:
            return "short-term"
        return "long-term"

    def _recommendation_id(self, news_key: str, tickers: List[str], action: str) -> str:
        tickers_key = ",".join(sorted([str(t).upper() for t in tickers]))
        return f"{news_key}:{tickers_key}:{action}"

    def _suggest_orders(self, action: str, tickers: List[str], portfolio: Dict[str, PortfolioItem], risk: str) -> List[Dict[str, Any]]:
        orders: List[Dict[str, Any]] = []
        if not tickers:
            return orders

        stop_factor = 0.95 if risk == "Conservative" else 0.92 if risk == "Moderate" else 0.90

        for t in tickers:
            item = portfolio.get(t)
            if not item:
                continue
            price = float(getattr(item, "current_price", 0.0) or 0.0)
            if price <= 0:
                continue
            orders.append(
                {
                    "type": "stop_loss",
                    "ticker": t,
                    "stop_price": round(price * stop_factor, 2),
                    "note": "Gợi ý ngưỡng bảo vệ rủi ro (MVP/heuristic).",
                }
            )
        return orders
