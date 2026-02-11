"""
memory/conversation_memory.py
ConversationMemory: Lưu lịch sử hội thoại, preferences, risk profile của user.

LangGraph-ready:
- Cooldown theo ticker để tránh spam
- Dedup news theo key trong time window
- Timestamp UTC timezone-aware
- load/save an toàn (dirname rỗng, reset history)
"""
from __future__ import annotations

from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
import json
import os
import hashlib


_ALLOWED_RISK = {"Conservative", "Moderate", "Aggressive"}
_ALLOWED_ACTIONS = {"Hold", "Sell", "BuyMore"}


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _utc_now_iso() -> str:
    return _utc_now().isoformat()


def _parse_iso(ts: str) -> Optional[datetime]:
    if not ts:
        return None
    try:
        dt = datetime.fromisoformat(ts)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception:
        return None


def stable_hash(text: str) -> str:
    return hashlib.sha256((text or "").encode("utf-8")).hexdigest()


@dataclass
class ConversationTurn:
    """Một lượt hội thoại (user -> AI)."""
    timestamp: str
    user_message: str
    assistant_response: str
    context: Optional[Dict[str, Any]] = None


@dataclass
class UserProfile:
    """Profile của user bao gồm risk tolerance, preferences."""
    user_id: str
    risk_tolerance: str  # "Conservative", "Moderate", "Aggressive"
    notification_threshold: float  # -0.5 đến -1.0
    preferred_actions: List[str]  # ["Hold", "Sell", "BuyMore"]
    rejected_recommendations: Optional[List[str]] = None

    def __post_init__(self):
        if self.rejected_recommendations is None:
            self.rejected_recommendations = []

        if self.risk_tolerance not in _ALLOWED_RISK:
            self.risk_tolerance = "Moderate"

        try:
            self.notification_threshold = float(self.notification_threshold)
        except Exception:
            self.notification_threshold = -0.5
        self.notification_threshold = max(-1.0, min(0.0, self.notification_threshold))

        self.preferred_actions = [a for a in (self.preferred_actions or []) if a in _ALLOWED_ACTIONS]
        if not self.preferred_actions:
            self.preferred_actions = ["Hold"]


