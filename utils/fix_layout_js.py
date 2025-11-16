"""
Fix layout JavaScript by copying scripts from ALL draft HTML files
"""

import os
import re


def extract_javascript_from_drafts():
    """Extract and merge JavaScript from ALL draft HTML files with safety checks"""
    draft_dir = "output/drafts"
    
    if not os.path.exists(draft_dir):
        print("❌ No drafts found")
        return None
    
    # Get all draft files
    draft_files = [f for f in os.listdir(draft_dir) if f.endswith('.html')]
    if not draft_files:
        print("❌ No draft HTML files found")
        return None
    
    all_js_blocks = []
    
    for draft_file in draft_files:
        draft_path = os.path.join(draft_dir, draft_file)
        page_name = draft_file.replace('.html', '')
        
        with open(draft_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Extract <script> content (excluding CDN scripts)
        script_pattern = r'<script(?!\s+src=)>(.*?)</script>'
        matches = re.findall(script_pattern, content, re.DOTALL)
        
        for js_block in matches:
            js_clean = js_block.strip()
            
            # Skip empty scripts
            if not js_clean:
                continue
            
            # Extract first element ID as guard
            element_ids = re.findall(r"getElementById\(['\"]([^'\"]+)['\"]\)", js_clean)
            
            if element_ids:
                # Wrap with existence check for safety
                guard_id = element_ids[0]
                wrapped_js = f"""// ===== {page_name} JavaScript =====
        if (document.getElementById('{guard_id}')) {{
            {js_clean.replace(chr(10), chr(10) + '            ')}
        }}"""
                all_js_blocks.append(wrapped_js)
                print(f"✅ Found JavaScript in {draft_file} (guarded by #{guard_id})")
            else:
                # No element IDs, add as-is (probably utility functions)
                all_js_blocks.append(f"// ===== {page_name} JavaScript =====\n        {js_clean}")
                print(f"✅ Found JavaScript in {draft_file}")
    
    if all_js_blocks:
        # Merge all JS blocks
        merged_js = "\n\n        ".join(all_js_blocks)
        return merged_js
    
    print("⚠️ No JavaScript found in drafts")
    return None


def update_layout_js(custom_js):
    """Update app.blade.php with custom JavaScript"""
    layout_path = "my-laravel/resources/views/layouts/app.blade.php"
    
    if not os.path.exists(layout_path):
        print("❌ app.blade.php not found")
        return False
    
    with open(layout_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Build new script block
    new_script = f"""    <script>
{custom_js}
    </script>"""
    
    # Pattern to match existing <script> block (not CDN scripts)
    # Find last <script> before </body>
    script_pattern = r'<script>(?!.*src=).*?</script>\s*</body>'
    
    if re.search(script_pattern, content, re.DOTALL):
        # Replace existing script block
        content = re.sub(
            r'<script>(?!.*src=)(.*?)</script>(\s*</body>)',
            lambda m: f'{new_script}\n{m.group(2)}',
            content,
            flags=re.DOTALL
        )
        print("✅ Replaced existing <script> block")
    else:
        # Insert before </body>
        content = content.replace('</body>', f'{new_script}\n</body>')
        print("✅ Added <script> block")
    
    with open(layout_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    return True


def main():
    print("⚡ Fixing layout JavaScript...\n")
    
    # Extract JS from all drafts
    custom_js = extract_javascript_from_drafts()
    
    if not custom_js:
        print("\n❌ No JavaScript to copy")
        return
    
    # Update layout
    if update_layout_js(custom_js):
        print("\n✅ Layout JavaScript updated!")
        print("\nJavaScript includes:")
        # Show first few lines
        lines = custom_js.split('\n')[:5]
        for line in lines:
            if line.strip():
                print(f"  {line.strip()}")
        if len(custom_js.split('\n')) > 5:
            print("  ...")
    else:
        print("\n❌ Failed to update layout")


if __name__ == "__main__":
    main()
