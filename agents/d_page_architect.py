def design_layout(plan):
    print("[PAGE ARCHITECT] Structuring layout...")
    return {
        "extends": "layouts.app",
        "sections": {
            "sidebar": "components.sidebar",
            "content": "components.user_table"
        }
    }
