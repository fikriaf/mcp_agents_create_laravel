import time
def design_layout(plan):
    print("\n\n🟡 [PAGE ARCHITECT] Structuring layout...")

    components = plan.get("components", [])

    time.sleep(1)
    return {
        "extends": "layouts.app",
        "sections": {
            "content": components
        },
        "page": plan.get("page", "untitled")
    }