"""
Fix Nested UI and Duplicate JavaScript Issues
Removes duplicate HTML structures and consolidates JavaScript
"""

import os
import re
from pathlib import Path

def fix_nested_ui(laravel_path: str = "my-laravel"):
    """Fix nested UI issues in multi-page applications"""
    print("🔧 Fixing nested UI and duplicate JavaScript...\n")
    
    # Step 1: Fix components with full HTML structure
    print("1️⃣ Fixing components with full HTML structure...")
    fix_component_html_structure(laravel_path)
    
    # Step 2: Remove duplicate JavaScript from layout
    print("\n2️⃣ Removing duplicate JavaScript from layout...")
    remove_duplicate_js_from_layout(laravel_path)
    
    # Step 3: Remove JavaScript from components (keep only in layout)
    print("\n3️⃣ Moving JavaScript from components to layout...")
    consolidate_component_js(laravel_path)
    
    print("\n✅ Nested UI and duplicate JavaScript fixed!")


def fix_component_html_structure(laravel_path: str = "my-laravel"):
    """Remove full HTML structure from components"""
    components_path = os.path.join(laravel_path, "resources", "views", "components")
    
    if not os.path.exists(components_path):
        return
    
    component_files = [f for f in os.listdir(components_path) if f.endswith('.blade.php')]
    
    for component_file in component_files:
        component_path = os.path.join(components_path, component_file)
        
        with open(component_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Check if component has full HTML structure
        has_html = re.search(r'<!DOCTYPE html>', content, re.IGNORECASE)
        has_head = re.search(r'<head>', content, re.IGNORECASE)
        has_body = re.search(r'<body[^>]*>', content, re.IGNORECASE)
        
        if has_html or has_head or has_body:
            print(f"   • Fixing {component_file}...")
            
            # Extract only the main content (inside <main> or <body>)
            main_content = extract_main_content(content)
            
            if main_content:
                # Keep the slot if it exists
                if '{{ $slot }}' in content:
                    # This is a layout component, convert to partial
                    content = convert_layout_component_to_partial(content)
                else:
                    content = main_content
                
                with open(component_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"      ✅ Converted to component-only structure")


def extract_main_content(html_content: str) -> str:
    """Extract main content from full HTML structure"""
    # Try to extract content from <main> tag
    main_match = re.search(r'<main[^>]*>(.*?)</main>', html_content, re.DOTALL)
    if main_match:
        return main_match.group(1).strip()
    
    # Try to extract content from <body> tag (excluding nav and footer)
    body_match = re.search(r'<body[^>]*>(.*?)</body>', html_content, re.DOTALL)
    if body_match:
        body_content = body_match.group(1)
        
        # Remove nav
        body_content = re.sub(r'<nav[^>]*>.*?</nav>', '', body_content, flags=re.DOTALL)
        
        # Remove footer
        body_content = re.sub(r'<footer[^>]*>.*?</footer>', '', body_content, flags=re.DOTALL)
        
        # Remove scripts
        body_content = re.sub(r'<script[^>]*>.*?</script>', '', body_content, flags=re.DOTALL)
        
        return body_content.strip()
    
    return html_content


def convert_layout_component_to_partial(html_content: str) -> str:
    """Convert layout component with {{ $slot }} to partial component"""
    # Extract the form container or main content area
    container_match = re.search(r'<div class="form-container[^"]*">(.*?{{ \$slot }}.*?)</div>', html_content, re.DOTALL)
    
    if container_match:
        container_content = container_match.group(1)
        
        # Clean up: remove nested title/description if they're duplicated
        # Keep only the slot and surrounding structure
        cleaned = re.sub(r'<div class="text-center[^"]*">.*?</div>\s*', '', container_content, count=1, flags=re.DOTALL)
        
        return f'<div class="form-container">\n{cleaned}\n</div>'
    
    # Fallback: just extract main content
    return extract_main_content(html_content)


def remove_duplicate_js_from_layout(laravel_path: str = "my-laravel"):
    """Remove duplicate JavaScript blocks from layout"""
    layout_file = os.path.join(laravel_path, "resources", "views", "layouts", "app.blade.php")
    
    if not os.path.exists(layout_file):
        return
    
    with open(layout_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Extract all JavaScript blocks
    js_blocks = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
    
    if len(js_blocks) > 1:
        print(f"   • Found {len(js_blocks)} JavaScript blocks")
        
        # Group by page-specific checks
        page_js_map = {}
        seen_code = set()
        
        for js_block in js_blocks:
            # Normalize for comparison
            normalized = re.sub(r'\s+', ' ', js_block.strip())
            
            # Skip if we've seen this exact code
            if normalized in seen_code:
                continue
            
            seen_code.add(normalized)
            
            # Find the page identifier (if statement checking for element)
            page_checks = re.findall(r"if \(document\.getElementById\(['\"]([^'\"]+)['\"]\)\)", js_block)
            
            if page_checks:
                # Use first element ID as key
                element_id = page_checks[0]
                
                # Store unique JS by element ID
                if element_id not in page_js_map:
                    # Extract the actual code inside the if block
                    # Remove outer if wrapper if it exists
                    clean_js = js_block.strip()
                    
                    # Check if entire block is wrapped in if
                    if clean_js.startswith('if (document.getElementById'):
                        # Extract content between first { and last }
                        brace_start = clean_js.find('{')
                        brace_end = clean_js.rfind('}')
                        if brace_start != -1 and brace_end != -1:
                            clean_js = clean_js[brace_start+1:brace_end].strip()
                    
                    page_js_map[element_id] = clean_js
        
        # Rebuild JavaScript section with unique blocks only
        if page_js_map:
            unique_js_blocks = []
            for elem_id, js_code in page_js_map.items():
                wrapped = f"        // ===== {elem_id} page JavaScript =====\n        if (document.getElementById('{elem_id}')) {{\n            {js_code}\n        }}"
                unique_js_blocks.append(wrapped)
            
            unique_js = '\n\n'.join(unique_js_blocks)
            
            # Remove all script tags
            content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
            
            # Add consolidated script before </body>
            content = content.replace('</body>', f'    <script>\n{unique_js}\n    </script>\n\n</body>')
            
            with open(layout_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"      ✅ Consolidated to {len(page_js_map)} unique JavaScript block(s)")


def consolidate_component_js(laravel_path: str = "my-laravel"):
    """Remove JavaScript from components and ensure it's in layout"""
    components_path = os.path.join(laravel_path, "resources", "views", "components")
    layout_file = os.path.join(laravel_path, "resources", "views", "layouts", "app.blade.php")
    
    if not os.path.exists(components_path):
        return
    
    component_files = [f for f in os.listdir(components_path) if f.endswith('.blade.php')]
    
    # Collect JavaScript from components
    component_js_map = {}
    
    for component_file in component_files:
        component_path = os.path.join(components_path, component_file)
        
        with open(component_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract JavaScript
        js_blocks = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
        
        if js_blocks:
            print(f"   • Found JavaScript in {component_file}")
            
            # Store JS
            component_name = component_file.replace('.blade.php', '')
            component_js_map[component_name] = js_blocks[0]
            
            # Remove JavaScript from component
            content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
            
            with open(component_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"      ✅ Removed JavaScript from component")
    
    # Add component JavaScript to layout if not already there
    if component_js_map and os.path.exists(layout_file):
        with open(layout_file, 'r', encoding='utf-8') as f:
            layout_content = f.read()
        
        for component_name, js_code in component_js_map.items():
            # Check if this JS is already in layout
            if js_code.strip() not in layout_content:
                print(f"   • Adding {component_name} JavaScript to layout")
                
                # Find a unique element ID from the JS
                element_match = re.search(r"getElementById\(['\"]([^'\"]+)['\"]\)", js_code)
                
                if element_match:
                    element_id = element_match.group(1)
                    
                    # Wrap in element check
                    wrapped_js = f"\n        // ===== {component_name} JavaScript =====\n        if (document.getElementById('{element_id}')) {{\n{js_code.strip()}\n        }}"
                    
                    # Add before closing script tag
                    layout_content = layout_content.replace('</script>', f'{wrapped_js}\n    </script>')
        
        with open(layout_file, 'w', encoding='utf-8') as f:
            f.write(layout_content)


if __name__ == "__main__":
    import sys
    laravel_path = sys.argv[1] if len(sys.argv) > 1 else "my-laravel"
    
    fix_nested_ui(laravel_path)
    
    print("\n🔍 Validating after fix...")
    from multi_page_validator import validate_multi_page_app
    validate_multi_page_app(laravel_path)
