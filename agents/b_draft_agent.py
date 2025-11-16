import re
from dotenv import load_dotenv
from agents.llm_client import get_llm_response

# Load API key dari .env
load_dotenv()

def draft_agent(prompt_expander: dict):
    print("\n\n🟢 [DRAFT UI AGENT] Creating a draft UI...")

    # ✅ SYSTEM PROMPT diperkuat:
    system_prompt = """
You are a professional and experienced AI frontend developer.

Your task is to generate a complete, high-quality HTML file that reflects modern, awesome, responsive, and visually polished design — suitable for real-world production use.

✅ Your response MUST include:
- Full HTML structure with <html>, <head>, and <body> tags
- Awesome UI and Responsive layout using **Tailwind CSS as the primary styling framework**
- Internal <style> section for **custom CSS enhancements** to refine the UI (e.g. advanced layout, animation, or visual polish)
- Internal <script> section for interactivity or UI behavior enhancements

⚠️ CRITICAL CSS RULES:
- DO NOT use @apply directive (not supported in Tailwind CDN)
- Write PURE CSS with standard properties only
- Use CSS variables for colors (--primary-color, --secondary-color)
- Example: .btn { padding: 1.5rem 1rem; border-radius: 9999px; } NOT @apply px-6 py-3

💡 You should prioritize:
- Tailwind CSS utility classes for rapid layout and component design
- Custom CSS to complement Tailwind where necessary
- Google Fonts
- Tailwind-compatible animation plugins or JS libraries if helpful (e.g. AOS, Alpine.js)

🎯 REQUIREMENTS:
- DO NOT use dummy src image placeholders
- DO NOT use generic lorem ipsum text — prefer realistic, meaningful interface labels and components
- Include smooth, subtle animations (e.g. transitions, hover effects, fade-ins)
- UI components must be real and usable (cards, buttons, navbars, modals, etc.)
- Design should be elegant, modern, and production-ready — not just functional

⚠️ REVISION MODE:
- If the user prompt includes "Previous Draft" or "KEEP THE DESIGN", you MUST preserve:
  * All existing colors, fonts, and styling
  * Layout structure and component arrangement
  * Custom CSS animations and effects
  * Background images and visual elements
- Only modify the specific parts mentioned in the new request
- DO NOT redesign or change the overall look and feel

🚫 DO NOT:
- Include any explanations, comments, or markdown text outside the code
- Return empty, generic, or unfinished templates
- Change the design when asked to keep it

🧾 Return ONLY a markdown code block formatted as:
```html
<!-- Your complete HTML code here -->
```
"""

    # ✅ Bisa tambah penguatan juga di user prompt
    user_prompt = f"{prompt_expander['new_prompt']}"

    # Use the new LLM client with Cerebras/Mistral fallback
    try:
        full_response = get_llm_response(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            max_tokens=32000,  # Increased for complete HTML generation
            temperature=0.7,
        )
        print("\n✅ Draft created successfully")

    except Exception as e:
        print(f"\n❌ Error creating draft: {e}")
        raise  # Let the error propagate - LLM client already has fallback

    # Remove <think> tags (from models like DeepSeek)
    full_response = re.sub(r'<think>.*?</think>', '', full_response, flags=re.DOTALL | re.IGNORECASE)
    
    # STRICT: Only extract content between ```html and ```
    # This prevents any thinking/explanation text from being included
    code_matches = re.findall(
        r"```html\s*(.*?)```", full_response, re.DOTALL | re.IGNORECASE
    )

    if code_matches:
        # Take the first match (should be the only one)
        get_draft = code_matches[0].strip()
        print(f"  ✅ Extracted HTML from ```html block (length: {len(get_draft)} chars)")
        
        # Debug: show last 100 chars
        print(f"  📝 Last 100 chars: ...{get_draft[-100:]}")
        
        # Check if HTML is complete
        ends_with_html = get_draft.endswith('</html>')
        print(f"  🔍 Ends with </html>: {ends_with_html}")
        
        if not ends_with_html:
            print("  ⚠️ Warning: HTML appears incomplete (missing </html>)")
            print("  🔄 Attempting to continue generation...")
            
            # Try to continue the generation
            continuation_prompt = f"""
Continue the HTML code from where it was cut off. 

Here's the incomplete HTML:
```html
{get_draft[-1000:]}
```

Continue from the last line and complete the HTML structure. Make sure to:
1. Close all open tags
2. End with </body> and </html>
3. Return ONLY the continuation part in ```html block

Start from where the code was cut off and complete it.
"""
            
            try:
                continuation_response = get_llm_response(
                    system_prompt="You are an HTML completion expert. Complete the incomplete HTML structure.",
                    user_prompt=continuation_prompt,
                    temperature=0.3,
                    max_tokens=32000,
                )
                
                # Extract continuation
                continuation_matches = re.findall(
                    r"```html\s*(.*?)```", continuation_response, re.DOTALL | re.IGNORECASE
                )
                
                if continuation_matches:
                    continuation = continuation_matches[0].strip()
                    # Merge with original
                    get_draft = get_draft + "\n" + continuation
                    print(f"  ✅ Continuation added (total length: {len(get_draft)} chars)")
                    
                    # Check again
                    if get_draft.endswith('</html>'):
                        print("  ✅ HTML structure now complete")
                    else:
                        print("  ⚠️ Still incomplete, but proceeding...")
                else:
                    print("  ⚠️ Could not extract continuation, proceeding with incomplete HTML")
                    
            except Exception as e:
                print(f"  ⚠️ Continuation failed: {str(e)[:100]}")
                print("  💡 Proceeding with incomplete HTML")
        else:
            print("  ✅ HTML structure complete")
    else:
        # Fallback: Try to extract HTML tags directly
        # This handles cases where LLM doesn't use markdown code blocks
        tag_match = re.search(
            r"<html.*?>.*?</html>", full_response, re.DOTALL | re.IGNORECASE
        )
        if tag_match:
            get_draft = tag_match.group(0).strip()
            print(f"  ✅ Extracted HTML from tags (length: {len(get_draft)} chars)")
        else:
            # Last resort: Use raw response but warn
            print("  ⚠️ No code block or HTML tags found, using raw response")
            get_draft = full_response.strip()
            print(f"  📝 Raw response length: {len(get_draft)} chars")
        
        # Check if HTML is complete (for fallback path too)
        print(f"  📝 Last 100 chars: ...{get_draft[-100:]}")
        ends_with_html = get_draft.endswith('</html>')
        print(f"  🔍 Ends with </html>: {ends_with_html}")
        
        if not ends_with_html:
            print("  ⚠️ Warning: HTML appears incomplete (missing </html>)")
            print("  🔄 Attempting to continue generation...")
            
            # Try to continue the generation
            continuation_prompt = f"""
Continue the HTML code from where it was cut off. 

Here's the incomplete HTML (last 1000 chars):
```
{get_draft[-1000:]}
```

Continue from the last line and complete the HTML structure. Make sure to:
1. Close all open tags
2. End with </body> and </html>
3. Return ONLY the continuation part in ```html block

Start from where the code was cut off and complete it.
"""
            
            try:
                continuation_response = get_llm_response(
                    system_prompt="You are an HTML completion expert. Complete the incomplete HTML structure.",
                    user_prompt=continuation_prompt,
                    temperature=0.3,
                    max_tokens=8000,
                )
                
                # Extract continuation
                continuation_matches = re.findall(
                    r"```html\s*(.*?)```", continuation_response, re.DOTALL | re.IGNORECASE
                )
                
                if continuation_matches:
                    continuation = continuation_matches[0].strip()
                    # Merge with original
                    get_draft = get_draft + "\n" + continuation
                    print(f"  ✅ Continuation added (total length: {len(get_draft)} chars)")
                    
                    # Check again
                    if get_draft.endswith('</html>'):
                        print("  ✅ HTML structure now complete")
                    else:
                        print("  ⚠️ Still incomplete, but proceeding...")
                else:
                    print("  ⚠️ Could not extract continuation, proceeding with incomplete HTML")
                    
            except Exception as e:
                print(f"  ⚠️ Continuation failed: {str(e)[:100]}")
                print("  💡 Proceeding with incomplete HTML")

    # Final cleanup: Remove any markdown code block markers that might remain
    get_draft = get_draft.strip()
    if get_draft.startswith('```html'):
        get_draft = get_draft[7:].strip()  # Remove ```html
    if get_draft.startswith('```'):
        get_draft = get_draft[3:].strip()  # Remove ```
    if get_draft.endswith('```'):
        get_draft = get_draft[:-3].strip()  # Remove trailing ```
    
    print(f"  🧹 Final cleanup done, draft length: {len(get_draft)} chars")
    
    return {"prompt": prompt_expander["new_prompt"], "draft": get_draft}
