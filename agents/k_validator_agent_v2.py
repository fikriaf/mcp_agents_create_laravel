"""
LLM-Powered Structure Validator Agent V2
Uses AI to understand component structure and detect issues
"""

import os
import re
from .llm_client import get_llm_response


def validate_component_structure(component_name, component_code):
    """Validate component structure only (fast, focused)"""
    
    system_prompt = """You are a Laravel Blade validator. Check ONLY structure issues.

CHECK THESE 5 CRITICAL RULES:
1. Component has {{ $slot }} but no @props directive? → Add @props(['slot'])
2. Component uses undefined variables? → Check @props matches all {{ $variable }}
3. Component includes itself? → Infinite loop error
4. Malformed route() calls? → Fix syntax
5. Unclosed HTML tags? → Close them

Respond with JSON:
{"is_valid": true/false, "issues": [{"severity": "error", "message": "...", "fix": "..."}]}"""

    user_prompt = f"Component: {component_name}\n\n```blade\n{component_code[:2000]}\n```\n\nCheck structure only."
    
    try:
        response = get_llm_response(system_prompt, user_prompt, temperature=0.2, max_tokens=500)
        import json
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        return json.loads(json_match.group(0)) if json_match else {"is_valid": True, "issues": []}
    except:
        return {"is_valid": True, "issues": []}


def validate_component_styling(component_name, component_code, draft_reference):
    """Validate component styling vs draft (focused on colors)"""
    
    if not draft_reference:
        return {"is_valid": True, "issues": []}
    
    system_prompt = """You are a styling validator. Check ONLY if colors match draft.

CHECK THESE 3 RULES:
1. Background colors: bg-* classes MUST match draft exactly
2. Text colors: text-* classes MUST match draft exactly  
3. Border colors: border-* classes MUST match draft exactly

ONLY report if colors are DIFFERENT. Do NOT suggest improvements.

Respond with JSON:
{"is_valid": true/false, "issues": [{"severity": "error", "type": "styling", "message": "...", "fix": "exact class"}]}"""

    user_prompt = f"Component: {component_name}\n\nDraft:\n{draft_reference}\n\nComponent:\n{component_code}\n\nCompare colors only."
    
    try:
        response = get_llm_response(system_prompt, user_prompt, temperature=0.2, max_tokens=500)
        import json
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        return json.loads(json_match.group(0)) if json_match else {"is_valid": True, "issues": []}
    except:
        return {"is_valid": True, "issues": []}


def validate_header_spacing(component_name, component_code, draft_reference):
    """Validate spacing between header and main content sections"""
    
    if not draft_reference:
        return {"is_valid": True, "issues": []}
    
    system_prompt = """You are a layout spacing validator. Check spacing between header/navbar and main content.

CHECK THESE SPACING RULES:
1. Is there appropriate vertical spacing (margin/padding) between header and main content?
2. Does the spacing match the draft design?
3. Common spacing classes: mt-16, mt-20, pt-16, pt-20, py-16, py-20
4. Header should not overlap with content below it
5. Spacing should be consistent across responsive breakpoints

ONLY report if spacing is MISSING, TOO SMALL, or DIFFERENT from draft.

Respond with JSON:
{"is_valid": true/false, "issues": [{"severity": "warning", "type": "spacing", "message": "...", "fix": "add mt-20 or pt-20 class"}]}"""

    user_prompt = f"Component: {component_name}\n\nDraft:\n{draft_reference}\n\nComponent:\n{component_code}\n\nCheck spacing between header and main content."
    
    try:
        response = get_llm_response(system_prompt, user_prompt, temperature=0.2, max_tokens=500)
        import json
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        return json.loads(json_match.group(0)) if json_match else {"is_valid": True, "issues": []}
    except:
        return {"is_valid": True, "issues": []}


