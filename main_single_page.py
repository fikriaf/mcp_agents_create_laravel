import json
import os
import shutil
import webbrowser
import datetime

# Removed: from agents.clean_history import clean_history (moved to utils_clean.py)

from agents.a_prompt_expander import prompt_expander
from agents.b_draft_agent import draft_agent
from agents.c_prompt_planner import plan_prompt
from agents.d_page_architect import design_layout
from agents.e_generate_layout_app import generate_layout_app
from agents.f_ui_generator import generate_blade
from agents.g_route_agent import generate_route
from agents.h_component_agent import list_components
from agents.i_validator_agent import validate
from agents.j_move_to_project import move_to_laravel_project


def save_history(prompt, draft):
    os.makedirs("history", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"history/{timestamp}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump({
            "prompt": prompt,
            "draft": draft
        }, f, indent=2)

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
    # Note: clean_history moved to utils_clean.py and clean_project.py
    prev_draft = None
    first_run = True
        
    while True:
        # Clean on first run or when starting build after revision
        if first_run:
            # Clean output folder
            if os.path.exists("output"):
                shutil.rmtree("output")
                print("🧹 Cleaned: output/")
            
            # Auto-clean Laravel views
            print("🧹 Cleaning previous Laravel views...")
            clean_laravel_views()
            print("✅ Laravel views cleaned\n")
            first_run = False
        
        prompt = input("Prompt: ")
        
        if prev_draft:
            revised_prompt = f"""
IMPORTANT: Keep the existing UI design, layout, colors, and styling from the previous draft.
Only modify based on this new request: {prompt}

Previous Draft (KEEP THE DESIGN):
{prev_draft}
            """
        else:
            revised_prompt = prompt
        
        preprompt = prompt_expander(revised_prompt)
        draft = draft_agent(preprompt)

        # 📂 Simpan draft HTML
        os.makedirs("output", exist_ok=True)
        draft_path = os.path.abspath("output/draft.html")
        with open(draft_path, "w", encoding="utf-8") as f:
            f.write(draft["draft"])
        print(f"\n📁 Draft disimpan di: {draft_path}")

        # 🌐 Buka otomatis di browser
        webbrowser.open(f"file://{draft_path}")
        
        confirm = input("[CONFIRMATION] Continue start building [y/n] ? ")
        if confirm.lower() == "y":
            break
        else:
            prev_draft = draft["draft"]
            print("\n🔁 OK, Please describe again your expectation.\n")

    # 🧠 Build proses setelah konfirmasi
    print("\n🧹 Cleaning Laravel views before build...")
    clean_laravel_views()
    print("✅ Laravel views cleaned\n")
    
    final_prompt = f"For UI design and materials, follow this draft reference: {draft['draft']}"
    
    plan = plan_prompt(final_prompt)
    layout = design_layout(plan)
    components = list_components(plan, draft["draft"])
    generate_blade(layout, components, draft["draft"])  # Pass draft HTML
    generate_layout_app(plan, draft['draft'])
    generate_route(plan, draft["draft"])

    # Import auto-fix functions
    from agents.i_validator_agent import validate_with_reason, auto_fix
    
    all_valid = True
    fixed_components = {}
    
    print("\n\n🟩 [VALIDATOR AGENT] On Validating...")
    for name, blade_code in components.items():
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
    components = fixed_components
    if True:  # Always move to Laravel (changed from: if all_valid)
        move_to_laravel_project(layout)
        
        # Auto-fix CSS, routes & styling for SINGLE-PAGE
        print("\n🔧 Auto-fixing CSS, routes, and styling (single-page mode)...")
        
        import sys
        sys.path.insert(0, 'utils')
        
        # Auto-fix: Only route removal (important for single-page)
        # Styling fixes DISABLED to preserve draft accuracy
        print("\n📌 Auto-fixing CSS, routes, and styling (single-page mode)...")
        
        try:
            from fix_single_page import fix_component_routes_single_page
            
            # Fix routes - remove all route() calls for single-page (IMPORTANT)
            print("\n  Removing route() calls (single-page)...")
            fix_component_routes_single_page()
            print("  ✅ Single-page route fixes applied")
            
        except Exception as e:
            print(f"  ⚠️ Route fix warning: {e}")
        
        # DISABLED: CSS and styling fixes can break layout
        # from fix_layout_css import extract_custom_css_from_draft, update_layout_css
        # from fix_component_styling import fix_hero_section, fix_all_components
        # These utils often change colors and styling that are already correct from draft
        print("  ℹ️ Styling fixes disabled to preserve draft accuracy")
        
        print("\n========================================")
        print(f"Open Link: http://localhost:8000{plan['route']}")
        print("========================================")
        webbrowser.open(f"http://localhost:8000{plan['route']}")

if __name__ == "__main__":
    main()
