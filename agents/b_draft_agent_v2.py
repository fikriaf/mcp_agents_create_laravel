import re
import os
from dotenv import load_dotenv
from agents.llm_client import get_llm_response

load_dotenv()


def draft_agent_multi(prompt_expander: dict, callback=None):
    """
    Enhanced draft agent that can generate multiple HTML drafts
    Detects if prompt requires multiple pages and generates accordingly
    
    Args:
        prompt_expander: dict with prompt info
        callback: optional async function to send progress updates (for WebSocket)
    """
    print("\n\n🟢 [MULTI-DRAFT AGENT] Analyzing prompt for multiple pages...")
    
    # Helper to call callback if provided
    def send_update(message):
        if callback and callable(callback):
            try:
                callback(message)
            except Exception as e:
                print(f"⚠️ Callback error: {e}")

    # First, detect if multiple pages are needed
    detection_prompt = f"""
Analyze this prompt and determine if it requires multiple separate pages/screens:

{prompt_expander['new_prompt']}

IMPORTANT:
- If this is a REVISION (contains "PREVIOUS DRAFT TO IMPROVE"), extract the page structure from the previous draft
- Keep the same pages, only improve the design
- If it's a new request, detect pages normally

Respond with JSON only:
{{
  "multiple_pages": true/false,
  "pages": [
    {{"name": "page-name", "description": "brief description"}},
    ...
  ]
}}

If single page, return: {{"multiple_pages": false, "pages": [{{"name": "main", "description": "single page"}}]}}
"""

    detection_system = """
You are a UI/UX analyst. Detect if a prompt requires multiple pages.

CRITICAL DISTINCTION:
- PAGES = Separate URLs/routes (home, login, dashboard, about, contact)
- SECTIONS = Parts within a single page (hero section, features section, pricing section)

Guidelines:
- If user explicitly mentions NUMBER of pages (e.g., "3 pages", "2 halaman") → Create that exact number
- If user explicitly mentions multiple pages/screens → Multiple pages
- If user mentions "page 1, page 2, page 3" → Multiple pages
- If user mentions different purposes (login, dashboard, profile) → Multiple pages
- If user only mentions sections of one page → Single page

PRIORITY RULE: If user specifies a NUMBER, that takes absolute priority. Create exactly that many pages.

When in doubt, prefer multiple pages if user intent suggests it.

IMPORTANT FOR REVISIONS:
- If prompt contains "PREVIOUS DRAFT TO IMPROVE", extract the page structure from the previous draft
- Keep the same number of pages as before
- Only change the design/content, not the structure

Examples of multi-page:
- "Create login and dashboard" → 2 pages
- "Build e-commerce with home, products, cart" → 3 pages
- "Make blog with posts list and detail" → 2 pages

Examples of single page with sections:
- "landing page with hero, features, pricing, contact" → 1 page (home)
- "one page website with about section and contact form" → 1 page (home)

Examples that should be multiple pages:
- "3 pages" → 3 pages (home, about, contact)
- "3 halaman" → 3 pages (home, about, contact)
- "2 pages" → 2 pages (home, about)
- "website with home, about, contact" → 3 pages
- "about us and contact pages" → 2 pages (about, contact)

CRITICAL: If user explicitly mentions a NUMBER of pages (e.g., "3 pages", "2 halaman"), you MUST create that exact number of pages.

Examples of revision:
- "home nya kurang professional" + previous 4 pages → Keep 4 pages, improve home

DESCRIPTION RULE:
- Page description should be brief purpose, NOT list of sections
- Good: "landing page for product showcase"
- Bad: "landing page with hero section, features section, pricing section, about us, contact us"

LANGUAGE RULE:
- ALWAYS use ENGLISH for page names
- Even if user input is in Indonesian/other language, translate to English
- Examples:
  - "beranda" → "home"
  - "tentang kami" → "about"
  - "kontak" → "contact"
  - "produk" → "products"

Respond ONLY with JSON. No explanations.
"""

    try:
        detection_response = get_llm_response(
            system_prompt=detection_system,
            user_prompt=detection_prompt,
            max_tokens=1000,
            temperature=0.3,
        )
        
        # Parse detection result
        import json
        json_match = re.search(r'\{.*\}', detection_response, re.DOTALL)
        if json_match:
            detection = json.loads(json_match.group(0))
        else:
            detection = {"multiple_pages": False, "pages": [{"name": "main", "description": "single page"}]}
            
    except Exception as e:
        print(f"⚠️ Detection failed, assuming single page: {e}")
        detection = {"multiple_pages": False, "pages": [{"name": "main", "description": "single page"}]}

    pages = detection.get("pages", [{"name": "main", "description": "single page"}])
    
    # FALLBACK: Check if user explicitly mentioned number of pages in prompt
    # This catches cases where LLM fails to detect properly
    number_match = re.search(r'(\d+)\s*(?:pages?|halaman)', prompt_expander['new_prompt'], re.IGNORECASE)
    if number_match:
        requested_count = int(number_match.group(1))
        if len(pages) != requested_count:
            print(f"⚠️ LLM detected {len(pages)} pages, but user requested {requested_count}. Correcting...")
            # Generate default pages
            default_pages = ["home", "about", "contact", "services", "portfolio", "blog", "team", "pricing"]
            pages = [
                {"name": default_pages[i] if i < len(default_pages) else f"page{i+1}", 
                 "description": f"{default_pages[i] if i < len(default_pages) else f'page {i+1}'} page"}
                for i in range(requested_count)
            ]
    
    print(f"\n📊 Detected {len(pages)} page(s) to draft:")
    for i, page in enumerate(pages, 1):
        print(f"  {i}. {page['name']} - {page['description']}")
    
    # Send pages detected callback
    send_update({"type": "pages_detected", "count": len(pages), "pages": pages})

    # Generate draft for each page
    drafts = {}
    
    for idx, page_info in enumerate(pages, 1):
        page_name = page_info['name'].lower()  # Normalize to lowercase
        page_desc = page_info['description']
        
        print(f"\n🎨 Generating draft {idx}/{len(pages)}: {page_name}...")
        send_update({"type": "page_draft_start", "page_name": page_name, "index": idx, "total": len(pages)})
        
        draft_html = generate_single_draft(
            prompt_expander['new_prompt'],
            page_name,
            page_desc,
            idx,
            len(pages),
            pages  # Pass all pages for navbar context
        )
        
        drafts[page_name] = draft_html
        
        # Save individual draft
        os.makedirs("output/drafts", exist_ok=True)
        draft_path = f"output/drafts/{page_name}.html"
        with open(draft_path, "w", encoding="utf-8") as f:
            f.write(draft_html)
        print(f"  ✅ Saved: {draft_path}")
        
        # Send page draft complete callback
        send_update({"type": "page_draft_complete", "page_name": page_name, "index": idx, "total": len(pages)})

    # Create index page with navigation to all drafts
    if len(pages) > 1:
        index_html = create_draft_index(pages, drafts)
        with open("output/draft.html", "w", encoding="utf-8") as f:
            f.write(index_html)
        print(f"\n📁 Main draft index: output/draft.html")
    else:
        # Single page - use it as main draft
        with open("output/draft.html", "w", encoding="utf-8") as f:
            f.write(drafts[pages[0]['name']])
        print(f"\n📁 Draft saved: output/draft.html")

    return {
        "prompt": prompt_expander["new_prompt"],
        "draft": drafts[pages[0]['name']] if len(pages) == 1 else index_html,
        "drafts": drafts,
        "pages": pages
    }


