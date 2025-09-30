import os, sys
import re
from dotenv import load_dotenv
from .llm_client import get_llm_response

# Load API key
load_dotenv()


def list_components(plan: dict, draft_html: str):
    print("\n\n⚪ [COMPONENT AGENT] Generating components...")

    components = plan.get("components", [])
    result = {}

    for comp in components:
        user_prompt = f"""
Create a Laravel Blade partial component named `{comp}`.

Reference HTML layout:
```html
{draft_html}
```
Use only relevant section of the HTML that belongs to {comp}.
Wrap the output inside a Blade partial, e.g., a file named {comp.lower()}.blade.php.

Respond only in:

```blade
<!-- blade content -->
```
"""
        system_prompt = """
You are a Laravel component generator AI.

Your task is to extract and convert relevant HTML into Laravel Blade components.

Return clean Blade markup using Tailwind CSS, and DO NOT include any explanations or markdown outside the code.

Change 'src' image to real link/url
"""

        # Use unified LLM client (prioritizes Cerebras, falls back to Mistral)
        try:
            full_response = get_llm_response(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=0.7,
                max_tokens=8000,
            )

            # Display response character by character for visual feedback
            prev_len = 0
            for i, char in enumerate(full_response):
                # Untuk tampil sementara: hanya karakter terbaru, bersihkan newline
                sanitized = char.replace("\n", " ").replace("\r", " ")
                pad = max(prev_len - len(sanitized), 0)
                sys.stdout.write("\r" + sanitized + " " * pad)
                sys.stdout.flush()
                prev_len = len(sanitized)

        except Exception as e:
            print(f"\n❌ Failed to generate component {comp}: {e}")
            full_response = ""

        match = re.findall(
            r"```blade\s*(.*?)```", full_response, re.DOTALL | re.IGNORECASE
        )
        blade_code = match[0].strip() if match else full_response.strip()

        result[comp] = blade_code

        # ⬇️ Simpan tiap komponen ke file:
        filename = f"output/components/{comp.lower()}.blade.php"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(blade_code)

    return result
