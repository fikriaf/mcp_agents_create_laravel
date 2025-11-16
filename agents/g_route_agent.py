import os
import re
from dotenv import load_dotenv
from .llm_client import get_llm_response

# Load .env
load_dotenv()


def generate_route(plan: dict, draft_html: str):
    print("\n\n⚫ [ROUTE AGENT] Generating Laravel routes...")
    
    # Normalize page name to match blade file naming convention
    page_name = plan['page']
    # Convert to lowercase for view name (Laravel is case-insensitive for views)
    view_name = page_name.lower().replace('-', '').replace('_', '')

    user_prompt = f"""
Based on the following HTML structure and page plan, generate the necessary Laravel route declarations.

📌 Page name: `{page_name}`
📌 Route path: `{plan['route']}`
📌 View name: `{view_name}` (this MUST be used in view() function)

📎 HTML Reference:
```html
{draft_html}
```

CRITICAL: Use view('{view_name}') in the route - this matches the blade file name.

Respond ONLY with valid Laravel route definitions using Route::get() in PHP format.
"""
    system_prompt = """
You are a Laravel route generation AI.

Given a page name and HTML layout, generate Laravel route declarations in clean PHP format.

CRITICAL RULES:
- Start with the PHP opening tag `<?php`
- Always include `use Illuminate\\Support\\Facades\\Route;`
- Only use `Route::get()` to return views
- View names MUST be lowercase without dashes or underscores
- Use the EXACT view name provided in the prompt
- Add ->name() for named routes (use kebab-case for route names)
- Do NOT include any explanation or extra text
- Respond ONLY with the complete PHP code wrapped inside a ```php code block

Example:
Route path: /login, View: login → Route::get('/login', function () { return view('login'); })->name('login');
Route path: /user-profile, View: userprofile → Route::get('/user-profile', function () { return view('userprofile'); })->name('user-profile');
"""

    # Use unified LLM client (prioritizes Cerebras, falls back to Mistral)
    try:
        full_response = get_llm_response(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.7,
            max_tokens=32000,
        )

        # Display response character by character for visual feedback
        for char in full_response:
            print(char, end="", flush=True)

    except Exception as e:
        print(f"\n❌ Failed to generate response: {e}")
        return ""

    match = re.findall(r"```php\s*(.*?)```", full_response, re.DOTALL | re.IGNORECASE)
    with open("output/web.php", "w", encoding="utf-8") as f:
        f.write(match[0].strip() if match else full_response.strip())
    return match[0].strip() if match else full_response.strip()
    return match[0].strip() if match else full_response.strip()
