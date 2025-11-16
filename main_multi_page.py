import json
import os
import shutil
import webbrowser
import datetime

# Removed: from agents.clean_history import clean_history (moved to utils_clean.py)
from agents.a_prompt_expander import prompt_expander
from agents.b_draft_agent_v2 import draft_agent_multi
from agents.c_prompt_planner_v2 import plan_prompt_multi
from agents.d_page_architect import design_layout
from agents.e_generate_layout_app import generate_layout_app
from agents.f_ui_generator import generate_blade
from agents.g_route_agent_v2 import generate_routes_multi
from agents.h_component_agent import list_components
from agents.i_validator_agent import validate
from agents.j_move_to_project import move_to_laravel_project


def save_history(prompt, draft):
    os.makedirs("history", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"history/{timestamp}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump({"prompt": prompt, "draft": draft}, f, indent=2)


def clean_laravel_views():
    """Clean previous generated views from Laravel project"""
    laravel_views = "my-laravel/resources/views"
    
    # Paths to clean
    paths_to_clean = [
        os.path.join(laravel_views, "components"),
        os.path.join(laravel_views, "layouts"),
    ]
    
    # Clean components and layouts
    for path in paths_to_clean:
        if os.path.exists(path):
            shutil.rmtree(path)
            print(f"🧹 Cleaned: {path}")
    
    # Clean blade files in views root (except welcome.blade.php)
    if os.path.exists(laravel_views):
        for file in os.listdir(laravel_views):
            if file.endswith('.blade.php') and file != 'welcome.blade.php':
                file_path = os.path.join(laravel_views, file)
                os.remove(file_path)
                print(f"🧹 Removed: {file}")
    
    # Reset routes to welcome
    route_file = "my-laravel/routes/web.php"
    default_routes = """<?php

use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return view('welcome');
});
"""
    with open(route_file, "w", encoding="utf-8") as f:
        f.write(default_routes)
    print(f"🧹 Reset routes to welcome")


def main():
    # Clean output folder
    if os.path.exists("output"):
        shutil.rmtree("output")
        print("🧹 Cleaned: output/")
    
    # Auto-clean Laravel views (no confirmation)
    print("🧹 Cleaning previous Laravel views...")
    clean_laravel_views()
    print("✅ Laravel views cleaned\n")

    # Note: clean_history moved to utils_clean.py and clean_project.py
    prev_draft = None

    # ========== PHASE 1: DRAFT GENERATION ==========
    while True:
        prompt = input("Prompt: ")

        # Smart revision: detect which pages to regenerate
        pages_to_regenerate = []
        if prev_draft and os.path.exists("output/drafts"):
            # Use LLM to detect which pages need revision
            print("🔍 Analyzing revision request...")
            
            from agents.llm_client import get_llm_response
            
            # Get list of existing pages
            existing_pages = [f.replace('.html', '') for f in os.listdir("output/drafts") if f.endswith('.html')]
            
            # Get page summaries for LLM to analyze
            print("   🔍 Extracting page summaries for analysis...")
            
            page_summaries = {}
            for page in existing_pages:
                page_path = f"output/drafts/{page}.html"
                if os.path.exists(page_path):
                    with open(page_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Extract visible text (remove HTML tags)
                    text_content = re.sub(r'<[^>]+>', ' ', content)
                    text_content = ' '.join(text_content.split())[:500]  # First 500 chars
                    
                    page_summaries[page] = text_content
                    print(f"      • {page}: {len(text_content)} chars")
            
            # Build page content summary for LLM
            pages_info = "\n\n".join([
                f"Page: {page}\nContent preview: {summary[:200]}..."
                for page, summary in page_summaries.items()
            ])
            
            detection_prompt = f"""
User wants to revise: "{prompt}"

Existing pages with content preview:
{pages_info}

YOUR TASK:
Analyze the user's revision request and determine which pages need to be regenerated.

CRITICAL ANALYSIS RULES:
1. If user mentions SPECIFIC element (button, form, table, section):
   - Check which pages contain that element
   - ONLY regenerate those pages
   - Example: "button Get Started terlalu besar" → only pages with "Get Started" button

2. If user mentions SPECIFIC page name:
   - Only regenerate that page
   - Example: "perbaiki halaman home" → only home

3. If user mentions SHARED component (navbar, footer, header):
   - Regenerate ALL pages (shared across pages)
   - Example: "ganti navbar" → all pages

4. If user mentions GLOBAL styling (color, font, spacing):
   - Regenerate ALL pages
   - Example: "ubah warna biru" → all pages

5. If UNCLEAR:
   - Default to pages_with_element if available
   - Otherwise, regenerate all (safe fallback)

Respond with JSON only:
{{
  "scope": "specific" or "global",
  "pages_to_regenerate": ["page1", "page2"] or ["all"],
  "reason": "brief explanation with evidence"
}}
"""
            
            detection_system = """
You are a smart revision analyzer. Read the page content previews and determine which pages need regeneration.

ANALYSIS APPROACH:

1. READ the user's revision request carefully
2. CHECK the content preview of each page
3. DETERMINE which pages are affected

DECISION RULES:

A. EXPLICIT PAGE MENTION:
   - "di page X", "halaman X", "on X page" → ONLY that page
   - Example: "di page pricing icon terlalu besar" → ["pricing"] ONLY
   - This OVERRIDES everything else

B. SPECIFIC ELEMENT/COMPONENT:
   - Check which pages contain that element in their content
   - Example: "button Get Started terlalu besar"
     * Check content: Does home have "Get Started"? Yes → include home
     * Check content: Does pricing have "Get Started"? No → exclude pricing
   - Only regenerate pages that have that element

C. MULTI-PART REQUESTS:
   - "X terlalu besar DAN di page Y ada Z"
     * Part 1: Check which pages have X
     * Part 2: Only page Y (explicit mention)
     * Result: Union of both parts
   
D. SHARED COMPONENTS:
   - navbar, footer, header, menu → ALL pages (shared across pages)
   
E. GLOBAL STYLING:
   - "ubah warna", "ganti font", "spacing" → ALL pages

IMPORTANT:
- Be SMART: Read the content previews
- Be PRECISE: Only regenerate what's needed
- Be LOGICAL: If user says "di page X", ONLY regenerate X

Respond with JSON:
{
  "scope": "specific" or "global",
  "pages_to_regenerate": ["page1", "page2"] or ["all"],
  "reason": "detailed explanation with evidence from content"
}
"""
            
            try:
                response = get_llm_response(
                    system_prompt=detection_system,
                    user_prompt=detection_prompt,
                    temperature=0.3,
                    max_tokens=500
                )
                
                import json
                
                # Try to extract JSON from response
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    json_str = json_match.group(0)
                    result = json.loads(json_str)
                else:
                    result = json.loads(response)
                
                scope = result.get("scope", "global")
                pages_list = result.get("pages_to_regenerate", [])
                
                # Handle "all" keyword
                if "all" in pages_list or scope == "global":
                    pages_to_regenerate = existing_pages
                    print(f"   🌐 Scope: GLOBAL - Regenerating all {len(existing_pages)} pages")
                else:
                    pages_to_regenerate = pages_list
                    print(f"   🎯 Scope: SPECIFIC - Regenerating: {', '.join(pages_to_regenerate)}")
                
                print(f"   💡 Reason: {result.get('reason', 'N/A')}")
                
                # Backup pages that won't be regenerated
                if scope == "specific" and pages_to_regenerate:
                    backup_dir = "output/drafts_backup"
                    os.makedirs(backup_dir, exist_ok=True)
                    
                    preserved_count = 0
                    for page in existing_pages:
                        if page not in pages_to_regenerate:
                            src = f"output/drafts/{page}.html"
                            dst = f"{backup_dir}/{page}.html"
                            if os.path.exists(src):
                                shutil.copy2(src, dst)
                                preserved_count += 1
                    
                    if preserved_count > 0:
                        print(f"   💾 Preserved: {preserved_count} page(s)")
                
            except json.JSONDecodeError as e:
                # Fallback: Simple keyword detection
                print(f"   ⚠️ JSON parsing failed, using keyword detection...")
                
                prompt_lower = prompt.lower()
                detected_pages = []
                
                # Check if any page name is mentioned
                for page in existing_pages:
                    if page.lower() in prompt_lower:
                        detected_pages.append(page)
                
                if detected_pages:
                    pages_to_regenerate = detected_pages
                    print(f"   🎯 Detected pages: {', '.join(detected_pages)}")
                else:
                    # No specific page mentioned, regenerate all
                    pages_to_regenerate = existing_pages
                    print(f"   🌐 No specific page detected, regenerating all")
                
            except Exception as e:
                print(f"   ⚠️ Detection failed: {e}")
                print("   🔄 Will regenerate all pages (safe fallback)")
                pages_to_regenerate = existing_pages
            
            # Clean drafts directory
            shutil.rmtree("output/drafts")
            print("🧹 Cleaned drafts for revision\n")

        if prev_draft:
            # prev_draft already contains page structure info
            revised_prompt = f"""
{prev_draft}

USER REVISION REQUEST:
{prompt}

IMPORTANT:
- Keep the existing UI design, layout, colors, and styling
- Only modify based on the user's revision request above
- Maintain the SAME number of pages as specified
"""
        else:
            revised_prompt = prompt

        preprompt = prompt_expander(revised_prompt)
        draft_result = draft_agent_multi(preprompt)
        
        # Draft styling is now handled by LLM in draft agent v2
        # No need for post-processing utilities
        
        # Restore preserved pages
        backup_dir = "output/drafts_backup"
        if os.path.exists(backup_dir):
            backup_files = [f for f in os.listdir(backup_dir) if f.endswith('.html')]
            if backup_files:
                print(f"\n📦 Restoring {len(backup_files)} preserved page(s)...")
                for backup_file in backup_files:
                    src = os.path.join(backup_dir, backup_file)
                    dst = os.path.join("output/drafts", backup_file)
                    shutil.copy2(src, dst)
                    
                    page_name = backup_file.replace('.html', '')
                    # Add to draft_result
                    with open(dst, 'r', encoding='utf-8') as f:
                        draft_result["drafts"][page_name] = f.read()
                    
                    print(f"   ✅ {page_name}")
                
                print(f"   💡 These pages were NOT regenerated (preserved from previous version)")
            
            # Clean backup
            shutil.rmtree(backup_dir)

        # Save main draft (index or single page)
        os.makedirs("output", exist_ok=True)
        draft_path = os.path.abspath("output/draft.html")
        print(f"\n📁 Draft(s) saved:")
        print(f"  Main: {draft_path}")
        
        # Show individual drafts if multiple
        if len(draft_result.get("drafts", {})) > 1:
            for page_name in draft_result["drafts"].keys():
                print(f"  • {page_name}: output/drafts/{page_name}.html")

        # Navbar/footer consistency is now handled by LLM in draft agent v2
        # Template-based generation ensures consistency from the start
        
        # Open in browser
        webbrowser.open(f"file://{draft_path}")

        confirm = input("[CONFIRMATION] Continue start building [y/n] ? ")
        if confirm.lower() == "y":
            # Clean Laravel views before building
            print("\n🧹 Cleaning Laravel views before build...")
            clean_laravel_views()
            print("✅ Laravel views cleaned\n")
            break
        else:
            # Save draft info for revision
            prev_draft_info = {
                "draft_html": draft_result["draft"],
                "pages": draft_result.get("pages", []),
                "drafts": draft_result.get("drafts", {})
            }
            
            # Strip GenLaravel navbar from draft HTML
            draft_html_clean = prev_draft_info["draft_html"]
            
            # Remove GenLaravel Draft Preview navbar section (more specific pattern)
            import re
            # Only remove if it contains "GenLaravel Draft Preview" text
            navbar_pattern = r'<div class="bg-gradient-to-r from-slate-700[^>]*>.*?GenLaravel Draft Preview.*?</div>\s*</div>\s*</div>'
            draft_html_clean = re.sub(navbar_pattern, '', draft_html_clean, flags=re.DOTALL)
            
            # Also remove the preview-container wrapper if exists
            draft_html_clean = draft_html_clean.replace('<div class="preview-container bg-gray-100">', '<div>')
            
            # Use individual drafts instead of index for better context
            if prev_draft_info["drafts"]:
                # Get first page draft as reference
                first_page = list(prev_draft_info["drafts"].values())[0]
                draft_html_clean = first_page  # Use actual page content (full)
            
            # Create context for revision with EXPLICIT page list
            pages_list = ", ".join([p["name"] for p in prev_draft_info["pages"]])
            pages_detail = "\n".join([
                f"  - {p['name']}: {p.get('description', 'page')}"
                for p in prev_draft_info["pages"]
            ])
            
            prev_draft = f"""
CRITICAL: This is a MULTI-PAGE project with {len(prev_draft_info["pages"])} pages.

EXISTING PAGES (DO NOT CHANGE):
{pages_detail}

You MUST generate these EXACT {len(prev_draft_info["pages"])} pages:
{pages_list}

PREVIOUS DRAFT HTML (for reference):
{draft_html_clean}

IMPORTANT:
- Keep the SAME {len(prev_draft_info["pages"])} pages structure
- Do NOT merge into single page
- Do NOT add or remove pages
- Only improve the design and content based on user feedback
"""
            print("\n🔁 OK, Please describe again your expectation.\n")

    # ========== PHASE 2: MULTI-PAGE PLANNING ==========
    # Use detected pages from draft (most accurate)
    pages_from_draft = draft_result.get("pages", [])
    
    print(f"\n📋 Planning components for {len(pages_from_draft)} page(s)...")
    
    final_prompt = f"For UI design and materials, follow this draft reference: {draft_result['draft']}"
    
    # Get component planning from LLM
    multi_plan = plan_prompt_multi(final_prompt)
    pages_from_planner = multi_plan.get("pages", [])
    
    # Use draft pages as source of truth, enhance with planner's component suggestions
    pages = []
    for i, draft_page in enumerate(pages_from_draft):
        page_data = {
            "page": draft_page["name"],
            "route": f"/{draft_page['name']}",
            "description": draft_page.get("description", ""),
            "draft_name": draft_page["name"]
        }
        
        # Try to get components from planner for this page
        if i < len(pages_from_planner):
            page_data["components"] = pages_from_planner[i].get("components", [])
        else:
            page_data["components"] = []
        
        pages.append(page_data)
    
    print(f"\n📊 Detected {len(pages)} page(s) to generate:")
    for i, page in enumerate(pages, 1):
        print(f"  {i}. {page['page']} → {page['route']}")
    
    # ========== PHASE 3: GENERATE EACH PAGE ==========
    all_layouts = []
    all_components = {}
    
    for idx, page_plan in enumerate(pages, 1):
        print(f"\n{'='*60}")
        print(f"🔨 GENERATING PAGE {idx}/{len(pages)}: {page_plan['page']}")
        print(f"{'='*60}")
        
        # Convert to single-page format for compatibility
        single_plan = {
            "page": page_plan["page"],
            "components": page_plan["components"],
            "route": page_plan["route"]
        }
        
        # Design layout for this page
        layout = design_layout(single_plan)
        all_layouts.append(layout)
        
        # Get the appropriate draft for this page
        page_draft_name = page_plan.get("draft_name", page_plan["page"])
        page_draft_html = draft_result.get("drafts", {}).get(page_draft_name, draft_result["draft"])
        
        # Generate components for this page
        components = list_components(single_plan, page_draft_html)
        
        # Merge components (avoid duplicates)
        for comp_name, comp_code in components.items():
            if comp_name not in all_components:
                all_components[comp_name] = comp_code
        
        # Generate blade view for this page
        generate_blade(layout, components)
        
        print(f"\n✅ Page '{page_plan['page']}' generated successfully")
    
    # ========== PHASE 4: GENERATE SHARED RESOURCES ==========
    print(f"\n{'='*60}")
    print("🔧 GENERATING SHARED RESOURCES")
    print(f"{'='*60}")
    
    # Generate app layout (once for all pages)
    # Collect all unique components from all pages
    all_component_names = []
    for page in pages:
        all_component_names.extend(page.get("components", []))
    all_component_names = list(set(all_component_names))  # Remove duplicates
    
    layout_plan = {
        "page": pages[0]["page"],
        "components": all_component_names
    }
    generate_layout_app(layout_plan, draft_result['draft'])
    
    # Generate all routes at once
    generate_routes_multi(pages)
    
    # ========== PHASE 5: VALIDATION ==========
    # Import auto-fix functions
    from agents.i_validator_agent import validate_with_reason, auto_fix
    
    all_valid = True
    fixed_components = {}
    
    print("\n\n🟩 [VALIDATOR AGENT] Validating all components...")
    
    for name, blade_code in all_components.items():
        print(f"\nValidating: {name}", end=" ", flush=True)
        is_valid, reason = validate_with_reason(blade_code)
        
        if is_valid:
            print(" ✅")
            fixed_components[name] = blade_code
        else:
            print(f" ❌\n   Error: {reason}")
            print(f"   🔧 Auto-fixing {name}...", end=" ", flush=True)
            
            fixed_code = auto_fix(blade_code, reason)
            
            # Validate fixed code
            is_fixed, _ = validate_with_reason(fixed_code)
            if is_fixed:
                print("✅ Fixed!")
                fixed_components[name] = fixed_code
                
                # Update output file
                output_path = f"output/{name}.blade.php"
                if os.path.exists(output_path):
                    with open(output_path, "w", encoding="utf-8") as f:
                        f.write(fixed_code)
            else:
                print("❌ Fix failed, using original")
                fixed_components[name] = blade_code
                all_valid = False

    print("\n===== ✅ Overall Component Validation =====")
    print("✅ All Components Valid" if all_valid else "⚠️ Some components may have issues")
    
    # Always proceed with fixed components
    all_components = fixed_components

    # ========== PHASE 6: MOVE TO LARAVEL PROJECT ==========
    if True:  # Always move (changed from: if all_valid)
        # Move all layouts
        for layout in all_layouts:
            move_to_laravel_project(layout)
        
        # ========== PHASE 6.5: MULTI-PAGE VALIDATION ==========
        print("\n🔍 Running multi-page validation...")
        from utils.multi_page_validator import validate_multi_page_app
        
        is_valid = validate_multi_page_app("my-laravel")
        
        if not is_valid:
            print("\n⚠️ Validation found issues. Attempting auto-fix...")
        
        # ========== PHASE 7: AUTO-FIX CSS, ROUTES & STYLING ==========
        print("\n🔧 Auto-fixing CSS, routes, and styling (multi-page mode)...")
        
        # Import and run fix functions
        import sys
        sys.path.insert(0, 'utils')
        
        try:
            # Fix nested UI first (critical)
            from fix_nested_ui import fix_nested_ui
            fix_nested_ui()
            print("  ✅ Nested UI fixed")
            print()
            from fix_layout_css import extract_custom_css_from_draft, update_layout_css
            from fix_layout_js import extract_javascript_from_drafts, update_layout_js
            from fix_existing_views import fix_component_routes
            from fix_component_styling import fix_hero_section, fix_all_components
            
            # Fix CSS
            custom_css = extract_custom_css_from_draft()
            if custom_css:
                update_layout_css(custom_css)
                print("  ✅ Custom CSS applied to layout")
            
            # Fix JavaScript
            print("\n  Merging JavaScript from all pages...")
            custom_js = extract_javascript_from_drafts()
            if custom_js:
                update_layout_js(custom_js)
                print("  ✅ JavaScript merged to layout")
            
            # Smart route sync (preserves valid routes)
            print("\n  Syncing routes with web.php...")
            from smart_route_sync import sync_navbar_routes
            sync_navbar_routes()
            print("  ✅ Routes synced")
            
            # Fix component styling
            print("\n  Fixing component styling...")
            fix_hero_section()
            fix_all_components()
            print("  ✅ Styling fixes applied")
            
            # Fix component name mismatches
            print("\n  Fixing component names...")
            from fix_component_names import fix_component_includes
            fix_component_includes()
            print("  ✅ Component names fixed")
            
        except Exception as e:
            print(f"  ⚠️ Auto-fix warning: {e}")
            print("  💡 Run manually: python utils/fix_all.py")
        
        print("\n========================================")
        print("✅ Multi-page Laravel application generated!")
        print("========================================")
        print("\n📄 Generated Pages:")
        for page in pages:
            print(f"  • {page['route']} → {page['page']}.blade.php")
        
        # Open first page
        first_route = pages[0]['route']
        print(f"\n🌐 Opening: http://localhost:8000{first_route}")
        webbrowser.open(f"http://localhost:8000{first_route}")


if __name__ == "__main__":
    main()
