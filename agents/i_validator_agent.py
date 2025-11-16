from .llm_client import get_llm_response
import os
import re
import json
from dotenv import load_dotenv

load_dotenv()


def validate(blade: str):
    """Basic structure validation (legacy function)"""
    system_prompt = """
You are a Laravel Blade syntax validator.

Your job is to check if a Blade template is structurally correct.

Requirements:
- All sections must be closed properly with @endsection.
- Blade directives like @extends, @include must use correct syntax.
- No missing or unmatched brackets.

If valid, return: VALID.
If invalid, return: INVALID + brief reason.
Only output this result. No code block.
"""

    # Use unified LLM client (prioritizes Cerebras, falls back to Mistral)
    try:
        result = get_llm_response(
            system_prompt=system_prompt,
            user_prompt=blade,
            temperature=0.3,
            max_tokens=32000,
        )

        # Display response character by character for visual feedback
        for char in result:
            print(char, end="", flush=True)

    except Exception as e:
        print(f"❌ Failed to validate: {e}")
        result = "INVALID - Validation service unavailable"

    return result.strip().upper().startswith("VALID")


def auto_fix(blade: str, error_reason: str, draft_reference=None):
    """Auto-fix invalid Blade component (structure, styling, scripts)"""
    
    # If error reason is empty or too vague, skip auto-fix
    if not error_reason or error_reason.strip() == "" or "INVALID" not in error_reason:
        print(f"\n⚠️ Skipping auto-fix: unclear error reason")
        return blade
    
    system_prompt = """
You are a Laravel Blade expert fixer.

Your job is to fix SPECIFIC issues in Blade templates:
- Structure: missing closing tags, unmatched brackets, malformed directives
- Styling: incorrect Tailwind classes, colors, spacing, typography
- Scripts: missing Alpine.js directives, JavaScript functionality

CRITICAL RULES:
- Fix ONLY the specific error mentioned
- Preserve all existing functionality
- Return ONLY the fixed Blade code inside ```blade code block
- Do NOT add explanations or comments
- Do NOT change working parts of the code

Example fixes:
- Add missing closing tags: </div>, </section>
- Fix unmatched brackets: {{ }} or @endif
- Correct Blade directive syntax
"""

    draft_context = ""
    if draft_reference:
        draft_context = f"""

DRAFT REFERENCE (Source of Truth for Styling & Scripts):
```html
{draft_reference[:2000]}
```

⚠️ IMPORTANT: Match ALL styling and scripts from draft exactly."""

    user_prompt = f"""
Fix this SPECIFIC error in Blade component:

Error: {error_reason}

Code:
```blade
{blade[:3000]}
```
{draft_context}

Return ONLY the fixed code in ```blade block. Fix ONLY the error mentioned above.
"""

    try:
        result = get_llm_response(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.2,  # Lower temperature for more deterministic fixes
            max_tokens=32000,
        )

        # Print AI response for debugging
        print(f"\n{'='*60}")
        print(f"[AI AUTO-FIX RESPONSE]")
        print(f"{'='*60}")
        print(result[:500] if len(result) > 500 else result)
        if len(result) > 500:
            print(f"... (truncated, total length: {len(result)} chars)")
        print(f"{'='*60}\n")

        # Extract code from ```blade block
        match = re.findall(r"```blade\s*(.*?)```", result, re.DOTALL | re.IGNORECASE)
        if match:
            fixed_code = match[0].strip()
            print(f"\n✅ Extracted code from ```blade block (length: {len(fixed_code)} chars)")
            
            # Sanity check: fixed code should not be empty
            if len(fixed_code) > 50:
                print(f"✅ Sanity check passed, returning fixed code")
                return fixed_code
            else:
                print(f"\n⚠️ Fixed code too short ({len(fixed_code)} chars), using original")
                return blade
        else:
            # Try to extract any code block
            match = re.findall(r"```\s*(.*?)```", result, re.DOTALL)
            if match:
                fixed_code = match[0].strip()
                print(f"\n✅ Extracted code from generic ``` block (length: {len(fixed_code)} chars)")
                if len(fixed_code) > 50:
                    print(f"✅ Sanity check passed, returning fixed code")
                    return fixed_code
            
            print(f"\n⚠️ No valid code block found in LLM response, using original")
            return blade  # Return original if can't extract

    except Exception as e:
        print(f"\n❌ Auto-fix exception: {str(e)[:100]}")
        return blade  # Return original on error