def validate_component_with_llm(component_name, component_code, draft_reference=None):
    """Validate component with focused, separate checks including spacing"""
    
    # Check 1: Structure (fast)
    structure_result = validate_component_structure(component_name, component_code)
    
    # Check 2: Styling (only if draft provided)
    styling_result = validate_component_styling(component_name, component_code, draft_reference)
    
    # Check 3: Header spacing (only for layout/page components with draft)
    spacing_result = {"issues": []}
    if draft_reference and ('layout' in component_name.lower() or 'page' in component_name.lower() or 'app' in component_name.lower()):
        spacing_result = validate_header_spacing(component_name, component_code, draft_reference)
    
    # Merge results
    all_issues = (
        structure_result.get('issues', []) + 
        styling_result.get('issues', []) +
        spacing_result.get('issues', [])
    )
    
    return {
        "is_valid": len(all_issues) == 0,
        "issues": all_issues,
        "suggestions": []
    }

    draft_context = ""
    if draft_reference:
        draft_context = f"""

DRAFT REFERENCE (Original Design - THIS IS THE SOURCE OF TRUTH FOR STYLING):
```html
{draft_reference[:3000]}
```

⚠️ IMPORTANT: Compare ALL styling classes between draft and component.
Report ANY differences in colors, spacing, typography, layout, borders, shadows, etc.
The component MUST match the draft styling exactly."""

    user_prompt = f"""Component: {component_name}

Generated Component Code:
```blade
{component_code[:3000]}
```
{draft_context}

Validate this component thoroughly:
1. Check structure issues
2. **CRITICALLY IMPORTANT**: Compare styling with draft HTML and report ALL differences
3. Provide exact class fixes to match draft styling

Report all structural AND styling issues."""

    try:
        response = get_llm_response(system_prompt, user_prompt, temperature=0.3, max_tokens=1000)
        
        # Extract JSON from response
        import json
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group(0))
            return result
        else:
            return {"is_valid": True, "issues": [], "suggestions": []}
            
    except Exception as e:
        print(f"  ⚠️ LLM validation error for {component_name}: {e}")
        return {"is_valid": True, "issues": [], "suggestions": []}


def validate_page_with_llm(page_name, page_code, available_components):
    """Validate page structure (focused check)"""
    
    system_prompt = """You are a Laravel Blade validator. Check ONLY these 4 critical errors:

1. Using @include for component with {{ $slot }}? → Use <x-component> instead
2. Missing variables in @include? → Pass all @props variables
3. Duplicate @include for same component? → Remove duplicates
4. Using 'partials' directory? → Use 'components' instead

Respond with JSON:
{"is_valid": true/false, "issues": [{"severity": "error", "message": "...", "fix": "..."}]}"""

    user_prompt = f"""Page: {page_name}

Available components: {', '.join(available_components)}

Code:
```blade
{page_code}
```

Validate this page structure."""

    try:
        response = get_llm_response(system_prompt, user_prompt, temperature=0.3, max_tokens=800)
        
        import json
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group(0))
            return result
        else:
            return {"is_valid": True, "issues": []}
            
    except Exception as e:
        print(f"  ⚠️ LLM validation error for {page_name}: {e}")
        return {"is_valid": True, "issues": []}


def auto_fix_component(component_name, component_code, issues):
    """Use LLM to auto-fix component issues including styling"""
    
    if not issues:
        return component_code
    
    # Quick fix: Replace 'partials' with 'components' before LLM processing
    component_code = re.sub(r"@include\(['\"]partials\.", r"@include('components.", component_code)
    
    system_prompt = """You are a Laravel Blade expert. Fix the component issues while preserving functionality.

FIXES TO APPLY:
- Remove duplicate navbar/footer from content components
- Fix malformed route() calls
- Close unclosed tags
- Fix self-includes
- **CRITICAL**: Apply exact styling fixes (Tailwind classes) as specified
- Match colors, spacing, typography, layout with draft
- Preserve all content and functionality

STYLING FIX RULES:
- Replace incorrect Tailwind classes with correct ones from draft
- Add missing classes that exist in draft
- Maintain responsive breakpoints
- Keep hover/focus states consistent

Return ONLY the fixed Blade code, no explanations."""

    issues_text = "\n".join([
        f"- [{issue.get('type', 'unknown').upper()}] {issue['message']}" + 
        (f"\n  Fix: {issue['fix']}" if 'fix' in issue else "")
        for issue in issues
    ])
    
    user_prompt = f"""Component: {component_name}

Issues to fix (including styling):
{issues_text}

Original code:
```blade
{component_code}
```

Apply ALL fixes (structure + styling) and return the corrected code:"""

    try:
        fixed_code = get_llm_response(system_prompt, user_prompt, temperature=0.2, max_tokens=8000)
        
        # Extract code from markdown if present
        code_match = re.search(r'```(?:blade)?\s*(.*?)\s*```', fixed_code, re.DOTALL)
        if code_match:
            return code_match.group(1).strip()
        else:
            return fixed_code.strip()
            
    except Exception as e:
        print(f"  ⚠️ Auto-fix error for {component_name}: {e}")
        return component_code


def load_draft_reference(page_name):
    """Load draft HTML for styling comparison"""
    draft_path = f"output/drafts/{page_name}.html"
    if os.path.exists(draft_path):
        with open(draft_path, 'r', encoding='utf-8') as f:
            return f.read()
    return None


