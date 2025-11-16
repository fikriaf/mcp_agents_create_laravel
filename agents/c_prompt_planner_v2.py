import re, json
from dotenv import load_dotenv
from agents.llm_client import get_llm_response

load_dotenv()


def plan_prompt_multi(user_prompt: str):
    """
    Enhanced planner that can detect and plan multiple pages
    Returns a list of page plans instead of single plan
    """
    print("\n🔵 [MULTI-PAGE PLANNER] Analyzing prompt for multiple pages...")

    sys_prompt = """
You are an expert Laravel application architect.

Analyze the user request and determine if it requires single or multiple pages.

Return a JSON object with:
{
  "pages": [
    {
      "page": "page-name",
      "components": ["ComponentName1", "ComponentName2"],
      "route": "/route-path",
      "description": "Brief description of this page"
    }
  ]
}

Guidelines:
- Detect if user wants multiple pages (e.g., "login and dashboard", "home, about, contact")
- Each page should have distinct purpose and route
- Components should be minimalist and reusable
- Use PascalCase for component names
- Use kebab-case for page names
- Routes should follow REST conventions

CRITICAL: ALWAYS use ENGLISH for page names and routes
- Even if user input is in Indonesian/other language, translate to English
- Examples:
  - "beranda" → "home"
  - "tentang kami" → "about"
  - "kontak" → "contact"
  - "produk" → "products"
  - "layanan" → "services"

Examples of multi-page requests:
- "Create login page and dashboard" → 2 pages
- "Build e-commerce with home, products, cart, checkout" → 4 pages
- "Make a blog with posts list and detail page" → 2 pages

Respond ONLY with valid JSON. No markdown. No explanations.
"""

    try:
        full_response = get_llm_response(
            system_prompt=sys_prompt,
            user_prompt=user_prompt,
            max_tokens=32000,
            temperature=0.3,
        )
        print("\n✅ Multi-page plan created successfully")

    except Exception as e:
        print(f"\n❌ Error creating plan: {e}")
        full_response = '{"pages": [{"page": "unknown", "components": [], "route": "/unknown", "description": "Error"}]}'

    # Parse JSON
    try:
        parsed = json.loads(full_response)
        return parsed
    except json.JSONDecodeError:
        json_block = re.search(r"\{.*\}", full_response, re.DOTALL)
        if json_block:
            try:
                return json.loads(json_block.group(0))
            except Exception:
                pass

    print("\n[ERROR] Failed to parse JSON from model.")
    return {"pages": [{"page": "unknown", "components": [], "route": "/unknown", "description": "Error"}]}


def plan_prompt(user_prompt: str):
    """
    Backward compatible wrapper - returns first page if single page detected
    """
    multi_plan = plan_prompt_multi(user_prompt)
    
    # If only one page, return in old format for compatibility
    if len(multi_plan.get("pages", [])) == 1:
        page = multi_plan["pages"][0]
        return {
            "page": page["page"],
            "components": page["components"],
            "route": page["route"]
        }
    
    # Return full multi-page plan
    return multi_plan
