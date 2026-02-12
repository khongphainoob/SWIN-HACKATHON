"""
services/llm_service.py
LLMService: Wrapper cho API Gemini/GPT, dùng chung cho các agent.

MVP hiện tại giả lập response để demo.
Bổ sung:
- Fallback config nếu file yaml không tồn tại
- structured_call cố parse JSON nếu model trả JSON
"""
from __future__ import annotations

import json
import os
from typing import Optional, Dict, Any

import yaml


class LLMService:
    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), "../configs/model_config.yaml")

        self.config: Dict[str, Any] = {
            "LLM": {
                "provider": "openai",
                "model": "gpt-4o-mini",
                "temperature": 0.2,
                "max_tokens": 1024,
            }
        }

        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    loaded = yaml.safe_load(f) or {}
                # merge shallow
                for k, v in loaded.items():
                    self.config[k] = v
            except Exception:
                # giữ default nếu config lỗi
                pass

        llm_cfg = self.config.get("LLM", {}) or {}
        self.provider = llm_cfg.get("provider", "openai")
        self.model = llm_cfg.get("model", "gpt-4o-mini")
        self.temperature = llm_cfg.get("temperature", 0.2)
        self.max_tokens = llm_cfg.get("max_tokens", 1024)

        # Lấy API key từ env (không hardcode)
        self.api_key = os.getenv("LLM_API_KEY")

    def call_llm(self, prompt: str, temperature: Optional[float] = None, max_tokens: Optional[int] = None) -> str:
        """
        Gửi prompt tới LLM (Gemini/OpenAI), trả về response text.
        MVP: stub.
        """
        temperature = self.temperature if temperature is None else temperature
        max_tokens = self.max_tokens if max_tokens is None else max_tokens

        if self.provider == "gemini":
            return self._call_gemini(prompt, temperature, max_tokens)
        if self.provider == "openai":
            return self._call_openai(prompt, temperature, max_tokens)
        raise ValueError(f"Unsupported LLM provider: {self.provider}")

    def _call_gemini(self, prompt: str, temperature: float, max_tokens: int) -> str:
        # TODO: Thay thế bằng code gọi Gemini API thực tế
        return f"[Gemini:{self.model}] {prompt[:200]}..."

    def _call_openai(self, prompt: str, temperature: float, max_tokens: int) -> str:
        # TODO: Thay thế bằng code gọi OpenAI API thực tế
        return f"[OpenAI:{self.model}] {prompt[:200]}..."

    def structured_call(self, prompt: str, json_schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gửi prompt và nhận structured output (dạng JSON) từ LLM.

        MVP: gọi call_llm rồi thử json.loads.
        Khi triển khai thật: dùng function calling / tools.
        """
        response_text = self.call_llm(prompt)

        # Try parse JSON nếu response là JSON
        try:
            parsed = json.loads(response_text)
            if isinstance(parsed, dict):
                return parsed
        except Exception:
            pass

        return {"response": response_text, "schema": json_schema}

    def count_tokens(self, text: str) -> int:
        """Đếm tokens (MVP): xấp xỉ bằng số từ."""
        return len((text or "").split())
