"""
Multi-Page Validator - Comprehensive validation for multi-page Laravel applications
Validates routes, components, CSS, JavaScript, and consistency across all pages
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple, Set

class MultiPageValidator:
    def __init__(self, laravel_path: str = "my-laravel"):
        self.laravel_path = laravel_path
        self.views_path = os.path.join(laravel_path, "resources", "views")
        self.components_path = os.path.join(self.views_path, "components")
        self.routes_file = os.path.join(laravel_path, "routes", "web.php")
        self.errors = []
        self.warnings = []
        
    def validate_all(self) -> Tuple[bool, List[str], List[str]]:
        """Run all validations and return results"""
        print("🔍 Starting comprehensive multi-page validation...")
        
        self.errors = []
        self.warnings = []
        
        # Run all validation checks
        self._validate_file_structure()
        self._validate_no_nested_html()
        self._validate_routes()
        self._validate_components()
        self._validate_component_references()
        self._validate_route_calls()
        self._validate_css_consistency()
        self._validate_js_consistency()
        self._validate_duplicate_js()
        self._validate_layout_consistency()
        self._validate_blade_syntax()
        
        # Print results
        self._print_results()
        
        return len(self.errors) == 0, self.errors, self.warnings
    
    def _validate_file_structure(self):
        """Validate that all required directories and files exist"""
        print("📁 Validating file structure...")
        
        required_dirs = [
            self.views_path,
            self.components_path,
            os.path.join(self.views_path, "layouts")
        ]
        
        for dir_path in required_dirs:
            if not os.path.exists(dir_path):
                self.errors.append(f"Missing required directory: {dir_path}")
        
        # Check for layout file
        layout_file = os.path.join(self.views_path, "layouts", "app.blade.php")
        if not os.path.exists(layout_file):
            self.errors.append(f"Missing layout file: {layout_file}")
        
        # Check for routes file
        if not os.path.exists(self.routes_file):
            self.errors.append(f"Missing routes file: {self.routes_file}")
    
    def _validate_no_nested_html(self):
        """Validate that components don't have full HTML structure"""
        print("🔍 Checking for nested HTML structures...")
        
        if not os.path.exists(self.components_path):
            return
        
        component_files = [f for f in os.listdir(self.components_path) if f.endswith('.blade.php')]
        
        for component_file in component_files:
            component_path = os.path.join(self.components_path, component_file)
            
            with open(component_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for full HTML structure
            has_doctype = re.search(r'<!DOCTYPE html>', content, re.IGNORECASE)
            has_html_tag = re.search(r'<html[^>]*>', content, re.IGNORECASE)
            has_head = re.search(r'<head>', content, re.IGNORECASE)
            has_body = re.search(r'<body[^>]*>', content, re.IGNORECASE)
            
            if has_doctype or has_html_tag or has_head or has_body:
                self.errors.append(
                    f"Component {component_file} has full HTML structure (DOCTYPE/html/head/body). "
                    f"Components should only contain partial HTML. Run: python utils/fix_nested_ui.py"
                )
    
    def _validate_routes(self):
        """Validate routes in web.php"""
        print("🛣️  Validating routes...")
        
        if not os.path.exists(self.routes_file):
            return
        
        with open(self.routes_file, 'r', encoding='utf-8') as f:
            routes_content = f.read()
        
        # Find all route definitions
        route_pattern = r"Route::get\(['\"]([^'\"]+)['\"],\s*function\s*\(\)\s*\{[^}]*return\s+view\(['\"]([^'\"]+)['\"]"
        routes = re.findall(route_pattern, routes_content)
        
        if not routes:
            self.warnings.append("No routes found in web.php")
            return
        
        # Check for duplicate routes
        route_paths = [r[0] for r in routes]
        duplicates = [path for path in route_paths if route_paths.count(path) > 1]
        if duplicates:
            self.errors.append(f"Duplicate route paths found: {set(duplicates)}")
        
        # Validate view files exist
        for route_path, view_name in routes:
            view_file = os.path.join(self.views_path, f"{view_name}.blade.php")
            if not os.path.exists(view_file):
                self.errors.append(f"Route '{route_path}' references non-existent view: {view_name}")
    
    def _validate_components(self):
        """Validate component files"""
        print("🧩 Validating components...")
        
        if not os.path.exists(self.components_path):
            return
        
        component_files = [f for f in os.listdir(self.components_path) if f.endswith('.blade.php')]
        
        if not component_files:
            self.warnings.append("No component files found")
            return
        
        for component_file in component_files:
            component_path = os.path.join(self.components_path, component_file)
            
            with open(component_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for empty components
            if len(content.strip()) < 10:
                self.warnings.append(f"Component {component_file} appears to be empty or too small")
            
            # Check for unclosed tags
            self._check_html_tags(content, component_file)
    
    def _validate_component_references(self):
        """Validate @include references in blade files"""
        print("📎 Validating component references...")
        
        blade_files = []
        for root, dirs, files in os.walk(self.views_path):
            for file in files:
                if file.endswith('.blade.php'):
                    blade_files.append(os.path.join(root, file))
        
        for blade_file in blade_files:
            with open(blade_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find all @include references
            includes = re.findall(r"@include\(['\"]components\.([^'\"]+)['\"]\)", content)
            
            for component_name in includes:
                component_file = os.path.join(self.components_path, f"{component_name}.blade.php")
                if not os.path.exists(component_file):
                    self.errors.append(
                        f"File {os.path.basename(blade_file)} references non-existent component: {component_name}"
                    )
    
    def _validate_route_calls(self):
        """Validate route() calls in blade files"""
        print("🔗 Validating route calls...")
        
        # Get all defined routes
        if not os.path.exists(self.routes_file):
            return
        
        with open(self.routes_file, 'r', encoding='utf-8') as f:
            routes_content = f.read()
        
        # Extract route names
        route_names = re.findall(r"->name\(['\"]([^'\"]+)['\"]\)", routes_content)
        route_paths = re.findall(r"Route::get\(['\"]([^'\"]+)['\"]", routes_content)
        
        # Check all blade files for route calls
        blade_files = []
        for root, dirs, files in os.walk(self.views_path):
            for file in files:
                if file.endswith('.blade.php'):
                    blade_files.append(os.path.join(root, file))
        
        for blade_file in blade_files:
            with open(blade_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find route() calls
            route_calls = re.findall(r"route\(['\"]([^'\"]+)['\"]\)", content)
            
            for route_call in route_calls:
                if route_call not in route_names:
                    # Check if it matches a path
                    matching_path = any(path.strip('/') == route_call.strip('/') for path in route_paths)
                    if not matching_path:
                        self.errors.append(
                            f"File {os.path.basename(blade_file)} calls undefined route: {route_call}"
                        )
    
    def _validate_css_consistency(self):
        """Validate CSS consistency across pages"""
        print("🎨 Validating CSS consistency...")
        
        layout_file = os.path.join(self.views_path, "layouts", "app.blade.php")
        if not os.path.exists(layout_file):
            return
        
        with open(layout_file, 'r', encoding='utf-8') as f:
            layout_content = f.read()
        
        # Extract CSS from layout
        layout_css = self._extract_css(layout_content)
        
        # Check all page files
        page_files = [f for f in os.listdir(self.views_path) if f.endswith('.blade.php') and f != 'app.blade.php']
        
        for page_file in page_files:
            page_path = os.path.join(self.views_path, page_file)
            with open(page_path, 'r', encoding='utf-8') as f:
                page_content = f.read()
            
            page_css = self._extract_css(page_content)
            
            # Check for conflicting styles
            if page_css and layout_css:
                # Look for duplicate selectors
                layout_selectors = set(re.findall(r'\.[\w-]+\s*\{', layout_css))
                page_selectors = set(re.findall(r'\.[\w-]+\s*\{', page_css))
                
                conflicts = layout_selectors & page_selectors
                if conflicts:
                    self.warnings.append(
                        f"Page {page_file} has CSS selectors that may conflict with layout: {conflicts}"
                    )
    
    def _validate_js_consistency(self):
        """Validate JavaScript consistency and safety"""
        print("⚡ Validating JavaScript safety...")
        
        blade_files = []
        for root, dirs, files in os.walk(self.views_path):
            for file in files:
                if file.endswith('.blade.php'):
                    blade_files.append(os.path.join(root, file))
        
        for blade_file in blade_files:
            with open(blade_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract JavaScript
            js_blocks = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
            
            for js_block in js_blocks:
                # Check for unsafe DOM access
                unsafe_patterns = [
                    (r'document\.getElementById\([^)]+\)\.', 'getElementById without null check'),
                    (r'document\.querySelector\([^)]+\)\.', 'querySelector without null check'),
                    (r'document\.getElementsByClassName\([^)]+\)\[', 'getElementsByClassName without length check'),
                ]
                
                for pattern, issue in unsafe_patterns:
                    if re.search(pattern, js_block):
                        # Check if there's a null check nearby
                        if 'if' not in js_block[:js_block.find(re.search(pattern, js_block).group())]:
                            self.warnings.append(
                                f"File {os.path.basename(blade_file)} has {issue}"
                            )
    
    def _validate_duplicate_js(self):
        """Validate for duplicate JavaScript blocks"""
        print("🔄 Checking for duplicate JavaScript...")
        
        layout_file = os.path.join(self.views_path, "layouts", "app.blade.php")
        
        if not os.path.exists(layout_file):
            return
        
        with open(layout_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract all JavaScript blocks
        js_blocks = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
        
        if len(js_blocks) > 1:
            # Check for duplicate code
            seen_js = set()
            duplicates = []
            
            for js_block in js_blocks:
                js_normalized = re.sub(r'\s+', ' ', js_block.strip())
                
                if js_normalized in seen_js:
                    duplicates.append(js_normalized[:100] + "...")
                else:
                    seen_js.add(js_normalized)
            
            if duplicates:
                self.errors.append(
                    f"Layout has duplicate JavaScript blocks. Run: python utils/fix_nested_ui.py"
                )
        
        # Check components for JavaScript (should be in layout only)
        if os.path.exists(self.components_path):
            component_files = [f for f in os.listdir(self.components_path) if f.endswith('.blade.php')]
            
            for component_file in component_files:
                component_path = os.path.join(self.components_path, component_file)
                
                with open(component_path, 'r', encoding='utf-8') as f:
                    comp_content = f.read()
                
                if '<script' in comp_content:
                    self.warnings.append(
                        f"Component {component_file} contains JavaScript. "
                        f"Consider moving to layout for better organization."
                    )
    
    def _validate_layout_consistency(self):
        """Validate that all pages use the same layout structure"""
        print("📐 Validating layout consistency...")
        
        page_files = [f for f in os.listdir(self.views_path) if f.endswith('.blade.php')]
        
        layouts_used = {}
        
        for page_file in page_files:
            page_path = os.path.join(self.views_path, page_file)
            with open(page_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for @extends
            extends_match = re.search(r"@extends\(['\"]([^'\"]+)['\"]\)", content)
            if extends_match:
                layout = extends_match.group(1)
                layouts_used[page_file] = layout
            else:
                self.warnings.append(f"Page {page_file} doesn't extend any layout")
        
        # Check if all pages use the same layout
        if layouts_used:
            unique_layouts = set(layouts_used.values())
            if len(unique_layouts) > 1:
                self.warnings.append(
                    f"Pages use different layouts: {dict((k, v) for k, v in layouts_used.items())}"
                )
    
    def _validate_blade_syntax(self):
        """Validate Blade syntax"""
        print("🔧 Validating Blade syntax...")
        
        blade_files = []
        for root, dirs, files in os.walk(self.views_path):
            for file in files:
                if file.endswith('.blade.php'):
                    blade_files.append(os.path.join(root, file))
        
        for blade_file in blade_files:
            with open(blade_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for common Blade syntax errors
            errors = []
            
            # Unclosed @section
            sections = re.findall(r'@section\([^)]+\)', content)
            endsections = re.findall(r'@endsection', content)
            if len(sections) != len(endsections):
                errors.append("Mismatched @section/@endsection")
            
            # Unclosed @if
            ifs = len(re.findall(r'@if\s*\(', content))
            endifs = len(re.findall(r'@endif', content))
            if ifs != endifs:
                errors.append("Mismatched @if/@endif")
            
            # Unclosed @foreach
            foreachs = len(re.findall(r'@foreach\s*\(', content))
            endforeachs = len(re.findall(r'@endforeach', content))
            if foreachs != endforeachs:
                errors.append("Mismatched @foreach/@endforeach")
            
            if errors:
                self.errors.append(f"Blade syntax errors in {os.path.basename(blade_file)}: {', '.join(errors)}")
    
    def _check_html_tags(self, content: str, filename: str):
        """Check for unclosed HTML tags"""
        # Simple tag matching
        opening_tags = re.findall(r'<(\w+)[^>]*>', content)
        closing_tags = re.findall(r'</(\w+)>', content)
        
        # Filter out self-closing tags
        self_closing = {'img', 'br', 'hr', 'input', 'meta', 'link'}
        opening_tags = [tag for tag in opening_tags if tag not in self_closing]
        
        # Count occurrences
        from collections import Counter
        opening_count = Counter(opening_tags)
        closing_count = Counter(closing_tags)
        
        for tag, count in opening_count.items():
            if closing_count.get(tag, 0) != count:
                self.warnings.append(
                    f"File {filename} may have unclosed <{tag}> tags: {count} opening, {closing_count.get(tag, 0)} closing"
                )
    
    def _extract_css(self, content: str) -> str:
        """Extract CSS from content"""
        css_blocks = re.findall(r'<style[^>]*>(.*?)</style>', content, re.DOTALL)
        return '\n'.join(css_blocks)
    
    def _print_results(self):
        """Print validation results"""
        print("\n" + "="*60)
        print("📊 VALIDATION RESULTS")
        print("="*60)
        
        if not self.errors and not self.warnings:
            print("✅ All validations passed! No errors or warnings found.")
        else:
            if self.errors:
                print(f"\n❌ ERRORS ({len(self.errors)}):")
                for i, error in enumerate(self.errors, 1):
                    print(f"  {i}. {error}")
            
            if self.warnings:
                print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
                for i, warning in enumerate(self.warnings, 1):
                    print(f"  {i}. {warning}")
        
        print("\n" + "="*60)
        
        if self.errors:
            print("❌ Validation FAILED - Please fix errors before proceeding")
        else:
            print("✅ Validation PASSED - Safe to proceed")
        print("="*60 + "\n")


def validate_multi_page_app(laravel_path: str = "my-laravel") -> bool:
    """
    Main validation function for multi-page applications
    Returns True if validation passes, False otherwise
    """
    validator = MultiPageValidator(laravel_path)
    is_valid, errors, warnings = validator.validate_all()
    return is_valid


if __name__ == "__main__":
    import sys
    laravel_path = sys.argv[1] if len(sys.argv) > 1 else "my-laravel"
    
    is_valid = validate_multi_page_app(laravel_path)
    sys.exit(0 if is_valid else 1)
