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
from typing import Optional, Dict, Any, List
from xmlrpc import client

import yaml
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class LLMService:
    def __init__(self, config_path: str = None, provider: str = None, model: str = None, api_key: str = None):
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), "../configs/model_config.yaml")

        self.config: Dict[str, Any] = {
            "LLM": {
                "provider": "gemini",
                "model": "gemini-2.0-flash-001",
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
        
        # Cho phép ghi đè provider và model khi khởi tạo
        self.provider = provider if provider else llm_cfg.get("provider", "gemini")
        self.model = model if model else llm_cfg.get("model", "gemini-2.0-flash-001")
        
        self.temperature = llm_cfg.get("temperature", 0.2)
        self.max_tokens = llm_cfg.get("max_tokens", 1024)

        # Quản lý API keys cho nhiều provider
        self.api_keys = {
            "openai": os.getenv("OPENAI_API_KEY") or os.getenv("LLM_API_KEY"),
            "gemini": os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"),
            "anthropic": os.getenv("ANTHROPIC_API_KEY"),
            "groq": os.getenv("GROQ_API_KEY")
        }
        
        # Cho phép override API key cho provider hiện tại
        if api_key:
            self.api_keys[self.provider] = api_key
            
    def get_api_key(self, provider: str = None) -> Optional[str]:
        """Lấy API key cho provider, trả về None nếu không có."""
        target_provider = provider if provider else self.provider
        return self.api_keys.get(target_provider)
    
    def set_api_key(self, provider: str, api_key: str):
        """Set API key cho provider cụ thể."""
        self.api_keys[provider] = api_key
        
    def validate_api_key(self, provider: str = None) -> bool:
        """Kiểm tra xem API key có tồn tại cho provider không."""
        key = self.get_api_key(provider)
        return bool(key and len(key.strip()) > 0)
    
    def _mock_response(self, prompt: str, provider: str) -> str:
        """Generate mock response when API is unavailable."""
        # Extract ticker for ticker extraction prompts
        if "Extract the stock ticker symbol" in prompt:
            import re
            matches = re.findall(r"'([^']*)'" , prompt)
            if matches:
                query = matches[0].upper()
                for t in ["AAPL", "MSFT", "GOOGL", "NVDA", "TSLA", "BTC-USD", "GC=F"]:
                    if t in query:
                        return t
            # Default tickers by provider for variety
            defaults = {
                "Gemini": "AAPL",
                "OpenAI": "MSFT",
                "Anthropic": "GOOGL",
                "Groq": "NVDA"
            }
            return defaults.get(provider, "AAPL")
        
        # Generic analysis response
        return f"[MOCK {provider}] Phân tích dựa trên các chỉ số kỹ thuật và tin tức gần đây cho thấy xu hướng tích cực với mức độ tin cậy vừa phải. Khuyến nghị theo dõi thêm các yếu tố vĩ mô."

    def call_llm(self, prompt: str, temperature: Optional[float] = None, max_tokens: Optional[int] = None, provider: str = None, model: str = None) -> str:
        """
        Gửi prompt tới LLM, hỗ trợ đổi provider/model linh hoạt trên từng shot.
        """
        target_provider = provider if provider else self.provider
        target_model = model if model else self.model
        
        temp = self.temperature if temperature is None else temperature
        tokens = self.max_tokens if max_tokens is None else max_tokens

        if target_provider == "gemini":
            return self._call_gemini(prompt, target_model, temp, tokens)
        if target_provider == "openai":
            return self._call_openai(prompt, target_model, temp, tokens)
        if target_provider == "anthropic":
            return self._call_anthropic(prompt, target_model, temp, tokens)
        if target_provider == "groq":
            return self._call_groq(prompt, target_model, temp, tokens)
            
        raise ValueError(f"Unsupported LLM provider: {target_provider}")

    def _call_gemini(self, prompt: str, model: str, temperature: float, max_tokens: int) -> str:
        """Call Google Gemini API."""
        api_key = self.get_api_key("gemini")
        
        if not api_key:
            print("⚠️  No Gemini API key found. Using mock response.")
            return self._mock_response(prompt, "Gemini")
        
        try:
            from google import genai
            from google.genai import types
            client = genai.Client(api_key=api_key)
            print("List of models that support generateContent:\n")
            for m in client.models.list():
                for action in m.supported_actions:
                    if action == "generateContent":
                        print(m.name)

            # print("List of models that support embedContent:\n")
            # for m in client.models.list():
            #     for action in m.supported_actions:
            #         if action == "embedContent":
            #             print(m.name)
            resp = client.models.generate_content(
            model="gemma-3-27b-it",
            contents=prompt,
            config=types.GenerateContentConfig(
               # system_instruction="Be concise and practical.",
                temperature=temperature,
                max_output_tokens=max_tokens,
            ),
        )
            return resp.text.strip()
            
        except ImportError:
            print("⚠️  google-generativeai not installed. Run: pip install google-generativeai")
            return self._mock_response(prompt, "Gemini")
        except Exception as e:
            print(f"⚠️  Gemini API error: {e}")
            return self._mock_response(prompt, "Gemini")

    def _call_openai(self, prompt: str, model: str, temperature: float, max_tokens: int) -> str:
        """Call OpenAI API (GPT models)."""
        api_key = self.get_api_key("openai")
        
        if not api_key:
            return self._mock_response(prompt, "OpenAI")
        
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=api_key)
            
            # Map model names
            model_name = model or "gpt-3.5-turbo"
            
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful financial analysis assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content.strip()
            
        except ImportError:
            print("⚠️  openai not installed. Run: pip install openai")
            return self._mock_response(prompt, "OpenAI")
        except Exception as e:
            print(f"⚠️  OpenAI API error: {e}")
            return self._mock_response(prompt, "OpenAI")

    def _call_anthropic(self, prompt: str, model: str, temperature: float, max_tokens: int) -> str:
        """Call Anthropic Claude API."""
        api_key = self.get_api_key("anthropic")
        
        if not api_key:
            return self._mock_response(prompt, "Anthropic")
        
        try:
            from anthropic import Anthropic
            
            client = Anthropic(api_key=api_key)
            
            # Map model names
            model_name = model or "claude-3-sonnet-20240229"
            
            response = client.messages.create(
                model=model_name,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return response.content[0].text.strip()
            
        except ImportError:
            print("⚠️  anthropic not installed. Run: pip install anthropic")
            return self._mock_response(prompt, "Anthropic")
        except Exception as e:
            print(f"⚠️  Anthropic API error: {e}")
            return self._mock_response(prompt, "Anthropic")

    def _call_groq(self, prompt: str, model: str, temperature: float, max_tokens: int) -> str:
        """Call Groq API (fast inference)."""
        api_key = self.get_api_key("groq")
        
        if not api_key:
            return self._mock_response(prompt, "Groq")
        
        try:
            from groq import Groq
            
            client = Groq(api_key=api_key)
            
            # Map model names
            model_name = model or "llama-3.1-70b-versatile"
            
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful financial analysis assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content.strip()
            
        except ImportError:
            print("⚠️  groq not installed. Run: pip install groq")
            return self._mock_response(prompt, "Groq")
        except Exception as e:
            print(f"⚠️  Groq API error: {e}")
            return self._mock_response(prompt, "Groq")

    def structured_call(self, prompt: str, json_schema: Dict[str, Any], provider: str = None, model: str = None) -> Dict[str, Any]:
        """
        Gửi prompt và nhận structured output (dạng JSON) từ LLM.

        MVP: gọi call_llm rồi thử json.loads.
        Khi triển khai thật: dùng function calling / tools.
        """
        response_text = self.call_llm(prompt, provider=provider, model=model)

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
if __name__ == "__main__":
    # Simple test
    llm = LLMService()
    prompt = "'What is the current price of Apple Inc. (AAPL)?'"
    result = llm.call_llm(prompt)
    print(f"Prompt: {prompt}")
    print(f"LLM Response: {result}")