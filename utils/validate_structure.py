"""
Comprehensive structure validator for Laravel Blade files
Validates component structure, nesting, and common issues
"""

import os
import re


def validate_component_structure(component_path):
    """Validate a single component for structural issues"""
    issues = []
    
    with open(component_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    component_name = os.path.basename(component_path).replace('.blade.php', '')
    
    # Check 1: Component should NOT have <header> or <footer> tags (unless it IS header/footer component)
    if component_name not in ['header', 'footer', 'navbar']:
        if '<header' in content or '<nav' in content.lower():
            if 'class="navbar"' in content or 'class="nav' in content:
                issues.append(f"⚠️  {component_name}: Contains navbar (should use @include('components.header') instead)")
        
        if '<footer' in content:
            issues.append(f"⚠️  {component_name}: Contains footer (should use @include('components.footer') instead)")
    
    # Check 2: Component should NOT include itself
    self_include_patterns = [
        f"@include('components.{component_name}')",
        f"@include(\"components.{component_name}\")",
        f"<x-{component_name}",
    ]
    for pattern in self_include_patterns:
        if pattern in content:
            issues.append(f"❌ {component_name}: Includes itself (infinite loop!)")
    
    # Check 3: Check for malformed route() calls
    malformed_routes = re.findall(r'route\([\'"][^\'"]+[\'"]\)[\'"][^\'"]+[\'"]\)\s*}}', content)
    if malformed_routes:
        issues.append(f"❌ {component_name}: Malformed route() calls detected: {len(malformed_routes)} instances")
    
    # Check 4: Check for unclosed tags
    header_open = content.count('<header')
    header_close = content.count('</header>')
    if header_open != header_close:
        issues.append(f"❌ {component_name}: Unclosed <header> tags ({header_open} open, {header_close} close)")
    
    footer_open = content.count('<footer')
    footer_close = content.count('</footer>')
    if footer_open != footer_close:
        issues.append(f"❌ {component_name}: Unclosed <footer> tags ({footer_open} open, {footer_close} close)")
    
    nav_open = content.count('<nav')
    nav_close = content.count('</nav>')
    if nav_open != nav_close:
        issues.append(f"❌ {component_name}: Unclosed <nav> tags ({nav_open} open, {nav_close} close)")
    
    return issues


def validate_page_structure(page_path):
    """Validate a page blade file"""
    issues = []
    
    with open(page_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    page_name = os.path.basename(page_path).replace('.blade.php', '')
    
    # Check 1: Page should extend layout
    if '@extends' not in content:
        issues.append(f"⚠️  {page_name}: Does not extend a layout")
    
    # Check 2: Check for duplicate includes
    includes = re.findall(r"@include\(['\"]([^'\"]+)['\"]\)", content)
    include_counts = {}
    for inc in includes:
        include_counts[inc] = include_counts.get(inc, 0) + 1
    
    for inc, count in include_counts.items():
        if count > 1:
            issues.append(f"⚠️  {page_name}: Includes '{inc}' {count} times (duplicate?)")
    
    # Check 3: Check for wrong include syntax (PascalCase without components. prefix)
    wrong_includes = re.findall(r"@include\(['\"]([A-Z][^'\"]+)['\"]\)", content)
    for inc in wrong_includes:
        if not inc.startswith('components.'):
            issues.append(f"❌ {page_name}: Wrong include syntax '{inc}' (should be 'components.{inc.lower()}')")
    
    return issues


def validate_all_structures():
    """Validate all blade files"""
    print("🔍 Validating Laravel Blade Structure\n")
    
    all_issues = []
    
    # Validate components
    components_dir = "my-laravel/resources/views/components"
    if os.path.exists(components_dir):
        print("📦 Validating Components:")
        for filename in os.listdir(components_dir):
            if filename.endswith('.blade.php'):
                filepath = os.path.join(components_dir, filename)
                issues = validate_component_structure(filepath)
                if issues:
                    all_issues.extend(issues)
                    for issue in issues:
                        print(f"  {issue}")
                else:
                    print(f"  ✅ {filename.replace('.blade.php', '')}")
    
    print()
    
    # Validate pages
    views_dir = "my-laravel/resources/views"
    if os.path.exists(views_dir):
        print("📄 Validating Pages:")
        for filename in os.listdir(views_dir):
            if filename.endswith('.blade.php') and filename != 'welcome.blade.php':
                filepath = os.path.join(views_dir, filename)
                issues = validate_page_structure(filepath)
                if issues:
                    all_issues.extend(issues)
                    for issue in issues:
                        print(f"  {issue}")
                else:
                    print(f"  ✅ {filename.replace('.blade.php', '')}")
    
    print(f"\n{'='*60}")
    if all_issues:
        print(f"❌ Found {len(all_issues)} issue(s)")
        print("\n💡 Run utilities to fix these issues:")
        print("   - python utils/fix_component_names.py")
        print("   - python utils/fix_existing_views.py")
    else:
        print("✅ All structures are valid!")
    print(f"{'='*60}")
    
    return len(all_issues) == 0


if __name__ == "__main__":
    validate_all_structures()
