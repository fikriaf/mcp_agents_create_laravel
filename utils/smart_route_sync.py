"""
Smart Route Synchronizer
Ensures navbar/footer links match actual routes in web.php
Never removes valid routes, only fixes broken ones
"""

import os
import re


def get_all_routes():
    """Get all routes from web.php with their paths"""
    route_file = "my-laravel/routes/web.php"
    
    if not os.path.exists(route_file):
        return {}
    
    with open(route_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    routes = {}
    
    # Pattern: Route::get('/path', ...)->name('route.name')
    pattern = r"Route::get\(['\"]([^'\"]+)['\"].*?->name\(['\"]([^'\"]+)['\"]\)"
    matches = re.findall(pattern, content, re.DOTALL)
    
    for path, name in matches:
        routes[name] = {
            'path': path,
            'name': name
        }
    
    return routes


def extract_nav_links_from_draft():
    """Extract navigation links from draft HTML"""
    draft_dir = "output/drafts"
    
    if not os.path.exists(draft_dir):
        return []
    
    # Get first draft file
    draft_files = [f for f in os.listdir(draft_dir) if f.endswith('.html')]
    if not draft_files:
        return []
    
    first_draft = os.path.join(draft_dir, draft_files[0])
    
    with open(first_draft, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract nav links
    nav_links = []
    
    # Find nav section
    nav_match = re.search(r'<nav[^>]*>(.*?)</nav>', content, re.DOTALL | re.IGNORECASE)
    if not nav_match:
        # Try header
        nav_match = re.search(r'<header[^>]*>(.*?)</header>', content, re.DOTALL | re.IGNORECASE)
    
    if nav_match:
        nav_content = nav_match.group(1)
        
        # Find all links
        link_pattern = r'<a[^>]*href=["\']([^"\']+)["\'][^>]*>([^<]+)</a>'
        links = re.findall(link_pattern, nav_content, re.IGNORECASE)
        
        for href, text in links:
            # Skip external links and anchors
            if href.startswith('http') or href == '#':
                continue
            
            # Clean href
            href_clean = href.strip('/').replace('.html', '')
            
            nav_links.append({
                'href': href_clean,
                'text': text.strip(),
                'original_href': href
            })
    
    return nav_links


def sync_navbar_routes():
    """Sync navbar routes with actual routes"""
    # Get available routes
    routes = get_all_routes()
    
    if not routes:
        print("❌ No routes found in web.php")
        return
    
    print(f"📋 Found {len(routes)} route(s) in web.php:")
    for route_name, route_info in routes.items():
        print(f"   • {route_name} → {route_info['path']}")
    
    # Get nav links from draft
    nav_links = extract_nav_links_from_draft()
    
    if not nav_links:
        print("\n⚠️ No nav links found in draft")
        return
    
    print(f"\n📋 Found {len(nav_links)} nav link(s) in draft:")
    for link in nav_links:
        print(f"   • {link['text']} → {link['href']}")
    
    # Build mapping
    link_to_route = {}
    
    for link in nav_links:
        href = link['href']
        text = link['text'].lower()
        
        # Try to match with routes
        matched_route = None
        
        # 1. Direct match by path
        for route_name, route_info in routes.items():
            route_path = route_info['path'].strip('/')
            if href == route_path or href == route_name:
                matched_route = route_name
                break
        
        # 2. Match by text similarity
        if not matched_route:
            for route_name, route_info in routes.items():
                route_path = route_info['path'].strip('/')
                if text in route_path.lower() or route_path.lower() in text:
                    matched_route = route_name
                    break
        
        # 3. Match by route name similarity
        if not matched_route:
            for route_name in routes.keys():
                if text in route_name.lower() or route_name.lower() in text:
                    matched_route = route_name
                    break
        
        if matched_route:
            link_to_route[link['text']] = matched_route
            print(f"\n✅ Matched: '{link['text']}' → route('{matched_route}')")
        else:
            print(f"\n⚠️ No match: '{link['text']}' (href: {link['href']})")
    
    # Update ALL components (not just header/footer)
    components_dir = "my-laravel/resources/views/components"
    
    if not os.path.exists(components_dir):
        return
    
    fixed_count = 0
    
    # Check ALL blade files
    for filename in os.listdir(components_dir):
        if not filename.endswith('.blade.php'):
            continue
        filepath = os.path.join(components_dir, filename)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix each nav link
        for link_text, route_name in link_to_route.items():
            # Pattern: <a ...>LinkText</a> with href="#" or plain href
            patterns = [
                # href="#"
                (rf'(<a[^>]*href=["\']#["\'][^>]*>)\s*{re.escape(link_text)}\s*(</a>)', 
                 rf'\1{link_text}\2'),
                # href="something"
                (rf'(<a[^>]*href=["\'][^"\']*["\'][^>]*>)\s*{re.escape(link_text)}\s*(</a>)', 
                 rf'\1{link_text}\2'),
            ]
            
            for pattern, _ in patterns:
                matches = list(re.finditer(pattern, content, re.IGNORECASE))
                for match in matches:
                    old_tag = match.group(0)
                    # Replace href with route()
                    new_tag = re.sub(
                        r'href=["\'][^"\']*["\']',
                        f'href="{{{{ route(\'{route_name}\') }}}}"',
                        old_tag
                    )
                    content = content.replace(old_tag, new_tag)
        
        # Also fix any existing route() calls that don't exist or use wrong name
        route_pattern = r'{{\s*route\([\'"]([^\'"]+)[\'"]\)\s*}}'
        found_routes = re.findall(route_pattern, content)
        
        for found_route in set(found_routes):
            if found_route not in routes:
                # Check if this is a path instead of route name
                # Example: route('settings-and-profile') should be route('settings.profile')
                matched_route = None
                
                for route_name, route_info in routes.items():
                    route_path = route_info['path'].strip('/')
                    
                    # Match by path
                    if found_route == route_path or found_route == route_path.replace('/', '-'):
                        matched_route = route_name
                        break
                
                if matched_route:
                    # Fix: replace with correct route name
                    content = re.sub(
                        rf'{{\{{\s*route\([\'\"]{re.escape(found_route)}[\'\"]\)\s*\}}}}',
                        f'{{{{ route(\'{matched_route}\') }}}}',
                        content
                    )
                    print(f"   ✅ Fixed route: {found_route} → {matched_route}")
                else:
                    # This route doesn't exist, replace with #
                    content = re.sub(
                        rf'{{\{{\s*route\([\'\"]{re.escape(found_route)}[\'\"]\)\s*\}}}}',
                        '#',
                        content
                    )
                    print(f"   ⚠️ Removed invalid route: {found_route}")
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"\n✅ Updated: {filename}")
            fixed_count += 1
    
    print(f"\n{'='*60}")
    if fixed_count > 0:
        print(f"✅ Synced routes in {fixed_count} component(s)")
    else:
        print("ℹ️ All routes already synced")
    print(f"{'='*60}")


def main():
    print("🔄 Smart Route Synchronizer\n")
    sync_navbar_routes()


if __name__ == "__main__":
    main()