def get_available_routes():
    """Extract available route names from web.php"""
    routes_file = "my-laravel/routes/web.php"
    available_routes = []
    
    if os.path.exists(routes_file):
        with open(routes_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract route names: ->name('routename')
        route_matches = re.findall(r"->name\(['\"]([^'\"]+)['\"]\)", content)
        available_routes = route_matches
    
    return available_routes


def validate_all_with_llm(callback=None):
    """Validate all components and pages using LLM with draft styling comparison
    
    Args:
        callback: optional function to send progress updates (for WebSocket)
    """
    
    def log(message):
        """Helper to print and optionally send to callback"""
        print(message)
        if callback:
            callback(message)
    
    log("\n[LLM VALIDATOR V2] Analyzing structure AND styling with AI...\n")
    
    all_issues = []
    components_to_fix = {}
    
    # Get available components
    components_dir = "my-laravel/resources/views/components"
    available_components = []
    if os.path.exists(components_dir):
        available_components = [f.replace('.blade.php', '') for f in os.listdir(components_dir) if f.endswith('.blade.php')]
    
    # Get available routes
    available_routes = get_available_routes()
    log(f"[INFO] Available routes: {', '.join(available_routes)}")
    
    # Load draft references for styling comparison
    drafts_dir = "output/drafts"
    draft_files = {}
    if os.path.exists(drafts_dir):
        for draft_file in os.listdir(drafts_dir):
            if draft_file.endswith('.html'):
                page_name = draft_file.replace('.html', '')
                draft_files[page_name] = load_draft_reference(page_name)
        log(f"[INFO] Loaded {len(draft_files)} draft(s) for styling comparison")
    
    # Validate components with draft styling comparison
    if os.path.exists(components_dir):
        log("Validating Components (Structure + Styling):")
        component_files = [f for f in os.listdir(components_dir) if f.endswith('.blade.php')]
        
        for idx, filename in enumerate(component_files, 1):
            component_name = filename.replace('.blade.php', '')
            filepath = os.path.join(components_dir, filename)
            
            # Only log every 3 components to reduce noise
            if idx == 1 or idx % 3 == 0 or idx == len(component_files):
                log(f"  Analyzing components... ({idx}/{len(component_files)})")
            
            with open(filepath, 'r', encoding='utf-8') as f:
                code = f.read()
            
            # Quick fix: Fix malformed route syntax (route('home') }}"home') }} → route('home') }})
            malformed_pattern = r"route\(['\"]([^'\"]+)['\"]\)\s*\}\}['\"]([^'\"]+)['\"]"
            if re.search(malformed_pattern, code):
                log(f"      Auto-fixing malformed route syntax...")
                code = re.sub(malformed_pattern, r"route('\1') }}", code)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(code)
            
            # Quick fix: Check for undefined routes
            route_matches = re.findall(r"route\(['\"]([^'\"]+)['\"]\)", code)
            undefined_routes = [r for r in route_matches if r not in available_routes]
            
            if undefined_routes:
                log(f"      Auto-fixing undefined routes: {', '.join(undefined_routes)}")
                for undefined_route in undefined_routes:
                    # Replace with '#' or closest match
                    if undefined_route == 'register':
                        # Replace register with login or #
                        code = re.sub(
                            rf"route\(['\"]register['\"]\)",
                            "'#'",
                            code
                        )
                    else:
                        # Replace with '#' for safety
                        code = re.sub(
                            rf"route\(['\"]" + re.escape(undefined_route) + rf"['\"]\)",
                            "'#'",
                            code
                        )
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(code)
            
            # Try to find matching draft for styling comparison
            draft_reference = None
            for page_name, draft_content in draft_files.items():
                if draft_content:
                    draft_reference = draft_content
                    break
            
            result = validate_component_with_llm(component_name, code, draft_reference)
            
            if not result.get('is_valid', True):
                log(f"  ❌ {component_name}:")
                for issue in result.get('issues', []):
                    severity_icon = "❌" if issue['severity'] == 'error' else "⚠️"
                    issue_type = issue.get('type', 'unknown')
                    log(f"     {severity_icon} [{issue_type.upper()}] {issue['message']}")
                    if 'fix' in issue:
                        log(f"        Fix: {issue['fix']}")
                    all_issues.append(issue)
                
                components_to_fix[component_name] = {
                    'path': filepath,
                    'code': code,
                    'issues': result.get('issues', [])
                }
            else:
                log(f"  ✅ {component_name}")
                if result.get('suggestions'):
                    for suggestion in result['suggestions']:
                        log(f"     [SUGGESTION] {suggestion}")
    
    log("")
    
    # Validate pages
    views_dir = "my-laravel/resources/views"
    if os.path.exists(views_dir):
        log("Validating Pages with AI:")
        page_files = [f for f in os.listdir(views_dir) if f.endswith('.blade.php') and f != 'welcome.blade.php']
        
        for idx, filename in enumerate(page_files, 1):
            page_name = filename.replace('.blade.php', '')
            filepath = os.path.join(views_dir, filename)
            
            # Only log progress, not every page
            if idx == 1 or idx == len(page_files):
                log(f"  Analyzing pages... ({idx}/{len(page_files)})")
            
            with open(filepath, 'r', encoding='utf-8') as f:
                code = f.read()
            
            # Quick fix: Replace 'partials' with 'components' before validation
            fixed = False
            if 'partials' in code:
                log(f"      Auto-fixing 'partials' → 'components'...")
                code = re.sub(r"@include\(['\"]partials\.", r"@include('components.", code)
                fixed = True
            
            # Quick fix: Remove kebab-case from component names (privacy-policy-content → privacypolicycontent)
            kebab_pattern = r"@include\(['\"]components\.([a-z]+(?:-[a-z]+)+)['\"]"
            kebab_matches = re.findall(kebab_pattern, code)
            if kebab_matches:
                log(f"      Auto-fixing kebab-case component names...")
                for kebab_name in kebab_matches:
                    camel_name = kebab_name.replace('-', '')
                    code = code.replace(f"components.{kebab_name}", f"components.{camel_name}")
                fixed = True
            
            # Quick fix: Check for component name mismatches
            include_pattern = r"@include\(['\"]components\.([a-z]+)['\"]"
            include_matches = re.findall(include_pattern, code)
            for included_name in include_matches:
                # Check if component exists
                if included_name not in available_components:
                    # Try to find close match
                    close_match = None
                    for comp in available_components:
                        if included_name in comp or comp in included_name:
                            close_match = comp
                            break
                    
                    if close_match:
                        log(f"      Auto-fixing component name: {included_name} → {close_match}")
                        code = code.replace(f"components.{included_name}", f"components.{close_match}")
                        fixed = True
            
            # Quick fix: Check for undefined routes in pages
            route_matches = re.findall(r"route\(['\"]([^'\"]+)['\"]\)", code)
            undefined_routes = [r for r in route_matches if r not in available_routes]
            
            if undefined_routes:
                log(f"      Auto-fixing undefined routes: {', '.join(undefined_routes)}")
                for undefined_route in undefined_routes:
                    code = re.sub(
                        rf"route\(['\"]" + re.escape(undefined_route) + rf"['\"]\)",
                        "'#'",
                        code
                    )
                fixed = True
            
            if fixed:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(code)
            
            result = validate_page_with_llm(page_name, code, available_components)
            
            if not result.get('is_valid', True):
                log(f"  ❌ {page_name}:")
                for issue in result.get('issues', []):
                    severity_icon = "❌" if issue['severity'] == 'error' else "⚠️"
                    log(f"     {severity_icon} {issue['message']}")
                    if 'fix' in issue:
                        log(f"        Fix: {issue['fix']}")
                    all_issues.append(issue)
            else:
                log(f"  ✅ {page_name}")
    
    log(f"\n{'='*60}")
    
    # Auto-fix if issues found
    if components_to_fix:
        log(f"Auto-fixing {len(components_to_fix)} component(s)...\n")
        
        for idx, (component_name, info) in enumerate(components_to_fix.items(), 1):
            # Only log progress, not every component
            if idx == 1 or idx % 3 == 0 or idx == len(components_to_fix):
                log(f"  Fixing components... ({idx}/{len(components_to_fix)})")
            
            # Show issues being fixed (only for first and last)
            if idx == 1 or idx == len(components_to_fix):
                structure_issues = [i for i in info['issues'] if i.get('type') == 'structure']
                styling_issues = [i for i in info['issues'] if i.get('type') == 'styling']
                
                if structure_issues:
                    log(f"      - {len(structure_issues)} structure issue(s)")
                if styling_issues:
                    log(f"      - {len(styling_issues)} styling issue(s)")
            
            fixed_code = auto_fix_component(component_name, info['code'], info['issues'])
            
            # Save fixed code
            with open(info['path'], 'w', encoding='utf-8') as f:
                f.write(fixed_code)
            
            log(f"  ✅ {component_name} fixed and saved")
        
        log(f"\n{'='*60}")
    
    # Summary
    structure_count = len([i for i in all_issues if i.get('type') == 'structure'])
    styling_count = len([i for i in all_issues if i.get('type') == 'styling'])
    
    if all_issues:
        log(f"Validation Summary:")
        log(f"   - Total issues found: {len(all_issues)}")
        if structure_count > 0:
            log(f"   - Structure issues: {structure_count}")
        if styling_count > 0:
            log(f"   - Styling issues: {styling_count}")
        log(f"   - All issues auto-fixed ✅")
    else:
        log("✅ All structures and styling are valid!")
    
    log(f"{'='*60}")
    
    return len(all_issues) == 0


if __name__ == "__main__":
    validate_all_with_llm()