def auto_fix_component(component_name, component_code, issues, draft_reference=None):
    """Use LLM to auto-fix component issues including styling and scripts"""
    
    if not issues:
        return component_code
    
    # Quick fix: Replace 'partials' with 'components' before LLM processing
    component_code = re.sub(r"@include\(['\"]partials\.", r"@include('components.", component_code)
    
    system_prompt = """You are a Laravel Blade expert. Fix ALL component issues while preserving functionality.

FIXES TO APPLY:
- Remove duplicate navbar/footer from content components
- Fix malformed route() calls
- Close unclosed tags
- Fix self-includes
- **CRITICAL**: Apply exact styling fixes (Tailwind classes) as specified
- Match colors, spacing, typography, layout with draft
- Preserve all Alpine.js directives and JavaScript functionality
- Preserve all content and functionality

STYLING FIX RULES:
- Replace incorrect Tailwind classes with correct ones from draft
- Add missing classes that exist in draft
- Maintain responsive breakpoints
- Keep hover/focus states consistent

SCRIPT FIX RULES:
- Preserve all Alpine.js directives (x-data, x-show, x-on:click, etc.)
- Keep all JavaScript event handlers
- Maintain interactivity (dropdowns, modals, toggles)

Return ONLY the fixed Blade code, no explanations."""

    issues_text = "\n".join([
        f"- [{issue.get('type', 'unknown').upper()}] {issue['message']}" + 
        (f"\n  Fix: {issue['fix']}" if 'fix' in issue else "")
        for issue in issues
    ])
    
    draft_context = ""
    if draft_reference:
        draft_context = f"""

DRAFT REFERENCE (Source of Truth):
```html
{draft_reference[:2000]}
```"""
    
    user_prompt = f"""Component: {component_name}

Issues to fix (structure + styling + scripts):
{issues_text}

Original code:
```blade
{component_code}
```
{draft_context}

Apply ALL fixes (structure + styling + scripts) and return the corrected code:"""

    try:
        fixed_code = get_llm_response(system_prompt, user_prompt, temperature=0.2, max_tokens=32000)
        
        # Extract code from markdown if present
        code_match = re.search(r'```(?:blade)?\s*(.*?)\s*```', fixed_code, re.DOTALL)
        if code_match:
            return code_match.group(1).strip()
        else:
            return fixed_code.strip()
            
    except Exception as e:
        print(f"  ⚠️ Auto-fix error for {component_name}: {e}")
        return component_code


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
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        return json.loads(json_match.group(0)) if json_match else {"is_valid": True, "issues": []}
    except:
        return {"is_valid": True, "issues": []}


def validate_component_styling(component_name, component_code, draft_reference):
    """Validate component styling vs draft (focused on colors, spacing, typography)"""
    
    if not draft_reference:
        return {"is_valid": True, "issues": []}
    
    system_prompt = """You are a styling validator. Check if styling matches draft.

CHECK THESE STYLING RULES:
1. Background colors: bg-* classes MUST match draft exactly
2. Text colors: text-* classes MUST match draft exactly  
3. Border colors: border-* classes MUST match draft exactly
4. Spacing: padding/margin (p-*, m-*) should match draft
5. Typography: font sizes (text-*) should match draft

ONLY report if styling is DIFFERENT from draft. Do NOT suggest improvements.

Respond with JSON:
{"is_valid": true/false, "issues": [{"severity": "error", "type": "styling", "message": "...", "fix": "exact class"}]}"""

    user_prompt = f"Component: {component_name}\n\nDraft:\n{draft_reference}\n\nComponent:\n{component_code}\n\nCompare styling."
    
    try:
        response = get_llm_response(system_prompt, user_prompt, temperature=0.2, max_tokens=500)
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        return json.loads(json_match.group(0)) if json_match else {"is_valid": True, "issues": []}
    except:
        return {"is_valid": True, "issues": []}


def validate_component_scripts(component_name, component_code, draft_reference):
    """Validate component scripts vs draft (Alpine.js, JavaScript)"""
    
    if not draft_reference:
        return {"is_valid": True, "issues": []}
    
    system_prompt = """You are a JavaScript/Alpine.js validator. Check if scripts match draft.

CHECK THESE SCRIPT RULES:
1. Alpine.js directives (x-data, x-show, x-on:click) should match draft functionality
2. JavaScript event handlers should match draft behavior
3. Data bindings should be consistent with draft
4. Interactive features (dropdowns, modals, toggles) should work like draft

ONLY report if functionality is MISSING or DIFFERENT from draft.

Respond with JSON:
{"is_valid": true/false, "issues": [{"severity": "error", "type": "script", "message": "...", "fix": "..."}]}"""

    user_prompt = f"Component: {component_name}\n\nDraft:\n{draft_reference}\n\nComponent:\n{component_code}\n\nCompare scripts and interactivity."
    
    try:
        response = get_llm_response(system_prompt, user_prompt, temperature=0.2, max_tokens=500)
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
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        return json.loads(json_match.group(0)) if json_match else {"is_valid": True, "issues": []}
    except:
        return {"is_valid": True, "issues": []}


