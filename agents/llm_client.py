"""
LLM Client Utility Module
Handles Cerebras Qwen Code as primary and Mistral as fallback
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


class LLMClient:
    """
    Unified LLM client that uses Cerebras Qwen Code as primary
    and falls back to Mistral on errors
    """

    def __init__(self):
        self.cerebras_client = None
        self.mistral_client = None

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

        # Initialize Mistral client
        if MISTRAL_AVAILABLE:
            mistral_api_key = os.environ.get("MISTRAL_API_KEY")
            if mistral_api_key:
                try:
                    self.mistral_client = Mistral(api_key=mistral_api_key)
                    print("✅ Mistral client initialized (fallback)")
                except Exception as e:
                    print(f"❌ Failed to initialize Mistral: {e}")
            else:
                print("⚠️ Mistral API key not found")

    def generate_response(self, system_prompt: str, user_prompt: str, **kwargs) -> str:
        """
        Generate response using Cerebras first, fallback to Mistral

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
                print("🔄 Falling back to Mistral...")

        # Fallback to Mistral
        if self.mistral_client:
            try:
                return self._generate_mistral(system_prompt, user_prompt, **kwargs)
            except Exception as e:
                print(f"❌ Mistral failed: {e}")
                raise Exception("Both Cerebras and Mistral failed to generate response")

        raise Exception("No LLM clients available")

    def _generate_cerebras(self, system_prompt: str, user_prompt: str, **kwargs) -> str:
        """Generate response using Cerebras Qwen Code"""
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": user_prompt})

        # Cerebras configuration
        config = {
            "messages": messages,
            "model": "zai-glm-4.6",
            "stream": True,
            "max_completion_tokens": kwargs.get("max_tokens", 40000),
            "temperature": kwargs.get("temperature", 0.7),
            "top_p": kwargs.get("top_p", 0.8),
        }

        stream = self.cerebras_client.chat.completions.create(**config)

        # Collect streamed response
        response_content = ""
        for chunk in stream:
            if chunk.choices[0].delta.content:
                response_content += chunk.choices[0].delta.content

        return response_content.strip()

    def _generate_mistral(self, system_prompt: str, user_prompt: str, **kwargs) -> str:
        """Generate response using Mistral with streaming"""
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": user_prompt})

        # Use streaming approach like in the example
        stream_response = self.mistral_client.chat.stream(
            model=kwargs.get("model", "codestral-latest"), messages=messages
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
