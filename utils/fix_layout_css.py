"""
Fix layout CSS by copying custom styles from draft HTML
"""

import os
import re


def extract_custom_css_from_draft():
    """Extract and merge custom CSS from ALL draft HTML files"""
    draft_dir = "output/drafts"
    
    if not os.path.exists(draft_dir):
        print("❌ No drafts found")
        return None
    
    # Get all draft files
    draft_files = [f for f in os.listdir(draft_dir) if f.endswith('.html')]
    if not draft_files:
        print("❌ No draft HTML files found")
        return None
    
    all_css = []
    css_seen = set()  # Track unique CSS blocks
    
    for draft_file in draft_files:
        draft_path = os.path.join(draft_dir, draft_file)
        
        with open(draft_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Extract <style> content
        style_pattern = r'<style>(.*?)</style>'
        matches = re.findall(style_pattern, content, re.DOTALL)
        
        for css_block in matches:
            css_clean = css_block.strip()
            # Use hash to avoid duplicates
            css_hash = hash(css_clean)
            if css_hash not in css_seen:
                css_seen.add(css_hash)
                all_css.append(css_clean)
                print(f"✅ Found custom CSS in {draft_file}")
    
    if all_css:
        # Merge all CSS blocks
        merged_css = "\n\n        /* ===== Merged from multiple pages ===== */\n\n".join(all_css)
        return merged_css
    
    print("⚠️ No custom CSS found in drafts")
    return None


def update_layout_css(custom_css):
    """Update app.blade.php with custom CSS"""
    layout_path = "my-laravel/resources/views/layouts/app.blade.php"
    
    if not os.path.exists(layout_path):
        print("❌ app.blade.php not found")
        return False
    
    with open(layout_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Replace existing <style> with custom CSS
    new_style = f"""    <style>
{custom_css}
    </style>"""
    
    # Pattern to match existing <style> block
    style_pattern = r'<style>.*?</style>'
    
    if re.search(style_pattern, content, re.DOTALL):
        content = re.sub(style_pattern, new_style, content, flags=re.DOTALL)
        print("✅ Replaced existing <style> block")
    else:
        # Insert before </head>
        content = content.replace('</head>', f'{new_style}\n</head>')
        print("✅ Added <style> block")
    
    with open(layout_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    return True


def main():
    print("🎨 Fixing layout CSS...\n")
    
    # Extract CSS from draft
    custom_css = extract_custom_css_from_draft()
    
    if not custom_css:
        print("\n❌ No custom CSS to copy")
        return
    
    # Update layout
    if update_layout_css(custom_css):
        print("\n✅ Layout CSS updated!")
        print("\nCustom CSS includes:")
        # Show first few lines
        lines = custom_css.split('\n')[:5]
        for line in lines:
            if line.strip():
                print(f"  {line.strip()}")
        if len(custom_css.split('\n')) > 5:
            print("  ...")
    else:
        print("\n❌ Failed to update layout")


if __name__ == "__main__":
    main()
