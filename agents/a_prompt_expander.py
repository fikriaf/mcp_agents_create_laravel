import json, os, sys
from dotenv import load_dotenv
from mistralai import Mistral

# Load .env file
load_dotenv()

# Ambil API key dari environment
api_key = os.getenv("MISTRAL_API_KEY")
model = "mistral-large-latest"
client = Mistral(api_key=api_key)

def prompt_expander(user_prompt: str):
    print("\n🟠 [PROMPT EXPANDER] describing prompt...")

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
        "You are a professional UI designer AI. "
        "Your task is to transform the user's brief request into a highly detailed, clear, and specific UI description that can be directly used by developers."
    )


    stream_response = client.chat.stream(
        model=model,
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": current_prompt}
        ]
    )



    full_response = ""
    prev_len = 0

    for chunk in stream_response:
        content = chunk.data.choices[0].delta.content
        if content:
            full_response += content  # Simpan utuh (termasuk \n)

            # Untuk tampil sementara: hanya karakter terbaru, bersihkan newline
            sanitized = content.replace("\n", " ").replace("\r", " ")
            pad = max(prev_len - len(sanitized), 0)
            sys.stdout.write("\r" + sanitized + " " * pad)
            sys.stdout.flush()
            prev_len = len(sanitized)


    return {
        "history": user_prompt if again else None,
        "new_prompt": full_response.strip()
    }
