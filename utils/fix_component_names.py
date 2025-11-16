"""
Fix component name mismatches
Ensures @include() references match actual file names
"""

import os
import re


def get_actual_component_files():
    """Get list of actual component files"""
    components_dir = "my-laravel/resources/views/components"
    
    if not os.path.exists(components_dir):
        return []
    
    files = []
    for filename in os.listdir(components_dir):
        if filename.endswith('.blade.php'):
            # Remove .blade.php extension
            component_name = filename.replace('.blade.php', '')
            files.append(component_name)
    
    return files


def fix_component_includes():
    """Fix @include() and <x-> references to match actual file names"""
    views_dir = "my-laravel/resources/views"
    
    if not os.path.exists(views_dir):
        return
    
    # Get actual component names from files
    actual_components = get_actual_component_files()
    
    print(f"📋 Found {len(actual_components)} actual component file(s):")
    for comp in sorted(actual_components):
        print(f"   • {comp}")
    
    print(f"\n🔍 Fixing references in blade files to match actual file names...\n")
    
    fixed_count = 0
    
    # Collect all blade files recursively
    blade_files = []
    for root, dirs, files in os.walk(views_dir):
        for filename in files:
            if filename.endswith('.blade.php'):
                filepath = os.path.join(root, filename)
                blade_files.append(filepath)
    

    
    # Process each blade file
    for filepath in blade_files:
        relative_path = os.path.relpath(filepath, views_dir)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"   ❌ Error reading {relative_path}: {e}")
            continue
        
        original_content = content
        
        # Find all @include('components.xxx') references
        include_pattern = r"@include\(['\"]components\.([^'\"]+)['\"]\)"
        includes = re.findall(include_pattern, content)
        
        for included_name in includes:
            # Normalize: lowercase and no-dash for comparison
            included_normalized = included_name.lower().replace('-', '')
            
            # Check if exact match exists
            if included_name in actual_components:
                continue  # Already correct
            
            # Try to find matching component (case-insensitive, dash-insensitive)
            matched_component = None
            for actual in actual_components:
                if actual.lower().replace('-', '') == included_normalized:
                    matched_component = actual
                    break
            
            if matched_component:
                # Fix: replace with actual component name
                old_ref = f"@include('components.{included_name}')"
                new_ref = f"@include('components.{matched_component}')"
                content = content.replace(old_ref, new_ref)
                print(f"   ✅ {relative_path}: {included_name} → {matched_component}")
            else:
                print(f"   ❌ {relative_path}: {included_name} - NOT FOUND")
        
        # Also check <x-component> syntax
        x_pattern = r'<x-([a-zA-Z0-9\-]+)'
        x_components = re.findall(x_pattern, content)
        
        for x_comp in x_components:
            # Convert to lowercase and check
            x_comp_lower = x_comp.lower()
            
            if x_comp_lower not in actual_components:
                # Try no-dash version
                no_dash = x_comp_lower.replace('-', '')
                
                if no_dash in actual_components:
                    content = re.sub(
                        rf'<x-{x_comp}',
                        f'<x-{no_dash}',
                        content,
                        flags=re.IGNORECASE
                    )
                    content = re.sub(
                        rf'</x-{x_comp}>',
                        f'</x-{no_dash}>',
                        content,
                        flags=re.IGNORECASE
                    )
                    print(f"   ✅ {relative_path}: <x-{x_comp}> → <x-{no_dash}>")
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            fixed_count += 1
    
    print(f"\n{'='*60}")
    if fixed_count > 0:
        print(f"✅ Fixed {fixed_count} file(s)")
    else:
        print("ℹ️ All component references are correct")
    print(f"{'='*60}")


def main():
    import sys
    import io
    # Fix Windows console encoding
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("🔧 Fixing Component Name Mismatches\n")
    fix_component_includes()


if __name__ == "__main__":
    main()
