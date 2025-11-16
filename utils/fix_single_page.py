"""
Fix script for SINGLE-PAGE applications
Removes all route() calls and replaces with # for anchor links
"""

import os
import re


def fix_component_routes_single_page():
    """Remove ALL route() calls from components for single-page apps"""
    components_dir = "my-laravel/resources/views/components"
    
    if not os.path.exists(components_dir):
        print("❌ Components directory not found")
        return
    
    fixed_count = 0
    
    for filename in os.listdir(components_dir):
        if filename.endswith('.blade.php'):
            filepath = os.path.join(components_dir, filename)
            
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            
            original_content = content
            
            # Remove ALL route() calls - replace with #
            # Pattern: {{ route('anything') }}
            content = re.sub(
                r'{{\s*route\([\'"][^\'"]+[\'"]\)\s*}}',
                '#',
                content
            )
            
            # Remove href with HTML file references
            content = re.sub(
                r'href=["\'][^"\']*\.html["\']',
                'href="#"',
                content,
                flags=re.IGNORECASE
            )
            
            # Remove href with page names (home, about, contact, etc.)
            page_names = ['home', 'about', 'contact', 'projects', 'services', 'blog', 'portfolio']
            for page in page_names:
                content = re.sub(
                    rf'href=["\']{page}["\']',
                    'href="#"',
                    content,
                    flags=re.IGNORECASE
                )
            
            # Only write if changed
            if content != original_content:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"✅ Fixed: {filename} (all hrefs → #)")
                fixed_count += 1
    
    if fixed_count == 0:
        print("ℹ️ No components needed fixes")
    else:
        print(f"\n✅ Fixed {fixed_count} component(s) for single-page")


def main():
    print("🔧 Fixing components for SINGLE-PAGE app...\n")
    fix_component_routes_single_page()
    print("\n✅ Single-page fixes completed!")


if __name__ == "__main__":
    main()
