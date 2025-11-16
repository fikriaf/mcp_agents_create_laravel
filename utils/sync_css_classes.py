"""
Sync CSS classes between layout and components
Ensures components use classes that actually exist in CSS
"""

import os
import re


def extract_css_classes_from_layout():
    """Extract all CSS class definitions from layout"""
    layout_path = "my-laravel/resources/views/layouts/app.blade.php"
    
    if not os.path.exists(layout_path):
        return {}
    
    with open(layout_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract <style> content
    style_match = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
    if not style_match:
        return {}
    
    css_content = style_match.group(1)
    
    # Find all class definitions with their full CSS
    class_definitions = {}
    
    # Pattern: .classname { ... }
    pattern = r'\.([a-zA-Z0-9_-]+)\s*\{([^}]+)\}'
    matches = re.findall(pattern, css_content)
    
    for class_name, css_rules in matches:
        class_definitions[class_name] = css_rules.strip()
    
    # Also find pseudo-class definitions like .dropdown:hover .dropdown-content
    pseudo_pattern = r'\.([a-zA-Z0-9_-]+):([a-zA-Z]+)\s+\.([a-zA-Z0-9_-]+)\s*\{([^}]+)\}'
    pseudo_matches = re.findall(pseudo_pattern, css_content)
    
    for parent, pseudo, child, css_rules in pseudo_matches:
        key = f"{parent}:{pseudo} .{child}"
        class_definitions[key] = css_rules.strip()
    
    return class_definitions


def find_undefined_classes_in_components():
    """Find classes used in components that don't exist in CSS"""
    components_dir = "my-laravel/resources/views/components"
    
    if not os.path.exists(components_dir):
        return {}
    
    css_classes = extract_css_classes_from_layout()
    defined_classes = set(css_classes.keys())
    
    # Extract simple class names (without pseudo-selectors)
    simple_classes = {c.split(':')[0] for c in defined_classes}
    
    undefined_usage = {}
    
    for filename in os.listdir(components_dir):
        if filename.endswith('.blade.php'):
            filepath = os.path.join(components_dir, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find all class attributes
            class_attrs = re.findall(r'class=["\']([^"\']+)["\']', content)
            
            for class_attr in class_attrs:
                classes = class_attr.split()
                
                for cls in classes:
                    # Skip Tailwind utility classes
                    if cls.startswith(('text-', 'bg-', 'p-', 'm-', 'flex', 'grid', 'hidden', 'block', 'inline', 'w-', 'h-', 'rounded', 'shadow', 'border', 'hover:', 'focus:', 'md:', 'lg:', 'xl:', 'sm:')):
                        continue
                    
                    # Check if this custom class exists in CSS
                    if cls not in simple_classes:
                        if filename not in undefined_usage:
                            undefined_usage[filename] = []
                        undefined_usage[filename].append(cls)
    
    return undefined_usage


def suggest_fixes():
    """Suggest fixes for undefined classes"""
    undefined = find_undefined_classes_in_components()
    css_classes = extract_css_classes_from_layout()
    
    if not undefined:
        print("✅ All custom classes are defined in CSS!")
        return
    
    print("⚠️  Found undefined classes in components:\n")
    
    for filename, classes in undefined.items():
        print(f"📄 {filename}")
        
        for cls in set(classes):
            print(f"   ❌ .{cls} - not defined in CSS")
            
            # Suggest similar classes
            similar = []
            for defined_cls in css_classes.keys():
                simple_cls = defined_cls.split(':')[0]
                if cls.lower() in simple_cls.lower() or simple_cls.lower() in cls.lower():
                    similar.append(simple_cls)
            
            if similar:
                print(f"      💡 Did you mean: {', '.join(similar[:3])}")
        
        print()
    
    print("=" * 60)
    print("💡 Suggestions:")
    print("   1. Add missing CSS classes to layout")
    print("   2. Or update components to use existing classes")
    print("   3. Run 'python utils/fix_component_styling.py' to auto-fix")


def main():
    print("🔍 Syncing CSS classes...\n")
    
    css_classes = extract_css_classes_from_layout()
    print(f"📋 Found {len(css_classes)} CSS class definitions in layout\n")
    
    print("Common classes:")
    for cls in sorted(css_classes.keys())[:10]:
        print(f"   • .{cls}")
    
    if len(css_classes) > 10:
        print(f"   ... and {len(css_classes) - 10} more\n")
    
    print("\n" + "=" * 60 + "\n")
    
    suggest_fixes()


if __name__ == "__main__":
    main()
