import json
from mistralai import Mistral

api_key = "mBng7pAtolwotaZRyOQxB5RclArjyM4P"
model = "mistral-large-latest"
client = Mistral(api_key=api_key)

def prompt_expander(user_prompt: str):
    print("[PROMPT EXPANDER] describing prompt...")

    try:
        # Coba cek apakah ini revisi
        prompt_history = json.loads(user_prompt)
        current_prompt = prompt_history.get("prompt", "")
        again = prompt_history.get("again", False)
    except:
        # Jika bukan JSON, anggap prompt asli
        current_prompt = user_prompt
        again = False

    # Buat prompt system untuk mendetailkan
    sys_prompt = (
        "Anda adalah AI perancang UI profesional. "
        "Tugas Anda adalah mengubah permintaan pengguna yang singkat menjadi deskripsi UI yang rinci, jelas, dan langsung bisa digunakan developer."
    )

    stream_response = client.chat.stream(
        model=model,
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": current_prompt}
        ]
    )

    detailed_prompt = ""

    for chunk in stream_response:
        content = chunk.data.choices[0].delta.content
        if content:
            print(content, end="", flush=True)
            detailed_prompt += content

    return {
        "history": user_prompt if again else None,
        "new_prompt": detailed_prompt.strip()
    }
