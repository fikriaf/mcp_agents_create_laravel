import re
from dotenv import load_dotenv
from agents.llm_client import get_llm_response

# Load API key dari .env
load_dotenv()

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
    user_prompt = f"{prompt_expander['new_prompt']}"

    # Use the new LLM client with Cerebras/Mistral fallback
    try:
        full_response = get_llm_response(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            max_tokens=8000,
            temperature=0.7,
        )
        print("\n✅ Draft created successfully")

    except Exception as e:
        print(f"\n❌ Error creating draft: {e}")
        # Fallback response
        full_response = """
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generated UI</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100">
    <div class="container mx-auto p-8">
        <h1 class="text-4xl font-bold text-gray-800 mb-4">Generated UI</h1>
        <p class="text-gray-600">This is a fallback template. Please check your LLM configuration.</p>
    </div>
</body>
</html>
```"""

    # Ambil isi dari blok ```html ... ```
    code_matches = re.findall(
        r"```html\s*(.*?)```", full_response, re.DOTALL | re.IGNORECASE
    )

    if code_matches:
        get_draft = code_matches[0].strip()
    else:
        # Fallback kalau blok tidak ditemukan
        tag_match = re.search(
            r"<html.*?>.*?</html>", full_response, re.DOTALL | re.IGNORECASE
        )
        get_draft = tag_match.group(0).strip() if tag_match else full_response.strip()

    return {"prompt": prompt_expander["new_prompt"], "draft": get_draft}
