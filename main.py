import json

from agents.a_prompt_expander import prompt_expander
from agents.b_draft_agent import draft_agent
from agents.c_prompt_planner import plan_prompt
from agents.d_page_architect import design_layout
from agents.e_ui_generator import generate_blade
from agents.f_route_agent import generate_route
from agents.g_component_agent import list_components
from agents.h_validator_agent import validate

def main():
    while True:
        prompt = input("Prompt: ")
        print(f"\n🟡 Prompt Awal: {prompt}")
        
        preprompt = prompt_expander(prompt)
        draft = draft_agent(preprompt)

        print("\n🔧 Draft Preview:\n", draft["draft"])
        confirm = input("[CONFIRMATION] Continue start building [y/n] ? ")

        if confirm.lower() == "y":
            final_prompt = f"""{draft['prompt']}, For UI design and materials, follow this draft reference: {draft['draft']}"""
            break
        else:
            print("\n🔁 OK, Please describe again your expectation.")

    # Mulai build dari final_prompt
    plan = plan_prompt(final_prompt)
    layout = design_layout(plan)
    blade = generate_blade(layout)
    route = generate_route(plan["route"])
    components = list_components(plan["components"])
    valid = validate(blade)

    print("\n===== ✅ Blade Output =====\n")
    print(blade)
    print("\n===== ✅ Route Output =====\n")
    print(route)
    print("\n===== ✅ Components =====\n")
    print(components)
    print("\n===== ✅ Validation =====\n")
    print("✅ Valid" if valid else "❌ Invalid")

if __name__ == "__main__":
    main()
