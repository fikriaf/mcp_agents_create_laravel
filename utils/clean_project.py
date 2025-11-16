"""
Utility script to clean GenLaravel project
Use this before starting a new generation to avoid conflicts
"""

import os
import shutil


def clean_output():
    """Clean output folder"""
    if os.path.exists("output"):
        shutil.rmtree("output")
        print("✅ Cleaned: output/")
    else:
        print("ℹ️ output/ already clean")


def clean_laravel_views():
    """Clean generated views from Laravel project"""
    laravel_views = "my-laravel/resources/views"
    
    # Clean components
    components_path = os.path.join(laravel_views, "components")
    if os.path.exists(components_path):
        shutil.rmtree(components_path)
        print("✅ Cleaned: my-laravel/resources/views/components/")
    
    # Clean layouts
    layouts_path = os.path.join(laravel_views, "layouts")
    if os.path.exists(layouts_path):
        shutil.rmtree(layouts_path)
        print("✅ Cleaned: my-laravel/resources/views/layouts/")
    
    # Clean blade files (except welcome.blade.php)
    if os.path.exists(laravel_views):
        for file in os.listdir(laravel_views):
            if file.endswith('.blade.php') and file != 'welcome.blade.php':
                file_path = os.path.join(laravel_views, file)
                os.remove(file_path)
                print(f"✅ Removed: {file}")


def reset_routes():
    """Reset routes to default Laravel routes"""
    route_file = "my-laravel/routes/web.php"
    
    default_routes = """<?php

use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return view('welcome');
});
"""
    
    with open(route_file, "w", encoding="utf-8") as f:
        f.write(default_routes)
    
    print("✅ Reset: my-laravel/routes/web.php")


def create_genlaravel_welcome():
    """Create GenLaravel branded welcome page"""
    welcome_path = "my-laravel/resources/views/welcome.blade.php"
    
    welcome_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GenLaravel - AI Laravel Generator</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body class="bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 min-h-screen flex items-center justify-center">
    <div class="container mx-auto px-6">
        <div class="max-w-4xl mx-auto text-center">
            <!-- Logo -->
            <div class="mb-8 flex justify-center">
                <img src="{{ asset('GenLaravel.png') }}" alt="GenLaravel Logo" class="w-32 h-32 object-contain">
            </div>

            <!-- Title -->
            <h1 class="text-6xl font-bold text-white mb-4">GenLaravel</h1>
            <p class="text-2xl text-gray-300 mb-8">AI-Powered Laravel Generator</p>

            <!-- Status -->
            <div class="bg-white bg-opacity-10 backdrop-blur-lg rounded-2xl p-8 mb-8 border border-white border-opacity-20">
                <div class="flex items-center justify-center space-x-3 mb-4">
                    <div class="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
                    <span class="text-white text-lg font-semibold">Ready to Generate</span>
                </div>
                <p class="text-gray-300">Your Laravel project is ready. Run GenLaravel to generate pages.</p>
            </div>

            <!-- Quick Start -->
            <div class="grid md:grid-cols-2 gap-6 mb-8">
                <div class="bg-white bg-opacity-10 backdrop-blur-lg rounded-xl p-6 border border-white border-opacity-20 hover:bg-opacity-20 transition">
                    <div class="text-red-400 text-3xl mb-3"><i class="fas fa-file"></i></div>
                    <h3 class="text-white font-bold text-lg mb-2">Single Page</h3>
                    <p class="text-gray-300 text-sm mb-3">Generate one page at a time</p>
                    <code class="bg-black bg-opacity-50 text-green-400 px-3 py-1 rounded text-sm">python main.py</code>
                </div>

                <div class="bg-white bg-opacity-10 backdrop-blur-lg rounded-xl p-6 border border-white border-opacity-20 hover:bg-opacity-20 transition">
                    <div class="text-red-400 text-3xl mb-3"><i class="fas fa-layer-group"></i></div>
                    <h3 class="text-white font-bold text-lg mb-2">Multi Page</h3>
                    <p class="text-gray-300 text-sm mb-3">Generate multiple pages</p>
                    <code class="bg-black bg-opacity-50 text-green-400 px-3 py-1 rounded text-sm">python main_multi_page.py</code>
                </div>
            </div>

            <!-- Features -->
            <div class="flex flex-wrap justify-center gap-4 text-gray-300">
                <div class="flex items-center space-x-2">
                    <i class="fas fa-check-circle text-green-400"></i>
                    <span>AI-Powered</span>
                </div>
                <div class="flex items-center space-x-2">
                    <i class="fas fa-check-circle text-green-400"></i>
                    <span>Tailwind CSS</span>
                </div>
                <div class="flex items-center space-x-2">
                    <i class="fas fa-check-circle text-green-400"></i>
                    <span>Blade Components</span>
                </div>
                <div class="flex items-center space-x-2">
                    <i class="fas fa-check-circle text-green-400"></i>
                    <span>Auto Routes</span>
                </div>
            </div>

            <!-- Footer -->
            <div class="mt-12 text-gray-400 text-sm">
                <p>Powered by AI Agents | Built with ❤️</p>
            </div>
        </div>
    </div>
</body>
</html>
"""
    
    with open(welcome_path, "w", encoding="utf-8") as f:
        f.write(welcome_content)
    
    print("✅ Created: GenLaravel welcome page")


def clean_history():
    """Clean generation history"""
    if os.path.exists("history"):
        shutil.rmtree("history")
        print("✅ Cleaned: history/")
    else:
        print("ℹ️ history/ already clean")


def main():
    print("🧹 GenLaravel Project Cleaner\n")
    
    print("What do you want to clean?")
    print("1. Output folder only")
    print("2. Laravel views only")
    print("3. Routes only")
    print("4. Everything (recommended for fresh start)")
    print("5. Cancel")
    
    choice = input("\nChoice [1-5]: ").strip()
    
    if choice == "1":
        clean_output()
    elif choice == "2":
        clean_laravel_views()
    elif choice == "3":
        reset_routes()
    elif choice == "4":
        print("\n🔥 Cleaning everything...\n")
        clean_output()
        clean_laravel_views()
        reset_routes()
        create_genlaravel_welcome()
        clean_history()
        print("\n✅ Project cleaned! Ready for fresh generation.")
    elif choice == "5":
        print("❌ Cancelled")
    else:
        print("❌ Invalid choice")


if __name__ == "__main__":
    main()
