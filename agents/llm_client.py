"""
LLM Client Utility Module
Handles 3 LLM providers with ENV-only configuration:
1. Cerebras (Primary) - Fast inference
2. OpenRouter (Fallback 2) - Reliable alternative
3. Mistral (Fallback 3) - Final fallback

ALL MODEL CONFIGURATIONS ARE FROM ENV VARIABLES ONLY.
No hardcoded values in code.

Required ENV variables:
- CEREBRAS_API_KEY, CEREBRAS_MODEL
- OPENROUTER_API_KEY, OPENROUTER_MODEL
- MISTRAL_API_KEY, MISTRAL_MODEL

See .env.example for full configuration options.
"""

import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    from cerebras.cloud.sdk import Cerebras

    CEREBRAS_AVAILABLE = True
except ImportError:
    CEREBRAS_AVAILABLE = False
    print("⚠️ Cerebras SDK not installed. Will use Mistral only.")

try:
    from mistralai import Mistral

    MISTRAL_AVAILABLE = True
except ImportError:
    MISTRAL_AVAILABLE = False
    print("⚠️ Mistral SDK not installed.")

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("⚠️ Requests library not installed.")


class LLMClient:
    """
    Unified LLM client that uses Cerebras Qwen Code as primary
    and falls back to Mistral on errors
    """

    def __init__(self):
        self.cerebras_client = None
        self.mistral_client = None
        self.openrouter_api_key = None

        # Initialize Cerebras client
        if CEREBRAS_AVAILABLE:
            cerebras_api_key = os.environ.get("CEREBRAS_API_KEY")
            if cerebras_api_key and cerebras_api_key != "your_cerebras_api_key_here":
                try:
                    self.cerebras_client = Cerebras(api_key=cerebras_api_key)
                    print("✅ Cerebras Qwen Code client initialized")
                except Exception as e:
                    print(f"❌ Failed to initialize Cerebras: {e}")
            else:
                print("⚠️ Cerebras API key not found or not set")

        # Initialize OpenRouter API key (fallback 2)
        if REQUESTS_AVAILABLE:
            openrouter_key = os.environ.get("OPENROUTER_API_KEY")
            if openrouter_key:
                self.openrouter_api_key = openrouter_key
                print("✅ OpenRouter API key loaded (fallback 2)")
            else:
                print("⚠️ OpenRouter API key not found")

        # Initialize Mistral client (fallback 3)
        if MISTRAL_AVAILABLE:
            mistral_api_key = os.environ.get("MISTRAL_API_KEY")
            if mistral_api_key:
                try:
                    self.mistral_client = Mistral(api_key=mistral_api_key)
                    print("✅ Mistral client initialized (fallback 3)")
                except Exception as e:
                    print(f"❌ Failed to initialize Mistral: {e}")
            else:
                print("⚠️ Mistral API key not found")

    def generate_response(self, system_prompt: str, user_prompt: str, **kwargs) -> str:
        """
        Generate response using Cerebras first, then OpenRouter, then Mistral

        Args:
            system_prompt: System message content
            user_prompt: User message content
            **kwargs: Additional parameters (temperature, max_tokens, etc.)

        Returns:
            Generated response string
        """

        # Try Cerebras first
        if self.cerebras_client:
            try:
                return self._generate_cerebras(system_prompt, user_prompt, **kwargs)
            except Exception as e:
                print(f"❌ Cerebras failed: {e}")
                print("🔄 Falling back to OpenRouter...")

        # Fallback to OpenRouter
        if self.openrouter_api_key:
            try:
                return self._generate_openrouter(system_prompt, user_prompt, **kwargs)
            except Exception as e:
                print(f"❌ OpenRouter failed: {e}")
                print("🔄 Falling back to Mistral...")

        # Fallback to Mistral
        if self.mistral_client:
            try:
                return self._generate_mistral(system_prompt, user_prompt, **kwargs)
            except Exception as e:
                print(f"❌ Mistral failed: {e}")
                raise Exception("All LLM providers (Cerebras, OpenRouter, Mistral) failed")

        raise Exception("No LLM clients available")

    def _generate_cerebras(self, system_prompt: str, user_prompt: str, **kwargs) -> str:
        """Generate response using Cerebras - ALL CONFIG FROM ENV"""
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": user_prompt})

        # Get model from ENV or kwargs (NO hardcoded defaults)
        model = kwargs.get("model") or os.environ.get("CEREBRAS_MODEL")
        if not model:
            raise Exception("CEREBRAS_MODEL not set in ENV and not provided in kwargs")

        # Cerebras configuration - all from ENV
        config = {
            "messages": messages,
            "model": model,
            "stream": True,
            "max_completion_tokens": kwargs.get("max_tokens", int(os.environ.get("CEREBRAS_MAX_TOKENS", "40000"))),
            "temperature": kwargs.get("temperature", float(os.environ.get("CEREBRAS_TEMPERATURE", "0.7"))),
            "top_p": kwargs.get("top_p", float(os.environ.get("CEREBRAS_TOP_P", "0.8"))),
        }

        stream = self.cerebras_client.chat.completions.create(**config)

        # Collect streamed response
        response_content = ""
        for chunk in stream:
            if chunk.choices[0].delta.content:
                response_content += chunk.choices[0].delta.content

        return response_content.strip()

    def _generate_openrouter(self, system_prompt: str, user_prompt: str, **kwargs) -> str:
        """Generate response using OpenRouter API - ALL CONFIG FROM ENV"""
        import json
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_prompt})
        
        # Get model from ENV or kwargs (NO hardcoded defaults)
        model = kwargs.get("model") or os.environ.get("OPENROUTER_MODEL")
        if not model:
            raise Exception("OPENROUTER_MODEL not set in ENV and not provided in kwargs")
        
        # Get provider preference from ENV (optional)
        provider_order = os.environ.get("OPENROUTER_PROVIDER_ORDER", "cerebras").split(",")
        allow_fallbacks = os.environ.get("OPENROUTER_ALLOW_FALLBACKS", "false").lower() == "true"
        
        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.openrouter_api_key}",
                    "HTTP-Referer": os.environ.get("OPENROUTER_REFERER", "https://github.com/genlaravel"),
                    "X-Title": os.environ.get("OPENROUTER_TITLE", "GenLaravel"),
                    "Content-Type": "application/json"
                },
                data=json.dumps({
                    "model": model,
                    "messages": messages,
                    "temperature": kwargs.get("temperature", 0.7),
                    "max_tokens": kwargs.get("max_tokens", 40000),
                    "provider": {
                        "order": provider_order,
                        "allow_fallbacks": allow_fallbacks
                    }
                }),
                timeout=int(os.environ.get("OPENROUTER_TIMEOUT", "120"))
            )
            
            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}: {response.text[:300]}")
            
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
            
        except json.JSONDecodeError as e:
            print(f"❌ OpenRouter JSON error: {response.text[:500]}")
            raise Exception(f"Invalid JSON: {str(e)}")
        except Exception as e:
            raise Exception(f"OpenRouter error: {str(e)}")

    def _generate_mistral(self, system_prompt: str, user_prompt: str, **kwargs) -> str:
        """Generate response using Mistral with streaming - ALL CONFIG FROM ENV"""
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": user_prompt})

        # Get model from ENV or kwargs (NO hardcoded defaults)
        model = kwargs.get("model") or os.environ.get("MISTRAL_MODEL")
        if not model:
            raise Exception("MISTRAL_MODEL not set in ENV and not provided in kwargs")

        # Use streaming approach
        stream_response = self.mistral_client.chat.stream(
            model=model, messages=messages
        )

        full_response = ""
        for chunk in stream_response:
            content = chunk.data.choices[0].delta.content
            if content:
                full_response += content

        return full_response.strip()


# Global LLM client instance
llm_client = LLMClient()


def get_llm_response(system_prompt: str, user_prompt: str, **kwargs) -> str:
    """
    Convenience function to get LLM response

    Args:
        system_prompt: System message content
        user_prompt: User message content
        **kwargs: Additional parameters

    Returns:
        Generated response string
    """
    return llm_client.generate_response(system_prompt, user_prompt, **kwargs)