def generate_single_draft(full_prompt: str, page_name: str, page_desc: str, current: int, total: int, all_pages: list = None):
    """Generate a single HTML draft for a specific page"""
    
    # For pages after the first, extract FULL templates from first page
    if total > 1 and current > 1 and all_pages:
        first_page_name = all_pages[0]['name']
        first_draft_path = f"output/drafts/{first_page_name}.html"
        
        if os.path.exists(first_draft_path):
            with open(first_draft_path, 'r', encoding='utf-8') as f:
                first_content = f.read()
            
            # Extract navbar (full HTML)
            nav_match = re.search(r'<(?:nav|header)[^>]*>.*?</(?:nav|header)>', first_content, re.DOTALL)
            navbar_template = nav_match.group(0) if nav_match else ""
            
            # Extract footer (full HTML)
            footer_match = re.search(r'<footer[^>]*>.*?</footer>', first_content, re.DOTALL)
            footer_template = footer_match.group(0) if footer_match else ""
            
            # Extract CSS (from <style> tag)
            css_match = re.search(r'<style[^>]*>(.*?)</style>', first_content, re.DOTALL)
            css_template = css_match.group(1) if css_match else ""
            
            # Extract JavaScript (from <script> tags, excluding CDN)
            js_matches = re.findall(r'<script(?![^>]*src=)[^>]*>(.*?)</script>', first_content, re.DOTALL)
            js_template = '\n'.join(js_matches) if js_matches else ""
            
            # Use template-based generation for consistency
            return generate_from_template(
                navbar_template,
                footer_template,
                css_template,
                js_template,
                page_name,
                page_desc,
                full_prompt,
                all_pages
            )
    
    # First page or single page - generate from scratch
    system_prompt = """
You are a professional AI frontend developer.

Generate a complete, high-quality HTML file with modern, responsive design.

✅ Requirements:
- Full HTML structure with <html>, <head>, and <body>
- Use Tailwind CSS CDN (LATEST VERSION): <script src="https://cdn.tailwindcss.com"></script>
- Add custom CSS for enhancements (PURE CSS, NO @apply)
- Include interactivity with vanilla JavaScript
- Modern, production-ready design
- Smooth animations and transitions
- Real, meaningful content (no lorem ipsum)
- Professional color scheme and typography

⚠️ CRITICAL CSS RULES:
- ALWAYS use: <script src="https://cdn.tailwindcss.com"></script> (NOT old link version)
- DO NOT use @apply directive (not supported in CDN)
- Write PURE CSS with standard properties
- Use CSS variables for colors (--primary, --secondary, etc.)
- Use standard CSS selectors and properties
- Example: .btn { padding: 0.75rem 1.5rem; border-radius: 0.5rem; background-color: var(--primary); }
- Load order: 1) Tailwind script, 2) Custom <style> block

⚠️ STYLING MUST WORK:
- Test that Tailwind classes work (bg-blue-500, text-white, etc.)
- Ensure custom CSS doesn't override Tailwind unnecessarily
- Use Tailwind for layout, custom CSS for specific enhancements only

✅ CONSISTENCY REQUIREMENTS (for multi-page):
- Use IDENTICAL navbar design across all pages
- Use IDENTICAL footer design across all pages
- Use SAME color palette (primary, secondary, accent colors)
- Use SAME typography (font families, sizes, weights)
- Use SAME button styles and hover effects
- Use SAME spacing and layout patterns
- Define CSS variables for colors to ensure consistency

🚫 DO NOT:
- Use dummy image placeholders
- Include explanations or comments outside code
- Return incomplete templates
- Change navbar/footer design between pages
- Use different color schemes for different pages

Return ONLY:
```html
<!-- Your complete HTML code -->
```
"""

    if total > 1 and all_pages:
        # Build page list for navbar
        page_list = '\n'.join([f"  - {p['name']}" for p in all_pages])
        
        user_prompt = f"""
Create HTML for page {current} of {total}:

Page Name: {page_name}
Page Purpose: {page_desc}

Context from full request:
{full_prompt}

CRITICAL REQUIREMENTS FOR CONSISTENCY:

1. NAVIGATION MENU:
   - ONLY include links to these {total} pages:
{page_list}
   - DO NOT add extra menu items
   - Use EXACT same navbar design across all pages
   - Same colors, fonts, layout, spacing

2. DESIGN CONSISTENCY:
   - Use the SAME color scheme for all pages
   - Use the SAME typography (fonts, sizes)
   - Use the SAME button styles
   - Use the SAME spacing and layout patterns
   - Navbar and Footer should look IDENTICAL across pages

3. FOOTER:
   - If you include a footer, use SAME design for all pages
   - Same background color, text color, layout
   - Include links to all {total} pages

4. BRANDING:
   - Use consistent logo/brand name placement
   - Same brand colors throughout

Focus on this specific page content while maintaining STRICT design consistency.
"""
    else:
        user_prompt = full_prompt

    try:
        full_response = get_llm_response(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            max_tokens=32000,  # Increased for complete HTML generation
            temperature=0.7,
        )

    except Exception as e:
        print(f"\n❌ Error creating draft for {page_name}: {e}")
        raise  # Let the error propagate - LLM client already has fallback

    # Remove <think> tags (from models like DeepSeek)
    full_response = re.sub(r'<think>.*?</think>', '', full_response, flags=re.DOTALL | re.IGNORECASE)
    
    # STRICT: Only extract content between ```html and ```
    # This prevents any thinking/explanation text from being included
    code_matches = re.findall(r"```html\s*(.*?)```", full_response, re.DOTALL | re.IGNORECASE)
    
    if code_matches:
        # Take the first match (should be the only one)
        html_content = code_matches[0].strip()
        print(f"  ✅ Extracted HTML from ```html block for {page_name} (length: {len(html_content)} chars)")
        
        # Check if HTML is complete
        if not html_content.endswith('</html>'):
            print(f"  ⚠️ Warning: {page_name} HTML appears incomplete (missing </html>)")
            print(f"  🔄 Attempting to continue generation for {page_name}...")
            
            # Try to continue the generation
            continuation_prompt = f"""
Continue the HTML code for page "{page_name}" from where it was cut off. 

Here's the incomplete HTML (last 1000 chars):
```html
{html_content[-1000:]}
```

Continue from the last line and complete the HTML structure. Make sure to:
1. Close all open tags
2. End with </body> and </html>
3. Return ONLY the continuation part in ```html block

Start from where the code was cut off and complete it.
"""
            
            try:
                continuation_response = get_llm_response(
                    system_prompt="You are an HTML completion expert. Complete the incomplete HTML structure.",
                    user_prompt=continuation_prompt,
                    temperature=0.3,
                    max_tokens=32000,
                )
                
                # Extract continuation
                continuation_matches = re.findall(
                    r"```html\s*(.*?)```", continuation_response, re.DOTALL | re.IGNORECASE
                )
                
                if continuation_matches:
                    continuation = continuation_matches[0].strip()
                    # Merge with original
                    html_content = html_content + "\n" + continuation
                    print(f"  ✅ Continuation added for {page_name} (total length: {len(html_content)} chars)")
                    
                    # Check again
                    if html_content.endswith('</html>'):
                        print(f"  ✅ HTML structure now complete for {page_name}")
                    else:
                        print(f"  ⚠️ Still incomplete for {page_name}, but proceeding...")
                else:
                    print(f"  ⚠️ Could not extract continuation for {page_name}, proceeding with incomplete HTML")
                    
            except Exception as e:
                print(f"  ⚠️ Continuation failed for {page_name}: {str(e)[:100]}")
                print(f"  💡 Proceeding with incomplete HTML for {page_name}")
        else:
            print(f"  ✅ HTML structure complete for {page_name}")
        
        # Final cleanup before return
        html_content = html_content.strip()
        if html_content.startswith('```html'):
            html_content = html_content[7:].strip()
        if html_content.startswith('```'):
            html_content = html_content[3:].strip()
        if html_content.endswith('```'):
            html_content = html_content[:-3].strip()
        
        return html_content
    else:
        # Fallback: Try to extract HTML tags directly
        # This handles cases where LLM doesn't use markdown code blocks
        tag_match = re.search(r"<html.*?>.*?</html>", full_response, re.DOTALL | re.IGNORECASE)
        if tag_match:
            result = tag_match.group(0).strip()
        else:
            # Last resort: Use raw response but warn
            print(f"  ⚠️ No code block or HTML tags found for {page_name}, using raw response")
            result = full_response.strip()
        
        # Final cleanup for fallback path too
        if result.startswith('```html'):
            result = result[7:].strip()
        if result.startswith('```'):
            result = result[3:].strip()
        if result.endswith('```'):
            result = result[:-3].strip()
        
        print(f"  🧹 Final cleanup done for {page_name}, length: {len(result)} chars")
        return result


