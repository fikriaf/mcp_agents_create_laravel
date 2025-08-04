import re
from mistralai import Mistral

api_key = "mBng7pAtolwotaZRyOQxB5RclArjyM4P"
model = "codestral-latest"

client = Mistral(api_key=api_key)

def draft_agent(prompt_expander: dict):
    print("[DRAFT UI AGENT] Creating a draft UI...")

    system_prompt = (
        "Anda adalah AI frontend developer. "
        "Tugas Anda adalah mengembalikan HTML code murni tanpa penjelasan tambahan. "
        "Selalu balas dalam format blok kode HTML (```html ... ```), tanpa komentar atau deskripsi."
    )

    stream_response = client.chat.stream(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt_expander["new_prompt"]},
        ]
    )

    full_response = ""

    for chunk in stream_response:
        content = chunk.data.choices[0].delta.content
        if content:
            print(content, end="", flush=True)
            full_response += content

    # Ambil isi dalam blok kode HTML
    code_matches = re.findall(r"```html\s*(.*?)```", full_response, re.DOTALL | re.IGNORECASE)

    if code_matches:
        get_draft = code_matches[0].strip()
    else:
        # Fallback kalau tak ditemukan
        tag_match = re.search(r"<body.*?>.*?</body>", full_response, re.DOTALL | re.IGNORECASE)
        get_draft = tag_match.group(0).strip() if tag_match else full_response.strip()

    return {
        "prompt": prompt_expander["new_prompt"],
        "draft": get_draft
    }
