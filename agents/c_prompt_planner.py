import re, json
from mistralai import Mistral

api_key = "mBng7pAtolwotaZRyOQxB5RclArjyM4P"
model = "mistral-large-latest"

client = Mistral(api_key=api_key)

def plan_prompt(user_prompt: str):
    print("[PROMPT PLANNER] Interpreting prompt...")

    sys_prompt = """
You are an expert Laravel UI analyst.
Given a user request to create a web page, break it down into:
- "page": the name of the view (string)
- "components": list of UI components needed (array)
- "route": suggested route path (e.g. "/dashboard")

Respond in strict JSON format ONLY, without explanations or comments.
"""

    stream_response = client.chat.stream(
        model=model,
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    full_response = ""

    for chunk in stream_response:
        content = chunk.data.choices[0].delta.content
        if content:
            print(content, end="", flush=True)
            full_response += content

    # Ambil hanya blok JSON
    try:
        # Coba parse langsung jika JSON mentah
        parsed = json.loads(full_response)
        return parsed
    except json.JSONDecodeError:
        # Jika ada kata tambahan, ekstrak blok JSON dengan regex
        json_block = re.search(r"\{.*\}", full_response, re.DOTALL)
        if json_block:
            try:
                return json.loads(json_block.group(0))
            except:
                pass

    print("\n[ERROR] Gagal parsing JSON dari model.")
    return {
        "page": "unknown",
        "components": [],
        "route": "/unknown"
    }
