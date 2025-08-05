import os
import shutil

def clean_history():
    laravel_root = "my-laravel"

    # Hapus folder components lama
    components_path = os.path.join(laravel_root, "resources/views")
    if os.path.exists(components_path):
        shutil.rmtree(components_path)
        print("🗑️ Folder lama telah dihapus.")

    # Hapus file web.php
    webphp_path = os.path.join(laravel_root, "routes/web.php")
    if os.path.exists(webphp_path):
        os.remove(webphp_path)
        print(f"🗑️ File route '{webphp_path}' telah dihapus.")

if __name__ == "__main__":
    clean_history()
