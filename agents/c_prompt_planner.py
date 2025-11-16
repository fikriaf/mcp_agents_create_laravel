import re, json
from dotenv import load_dotenv
from agents.llm_client import get_llm_response

# Load .env file
load_dotenv()


def plan_prompt(user_prompt: str):
    print("\n🔵 [PROMPT PLANNER] Interpreting prompt...")

    sys_prompt = """
You are an expert Laravel UI analyst.

Given a user request to create a web page, break it down into a JSON object with:
- "page": the name of the view (string, lowercase)
- "components": list of **distinct and essential** UI component names in PascalCase (e.g., "EmailInput", "LoginButton")
- "route": suggested route path (e.g. "/dashboard")

Guidelines:
- Be minimalist. Only include essential UI components.
- Avoid listing generic HTML tags (like "Input", "Button") — use descriptive and reusable names like "SearchForm" or "AuthCard".
- Group related elements under a higher-level component when possible, e.g., use "LoginForm" instead of listing "EmailInput", "PasswordInput", and "SubmitButton" separately.
- Do NOT duplicate similar components.
- Do NOT create separate components for sub-sections that are part of a larger component (e.g., if you have "ChatArea", do NOT also create "ChatSidebar" or "ChatInput" separately).
- Do NOT include raw HTML, CSS classes, or descriptions — only semantic component names used in Laravel Blade.
- Prefer abstract or high-level components that represent purpose or function (e.g., "Navbar", "TaskCard", "UserProfileSection").
- Each component should be a complete, standalone section of the page.

Respond ONLY with valid JSON, without explanations or formatting. No markdown. No comments.
"""

    # Use the new LLM client with Cerebras/Mistral fallback
    try:
        full_response = get_llm_response(
            system_prompt=sys_prompt,
            user_prompt=user_prompt,
            max_tokens=32000,
            temperature=0.3,  # Lower temperature for more consistent JSON
        )
        print("\n✅ Plan created successfully")

    except Exception as e:
        print(f"\n❌ Error creating plan: {e}")
        # Fallback response
        full_response = '{"page": "unknown", "components": [], "route": "/unknown"}'

    # Ambil hanya blok JSON
    try:
        # Coba parse langsung jika JSON mentah
        parsed = json.loads(full_response)
        return parsed
    except json.JSONDecodeError:
        # Jika ada kata tambahan, ekstrak blok JSON dengan regex
        json_block = re.search(r"\{.*\}", full_response, re.DOTALL)
        if json_block:
            try:
                return json.loads(json_block.group(0))
            except Exception:
                pass

    print("\n[ERROR] Gagal parsing JSON dari model.")
    return {"page": "unknown", "components": [], "route": "/unknown"}
