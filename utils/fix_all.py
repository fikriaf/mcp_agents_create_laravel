"""
Comprehensive fix script - Run this if you encounter any errors
Supports both SINGLE-PAGE and MULTI-PAGE modes
"""

import os
import sys

# Add utils to path
sys.path.insert(0, os.path.dirname(__file__))

from fix_layout_css import extract_custom_css_from_draft, update_layout_css
from fix_layout_js import extract_javascript_from_drafts, update_layout_js
from fix_existing_views import fix_app_layout, fix_component_routes, fix_route_views
from fix_single_page import fix_component_routes_single_page
from fix_component_styling import fix_hero_section, fix_all_components


def main():
    print("🔧 Running comprehensive fixes...\n")
    
    # Ask mode
    mode = input("Select mode [1=Single-Page, 2=Multi-Page]: ").strip()
    
    print("\n" + "=" * 60)
    print("1. Fixing app.blade.php layout...")
    print("=" * 60)
    fix_app_layout()
    
    print("\n" + "=" * 60)
    print("2. Fixing component routes...")
    print("=" * 60)
    if mode == "1":
        print("Mode: SINGLE-PAGE (removing all route() calls)")
        fix_component_routes_single_page()
    else:
        print("Mode: MULTI-PAGE (fixing route() calls)")
        fix_component_routes()
    
    print("\n" + "=" * 60)
    print("3. Fixing route view names...")
    print("=" * 60)
    fix_route_views()
    
    print("\n" + "=" * 60)
    print("4. Fixing layout CSS...")
    print("=" * 60)
    custom_css = extract_custom_css_from_draft()
    if custom_css:
        update_layout_css(custom_css)
        print("✅ Custom CSS applied")
    else:
        print("⚠️ No custom CSS found")
    
    print("\n" + "=" * 60)
    print("5. Fixing layout JavaScript...")
    print("=" * 60)
    custom_js = extract_javascript_from_drafts()
    if custom_js:
        update_layout_js(custom_js)
        print("✅ JavaScript merged")
    else:
        print("⚠️ No JavaScript found")
    
    print("\n" + "=" * 60)
    print("6. Fixing component styling...")
    print("=" * 60)
    fix_hero_section()
    fix_all_components()
    
    print("\n" + "=" * 60)
    print("✅ ALL FIXES COMPLETED!")
    print("=" * 60)
    print("\nYou can now run:")
    print("  cd my-laravel")
    print("  php artisan serve")
    print("\nIf you still see errors, check:")
    print("  php artisan route:list")


if __name__ == "__main__":
    main()
