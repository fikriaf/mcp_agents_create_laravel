"""
Fix route view names to match actual blade files
Prevents "View [x.y] not found" errors
"""

import os
import re


def get_blade_files():
    """Get list of blade files in views directory"""
    views_dir = "my-laravel/resources/views"
    blade_files = []
    
    for file in os.listdir(views_dir):
        if file.endswith('.blade.php') and file != 'welcome.blade.php':
            # Remove .blade.php extension
            view_name = file.replace('.blade.php', '')
            blade_files.append(view_name)
    
    return blade_files


def fix_route_views():
    """Fix view names in routes to match actual files"""
    route_file = "my-laravel/routes/web.php"
    
    if not os.path.exists(route_file):
        print("❌ routes/web.php not found")
        return
    
    with open(route_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    original_content = content
    blade_files = get_blade_files()
    
    print(f"📋 Found blade files: {', '.join(blade_files)}")
    
    # Fix common patterns
    # auth.login → login
    # auth.register → register
    # admin.dashboard → dashboard
    
    for blade_file in blade_files:
        # Pattern: view('folder.filename') → view('filename')
        patterns = [
            (rf"view\(['\"]auth\.{blade_file}['\"]\)", f"view('{blade_file}')"),
            (rf"view\(['\"]admin\.{blade_file}['\"]\)", f"view('{blade_file}')"),
            (rf"view\(['\"]pages\.{blade_file}['\"]\)", f"view('{blade_file}')"),
        ]
        
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content)
    
    # Also fix registration → registration (if file is registration.blade.php)
    if 'registration' in blade_files:
        content = re.sub(
            r"view\(['\"]register['\"]\)",
            "view('registration')",
            content
        )
    
    if content != original_content:
        with open(route_file, "w", encoding="utf-8") as f:
            f.write(content)
        print("✅ Fixed route view names")
        
        # Show changes
        print("\n📝 Changes made:")
        original_lines = original_content.split('\n')
        new_lines = content.split('\n')
        
        for i, (old, new) in enumerate(zip(original_lines, new_lines)):
            if old != new:
                print(f"  Line {i+1}:")
                print(f"    - {old.strip()}")
                print(f"    + {new.strip()}")
    else:
        print("ℹ️ No fixes needed")


def main():
    print("🔧 Fixing route view names...\n")
    fix_route_views()
    print("\n✅ Done!")


if __name__ == "__main__":
    main()
