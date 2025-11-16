"""
Script to fix existing Laravel views:
1. Remove draft preview navbar from app.blade.php
2. Convert HTML links to Laravel routes in components
"""

import os
import re

def fix_app_layout():
    """Fix app.blade.php to remove draft preview UI"""
    layout_path = "my-laravel/resources/views/layouts/app.blade.php"
    
    if not os.path.exists(layout_path):
        print("❌ app.blade.php not found")
        return
    
    # Create clean layout
    clean_layout = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>@yield('title', 'My Portfolio')</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --primary-color: #3b82f6;
            --secondary-color: #8b5cf6;
        }
        
        .text-primary-color {
            color: var(--primary-color);
        }
        
        .text-secondary-color {
            color: var(--secondary-color);
        }
        
        .bg-primary-color {
            background-color: var(--primary-color);
        }
        
        .bg-secondary-color {
            background-color: var(--secondary-color);
        }
    </style>
</head>
<body class="bg-gray-50">
    @yield('content')
</body>
</html>
"""
    
    with open(layout_path, "w", encoding="utf-8") as f:
        f.write(clean_layout)
    
    print(f"✅ Fixed: {layout_path}")


def get_available_routes():
    """Get available routes from web.php with path mapping"""
    route_file = "my-laravel/routes/web.php"
    available_routes = {}
    route_paths = {}
    
    if os.path.exists(route_file):
        with open(route_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Extract route names: ->name('route-name')
        route_pattern = r"Route::get\(['\"]([^'\"]+)['\"].*?->name\(['\"]([^'\"]+)['\"]\)"
        matches = re.findall(route_pattern, content, re.DOTALL)
        
        for path, route_name in matches:
            available_routes[route_name] = True
            route_paths[route_name] = path
            
            # Also map path without leading slash
            path_clean = path.lstrip('/')
            route_paths[path_clean] = route_name
        
        print(f"📋 Available routes: {', '.join(available_routes.keys())}")
    
    return available_routes, route_paths


def fix_component_routes():
    """Fix routes in all components based on available routes"""
    components_dir = "my-laravel/resources/views/components"
    
    if not os.path.exists(components_dir):
        print("❌ Components directory not found")
        return
    
    # Get available routes with path mapping
    available_routes, route_paths = get_available_routes()
    
    if not available_routes:
        print("⚠️ No routes found in web.php")
        return
    
    # Build smart route mapping
    route_map = {}
    
    # Map common page names to routes
    page_name_mapping = {
        'home': ['home', 'index', 'beranda'],
        'about': ['about', 'tentang', 'tentang-kami'],
        'contact': ['contact', 'kontak', 'hubungi-kami'],
        'projects': ['projects', 'proyek', 'portfolio'],
        'services': ['services', 'layanan'],
        'blog': ['blog', 'artikel'],
        'features': ['features', 'fitur'],
        'pricing': ['pricing', 'harga', 'price'],
        'chat': ['chat', 'chat-interface'],
        'speech': ['speech', 'speech-recognition-settings', 'speech-settings'],
        'voice': ['voice', 'voice-settings'],
        'settings': ['settings', 'pengaturan'],
        'dashboard': ['dashboard', 'dasbor'],
        'profile': ['profile', 'profil'],
        'docs': ['docs', 'documentation', 'dokumentasi'],
        'faq': ['faq', 'help', 'bantuan'],
    }
    
    # Build mapping from page paths to route names
    for page_key, variants in page_name_mapping.items():
        for variant in variants:
            # Check if this variant exists as a route path
            if variant in route_paths:
                route_name = route_paths[variant]
                # Map all variants to this route
                for v in variants:
                    route_map[rf'href=["\']/?{v}["\']'] = f'href="{{{{ route(\'{route_name}\') }}}}"'
                    route_map[rf'href=["\']/?{v}\.html["\']'] = f'href="{{{{ route(\'{route_name}\') }}}}"'
                break
    
    # DYNAMIC FALLBACK: Add all available routes directly
    # This handles routes not in the predefined mapping
    for route_name in available_routes.keys():
        # Convert route name to path (e.g., 'admin.panel' -> 'admin-panel')
        route_path = route_name.replace('.', '-')
        
        # Add direct mapping
        route_map[rf'href=["\']/?{route_path}["\']'] = f'href="{{{{ route(\'{route_name}\') }}}}"'
        route_map[rf'href=["\']/?{route_path}\.html["\']'] = f'href="{{{{ route(\'{route_name}\') }}}}"'
        
        # Also map the route name itself
        route_map[rf'href=["\']/?{route_name}["\']'] = f'href="{{{{ route(\'{route_name}\') }}}}"'
    
    fixed_count = 0
    
    for filename in os.listdir(components_dir):
        if filename.endswith('.blade.php'):
            filepath = os.path.join(components_dir, filename)
            
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            
            original_content = content
            
            # Skip file if it already has route() calls (already processed)
            if '{{ route(' in content:
                print(f"  ⏭️  {filename}: Already has route() calls, skipping")
                continue
            
            # Apply route replacements
            for pattern, replacement in route_map.items():
                content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
            
            # Fix plain text links (e.g., <a href="#">Home</a>)
            # Match link text with available routes
            for route_name in available_routes.keys():
                # Pattern: <a href="#">RouteNameText</a>
                # Convert route name to title case for matching
                route_title = route_name.replace('-', ' ').replace('_', ' ').replace('.', ' ').title()
                route_single = route_name.replace('-', '').replace('_', '').replace('.', '')
                
                # Try multiple patterns
                patterns = [
                    # Title case: "Admin Panel"
                    (rf'(<a[^>]*href=["\']#["\'][^>]*>)\s*{re.escape(route_title)}\s*(</a>)', route_name),
                    # Single word: "adminpanel"
                    (rf'(<a[^>]*href=["\']#["\'][^>]*>)\s*{re.escape(route_single)}\s*(</a>)', route_name),
                    # With dashes: "admin-panel"
                    (rf'(<a[^>]*href=["\']#["\'][^>]*>)\s*{re.escape(route_name)}\s*(</a>)', route_name),
                    # Capitalized: "Home", "Features"
                    (rf'(<a[^>]*href=["\']#["\'][^>]*>)\s*{re.escape(route_name.capitalize())}\s*(</a>)', route_name),
                ]
                
                for pattern, target_route in patterns:
                    matches = list(re.finditer(pattern, content, re.IGNORECASE))
                    for match in matches:
                        # Replace href="#" with route()
                        old_tag = match.group(0)
                        new_tag = re.sub(r'href=["\']#["\']', f'href="{{{{ route(\'{target_route}\') }}}}"', old_tag)
                        content = content.replace(old_tag, new_tag)
            
            # Fix ALL route() calls that don't exist (dynamic detection)
            # Find all route('...') patterns
            route_pattern = r'{{\s*route\([\'"]([^\'"]+)[\'"]\)\s*}}'
            found_routes = re.findall(route_pattern, content)
            
            for route_name in set(found_routes):
                if route_name not in available_routes:
                    # Replace route('nonexistent') with #
                    content = re.sub(
                        rf'{{\{{\s*route\([\'\"]{route_name}[\'\"]\)\s*\}}}}',
                        '#',
                        content
                    )
                    print(f"  ⚠️ Fixed undefined route: {route_name} → #")
            
            # Also check for plain href with route names that don't exist
            # Pattern: href="route-name" or href="/route-name"
            href_pattern = r'href=["\']/?([a-zA-Z0-9\-_\.]+)["\']'
            found_hrefs = re.findall(href_pattern, content)
            
            for href_value in set(found_hrefs):
                # Skip if it's already a route() call, #, or external URL
                if href_value in ['#', ''] or href_value.startswith('http') or '{{' in href_value:
                    continue
                
                # Check if this looks like a route name
                potential_route = href_value.replace('/', '').replace('.html', '')
                
                # If it matches a route name but not converted yet, it's an error
                if potential_route in available_routes and f"route('{potential_route}')" not in content:
                    # This should have been converted but wasn't
                    print(f"  💡 Hint: Found href='{href_value}' - consider adding to mapping")
            
            # Only write if changed
            if content != original_content:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"✅ Fixed routes in: {filename}")
                fixed_count += 1
    
    if fixed_count == 0:
        print("ℹ️ No components needed route fixes")
    else:
        print(f"\n✅ Fixed {fixed_count} component(s)")


def fix_route_views():
    """Fix view names in routes to match actual files"""
    route_file = "my-laravel/routes/web.php"
    
    if not os.path.exists(route_file):
        print("⚠️ routes/web.php not found")
        return
    
    with open(route_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    original_content = content
    
    # Get blade files
    views_dir = "my-laravel/resources/views"
    blade_files = []
    
    if os.path.exists(views_dir):
        for file in os.listdir(views_dir):
            if file.endswith('.blade.php') and file != 'welcome.blade.php':
                blade_files.append(file.replace('.blade.php', ''))
    
    # Fix common patterns
    for blade_file in blade_files:
        patterns = [
            (rf"view\(['\"]auth\.{blade_file}['\"]\)", f"view('{blade_file}')"),
            (rf"view\(['\"]admin\.{blade_file}['\"]\)", f"view('{blade_file}')"),
            (rf"view\(['\"]pages\.{blade_file}['\"]\)", f"view('{blade_file}')"),
        ]
        
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content)
    
    # Fix registration → registration
    if 'registration' in blade_files:
        content = re.sub(r"view\(['\"]register['\"]\)", "view('registration')", content)
    
    # Fix Laravel auth routes that don't exist
    auth_routes_to_remove = [
        'password.request',
        'password.email',
        'password.reset',
        'password.confirm',
        'verification.notice',
        'verification.verify',
        'verification.send',
    ]
    
    for auth_route in auth_routes_to_remove:
        # Replace route('auth.route') with #
        content = re.sub(
            rf'{{\{{\s*route\([\'\"]{auth_route}[\'\"]\)\s*\}}}}',
            '#',
            content
        )
    
    if content != original_content:
        with open(route_file, "w", encoding="utf-8") as f:
            f.write(content)
        print("✅ Fixed route view names")
    else:
        print("ℹ️ Route view names already correct")


def main():
    print("🔧 Fixing existing Laravel views...\n")
    
    print("1. Fixing app.blade.php layout...")
    fix_app_layout()
    
    print("\n2. Fixing component routes...")
    fix_component_routes()
    
    print("\n3. Fixing route view names...")
    fix_route_views()
    
    print("\n✅ All fixes applied!")
    print("\nYou can now run: php artisan serve")


if __name__ == "__main__":
    main()
