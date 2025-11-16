import os
import re
from dotenv import load_dotenv
from .llm_client import get_llm_response

load_dotenv()


def generate_routes_multi(pages_plan: list):
    """
    Generate multiple Laravel routes for multiple pages
    """
    print("\n\n⚫ [MULTI-ROUTE AGENT] Generating Laravel routes for all pages...")

    # Build routes description
    routes_desc = "\n".join([
        f"- Page: {page['page']}, Route: {page['route']}, Description: {page.get('description', 'N/A')}"
        for page in pages_plan
    ])

    user_prompt = f"""
Generate Laravel route declarations for the following pages:

{routes_desc}

Requirements:
- Each route should use Route::get()
- Return appropriate view for each route
- Use descriptive route names
- Follow Laravel conventions

Respond ONLY with valid PHP route code.
"""

    system_prompt = """
You are a Laravel route generation AI.

Generate multiple Laravel route declarations in clean PHP format.

CRITICAL RULES:
- Start with `<?php`
- Include `use Illuminate\\Support\\Facades\\Route;`
- Use Route::get() with closure function for each page
- Use ->name() for named routes
- Return views with view() helper inside closure
- View names must match blade file names exactly
- If page is "login", use view('login') NOT view('auth.login')
- If page is "dashboard", use view('dashboard') NOT view('admin.dashboard')
- No folder prefixes in view names unless explicitly specified
- No explanations, only code
- Wrap in ```php code block

CORRECT SYNTAX (use this format):
```php
<?php

use Illuminate\\Support\\Facades\\Route;

Route::get('/home', function () {
    return view('home');
})->name('home');

Route::get('/about', function () {
    return view('about');
})->name('about');
```

WRONG SYNTAX (DO NOT use):
❌ Route::get('/home')->name('home')->view('home');
❌ Route::view('/home', 'home')->name('home');
❌ Route::get('/home')->view('home')->name('home');

LANGUAGE RULE:
- ALWAYS use ENGLISH for route names and view names
- Even if page names are in other languages, use English equivalents
- Examples:
  - beranda → home
  - tentang-kami → about
  - kontak → contact
"""

    try:
        full_response = get_llm_response(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.7,
            max_tokens=32000,
        )

        for char in full_response:
            print(char, end="", flush=True)

    except Exception as e:
        print(f"\n❌ Failed to generate routes: {e}")
        return ""

    match = re.findall(r"```php\s*(.*?)```", full_response, re.DOTALL | re.IGNORECASE)
    route_code = match[0].strip() if match else full_response.strip()
    
    with open("output/web.php", "w", encoding="utf-8") as f:
        f.write(route_code)
    
    return route_code


def generate_route(plan: dict, draft_html: str = ""):
    """
    Backward compatible - handles both single and multi-page plans
    """
    # Check if it's multi-page plan
    if "pages" in plan:
        return generate_routes_multi(plan["pages"])
    
    # Single page (old format)
    print("\n\n⚫ [ROUTE AGENT] Generating Laravel route...")

    user_prompt = f"""
Based on the following page plan, generate Laravel route declaration.

📌 Page name: `{plan['page']}`
📌 Route path: `{plan['route']}`

Respond ONLY with valid Laravel route using Route::get() in PHP format.
"""
    
    system_prompt = """
You are a Laravel route generation AI.

Generate Laravel route declaration in clean PHP format.

Requirements:
- Start with `<?php`
- Include `use Illuminate\\Support\\Facades\\Route;`
- Use Route::get() to return view
- No explanations
- Wrap in ```php code block
"""

    try:
        full_response = get_llm_response(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.7,
            max_tokens=32000,
        )

        for char in full_response:
            print(char, end="", flush=True)

    except Exception as e:
        print(f"\n❌ Failed to generate route: {e}")
        return ""

    match = re.findall(r"```php\s*(.*?)```", full_response, re.DOTALL | re.IGNORECASE)
    route_code = match[0].strip() if match else full_response.strip()
    
    with open("output/web.php", "w", encoding="utf-8") as f:
        f.write(route_code)
    
    return route_code
