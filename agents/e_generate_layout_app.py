import os, sys
import re
from dotenv import load_dotenv
from mistralai import Mistral

# Load .env
load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")
model = "codestral-latest"
client = Mistral(api_key=api_key)

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

    stream_response = client.chat.stream(
        model=model,
        messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
        ]
    )

    full_response = ""
    prev_len = 0

    for chunk in stream_response:
        content = chunk.data.choices[0].delta.content
        if content:
            full_response += content  # Simpan utuh (termasuk \n)

            # Untuk tampil sementara: hanya karakter terbaru, bersihkan newline
            sanitized = content.replace("\n", " ").replace("\r", " ")
            pad = max(prev_len - len(sanitized), 0)
            sys.stdout.write("\r" + sanitized + " " * pad)
            sys.stdout.flush()
            prev_len = len(sanitized)

    match = re.findall(r"```blade\s*(.*?)```", full_response, re.DOTALL | re.IGNORECASE)
    output_path = "output/layouts/app.blade.php"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(match[0].strip() if match else full_response.strip())
        
    return match[0].strip() if match else full_response.strip()