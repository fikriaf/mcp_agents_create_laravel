"""
Master Fix Script - Fix All Multi-Page Issues
Runs all auto-fix utilities in the correct order
"""

import sys
import os

# Add utils to path
sys.path.insert(0, 'utils')

def main():
    print("="*60)
    print("🔧 MASTER FIX - Multi-Page Application")
    print("="*60)
    print()
    
    success_count = 0
    total_fixes = 5
    
    # Fix 1: Draft Styling
    print("1️⃣ Fixing draft HTML styling...")
    try:
        from fix_draft_styling import fix_all_drafts
        fix_all_drafts()
        success_count += 1
        print()
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
    
    # Fix 2: Nested UI
    print("2️⃣ Fixing nested UI and duplicate JavaScript...")
    try:
        from fix_nested_ui import fix_nested_ui
        fix_nested_ui()
        success_count += 1
        print()
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
    
    # Fix 3: Component Names
    print("3️⃣ Fixing component name mismatches...")
    try:
        from fix_component_names import fix_component_includes
        fix_component_includes()
        print("   ✅ Component names fixed")
        success_count += 1
        print()
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
    
    # Fix 4: Routes
    print("4️⃣ Syncing routes...")
    try:
        from smart_route_sync import sync_navbar_routes
        sync_navbar_routes()
        print("   ✅ Routes synced")
        success_count += 1
        print()
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
    
    # Fix 5: Component Styling
    print("5️⃣ Fixing component styling...")
    try:
        from fix_component_styling import fix_all_components
        fix_all_components()
        print("   ✅ Component styling fixed")
        success_count += 1
        print()
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
    
    # Summary
    print("="*60)
    print(f"✅ Completed: {success_count}/{total_fixes} fixes applied")
    print("="*60)
    print()
    
    # Run validation
    print("🔍 Running validation...\n")
    try:
        from multi_page_validator import validate_multi_page_app
        is_valid = validate_multi_page_app()
        
        if is_valid:
            print("\n🎉 SUCCESS! All issues fixed and validated.")
            return 0
        else:
            print("\n⚠️ Some issues remain. Check validation output above.")
            return 1
    except Exception as e:
        print(f"⚠️ Validation error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
