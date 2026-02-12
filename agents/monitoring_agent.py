"""
agents/monitoring_agent.py
MonitoringAgent: Giám sát chất lượng output, validate recommendations, error tracking.

LangGraph-ready:
- Hỗ trợ gate trước notify: node_gate(state) -> state
- execute() chấp nhận cả:
  - {'agent_output': {...}} (legacy)
  - {'state': {...}} hoặc trực tiếp state dict (LangGraph)
"""
from __future__ import annotations

from typing import Optional, Dict, Any, List
from agents.base_agent import Agent


class MonitoringAgent(Agent):
    """
    Agent giám sát chất lượng và consistency của output từ các agent khác.

    Trách nhiệm:
    1. Validate recommendation logic
    2. Check consistency với recommendations trước đó
    3. Error detection & logging
    4. Generate quality report
    5. Gate trước notify (LangGraph)
    """

    def __init__(self, config_path: str = None, **kwargs):
        super().__init__(
            name="MonitoringAgent",
            description="Giám sát chất lượng output, validate recommendations.",
            config_path=config_path,
            **kwargs,
        )
        self.quality_metrics: Dict[str, Any] = {
            "total_validations": 0,
            "passed": 0,
            "failed": 0,
            "warnings": [],
        }
        self.recommendation_history: List[Dict[str, Any]] = []

        # Gate policy (có thể override trong configs/model_config.yaml -> AGENTS.MonitoringAgent)
        self.min_confidence_to_notify: float = 0.60
        self.block_rumor_notify: bool = True
        self.block_unverified_trade_action: bool = True

        cfg = getattr(self.llm_service, "config", {}) or {}
        agent_cfg = (cfg.get("AGENTS", {}) or {}).get("MonitoringAgent", {})
        for k in ["min_confidence_to_notify", "block_rumor_notify", "block_unverified_trade_action"]:
            if k in agent_cfg:
                setattr(self, k, agent_cfg[k])

    def execute(self, task: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Validate output từ SentimentAgent và các agent khác.

        Hỗ trợ 3 kiểu input:
        - Legacy: task={'agent_output': Dict, 'action': 'validate'}
        - LangGraph: task={'state': Dict}
        - LangGraph: task chính là state Dict

        Returns (legacy validation result):
            {
                'is_valid': bool,
                'quality_score': float,
                'issues': List[str],
                'warnings': List[str],
                'recommendations_for_fix': List[str],
                'safe_to_notify': bool
            }
        """
        agent_output = None
        if isinstance(task, dict) and "agent_output" in task:
            agent_output = task.get("agent_output")
        elif isinstance(task, dict) and "state" in task:
            agent_output = task.get("state")
        else:
            agent_output = task

        if not agent_output:
            return {"error": "No agent output provided"}

        # STEP 1: Validate structure
        structure_issues = self._validate_structure(agent_output)

        # STEP 2: Validate logic
        logic_issues = self._validate_logic(agent_output, context)

        # STEP 3: Check consistency with history
        consistency_issues = self._check_consistency(agent_output)

        # STEP 4: Calculate quality score
        quality_score = self._calculate_quality_score(structure_issues, logic_issues, consistency_issues)

        all_issues = structure_issues + logic_issues + consistency_issues
        is_valid = quality_score > 0.7  # Threshold: 70%

        # Gate decision (để dùng trước notify)
        safe_to_notify = self._gate_policy(agent_output, is_valid)

        result = {
            "is_valid": bool(is_valid),
            "quality_score": float(quality_score),
            "issues": all_issues,
            "warnings": self.quality_metrics["warnings"],
            "recommendations_for_fix": self._suggest_fixes(all_issues),
            "safe_to_notify": bool(safe_to_notify),
        }

        self.log_execution(task, result, "success")
        self._update_metrics(bool(is_valid))

        return result

    # -------- LangGraph helper: gate node --------
    def node_gate(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Dùng như node ngay trước notify.

        Input: state sau SentimentAgent (có should_alert, recommendation, verification...)
        Output: state + state['monitoring'] + có thể chỉnh:
          - should_alert False
          - recommendation.action downgrade (Sell/BuyMore -> Hold) nếu chưa verified
          - alert_message None nếu bị block
        """
        validation = self.execute({"state": state}, context=state)
        monitoring = {
            "is_valid": validation.get("is_valid", False),
            "quality_score": validation.get("quality_score", 0.0),
            "issues": validation.get("issues", []),
            "warnings": validation.get("warnings", []),
            "safe_to_notify": validation.get("safe_to_notify", False),
        }
        state["monitoring"] = monitoring

        # Apply gate
        if not monitoring["safe_to_notify"]:
            state["should_alert"] = False
            state["alert_message"] = None

        return state

    # -------- Internal checks --------
    def _validate_structure(self, agent_output: Dict[str, Any]) -> List[str]:
        issues: List[str] = []
        required_fields = ["sentiment_score", "verification", "impact", "recommendation", "should_alert"]

        for field in required_fields:
            if field not in agent_output:
                issues.append(f"Missing required field: {field}")

        # Validate data types
        if "sentiment_score" in agent_output:
            if not isinstance(agent_output["sentiment_score"], (int, float)):
                issues.append("sentiment_score must be a number")
            elif not (-1.0 <= float(agent_output["sentiment_score"]) <= 1.0):
                issues.append("sentiment_score must be between -1.0 and 1.0")

        if "should_alert" in agent_output:
            if not isinstance(agent_output["should_alert"], bool):
                issues.append("should_alert must be a boolean")

        return issues

    def _validate_logic(self, agent_output: Dict[str, Any], context: Optional[Dict[str, Any]]) -> List[str]:
        issues: List[str] = []

        impact = agent_output.get("impact", {}) or {}
        impact_pct = float(impact.get("estimated_impact_pct", 0) or 0)
        sentiment = float(agent_output.get("sentiment_score", 0) or 0)
        urgency = (agent_output.get("recommendation", {}) or {}).get("urgency", "Unknown")

        # Rule 1: Nếu impact > 7% và sentiment < -0.7 thì urgency phải HIGH
        if abs(impact_pct) > 7 and sentiment < -0.7:
            if urgency != "High":
                issues.append(
                    f"Logic error: High impact ({abs(impact_pct):.1f}%) and negative sentiment ({sentiment:.1f}) "
                    f"should have HIGH urgency, not {urgency}"
                )

        # Rule 2: Nếu action = "Sell" thì sentiment phải negative (đủ mạnh)
        action = (agent_output.get("recommendation", {}) or {}).get("action", "Hold")
        if action == "Sell" and sentiment > -0.3:
            issues.append(f"Logic error: Sell action requires negative sentiment, got {sentiment:.1f}")

        # Rule 3: Confidence score phải > 0.5 nếu should_alert = True
        confidence = float((agent_output.get("recommendation", {}) or {}).get("confidence", 0) or 0)
        should_alert = bool(agent_output.get("should_alert", False))
        if should_alert and confidence < 0.5:
            issues.append(f"Logic error: Alert with low confidence ({confidence:.2f}) is risky")

        return issues

    def _check_consistency(self, agent_output: Dict[str, Any]) -> List[str]:
        issues: List[str] = []

        recommendation = agent_output.get("recommendation", {}) or {}
        tickers = (agent_output.get("impact", {}) or {}).get("affected_tickers", []) or []
        current_action = recommendation.get("action", "Hold")

        for ticker in tickers:
            for prev_rec in self.recommendation_history:
                if prev_rec.get("ticker") == ticker:
                    prev_action = prev_rec.get("action", "Hold")
                    if prev_action != current_action:
                        issues.append(
                            f"Consistency check: Ticker {ticker} had {prev_action} recommendation recently, now suggests {current_action}"
                        )

        ts = agent_output.get("timestamp_utc") or agent_output.get("timestamp") or "unknown"
        for ticker in tickers:
            self.recommendation_history.append({"ticker": ticker, "action": current_action, "timestamp": ts})

        if len(self.recommendation_history) > 50:
            self.recommendation_history = self.recommendation_history[-50:]

        return issues

    def _calculate_quality_score(
        self, structure_issues: List[str], logic_issues: List[str], consistency_issues: List[str]
    ) -> float:
        total_issues = len(structure_issues) + len(logic_issues) * 2 + len(consistency_issues) * 0.5
        max_issues = 10
        quality_score = max(0.0, 1.0 - (total_issues / max_issues))
        return round(float(quality_score), 2)

    def _suggest_fixes(self, issues: List[str]) -> List[str]:
        suggestions: List[str] = []
        for issue in issues:
            if "Missing required field" in issue:
                suggestions.append("Re-run SentimentAgent with complete config")
            elif "Logic error" in issue:
                suggestions.append("Review recommendation logic in SentimentAgent.node_recommend()")
            elif "Consistency check" in issue:
                suggestions.append("Check if sentiment/market conditions changed - might be valid")
        return suggestions

    def _update_metrics(self, is_valid: bool):
        self.quality_metrics["total_validations"] += 1
        if is_valid:
            self.quality_metrics["passed"] += 1
        else:
            self.quality_metrics["failed"] += 1

    def get_quality_report(self) -> str:
        total = self.quality_metrics["total_validations"]
        passed = self.quality_metrics["passed"]
        failed = self.quality_metrics["failed"]

        if total == 0:
            return "No validations yet."

        pass_rate = (passed / total) * 100.0
        report = f"""
=== QUALITY MONITORING REPORT ===
Total validations: {total}
Passed: {passed} ({pass_rate:.1f}%)
Failed: {failed} ({100-pass_rate:.1f}%)

Warnings: {len(self.quality_metrics['warnings'])}
"""
        if self.quality_metrics["warnings"]:
            report += "\nRecent warnings:\n"
            for warning in self.quality_metrics["warnings"][-5:]:
                report += f"  - {warning}\n"
        return report

    def _gate_policy(self, agent_output: Dict[str, Any], is_valid: bool) -> bool:
        """
        Gate policy trước notify:
        - Nếu Rumor và block_rumor_notify -> block
        - Nếu confidence < min_confidence_to_notify -> block
        - Nếu action Sell/BuyMore nhưng chưa Verified/Social Confirmed và block_unverified_trade_action -> downgrade action về Hold
        - Nếu validation fail -> block
        """
        should_alert = bool(agent_output.get("should_alert", False))
        if not should_alert:
            return False

        verification = agent_output.get("verification", {}) or {}
        v_status = str(verification.get("status", "") or "")
        if self.block_rumor_notify and v_status.lower() == "rumor":
            self.quality_metrics["warnings"].append("Blocked notify: rumor source.")
            return False

        reco = agent_output.get("recommendation", {}) or {}
        conf = float(reco.get("confidence", 0.0) or 0.0)
        if conf < float(self.min_confidence_to_notify):
            self.quality_metrics["warnings"].append(f"Blocked notify: low confidence ({conf:.2f}).")
            return False

        action = str(reco.get("action", "Hold") or "Hold")
        if self.block_unverified_trade_action and action in ("Sell", "BuyMore"):
            if v_status not in ("Verified", "Social Confirmed"):
                reco["action"] = "Hold"
                agent_output["recommendation"] = reco
                self.quality_metrics["warnings"].append("Downgraded action to Hold due to unverified source.")

        if not bool(is_valid):
            self.quality_metrics["warnings"].append("Blocked notify: validation failed.")
            return False

        return True

    def validate_output(self, output: Dict[str, Any]) -> bool:
        required_keys = ["is_valid", "quality_score", "issues"]
        return all(key in output for key in required_keys)
