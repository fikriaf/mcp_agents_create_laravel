import json
import os
import shutil
import webbrowser

from agents.clean_history import clean_history

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

def main():

    if os.path.exists("output"):
        shutil.rmtree("output")
        print("🧹 Folder 'output' lama telah dihapus.")
        
    clean_history()
        
    while True:
        prompt = input("Prompt: ")
        
        preprompt = prompt_expander(prompt)
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
            print("\n🔁 OK, Please describe again your expectation.\n")

    # 🧠 Build proses setelah konfirmasi
    final_prompt = f"For UI design and materials, follow this draft reference: {draft['draft']}"
    
    plan = plan_prompt(final_prompt)
    layout = design_layout(plan)
    components = list_components(plan, draft["draft"])
    generate_blade(layout, components)
    generate_layout_app(plan, draft['draft'])
    generate_route(plan, draft["draft"])

    all_valid = True
    print("\n\n🟩 [VALIDATOR AGENT] On Validating...")
    for name, blade_code in components.items():
        print(f"\nValidating: {name}", end=" ", flush=True)
        is_valid = validate(blade_code)
        print(" ✅" if is_valid else " ❌")

        if not is_valid:
            all_valid = False

    print("\n===== ✅ Overall Component Validation =====")
    print("✅ All Components Valid" if all_valid else "❌ Some Components Invalid")
    
    if all_valid:
        move_to_laravel_project(layout)
        
        print("\n========================================")
        print(f"Open Link: http://localhost:8000{plan['route']}")
        print("========================================")
        webbrowser.open(f"http://localhost:8000{plan['route']}")

if __name__ == "__main__":
    main()
