# move_to_laravel.py

import os
import shutil

def move_to_laravel_project(layout):
    print("\n🟦 [MOVE TO PROJECT] Moving to Laravel Project...")
    
    laravel_root = "my-laravel"

    view_src = "output/layouts/app.blade.php"
    view_dest_dir = os.path.join(laravel_root, "resources/views/layouts")
    view_dest_file = os.path.join(view_dest_dir, "app.blade.php")
    if os.path.exists(view_src):
        os.makedirs(view_dest_dir, exist_ok=True)
        shutil.copy(view_src, view_dest_file)
        print(f"✅ app.blade.php dipindahkan ke {view_dest_file}")
    else:
        print("⚠️ app.blade.php tidak ditemukan.")
        
    # Pindahkan view utama
    view_src = f"output/{layout['page']}.blade.php"
    view_dest = os.path.join(laravel_root, f"resources/views/{layout['page']}.blade.php")
    if os.path.exists(view_src):
        shutil.copy(view_src, view_dest)
        print(f"✅ {layout['page']}.blade.php dipindahkan ke {view_dest}")
    else:
        print(f"⚠️ {layout['page']}.blade.php tidak ditemukan.")

    # Pindahkan semua komponen ke folder components Laravel
    components_src = "output/components"
    components_dest = os.path.join(laravel_root, "resources/views/components")

    if os.path.exists(components_src):
        os.makedirs(components_dest, exist_ok=True)
        for file in os.listdir(components_src):
            src_file = os.path.join(components_src, file)
            dest_file = os.path.join(components_dest, file)
            shutil.copy(src_file, dest_file)
        print(f"✅ Semua komponen dipindahkan ke {components_dest}")
    else:
        print("⚠️ Tidak ada komponen yang ditemukan untuk dipindahkan.")

    # Tambahkan route ke web.php Laravel
    route_src = "output/web.php"
    route_dest = os.path.join(laravel_root, "routes/web.php")

    if os.path.exists(route_src):
        with open(route_src, "r", encoding="utf-8") as f:
            new_routes = f.read()

        with open(route_dest, "a", encoding="utf-8") as f:
            f.write("\n\n" + new_routes)

        print(f"✅ Route baru ditambahkan ke {route_dest}")
    else:
        print("⚠️ File routes.txt tidak ditemukan.")
