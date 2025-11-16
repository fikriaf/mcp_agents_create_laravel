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
Create a Laravel Blade component for: `{comp}`

**REFERENCE HTML (Source of Truth):**
```html
{draft_html}
```

**YOUR TASK:**
1. Find the section in the HTML above that represents `{comp}`
2. Extract ONLY that section
3. Convert to Laravel Blade syntax
4. **PRESERVE ALL STYLING EXACTLY** - Do NOT change any Tailwind classes
5. **PRESERVE ALL COLORS EXACTLY** - Copy color classes as-is from draft

**CRITICAL:**
- If draft has `bg-blue-600`, you MUST use `bg-blue-600` (NOT bg-blue-500)
- If draft has `text-gray-800`, you MUST use `text-gray-800` (NOT text-gray-700)
- Copy the HTML structure and classes EXACTLY as they appear
- Only change: HTML links to Laravel route() syntax

**OUTPUT FORMAT:**
```blade
<!-- Your Blade component code here -->
```

Return ONLY the Blade code, no explanations.
"""
        # Get available pages from plan for route context
        available_pages = []
        if isinstance(plan, dict):
            # Try to get page info
            if 'page' in plan:
                available_pages.append(plan['page'])
            if 'pages' in plan:
                available_pages = [p.get('page', p.get('name', '')) for p in plan['pages']]
        
        pages_context = f"\nAvailable pages/routes: {', '.join(available_pages)}" if available_pages else ""
        
        system_prompt = f"""
You are a Laravel component generator AI.

Your task is to extract and convert relevant HTML into Laravel Blade components.

CRITICAL RULES:
- Return clean Blade markup using Tailwind CSS
- **PRESERVE EXACT COLORS from draft HTML** - Do NOT change any color classes
- **PRESERVE EXACT STYLING from draft HTML** - Do NOT modify Tailwind classes
- Convert HTML links to Laravel routes ONLY for pages that exist
- Use Laravel route() helper for internal links
- Use real image URLs (Unsplash, Pexels, etc.) instead of placeholders
- DO NOT include explanations or markdown outside the code
{pages_context}

COLOR PRESERVATION RULES:
- If draft uses bg-blue-600, keep bg-blue-600 (NOT bg-blue-500 or bg-primary)
- If draft uses text-gray-800, keep text-gray-800 (NOT text-gray-700)
- Copy ALL Tailwind color classes exactly as they appear in draft
- Do NOT substitute colors with CSS variables or custom classes
- Do NOT "improve" or "modernize" the color scheme

Route conversion rules:
- ONLY use route() for pages that exist in the available pages list
- For links to non-existent pages, use "#" instead
- Keep anchor links (#section) as is
- Keep external links (https://...) as is

Example conversions:
<a href="home.html"> → <a href="{{{{ route('home') }}}}"> (if 'home' exists)
<a href="about.html"> → <a href="#"> (if 'about' does NOT exist)
<a href="#section"> → <a href="#section"> (anchor link)
<a href="https://external.com"> → <a href="https://external.com"> (external)
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

        # Remove <think> tags (from models like DeepSeek) - must be done FIRST
        full_response = re.sub(r'<think>.*?</think>', '', full_response, flags=re.DOTALL | re.IGNORECASE)
        full_response = full_response.strip()
        
        match = re.findall(
            r"```blade\s*(.*?)```", full_response, re.DOTALL | re.IGNORECASE
        )
        blade_code = match[0].strip() if match else full_response.strip()
        
        # Final cleanup: remove markdown markers
        if blade_code.startswith('```blade'):
            blade_code = blade_code[8:].strip()
        if blade_code.startswith('```'):
            blade_code = blade_code[3:].strip()
        if blade_code.endswith('```'):
            blade_code = blade_code[:-3].strip()
        
        # Fix malformed route syntax (common LLM errors)
        # Fix: {{ route('x') }}) }} → {{ route('x') }}
        blade_code = re.sub(r"(\{\{\s*route\(['\"][^'\"]+['\"]\)\s*)\}\}\s*\)\s*\}\}", r'\1}}', blade_code)
        # Fix: {{ route('x'}}text → {{ route('x') }}" class="text
        blade_code = re.sub(r"(\{\{\s*route\(['\"][^'\"]+['\"])\}\}([a-zA-Z])", r'\1) }}" class="\2', blade_code)
        # Fix missing closing parenthesis: {{ route('x' }} → {{ route('x') }}
        blade_code = re.sub(r"(\{\{\s*route\(['\"][^'\"]+['\"])\s*\}\}", r'\1) }}', blade_code)
        # Fix extra closing braces: {{ route('x') }}}} → {{ route('x') }}
        blade_code = re.sub(r"(\{\{\s*route\(['\"][^'\"]+['\"]\)\s*\}\})\}\}", r'\1', blade_code)
        
        # Check if component is empty or just error message
        if len(blade_code) < 50 or 'not contain' in blade_code.lower() or 'not found' in blade_code.lower():
            print(f"\n  ⚠️ {comp} appears empty or not found in draft, creating minimal component")
            blade_code = f"<!-- {comp} component -->\n<div class=\"{comp.lower()}\">\n    <!-- Add {comp} content here -->\n</div>"

        result[comp] = blade_code

        # ⬇️ Simpan tiap komponen ke file:
        filename = f"output/components/{comp.lower()}.blade.php"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(blade_code)

    return result