class ConversationMemory:
    """Quản lý lịch sử hội thoại, user preferences, và context."""

    def __init__(self, user_id: str = "default_user"):
        self.user_id = user_id
        self.conversation_history: List[ConversationTurn] = []
        self.user_profile = UserProfile(
            user_id=user_id,
            risk_tolerance="Moderate",
            notification_threshold=-0.5,
            preferred_actions=["Hold", "Sell", "BuyMore"],
        )
        self.max_messages = 100

        # stateful controls
        self.last_alert_at_by_ticker: Dict[str, str] = {}   # ticker -> iso timestamp
        self.seen_news_at: Dict[str, str] = {}              # news_key(hash) -> iso timestamp

    # ---------- user profile ----------
    def set_user_profile(self, risk_tolerance: str, notification_threshold: float, preferred_actions: List[str]):
        self.user_profile = UserProfile(
            user_id=self.user_id,
            risk_tolerance=risk_tolerance,
            notification_threshold=notification_threshold,
            preferred_actions=preferred_actions,
            rejected_recommendations=self.user_profile.rejected_recommendations,
        )

    def get_user_profile(self) -> UserProfile:
        return self.user_profile

    # ---------- conversation turns ----------
    def add_turn(self, user_message: str, assistant_response: str, context: Optional[Dict[str, Any]] = None):
        turn = ConversationTurn(
            timestamp=_utc_now_iso(),
            user_message=user_message,
            assistant_response=assistant_response,
            context=context,
        )
        self.conversation_history.append(turn)
        if len(self.conversation_history) > self.max_messages:
            self.conversation_history = self.conversation_history[-self.max_messages :]

    def get_recent_history(self, n: int = 10) -> List[ConversationTurn]:
        return self.conversation_history[-n:]

    # ---------- recommendation preference ----------
    def reject_recommendation(self, recommendation_id: str):
        if recommendation_id and recommendation_id not in self.user_profile.rejected_recommendations:
            self.user_profile.rejected_recommendations.append(recommendation_id)

    def is_rejected_before(self, recommendation_id: str) -> bool:
        return bool(recommendation_id) and recommendation_id in self.user_profile.rejected_recommendations

    # ---------- cooldown ----------
    def record_alert(
        self,
        tickers: List[str],
        news_id: str,
        recommendation_id: Optional[str] = None,
        summary: str = "",
        metadata: Optional[Dict[str, Any]] = None,
    ):
        ts = _utc_now_iso()
        tickers_norm = [str(t).upper() for t in (tickers or [])]
        for t in tickers_norm:
            self.last_alert_at_by_ticker[t] = ts

        ctx = {
            "event": "alert",
            "tickers": tickers_norm,
            "news_id": news_id,
            "recommendation_id": recommendation_id,
            "metadata": metadata or {},
        }
        self.add_turn(user_message="[system] alert", assistant_response=summary or "", context=ctx)

    def is_in_alert_cooldown(self, tickers: List[str], cooldown_mins: int) -> bool:
        if not tickers or cooldown_mins <= 0:
            return False
        now = _utc_now()
        delta = timedelta(minutes=int(cooldown_mins))
        for t in [str(x).upper() for x in tickers]:
            last_ts = self.last_alert_at_by_ticker.get(t)
            last_dt = _parse_iso(last_ts) if last_ts else None
            if last_dt and (now - last_dt) < delta:
                return True
        return False

    # ---------- dedup news ----------
    def normalize_news_key(self, news_key: str) -> str:
        """
        news_key có thể là news_id hoặc headline+source.
        Để lưu bền vững, ta hash thành sha256.
        """
        return stable_hash(news_key.strip().lower())

    def is_duplicate_news(self, news_key: str, window_mins: int = 60) -> bool:
        if not news_key:
            return False
        key = self.normalize_news_key(news_key)
        last_ts = self.seen_news_at.get(key)
        if not last_ts:
            return False
        last_dt = _parse_iso(last_ts)
        if not last_dt:
            return False
        return (_utc_now() - last_dt) < timedelta(minutes=int(window_mins))

    def mark_news_seen(self, news_key: str):
        if not news_key:
            return
        key = self.normalize_news_key(news_key)
        self.seen_news_at[key] = _utc_now_iso()
        # giới hạn size tránh phình
        if len(self.seen_news_at) > 1000:
            # drop các item cũ nhất (MVP: sort theo timestamp string)
            items = sorted(self.seen_news_at.items(), key=lambda kv: kv[1])
            self.seen_news_at = dict(items[-800:])

    # ---------- persistence ----------
    def save_to_file(self, filepath: str):
        data = {
            "user_id": self.user_id,
            "user_profile": {
                "user_id": self.user_profile.user_id,
                "risk_tolerance": self.user_profile.risk_tolerance,
                "notification_threshold": self.user_profile.notification_threshold,
                "preferred_actions": self.user_profile.preferred_actions,
                "rejected_recommendations": self.user_profile.rejected_recommendations,
            },
            "conversation_history": [
                {
                    "timestamp": t.timestamp,
                    "user_message": t.user_message,
                    "assistant_response": t.assistant_response,
                    "context": t.context,
                }
                for t in self.conversation_history
            ],
            "last_alert_at_by_ticker": self.last_alert_at_by_ticker,
            "seen_news_at": self.seen_news_at,
        }

        dirpath = os.path.dirname(filepath)
        if dirpath:
            os.makedirs(dirpath, exist_ok=True)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load_from_file(self, filepath: str):
        if not os.path.exists(filepath):
            return
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f) or {}

        profile_data = data.get("user_profile", {}) or {}
        self.user_profile = UserProfile(
            user_id=profile_data.get("user_id", self.user_id),
            risk_tolerance=profile_data.get("risk_tolerance", "Moderate"),
            notification_threshold=profile_data.get("notification_threshold", -0.5),
            preferred_actions=profile_data.get("preferred_actions", ["Hold", "Sell", "BuyMore"]),
            rejected_recommendations=profile_data.get("rejected_recommendations", []),
        )

        self.conversation_history = []
        for td in data.get("conversation_history", []) or []:
            self.conversation_history.append(
                ConversationTurn(
                    timestamp=td.get("timestamp", ""),
                    user_message=td.get("user_message", ""),
                    assistant_response=td.get("assistant_response", ""),
                    context=td.get("context"),
                )
            )
        if len(self.conversation_history) > self.max_messages:
            self.conversation_history = self.conversation_history[-self.max_messages :]

        self.last_alert_at_by_ticker = data.get("last_alert_at_by_ticker", {}) or {}
        self.seen_news_at = data.get("seen_news_at", {}) or {}
