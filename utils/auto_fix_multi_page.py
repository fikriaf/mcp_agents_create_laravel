"""
Auto-Fix Multi-Page Issues
Automatically fixes common issues detected by the validator
"""

import os
import re
from pathlib import Path

def auto_fix_all(laravel_path: str = "my-laravel"):
    """Run all auto-fix functions"""
    print("🔧 Starting auto-fix for multi-page application...\n")
    
    fixes_applied = []
    
    # Fix 1: Component name mismatches
    try:
        from fix_component_names import fix_component_includes
        print("1️⃣ Fixing component name mismatches...")
        fix_component_includes(laravel_path)
        fixes_applied.append("Component names")
        print("   ✅ Done\n")
    except Exception as e:
        print(f"   ⚠️ Warning: {e}\n")
    
    # Fix 2: Route synchronization
    try:
        from smart_route_sync import sync_navbar_routes
        print("2️⃣ Syncing routes...")
        sync_navbar_routes(laravel_path)
        fixes_applied.append("Route synchronization")
        print("   ✅ Done\n")
    except Exception as e:
        print(f"   ⚠️ Warning: {e}\n")
    
    # Fix 3: CSS consistency
    try:
        from sync_css_classes import sync_all_css
        print("3️⃣ Syncing CSS classes...")
        sync_all_css(laravel_path)
        fixes_applied.append("CSS consistency")
        print("   ✅ Done\n")
    except Exception as e:
        print(f"   ⚠️ Warning: {e}\n")
    
    # Fix 4: Component styling
    try:
        from fix_component_styling import fix_all_components
        print("4️⃣ Fixing component styling...")
        fix_all_components(laravel_path)
        fixes_applied.append("Component styling")
        print("   ✅ Done\n")
    except Exception as e:
        print(f"   ⚠️ Warning: {e}\n")
    
    # Fix 5: JavaScript safety
    try:
        print("5️⃣ Adding JavaScript safety guards...")
        fix_javascript_safety(laravel_path)
        fixes_applied.append("JavaScript safety")
        print("   ✅ Done\n")
    except Exception as e:
        print(f"   ⚠️ Warning: {e}\n")
    
    # Fix 6: Blade syntax
    try:
        print("6️⃣ Fixing Blade syntax issues...")
        fix_blade_syntax(laravel_path)
        fixes_applied.append("Blade syntax")
        print("   ✅ Done\n")
    except Exception as e:
        print(f"   ⚠️ Warning: {e}\n")
    
    # Fix 7: Missing route names
    try:
        print("7️⃣ Adding missing route names...")
        fix_route_names(laravel_path)
        fixes_applied.append("Route names")
        print("   ✅ Done\n")
    except Exception as e:
        print(f"   ⚠️ Warning: {e}\n")
    
    print("="*60)
    print(f"✅ Auto-fix completed! Applied {len(fixes_applied)} fix(es):")
    for fix in fixes_applied:
        print(f"  • {fix}")
    print("="*60)


def fix_javascript_safety(laravel_path: str = "my-laravel"):
    """Add null checks to JavaScript DOM access"""
    views_path = os.path.join(laravel_path, "resources", "views")
    
    blade_files = []
    for root, dirs, files in os.walk(views_path):
        for file in files:
            if file.endswith('.blade.php'):
                blade_files.append(os.path.join(root, file))
    
    for blade_file in blade_files:
        with open(blade_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Pattern 1: getElementById without null check
        pattern1 = r'(const|let|var)\s+(\w+)\s*=\s*document\.getElementById\([^)]+\);?\s*\n\s*(\2\.\w+)'
        
        def add_null_check1(match):
            var_type = match.group(1)
            var_name = match.group(2)
            usage = match.group(3)
            return f"{var_type} {var_name} = document.getElementById('{var_name}');\nif ({var_name}) {{\n  {usage}"
        
        # Pattern 2: Direct getElementById usage
        pattern2 = r'document\.getElementById\(([^)]+)\)\.(\w+)'
        
        def add_null_check2(match):
            element_id = match.group(1)
            property = match.group(2)
            return f"document.getElementById({element_id})?.{property}"
        
        # Apply fixes
        content = re.sub(pattern2, add_null_check2, content)
        
        if content != original_content:
            with open(blade_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"   • Fixed: {os.path.basename(blade_file)}")


def fix_blade_syntax(laravel_path: str = "my-laravel"):
    """Fix common Blade syntax issues"""
    views_path = os.path.join(laravel_path, "resources", "views")
    
    blade_files = []
    for root, dirs, files in os.walk(views_path):
        for file in files:
            if file.endswith('.blade.php'):
                blade_files.append(os.path.join(root, file))
    
    for blade_file in blade_files:
        with open(blade_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix 1: Unclosed @section (add @endsection if missing)
        sections = len(re.findall(r'@section\([^)]+\)', content))
        endsections = len(re.findall(r'@endsection', content))
        
        if sections > endsections:
            # Add missing @endsection at the end
            content = content.rstrip() + '\n@endsection\n'
        
        # Fix 2: Unclosed @if (add @endif if missing)
        ifs = len(re.findall(r'@if\s*\(', content))
        endifs = len(re.findall(r'@endif', content))
        
        if ifs > endifs:
            content = content.rstrip() + '\n@endif\n'
        
        # Fix 3: Unclosed @foreach (add @endforeach if missing)
        foreachs = len(re.findall(r'@foreach\s*\(', content))
        endforeachs = len(re.findall(r'@endforeach', content))
        
        if foreachs > endforeachs:
            content = content.rstrip() + '\n@endforeach\n'
        
        if content != original_content:
            with open(blade_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"   • Fixed: {os.path.basename(blade_file)}")


def fix_route_names(laravel_path: str = "my-laravel"):
    """Add missing route names to routes"""
    routes_file = os.path.join(laravel_path, "routes", "web.php")
    
    if not os.path.exists(routes_file):
        return
    
    with open(routes_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Find routes without names
    route_pattern = r"Route::get\(['\"]([^'\"]+)['\"],\s*function\s*\(\)\s*\{[^}]*return\s+view\(['\"]([^'\"]+)['\"][^}]*\}\)(?!->name)"
    
    def add_route_name(match):
        path = match.group(1)
        view = match.group(2)
        
        # Generate route name from path
        if path == '/':
            route_name = 'home'
        else:
            route_name = path.strip('/').replace('/', '.')
        
        return match.group(0) + f"->name('{route_name}')"
    
    content = re.sub(route_pattern, add_route_name, content)
    
    if content != original_content:
        with open(routes_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"   • Added route names to web.php")


if __name__ == "__main__":
    import sys
    laravel_path = sys.argv[1] if len(sys.argv) > 1 else "my-laravel"
    
    auto_fix_all(laravel_path)
    
    # Run validation after fixes
    print("\n🔍 Running validation after fixes...\n")
    from multi_page_validator import validate_multi_page_app
    
    is_valid = validate_multi_page_app(laravel_path)
    
    if is_valid:
        print("\n✅ All issues fixed!")
    else:
        print("\n⚠️ Some issues remain. Please check manually.")
