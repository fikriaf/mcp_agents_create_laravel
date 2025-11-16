import json
from dotenv import load_dotenv

# Load .env file
load_dotenv()


def prompt_expander(user_prompt: str):
    print("\n🟠 [PROMPT EXPANDER] describing prompt...")

    try:
        # Coba cek apakah ini revisi
        prompt_history = json.loads(user_prompt)
        current_prompt = prompt_history.get("prompt", "")
        again = prompt_history.get("again", False)
    except Exception:
        # Jika bukan JSON, anggap prompt asli
        current_prompt = user_prompt
        again = False

    # Buat prompt system untuk mendetailkan
    sys_prompt = (
        "You are a professional UI designer AI. "
        "Your task is to transform the user's brief request into a highly detailed, clear, and specific UI description that can be directly used by developers."
    )

    # Use the new LLM client with Cerebras/Mistral fallback
    from agents.llm_client import get_llm_response

    try:
        full_response = get_llm_response(
            system_prompt=sys_prompt,
            user_prompt=current_prompt,
            max_tokens=32000,
            temperature=0.7,
        )

        print("\n✅ Prompt expanded successfully")

    except Exception as e:
        print(f"\n❌ Error expanding prompt: {e}")
        # Fallback to original prompt if expansion fails
        full_response = current_prompt

    return {
        "history": user_prompt if again else None,
        "new_prompt": full_response.strip(),
    }