def generate_from_template(navbar_html: str, footer_html: str, css: str, js: str, page_name: str, page_desc: str, full_prompt: str, all_pages: list):
    """Generate page using exact templates from first page"""
    
    system_prompt = """
You are a professional AI frontend developer.

Generate ONLY the main content section for a page.
The navbar, footer, CSS, and JavaScript will be provided - DO NOT recreate them.

✅ Requirements:
- Generate ONLY the <main> or content section
- Match the design style of provided templates
- Use same color scheme and typography
- Real, meaningful content (no lorem ipsum)
- Responsive design with Tailwind classes

🚫 DO NOT:
- Create navbar or footer (already provided)
- Add <html>, <head>, or <body> tags
- Include <style> or <script> tags
- Change color scheme or typography
- Use dummy placeholders

Return ONLY the main content HTML (no markdown, no explanations).
"""

    page_list = '\n'.join([f"  - {p['name']}" for p in all_pages])
    
    user_prompt = f"""
Create the MAIN CONTENT section for:

Page Name: {page_name}
Page Purpose: {page_desc}

Context: {full_prompt}

Available pages for reference:
{page_list}

Generate ONLY the main content area (between navbar and footer).
Match the design style, colors, and typography of the existing templates.
"""

    try:
        content_response = get_llm_response(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            max_tokens=32000,  # Increased for complete content generation
            temperature=0.7,
        )
        
        # Remove <think> tags (from models like DeepSeek)
        content_response = re.sub(r'<think>.*?</think>', '', content_response, flags=re.DOTALL | re.IGNORECASE)
        
        # STRICT: Only extract content between ```html and ``` (if present)
        code_matches = re.findall(r"```html\s*(.*?)```", content_response, re.DOTALL | re.IGNORECASE)
        
        if code_matches:
            # Use content from code block
            content_html = code_matches[0].strip()
            print(f"    ✅ Extracted content from ```html block for {page_name} (length: {len(content_html)} chars)")
        else:
            # No code block, use raw response (LLM might return plain HTML)
            content_html = content_response.strip()
            print(f"    ⚠️ No ```html block found for {page_name}, using raw response")
        
        # Update navbar active state
        navbar_updated = navbar_html
        for page in all_pages:
            # Remove active classes from all links
            navbar_updated = re.sub(
                rf'(<a[^>]*href=["\']#{page["name"]}["\'][^>]*class=["\'][^"\']*)(bg-blue-600|text-blue-600|border-blue-600|active)([^"\']*["\'])',
                r'\1\3',
                navbar_updated
            )
        
        # Add active class to current page link
        navbar_updated = re.sub(
            rf'(<a[^>]*href=["\']#{page_name}["\'][^>]*class=["\'])([^"\']*)',
            rf'\1\2 bg-blue-600 text-white',
            navbar_updated
        )
        
        # Assemble complete HTML
        complete_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_name.replace('-', ' ').title()}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
{css}
    </style>
