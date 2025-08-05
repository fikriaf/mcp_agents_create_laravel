import os, sys
import re
from dotenv import load_dotenv
from mistralai import Mistral

# Load API key
load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")
model = "codestral-latest"
client = Mistral(api_key=api_key)

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

Check 'src', if dummy value, u must change to real source
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
        blade_code = match[0].strip() if match else full_response.strip()

        result[comp] = blade_code

        # ⬇️ Simpan tiap komponen ke file:
        filename = f"output/components/{comp.lower()}.blade.php"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(blade_code)

    return result
