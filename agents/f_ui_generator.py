import os, sys
import re
from dotenv import load_dotenv
from .llm_client import get_llm_response

# Load .env
load_dotenv()


def detect_nested_components(components: dict):
    """Detect which components are nested inside others"""
    nested = set()
    
    for name, code in components.items():
        # Find all @include and <x- references in this component
        includes = re.findall(r"@include\(['\"]components\.(\w+)", code, re.IGNORECASE)
        x_tags = re.findall(r"<x-(\w+)", code, re.IGNORECASE)
        
        # Add to nested set
        for comp in includes + x_tags:
            nested.add(comp.lower())
    
    return nested


def generate_blade(layout: dict, components: dict, draft_html: str = ""):
    print("\n🟤 [UI GENERATOR AGENT] Generating Blade template using AI...")
    
    # Load draft HTML if not provided
    if not draft_html and os.path.exists("output/draft.html"):
        with open("output/draft.html", "r", encoding="utf-8") as f:
            draft_html = f.read()
            print(f"   📄 Loaded draft HTML ({len(draft_html)} chars) as reference")

    # 🔧 Detect nested components
    nested_components = detect_nested_components(components)
    if nested_components:
        print(f"   Detected nested components: {', '.join(nested_components)}")

    # 🔧 Build layout description
    section_desc = "\n".join(
        [
            f"- Section `{k}` contains component `{v}`"
            for k, v in layout.get("sections", {}).items()
        ]
    )

    # 🔧 Sertakan isi semua komponen apa adanya
    component_info = "\n\n".join(
        [
            f"🔹 {name}.blade.php:\n```blade\n{code.strip()}\n```"
            for name, code in components.items()
        ]
    )

    # Build nested components warning
    nested_warning = ""
    if nested_components:
        nested_list = ", ".join(nested_components)
        nested_warning = f"""
⚠️ NESTED COMPONENTS DETECTED:
The following components are already included inside other components: {nested_list}
DO NOT include these components separately in the main blade file!
"""

    # Build exact component names list and detect nested components
    component_names = list(components.keys())
    
    # Detect which components are nested (included by other components)
    nested_components = set()
    for comp_name, comp_code in components.items():
        # Find all @include references in this component
        includes = re.findall(r"@include\(['\"]components\.([^'\"]+)['\"]\)", comp_code)
        nested_components.update(includes)
        # Also check for <x-component> syntax
        x_components = re.findall(r"<x-([a-z\-]+)", comp_code)
        nested_components.update(x_components)
    
    # Top-level components are those NOT nested in others
    top_level_components = [name for name in component_names if name not in nested_components]
    
    component_names_list = "\n".join([f"  - {name}" for name in component_names])
    top_level_list = "\n".join([f"  - {name}" for name in top_level_components])
    nested_list = "\n".join([f"  - {name} (nested, don't include directly)" for name in nested_components]) if nested_components else "  (none)"
    
    user_prompt = f"""
🧭 Your Task:
Generate the `{layout['page']}.blade.php` file.

⚠️ TOP-LEVEL COMPONENTS (include these in main page):
{top_level_list}

⚠️ NESTED COMPONENTS (already included by other components, DON'T include directly):
{nested_list}

⚠️ ALL AVAILABLE COMPONENTS:
{component_names_list}

⚠️ Instruction:
1. Use `@extends` and `@section('content')` properly.
2. **ONLY include TOP-LEVEL components** - nested components are already included by their parent components
3. For components that contain `$slot`, use `<x-componentname>Content</x-componentname>` syntax.
4. For other components:
    - Use `@include('components.EXACTNAME', [...])`  ← Use EXACT name from TOP-LEVEL list
    - **CRITICAL**: Extract ALL variables from @props directive in component
    - If component has @props(['var1', 'var2', 'var3']), you MUST pass ALL three variables
    - Pass **dummy values** (e.g. `'iconColor' => 'blue-500'`, `'title' => 'Example'`) where necessary.
    - DO NOT omit any variable from @props, even if it seems optional
5. **DO NOT include nested components** - they are already included by their parent components

⚠️ CRITICAL RULES:
- ALWAYS use 'components' directory: @include('components.xxx')
- NEVER use 'partials' directory: @include('partials.xxx') ← WRONG!
- Use EXACT component names from the list above
- Do NOT modify component names (no dashes, no removing suffixes)
- Example: If component is 'headercomponent', use @include('components.headercomponent')
- Example: If component is 'herocomponent', use @include('components.herocomponent')
- WRONG: @include('components.header') when component is 'headercomponent'
- WRONG: @include('components.hero-component') when component is 'herocomponent'

⚠️ CRITICAL - Variable Passing:
- Check @props directive in each component
- Pass ALL variables listed in @props, no exceptions
- Example: @props(['icon', 'iconColor', 'title']) → MUST pass all 3
- Use sensible dummy values if real values not available
- Missing variables will cause "Undefined variable" errors

Warning:
- DO NOT Omit any required variable from @props
- DO NOT Copy or inline component content
- DO NOT Invent components not listed
- DO NOT Create Component UI Again, because already have on Blade Component
- DO NOT use 'partials' directory (use 'components' instead)
- DO NOT modify component names from the list
{nested_warning}

🧱 Layout Specification:
- Extends: `{layout['extends']}`
{section_desc}

🧩 Blade Components (with source code):
{component_info}

📄 **ORIGINAL DRAFT HTML (for reference):**
```html
{draft_html if draft_html else "Not available"}
```

⚠️ **IMPORTANT:** The components above were extracted from this draft HTML.
Make sure the final page structure matches the draft HTML layout order.
"""

    system_prompt = """
You are a Laravel Blade view generator AI.

Generate a Laravel Blade view file using the provided layout and Blade components.

**CRITICAL RULES:**
- The components were extracted from the draft HTML
- Arrange components in the SAME ORDER as they appear in the draft
- Use @extends('layouts.app') and @section('content') properly
- Use <x-componentname> for components with $slot
- Use @include(...) with full variable assignments for others
- Do NOT skip any required variable
- Do NOT include explanation or comments
- Match the draft HTML structure as closely as possible

⚠️ CRITICAL - Component Directory:
- ALL components are in 'components' directory
- NEVER use 'partials' directory
- Correct: @include('components.header')
- Correct: @include('components.footer')
- Correct: <x-hero-section>
- WRONG: @include('partials.header')
- WRONG: @include('partials.footer')

⚠️ CRITICAL - Component Naming:
- Component names are EXACTLY as provided in the component list
- Use the EXACT component name without modification
- Do NOT add dashes, do NOT remove 'component' suffix
- Do NOT change case or format
- Example: If component is 'headercomponent', use @include('components.headercomponent')
- Example: If component is 'herocomponent', use @include('components.herocomponent')
- WRONG: @include('components.header') when component is 'headercomponent'
- WRONG: @include('components.hero-component') when component is 'herocomponent'

⚠️ CRITICAL - Avoid Duplicates:
- Check if a component is already included inside another component
- DO NOT include child components separately if they're already part of a parent
- Example: If ContactSection already contains ContactForm, DO NOT include ContactForm again
- Example: If ProjectsSection already contains ProjectCard, DO NOT include ProjectCard again
- Only include TOP-LEVEL components (Header, Hero, About, Projects, Contact, Footer, etc.)

Respond only inside:
```blade
<!-- blade content -->
```
"""

    # Use unified LLM client (prioritizes Cerebras, falls back to Mistral)
    try:
        full_response = get_llm_response(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.7,
            max_tokens=32000,
        )

        # Display response character by character for visual feedback
        for i, char in enumerate(full_response):
            sanitized_char = char.replace("\n", " ").replace("\r", " ")
            sys.stdout.write(sanitized_char)
            sys.stdout.flush()

        print()  # New line after streaming display

    except Exception as e:
        print(f"\n❌ Failed to generate response: {e}")
        return ""

    # Ambil isi dalam ```blade ... ``` jika ada
    match = re.findall(r"```blade\s*(.*?)```", full_response, re.DOTALL | re.IGNORECASE)
    
    # Normalize filename: lowercase, remove dashes and underscores
    # This ensures consistency with route naming
    page_name = layout['page'].lower().replace('-', '').replace('_', '').replace(' ', '')
    
    with open(f"output/{page_name}.blade.php", "w", encoding="utf-8") as f:
        f.write(match[0].strip() if match else full_response.strip())
    
    print(f"\n✅ Saved: output/{page_name}.blade.php")
    return match[0].strip() if match else full_response.strip()