def validate_with_reason(blade: str, draft_reference=None):
    """Validate structure, styling, and scripts - return reason if invalid"""
    
    # Quick syntax check first (no LLM) - RELAXED
    basic_issues = []
    
    # Only check critical syntax errors
    if blade.count('{{') != blade.count('}}'):
        basic_issues.append("Unmatched {{ }} brackets")
    
    # Allow some flexibility for @if/@endif (might be in comments or conditional)
    if blade.count('@if') > blade.count('@endif') + 2:  # Allow 2 difference
        basic_issues.append("Missing @endif")
    
    if blade.count('@foreach') > blade.count('@endforeach') + 1:
        basic_issues.append("Missing @endforeach")
    
    # Don't check div tags - too many false positives with SVG, self-closing tags, etc.
    # if blade.count('<div') > blade.count('</div>'):
    #     basic_issues.append("Unclosed <div> tags")
    
    if 'partials.' in blade:
        basic_issues.append("Using 'partials' directory instead of 'components'")
    
    # If basic issues found, return immediately
    if basic_issues:
        return False, "INVALID: " + "; ".join(basic_issues)
    
    # If no basic issues, consider it valid (skip LLM validation to save tokens)
    # LLM validation is too strict and gives vague errors
    return True, ""
    
    # Structure validation with LLM (fast, focused)
    system_prompt = """You are a Laravel Blade validator. Check these 5 critical errors:

1. Component has {{ $slot }} but called with @include? → Use <x-component>
2. Missing variables from @props? → Pass all variables
3. Unclosed tags or brackets? → Close them
4. Malformed route() calls? → Fix syntax
5. Using 'partials' directory? → Use 'components'

If valid: VALID
If invalid: INVALID: [brief specific reason]

Be concise and specific about the error."""

    try:
        result = get_llm_response(
            system_prompt=system_prompt,
            user_prompt=f"Validate:\n```blade\n{blade[:2000]}\n```",
            temperature=0.1,  # Very low for consistent validation
            max_tokens=200,
        )

        is_valid = result.strip().upper().startswith("VALID")
        reason = result.strip() if not is_valid else ""
        
        # If reason is too vague, add context
        if not is_valid and (not reason or len(reason) < 10):
            reason = "INVALID: Structure issues detected"
        
        # If structure valid and draft provided, check styling
        if is_valid and draft_reference:
            styling_prompt = """Check if styling (colors, spacing, typography) matches draft.

If styling matches: VALID
If styling differs: INVALID: [which styling differs]"""
            
            try:
                styling_result = get_llm_response(
                    system_prompt=styling_prompt,
                    user_prompt=f"Draft:\n{draft_reference}\n\nComponent:\n{blade}",
                    temperature=0.2,
                    max_tokens=300,
                )
                
                if not styling_result.strip().upper().startswith("VALID"):
                    return False, styling_result.strip()
            except:
                pass  # Skip styling check if fails
            
            # Check scripts/interactivity
            script_prompt = """Check if scripts and interactivity match draft.

If scripts match: VALID
If scripts differ: INVALID: [what's missing or different]"""
            
            try:
                script_result = get_llm_response(
                    system_prompt=script_prompt,
                    user_prompt=f"Draft:\n{draft_reference}\n\nComponent:\n{blade}",
                    temperature=0.2,
                    max_tokens=300,
                )
                
                if not script_result.strip().upper().startswith("VALID"):
                    return False, script_result.strip()
            except:
                pass  # Skip script check if fails
        
        return is_valid, reason

    except Exception as e:
        return False, f"INVALID: Validation service unavailable - {e}"



def load_draft_reference(page_name=None):
    """Load draft HTML for styling and script comparison"""
    if page_name:
        draft_path = f"output/drafts/{page_name}.html"
        if os.path.exists(draft_path):
            with open(draft_path, 'r', encoding='utf-8') as f:
                return f.read()
    
    # If no specific page, try to load any available draft
    drafts_dir = "output/drafts"
    if os.path.exists(drafts_dir):
        draft_files = [f for f in os.listdir(drafts_dir) if f.endswith('.html')]
        if draft_files:
            with open(os.path.join(drafts_dir, draft_files[0]), 'r', encoding='utf-8') as f:
                return f.read()
    
    return None


def validate_component_with_draft(component_name, component_code, draft_reference=None):
    """Validate component with structure, styling, script, and spacing checks"""
    
    # Check 1: Structure (fast)
    structure_result = validate_component_structure(component_name, component_code)
    
    # Check 2: Styling (only if draft provided)
    styling_result = validate_component_styling(component_name, component_code, draft_reference)
    
    # Check 3: Scripts (only if draft provided)
    script_result = validate_component_scripts(component_name, component_code, draft_reference)
    
    # Check 4: Header spacing (only for layout/page components with draft)
    spacing_result = {"issues": []}
    if draft_reference and ('layout' in component_name.lower() or 'page' in component_name.lower() or 'app' in component_name.lower()):
        spacing_result = validate_header_spacing(component_name, component_code, draft_reference)
    
    # Merge results
    all_issues = (
        structure_result.get('issues', []) + 
        styling_result.get('issues', []) + 
        script_result.get('issues', []) +
        spacing_result.get('issues', [])
    )
    
    return {
        "is_valid": len(all_issues) == 0,
        "issues": all_issues,
        "suggestions": []
    }
