import re, json, os
from mistralai import Mistral
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Ambil API key dari environment
api_key = os.getenv("MISTRAL_API_KEY")
model = "mistral-large-latest"

client = Mistral(api_key=api_key)

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
- Do NOT include raw HTML, CSS classes, or descriptions — only semantic component names used in Laravel Blade.
- Prefer abstract or high-level components that represent purpose or function (e.g., "Navbar", "TaskCard", "UserProfileSection").

Respond ONLY with valid JSON, without explanations or formatting. No markdown. No comments.
"""


    stream_response = client.chat.stream(
        model=model,
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    full_response = ""

    for chunk in stream_response:
        content = chunk.data.choices[0].delta.content
        if content:
            print(content, end="", flush=True)
            full_response += content

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
            except:
                pass

    print("\n[ERROR] Gagal parsing JSON dari model.")
    return {
        "page": "unknown",
        "components": [],
        "route": "/unknown"
    }
