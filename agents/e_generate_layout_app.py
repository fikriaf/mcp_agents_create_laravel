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

CRITICAL: Extract and preserve ALL custom CSS and JavaScript from the HTML reference.

CSS - Copy ALL from <style> tag:
- Custom classes (.hero-section, .feature-card, etc.)
- Animations and transitions
- Hover effects
- Gradients and clip-paths
- Any custom styling

JavaScript - Copy ALL from <script> tag:
- Loading screen hide logic
- Mobile menu toggle
- Smooth scrolling
- Scroll to top button
- Fade-in animations
- Any interactive features

Respond ONLY with the content of app.blade.php inside a ```blade code block.

📌 Page name: `{plan['page']}`
📌 Dont create component UI again, because Already Created: `{plan['components']}`

📎 HTML Reference:
```html
{draft_html}
```

IMPORTANT: Copy ALL <style> and <script> content from the HTML reference into the layout.
"""

    system_prompt = """
You are a Laravel layout generator AI.

Your job is to create a clean, reusable layout Blade file called `app.blade.php`.

CRITICAL RULES:
- ONLY include the layout shell structure:
  - <!DOCTYPE html>, <html>, <head>, <body>
  - Meta tags, <title>, CDN links (Tailwind, fonts, etc.)
  - Global styles in <style> tag - COPY ALL custom CSS from HTML reference
  - JavaScript in <script> tag - COPY ALL JavaScript from HTML reference
  - Background wrappers or body classes
- Place @yield('content') where the page content will be injected
- DO NOT include any preview UI, draft navigation, tabs, or buttons
- DO NOT include any page-specific content (navbar, hero, footer, etc.)
- DO NOT include iframes or JavaScript for page switching
- This is for PRODUCTION Laravel app, not draft preview

IMPORTANT FOR STYLING & INTERACTIVITY:
- Extract and preserve ALL <style> content from the HTML reference
  * Custom classes (.hero-section, .feature-card, etc.)
  * Animations, transitions, hover effects
  * Gradients, clip-paths, and visual enhancements
- Extract and preserve ALL <script> content from the HTML reference
  * Loading screen hide logic (window.addEventListener('load'))
  * Mobile menu toggle
  * Smooth scrolling for anchor links
  * Scroll to top button functionality
  * Fade-in animations with IntersectionObserver
  * Any interactive features

Example structure:
```blade
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>@yield('title', 'My App')</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        /* Copy ALL custom CSS from HTML reference */
    </style>
</head>
<body class="bg-gray-50">
    @yield('content')
    
    <script>
        /* Copy ALL JavaScript from HTML reference */
    </script>
</body>
</html>
```

Respond STRICTLY inside:
```blade
<!-- layout content -->
```
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
