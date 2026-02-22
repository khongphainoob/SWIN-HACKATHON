"""
agents/agent_utils.py
Shared utility functions for all agents.
"""
from datetime import datetime, timezone
from typing import Any, List


def _utc_now_iso() -> str:
    """Get current UTC time in ISO format."""
    return datetime.now(timezone.utc).isoformat()


def print_agent_banner(agent_name: str, step_number: int = 0) -> None:
    """Print a visual banner when an agent starts execution."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print("\n" + "="*70)
    print(f"🤖 AGENT #{step_number}: {agent_name}")
    print(f"⏰ Time: {timestamp}")
    print("="*70)


def print_agent_output(key: str, value: Any, indent: int = 2) -> None:
    """Print agent output in a formatted way."""
    prefix = " " * indent
    if isinstance(value, (dict, list)):
        print(f"{prefix}📤 {key}: {type(value).__name__} ({len(value)} items)")
    elif isinstance(value, (int, float)):
        print(f"{prefix}📤 {key}: {value}")
    else:
        str_val = str(value)
        if len(str_val) > 60:
            str_val = str_val[:57] + "..."
        print(f"{prefix}📤 {key}: {str_val}")


def print_agent_summary(messages: List[str]) -> None:
    """Print agent execution summary."""
    print("✅ Status: Completed")
    for msg in messages:
        print(f"   {msg}")
    print("-" * 70)
