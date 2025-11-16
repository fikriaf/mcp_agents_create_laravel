"""
Enforce navbar and footer consistency across all draft pages
Extracts from first page and applies to others
"""

import os
import re


def extract_navbar_footer(html_content):
    """Extract navbar and footer from HTML"""
    # Extract navbar (nav or header tag)
    nav_match = re.search(r'(<(?:nav|header)[^>]*>.*?</(?:nav|header)>)', html_content, re.DOTALL | re.IGNORECASE)
    navbar = nav_match.group(1) if nav_match else None
    
    # Extract footer
    footer_match = re.search(r'(<footer[^>]*>.*?</footer>)', html_content, re.DOTALL | re.IGNORECASE)
    footer = footer_match.group(1) if footer_match else None
    
    return navbar, footer


def extract_css_js(html_content):
    """Extract CSS and JavaScript from HTML"""
    # Extract CSS (everything in <style> tags)
    css_match = re.search(r'<style>(.*?)</style>', html_content, re.DOTALL | re.IGNORECASE)
    css = css_match.group(1) if css_match else None
    
    # Extract JavaScript (everything in <script> tags, excluding CDN)
    js_blocks = []
    script_pattern = r'<script(?!\s+src=)>(.*?)</script>'
    js_matches = re.findall(script_pattern, html_content, re.DOTALL | re.IGNORECASE)
    
    if js_matches:
        js = '\n\n'.join(js_matches)
    else:
        js = None
    
    return css, js


def replace_navbar_footer(html_content, navbar_template, footer_template):
    """Replace navbar and footer in HTML with templates"""
    result = html_content
    
    # Replace navbar
    if navbar_template:
        result = re.sub(
            r'<(?:nav|header)[^>]*>.*?</(?:nav|header)>',
            navbar_template,
            result,
            flags=re.DOTALL | re.IGNORECASE,
            count=1
        )
    
    # Replace footer
    if footer_template:
        result = re.sub(
            r'<footer[^>]*>.*?</footer>',
            footer_template,
            result,
            flags=re.DOTALL | re.IGNORECASE,
            count=1
        )
    
    return result


def replace_css_js(html_content, css_template, js_template):
    """Replace CSS and JavaScript in HTML with templates"""
    result = html_content
    
    # Replace CSS
    if css_template:
        result = re.sub(
            r'<style>.*?</style>',
            f'<style>{css_template}</style>',
            result,
            flags=re.DOTALL | re.IGNORECASE,
            count=1
        )
    
    # Replace JavaScript (keep page-specific JS, add common JS)
    if js_template:
        # Find existing script blocks
        existing_scripts = re.findall(r'<script(?!\s+src=)>(.*?)</script>', result, re.DOTALL | re.IGNORECASE)
        
        # Merge: common JS from template + page-specific JS
        if existing_scripts:
            # Keep page-specific JS that's not in template
            page_specific_js = []
            for script in existing_scripts:
                # Check if this script is page-specific (has unique element IDs)
                if script.strip() and script.strip() not in js_template:
                    page_specific_js.append(script.strip())
            
            # Combine common + page-specific
            if page_specific_js:
                combined_js = js_template + '\n\n        // Page-specific JavaScript\n        ' + '\n\n        '.join(page_specific_js)
            else:
                combined_js = js_template
            
            # Replace all script blocks with combined
            result = re.sub(
                r'<script(?!\s+src=)>.*?</script>',
                '',
                result,
                flags=re.DOTALL | re.IGNORECASE
            )
            result = result.replace('</body>', f'    <script>\n        {combined_js}\n    </script>\n</body>')
        else:
            # No existing scripts, just add template
            result = result.replace('</body>', f'    <script>\n        {js_template}\n    </script>\n</body>')
    
    return result


def update_active_link(navbar, page_name):
    """Update active link in navbar for current page"""
    # Remove existing active classes
    navbar = re.sub(r'\s*class="([^"]*)\s*active[^"]*"', r' class="\1"', navbar)
    navbar = re.sub(r'\s*class="active[^"]*"', '', navbar)
    
    # Add active class to current page link
    # Find link with href matching page name
    pattern = rf'(<a[^>]*href=["\'][^"\']*{page_name}[^"\']*["\'][^>]*)(>)'
    
    def add_active(match):
        link_tag = match.group(1)
        if 'class=' in link_tag:
            # Add to existing class
            link_tag = re.sub(r'class="([^"]*)"', r'class="\1 active"', link_tag)
        else:
            # Add new class attribute
            link_tag += ' class="active"'
        return link_tag + match.group(2)
    
    navbar = re.sub(pattern, add_active, navbar, flags=re.IGNORECASE)
    
    return navbar


def enforce_consistency():
    """Enforce navbar/footer/CSS/JS consistency across all draft pages"""
    draft_dir = "output/drafts"
    
    if not os.path.exists(draft_dir):
        print("❌ No drafts directory found")
        return
    
    draft_files = sorted([f for f in os.listdir(draft_dir) if f.endswith('.html')])
    
    if len(draft_files) < 2:
        print("ℹ️ Only one page, no consistency enforcement needed")
        return
    
    # Extract templates from first page
    first_file = os.path.join(draft_dir, draft_files[0])
    with open(first_file, 'r', encoding='utf-8') as f:
        first_content = f.read()
    
    navbar_template, footer_template = extract_navbar_footer(first_content)
    css_template, js_template = extract_css_js(first_content)
    
    if not any([navbar_template, footer_template, css_template, js_template]):
        print("⚠️ No templates found in first page")
        return
    
    print(f"✅ Extracted templates from {draft_files[0]}")
    if navbar_template:
        print(f"   • Navbar: {len(navbar_template)} chars")
    if footer_template:
        print(f"   • Footer: {len(footer_template)} chars")
    if css_template:
        print(f"   • CSS: {len(css_template)} chars")
    if js_template:
        print(f"   • JavaScript: {len(js_template)} chars")
    
    # Apply to other pages
    fixed_count = 0
    for draft_file in draft_files[1:]:
        page_name = draft_file.replace('.html', '')
        draft_path = os.path.join(draft_dir, draft_file)
        
        with open(draft_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Update active link in navbar for this page
        navbar_for_page = update_active_link(navbar_template, page_name) if navbar_template else None
        
        # Replace navbar and footer
        content = replace_navbar_footer(content, navbar_for_page, footer_template)
        
        # Replace CSS and JS
        content = replace_css_js(content, css_template, js_template)
        
        if content != original_content:
            with open(draft_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Fixed: {draft_file}")
            fixed_count += 1
    
    print(f"\n✅ Enforced consistency across {fixed_count} page(s)")
    print("   • Navbar/Footer: Identical")
    print("   • CSS: Shared styles")
    print("   • JavaScript: Common + page-specific")


def main():
    print("🔧 Enforcing navbar/footer consistency...\n")
    enforce_consistency()


if __name__ == "__main__":
    main()
