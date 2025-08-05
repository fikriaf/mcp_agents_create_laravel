import re, os, sys
from dotenv import load_dotenv
from mistralai import Mistral

# Load API key dari .env
load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")
model = "codestral-latest"
client = Mistral(api_key=api_key)

def draft_agent(prompt_expander: dict):
    print("\n\n🟢 [DRAFT UI AGENT] Creating a draft UI...")

    # ✅ SYSTEM PROMPT diperkuat:
    system_prompt = """
You are a professional and experienced AI frontend developer.

Your task is to generate a complete, high-quality HTML file that reflects modern, awesome, responsive, and visually polished design — suitable for real-world production use.

✅ Your response MUST include:
- Full HTML structure with <html>, <head>, and <body> tags
- Awesome UI and Responsive layout using **Tailwind CSS as the primary styling framework**
- Internal <style> section for **custom CSS enhancements** to refine the UI (e.g. advanced layout, animation, or visual polish)
- Internal <script> section for interactivity or UI behavior enhancements

💡 You should prioritize:
- Tailwind CSS utility classes for rapid layout and component design
- Custom CSS to complement Tailwind where necessary
- Google Fonts
- Tailwind-compatible animation plugins or JS libraries if helpful (e.g. AOS, Alpine.js)

🎯 REQUIREMENTS:
- DO NOT use dummy src image placeholders
- DO NOT use generic lorem ipsum text — prefer realistic, meaningful interface labels and components
- Include smooth, subtle animations (e.g. transitions, hover effects, fade-ins)
- UI components must be real and usable (cards, buttons, navbars, modals, etc.)
- Design should be elegant, modern, and production-ready — not just functional

🚫 DO NOT:
- Include any explanations, comments, or markdown text outside the code
- Return empty, generic, or unfinished templates

🧾 Return ONLY a markdown code block formatted as:
```html
<!-- Your complete HTML code here -->
```
"""

    # ✅ Bisa tambah penguatan juga di user prompt
    user_prompt = (
        f"{prompt_expander['new_prompt']}"
    )

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


    # Ambil isi dari blok ```html ... ```
    code_matches = re.findall(r"```html\s*(.*?)```", full_response, re.DOTALL | re.IGNORECASE)

    if code_matches:
        get_draft = code_matches[0].strip()
    else:
        # Fallback kalau blok tidak ditemukan
        tag_match = re.search(r"<html.*?>.*?</html>", full_response, re.DOTALL | re.IGNORECASE)
        get_draft = tag_match.group(0).strip() if tag_match else full_response.strip()

    return {
        "prompt": prompt_expander["new_prompt"],
        "draft": get_draft
    }