</head>
<body>
{navbar_updated}

{content_html}

{footer_html}

<script>
{js}
</script>
</body>
</html>"""
        
        return complete_html
        
    except Exception as e:
        print(f"  ⚠️ Template generation error: {e}")
        raise  # Let the error propagate - LLM client already has fallback


def create_draft_index(pages: list, drafts: dict):
    """Create an index page with tabs/navigation to view all drafts"""
    
    tabs_html = "\n".join([
        f'<button onclick="showPage(\'{page["name"]}\')" id="tab-{page["name"]}" class="px-6 py-3 font-semibold rounded-lg transition {" bg-blue-600 text-white" if i == 0 else "bg-gray-200 text-gray-700 hover:bg-gray-300"}">{page["name"].replace("-", " ").title()}</button>'
        for i, page in enumerate(pages)
    ])
    
    # Create links to open in new tab instead of iframe to avoid issues
    links_html = "\n".join([
        f'''
        <div id="page-{page["name"]}" class="{"" if i == 0 else "hidden"} h-full overflow-auto">
            <div class="bg-white rounded-lg shadow-lg p-6 m-4">
                <div class="flex items-center justify-between mb-4">
                    <h2 class="text-2xl font-bold text-gray-800">Preview: {page["name"].replace("-", " ").title()}</h2>
                    <a href="drafts/{page["name"]}.html" target="_blank" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">
                        <i class="fas fa-external-link-alt mr-2"></i>Open in New Tab
                    </a>
                </div>
                <iframe class="w-full border border-gray-300 rounded-lg" style="height: calc(100vh - 250px);" src="drafts/{page["name"]}.html"></iframe>
            </div>
        </div>
        '''
        for i, page in enumerate(pages)
    ])
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GenLaravel - Multi-Page Draft Preview</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {{
            margin: 0;
            padding: 0;
            height: 100vh;
            display: flex;
            flex-direction: column;
        }}
        .preview-container {{
            flex: 1;
            overflow: hidden;
        }}
    </style>
</head>
<body class="bg-gray-100">
    <div class="bg-gradient-to-r from-slate-700 to-slate-800 text-white p-4 shadow-lg">
        <div class="container mx-auto">
            <div class="flex items-center justify-between">
                <div>
                    <h1 class="text-2xl font-bold">GenLaravel Draft Preview</h1>
                    <p class="text-sm text-gray-300">Multi-Page Application - {len(pages)} Pages</p>
                </div>
                <div class="flex space-x-2">
                    {tabs_html}
                </div>
            </div>
        </div>
    </div>
    
    <div class="preview-container bg-gray-100">
        {links_html}
    </div>
    
    <script>
        function showPage(pageName) {{
            // Hide all page containers
            document.querySelectorAll('div[id^="page-"]').forEach(div => {{
                div.classList.add('hidden');
            }});
            
            // Remove active state from all tabs
            document.querySelectorAll('button[id^="tab-"]').forEach(tab => {{
                tab.classList.remove('bg-blue-600', 'text-white');
                tab.classList.add('bg-gray-200', 'text-gray-700');
            }});
            
            // Show selected page
            document.getElementById('page-' + pageName).classList.remove('hidden');
            
            // Activate selected tab
            const activeTab = document.getElementById('tab-' + pageName);
            activeTab.classList.remove('bg-gray-200', 'text-gray-700');
            activeTab.classList.add('bg-blue-600', 'text-white');
        }}
    </script>
</body>
</html>"""





def draft_agent(prompt_expander: dict):
    """
    Backward compatible wrapper
    Returns single draft format for compatibility
    """
    result = draft_agent_multi(prompt_expander)
    
    # Return in old format for backward compatibility
    return {
        "prompt": result["prompt"],
        "draft": result["draft"]
    }
