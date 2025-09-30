import os, sys
import re
from dotenv import load_dotenv
from .llm_client import get_llm_response

# Load .env
load_dotenv()


def generate_layout_app(plan: dict, draft_html: str):
    print("\n\n🟣 [LAYOUT AGENT] Generating app layout Blade file...")

    user_prompt = f"""
Create a Laravel Blade layout file named `app.blade.php` using the HTML structure below and considering the following page plan.
Respond ONLY with the content of app.blade.php inside a ```blade code block.

📌 Page name: `{plan['page']}`
📌 Dont create component UI again, because Already Created: `{plan['components']}`

📎 HTML Reference:
```html
{draft_html}
```
"""

    system_prompt = """
You are a Laravel layout generator AI.

Your job is to create a clean, reusable layout Blade file called `app.blade.php`.

Rules:
- ONLY include the layout shell structure:
  - <html>, <head>, <body>
  - Meta tags, title, style, scripts, font links, background wrappers, etc.
- Place @yield('content') where the page content will be injected
- DO NOT include any UI components, inputs, navbars, buttons, or text sections

Respond STRICTLY inside:
```blade
<!-- layout content -->
````
"""

    full_response = get_llm_response(
        system_prompt, user_prompt, temperature=0.7, max_tokens=8000
    )

    match = re.findall(r"```blade\s*(.*?)```", full_response, re.DOTALL | re.IGNORECASE)
    output_path = "output/layouts/app.blade.php"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(match[0].strip() if match else full_response.strip())

    return match[0].strip() if match else full_response.strip()
