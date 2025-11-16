"""
Fix Draft HTML Styling Issues
Ensures Tailwind CSS loads properly and styling is consistent
"""

import os
import re
from pathlib import Path

def fix_draft_styling(drafts_dir: str = "output/drafts"):
    """Fix styling issues in draft HTML files"""
    print("🎨 Fixing draft HTML styling...\n")
    
    if not os.path.exists(drafts_dir):
        print("   ⚠️ No drafts directory found")
        return
    
    draft_files = [f for f in os.listdir(drafts_dir) if f.endswith('.html')]
    
    if not draft_files:
        print("   ⚠️ No draft files found")
        return
    
    for draft_file in draft_files:
        draft_path = os.path.join(drafts_dir, draft_file)
        
        with open(draft_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix 1: Update Tailwind CDN to latest version
        content = fix_tailwind_cdn(content)
        
        # Fix 2: Ensure proper CSS loading order
        content = fix_css_loading_order(content)
        
        # Fix 3: Add missing viewport meta
        content = ensure_viewport_meta(content)
        
        # Fix 4: Fix CSS variable conflicts
        content = fix_css_variables(content)
        
        if content != original_content:
            with open(draft_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"   ✅ Fixed: {draft_file}")
        else:
            print(f"   ℹ️  No changes: {draft_file}")
    
    print(f"\n✅ Processed {len(draft_files)} draft file(s)")


def fix_tailwind_cdn(html_content: str) -> str:
    """Update Tailwind CDN to latest version"""
    # Replace old Tailwind CDN links
    old_patterns = [
        r'<link href="https://cdn\.jsdelivr\.net/npm/tailwindcss@[\d.]+/dist/tailwind\.min\.css" rel="stylesheet">',
        r'<link href="https://unpkg\.com/tailwindcss@[\d.]+/dist/tailwind\.min\.css" rel="stylesheet">',
    ]
    
    # Use script version (more reliable and up-to-date)
    new_tailwind = '<script src="https://cdn.tailwindcss.com"></script>'
    
    for pattern in old_patterns:
        html_content = re.sub(pattern, new_tailwind, html_content)
    
    # If no Tailwind found, add it
    if 'tailwindcss' not in html_content.lower():
        # Add before </head>
        html_content = html_content.replace('</head>', f'    {new_tailwind}\n</head>')
    
    return html_content


def fix_css_loading_order(html_content: str) -> str:
    """Ensure CSS loads in correct order: Tailwind first, then custom CSS"""
    # Extract head content
    head_match = re.search(r'<head>(.*?)</head>', html_content, re.DOTALL)
    
    if not head_match:
        return html_content
    
    head_content = head_match.group(1)
    
    # Extract components
    meta_tags = re.findall(r'<meta[^>]+>', head_content)
    title_tag = re.search(r'<title>.*?</title>', head_content)
    font_links = re.findall(r'<link[^>]*fonts[^>]*>', head_content)
    tailwind_script = re.search(r'<script[^>]*tailwindcss[^>]*></script>', head_content)
    custom_styles = re.search(r'<style>(.*?)</style>', head_content, re.DOTALL)
    
    # Rebuild head in correct order
    new_head = '\n'
    
    # 1. Meta tags
    for meta in meta_tags:
        new_head += f'    {meta}\n'
    
    # 2. Title
    if title_tag:
        new_head += f'    {title_tag.group(0)}\n'
    
    # 3. Fonts
    for font in font_links:
        new_head += f'    {font}\n'
    
    # 4. Tailwind (must be before custom styles)
    if tailwind_script:
        new_head += f'    {tailwind_script.group(0)}\n'
    else:
        new_head += '    <script src="https://cdn.tailwindcss.com"></script>\n'
    
    # 5. Custom styles (after Tailwind)
    if custom_styles:
        new_head += f'    <style>\n{custom_styles.group(1)}\n    </style>\n'
    
    # Replace head content
    html_content = html_content.replace(head_match.group(0), f'<head>{new_head}</head>')
    
    return html_content


def ensure_viewport_meta(html_content: str) -> str:
    """Ensure viewport meta tag exists"""
    if 'viewport' not in html_content:
        # Add after charset
        html_content = html_content.replace(
            '<meta charset="UTF-8">',
            '<meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">'
        )
    
    return html_content


def fix_css_variables(html_content: str) -> str:
    """Fix CSS variable conflicts and ensure proper usage"""
    # Extract style block
    style_match = re.search(r'<style>(.*?)</style>', html_content, re.DOTALL)
    
    if not style_match:
        return html_content
    
    style_content = style_match.group(1)
    
    # Common fixes
    fixes = [
        # Fix color variable naming conflicts
        (r'--primary-color:\s*#([0-9A-Fa-f]{6});', r'--primary: #\1;'),
        (r'--secondary-color:\s*#([0-9A-Fa-f]{6});', r'--secondary: #\1;'),
        
        # Fix usage in CSS
        (r'var\(--primary-color\)', r'var(--primary)'),
        (r'var\(--secondary-color\)', r'var(--secondary)'),
    ]
    
    for pattern, replacement in fixes:
        style_content = re.sub(pattern, replacement, style_content)
    
    # Replace style content
    html_content = html_content.replace(style_match.group(0), f'<style>{style_content}</style>')
    
    return html_content


def add_tailwind_config(html_content: str) -> str:
    """Add Tailwind configuration for better styling"""
    # Check if config already exists
    if 'tailwind.config' in html_content:
        return html_content
    
    # Add config after Tailwind script
    config = """
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        primary: '#3b82f6',
                        secondary: '#6b7280',
                    }
                }
            }
        }
    </script>"""
    
    # Add after Tailwind CDN script
    html_content = html_content.replace(
        '<script src="https://cdn.tailwindcss.com"></script>',
        f'<script src="https://cdn.tailwindcss.com"></script>\n{config}'
    )
    
    return html_content


def fix_all_drafts():
    """Fix all draft files including main draft"""
    print("🎨 Fixing all draft styling issues...\n")
    
    # Fix individual drafts
    fix_draft_styling("output/drafts")
    
    # Fix main draft if exists
    main_draft = "output/draft.html"
    if os.path.exists(main_draft):
        print("\n📄 Fixing main draft...")
        with open(main_draft, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        content = fix_tailwind_cdn(content)
        content = ensure_viewport_meta(content)
        
        if content != original:
            with open(main_draft, 'w', encoding='utf-8') as f:
                f.write(content)
            print("   ✅ Fixed: draft.html")
    
    print("\n✅ All drafts fixed!")


if __name__ == "__main__":
    fix_all_drafts()
