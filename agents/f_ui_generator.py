import os, sys
import re
from dotenv import load_dotenv
from mistralai import Mistral

# Load .env
load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")
model = "codestral-latest"
client = Mistral(api_key=api_key)

def generate_blade(layout: dict, components: dict):
    print("\n🟤 [UI GENERATOR AGENT] Generating Blade template using AI...")

    # 🔧 Build layout description
    section_desc = "\n".join(
        [f"- Section `{k}` contains component `{v}`" for k, v in layout.get("sections", {}).items()]
    )

    # 🔧 Sertakan isi semua komponen apa adanya
    component_info = "\n\n".join(
        [f"🔹 {name}.blade.php:\n```blade\n{code.strip()}\n```"
        for name, code in components.items()]
    )

    user_prompt = f"""
🧭 Your Task:
Generate the `{layout['page']}.blade.php` file.

⚠️ Instruction:
1. Use `@extends` and `@section('content')` properly.
2. For components that contain `$slot`, use `<x-componentname>Content</x-componentname>` syntax.
3. For other components:
    - Use `@include('components.name', [...])`
    - Use <x-componentname> for components with $slot.
    - Carefully extract all required variables from the component definition.
    - Pass **dummy values** (e.g. `id='example'`, `href='#'`) where necessary.

Warning:
- DO NOT Omit any required variable.
- DO NOT Copy or inline component content.
- DO NOT Invent components not listed.
- DO NOT Create Component UI Again, because already have on Blade Component

🧱 Layout Specification:
- Extends: `{layout['extends']}`
{section_desc}

🧩 Blade Components (with source code):
{component_info}
"""


    system_prompt = """
You are a Laravel Blade view generator AI.

Generate a Laravel Blade view file using the provided layout and Blade components.

Requirements:
- Use @extends('layouts.app') and @section('content') properly.
- Use <x-componentname> for components with $slot.
- Use @include(...) with full variable assignments for others.
- Do not skip any required variable.
- Do not include explanation or comments.
- Respond only inside:
```blade
<!-- blade content -->
```
"""
    # Kirim ke Mistral
    stream_response = client.chat.stream(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
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

    # Ambil isi dalam ```blade ... ``` jika ada
    match = re.findall(r"```blade\s*(.*?)```", full_response, re.DOTALL | re.IGNORECASE)
    with open(f"output/{layout['page']}.blade.php", "w", encoding="utf-8") as f:
      f.write(match[0].strip() if match else full_response.strip())
    return match[0].strip() if match else full_response.strip()
