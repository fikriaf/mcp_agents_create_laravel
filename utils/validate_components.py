"""
Comprehensive component validator
Detects common styling issues and provides fixes
"""

import os
import re


def validate_component(filepath, available_css_classes):
    """Validate a single component and return issues"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    issues = []
    
    # 1. Check for inline background-image styles
    if 'style="background-image:' in content or "style='background-image:" in content:
        if 'hero' in available_css_classes:
            issues.append({
                'type': 'inline_style',
                'severity': 'warning',
                'message': 'Inline background-image found, should use .hero class',
                'fix': 'Remove inline style and add .hero class'
            })
    
    # 2. Check for Tailwind bg-[url(...)]
    if 'bg-[url(' in content:
        issues.append({
            'type': 'tailwind_arbitrary',
            'severity': 'error',
            'message': 'Tailwind bg-[url(...)] not supported in CDN',
            'fix': 'Use .hero class instead'
        })
    
    # 3. Check for hardcoded colors
    hardcoded_colors = re.findall(r'(bg-(?:red|blue|green|yellow|purple)-\d+)', content)
    if hardcoded_colors:
        issues.append({
            'type': 'hardcoded_color',
            'severity': 'warning',
            'message': f'Hardcoded colors found: {", ".join(set(hardcoded_colors))}',
            'fix': 'Use CSS variables (bg-primary-color, bg-secondary-color)'
        })
    
    # 4. Check for @apply in components (should only be in layout)
    if '@apply' in content:
        issues.append({
            'type': 'apply_directive',
            'severity': 'error',
            'message': '@apply directive found in component',
            'fix': 'Use pure CSS or Tailwind classes'
        })
    
    # 5. Check for missing route() in href
    plain_hrefs = re.findall(r'href=["\']([a-zA-Z0-9\-_]+)["\']', content)
    for href in plain_hrefs:
        if href not in ['#', ''] and not href.startswith('http'):
            issues.append({
                'type': 'plain_href',
                'severity': 'info',
                'message': f'Plain href found: {href}',
                'fix': 'Consider using route() helper'
            })
    
    # 6. Check for undefined route() calls
    route_calls = re.findall(r"route\(['\"]([^'\"]+)['\"]\)", content)
    if route_calls:
        issues.append({
            'type': 'route_call',
            'severity': 'info',
            'message': f'Route calls found: {", ".join(set(route_calls))}',
            'fix': 'Ensure routes exist in web.php'
        })
    
    return issues


def validate_all_components():
    """Validate all components and report issues"""
    components_dir = "my-laravel/resources/views/components"
    
    if not os.path.exists(components_dir):
        print("❌ Components directory not found")
        return
    
    # Get available CSS classes from layout
    layout_path = "my-laravel/resources/views/layouts/app.blade.php"
    available_classes = set()
    
    if os.path.exists(layout_path):
        with open(layout_path, 'r', encoding='utf-8') as f:
            layout_content = f.read()
        
        style_match = re.search(r'<style>(.*?)</style>', layout_content, re.DOTALL)
        if style_match:
            css_content = style_match.group(1)
            class_pattern = r'\.([a-zA-Z0-9_-]+)\s*\{'
            available_classes = set(re.findall(class_pattern, css_content))
    
    print(f"🔍 Validating components...")
    print(f"   📋 Available CSS classes: {len(available_classes)}\n")
    
    total_issues = 0
    components_with_issues = 0
    
    for filename in sorted(os.listdir(components_dir)):
        if filename.endswith('.blade.php'):
            filepath = os.path.join(components_dir, filename)
            issues = validate_component(filepath, available_classes)
            
            if issues:
                components_with_issues += 1
                print(f"⚠️  {filename}")
                
                for issue in issues:
                    severity_icon = {
                        'error': '❌',
                        'warning': '⚠️',
                        'info': 'ℹ️'
                    }.get(issue['severity'], '•')
                    
                    print(f"   {severity_icon} [{issue['type']}] {issue['message']}")
                    print(f"      💡 Fix: {issue['fix']}")
                
                total_issues += len(issues)
                print()
    
    print("=" * 60)
    if total_issues == 0:
        print("✅ All components validated successfully!")
    else:
        print(f"⚠️  Found {total_issues} issue(s) in {components_with_issues} component(s)")
        print("\n💡 Run 'python utils/fix_component_styling.py' to auto-fix")
    print("=" * 60)


def main():
    print("🔍 Component Validator\n")
    validate_all_components()


if __name__ == "__main__":
    main()
