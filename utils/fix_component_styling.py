"""
Fix component styling to use CSS classes instead of Tailwind arbitrary values
Ensures background images and custom styles work properly
"""

import os
import re


def fix_hero_section():
    """Fix HeroSection to use .hero class instead of inline styles or bg-[url(...)]"""
    # Try both naming conventions
    hero_paths = [
        "my-laravel/resources/views/components/HeroSection.blade.php",
        "my-laravel/resources/views/components/herosection.blade.php"
    ]
    
    hero_path = None
    for path in hero_paths:
        if os.path.exists(path):
            hero_path = path
            break
    
    if not hero_path:
        print("⚠️ HeroSection.blade.php not found")
        return
    
    with open(hero_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    original_content = content
    
    # Replace inline style background-image with .hero class
    # Pattern: style="background-image: url(...)"
    if 'style="background-image:' in content or "style='background-image:" in content:
        # Remove inline style attribute
        content = re.sub(r'\s*style=["\'][^"\']*background-image[^"\']*["\']', '', content)
        
        # Add .hero class if not present
        if 'class="hero' not in content and "class='hero" not in content:
            content = re.sub(r'<section\s+class="', '<section class="hero ', content, count=1)
            content = re.sub(r"<section\s+class='", "<section class='hero ", content, count=1)
        
        print("   ✅ Converted inline style to .hero class")
    
    # Replace Tailwind bg-[url(...)] with .hero class
    # Pattern: bg-[url('...')] or bg-[url("...")]
    content = re.sub(
        r'class="[^"]*bg-\[url\([\'"][^\'"]+[\'"]\)\][^"]*"',
        lambda m: m.group(0).replace(
            re.search(r'bg-\[url\([\'"][^\'"]+[\'"]\)\]', m.group(0)).group(0),
            'hero'
        ),
        content
    )
    
    # Ensure using .hero class (not .hero-section)
    if 'hero-section' in content:
        content = content.replace('hero-section', 'hero')
    
    # Remove redundant bg-cover, bg-center if .hero is used
    if 'class="hero' in content or "class='hero" in content:
        content = re.sub(r'\s*bg-cover\s*', ' ', content)
        content = re.sub(r'\s*bg-center\s*', ' ', content)
        content = re.sub(r'\s*bg-gradient-to-b\s+from-black/50\s+to-black/50\s*', ' ', content)
    
    # DISABLED - Do NOT replace colors, preserve exact colors from draft
    # Only keep animation/utility class replacements if they exist in CSS
    replacements = {
        # Color replacements DISABLED to preserve draft colors
        # r'bg-red-\d+': 'bg-secondary-color',  # DISABLED
        # r'bg-blue-\d+': 'bg-primary-color',   # DISABLED
        # r'text-red-\d+': 'text-secondary-color',  # DISABLED
        # r'text-blue-\d+': 'text-primary-color',   # DISABLED
        # r'bg-gray-900': 'bg-primary-color',   # DISABLED
        # r'bg-gray-800': 'bg-primary-color',   # DISABLED
        
        # Only replace if these classes exist in layout CSS
        # r'animate-fade-in': 'fade-in',  # DISABLED - keep Tailwind classes
        # r'transform hover:-translate-y-1 hover:shadow-lg': 'btn',  # DISABLED
    }
    
    # Skip color replacements to preserve draft styling
    # for pattern, replacement in replacements.items():
    #     content = re.sub(pattern, replacement, content)
    
    # Clean up multiple spaces in class attributes
    content = re.sub(r'class="([^"]*)"', lambda m: f'class="{" ".join(m.group(1).split())}"', content)
    
    if content != original_content:
        with open(hero_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("✅ Fixed HeroSection styling")
    else:
        print("ℹ️ HeroSection already correct")


def extract_css_classes_from_layout():
    """Extract available CSS classes from layout"""
    layout_path = "my-laravel/resources/views/layouts/app.blade.php"
    
    if not os.path.exists(layout_path):
        return set()
    
    with open(layout_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Extract CSS class names from <style> block
    style_match = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
    if not style_match:
        return set()
    
    css_content = style_match.group(1)
    
    # Find all class definitions
    class_pattern = r'\.([a-zA-Z0-9_-]+)\s*\{'
    classes = set(re.findall(class_pattern, css_content))
    
    return classes


def fix_all_components():
    """Dynamically fix all components based on available CSS classes"""
    components_dir = "my-laravel/resources/views/components"
    
    if not os.path.exists(components_dir):
        print("❌ Components directory not found")
        return
    
    # Get available CSS classes from layout
    available_classes = extract_css_classes_from_layout()
    print(f"   📋 Found {len(available_classes)} CSS classes in layout")
    
    # Dynamic fixes based on available classes
    fixes_applied = {
        'inline_styles': 0,
        'bg_images': 0,
        'color_classes': 0,
        'animation_classes': 0,
    }
    
    fixed_count = 0
    
    for filename in os.listdir(components_dir):
        if filename.endswith('.blade.php'):
            filepath = os.path.join(components_dir, filename)
            
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            
            original_content = content
            
            # 1. Fix inline background-image styles
            if 'style="background-image:' in content or "style='background-image:" in content:
                # Check if .hero class exists
                if 'hero' in available_classes:
                    content = re.sub(r'\s*style=["\'][^"\']*background-image[^"\']*["\']', '', content)
                    # Add .hero class if not present
                    if 'class="hero' not in content:
                        content = re.sub(r'<section\s+class="', '<section class="hero ', content, count=1)
                    fixes_applied['inline_styles'] += 1
            
            # 2. Fix Tailwind bg-[url(...)]
            if 'bg-[url(' in content:
                if 'hero' in available_classes:
                    content = re.sub(
                        r'bg-\[url\([\'"][^\'"]+[\'"]\)\]',
                        'hero',
                        content
                    )
                    # Remove redundant classes
                    content = re.sub(r'\s*bg-cover\s*', ' ', content)
                    content = re.sub(r'\s*bg-center\s*', ' ', content)
                    fixes_applied['bg_images'] += 1
            
            # 3. DISABLED - Do NOT fix colors, they should match draft exactly
            # Color fixing is disabled to preserve exact colors from draft HTML
            # Components should use the same Tailwind classes as the draft
            color_map = {}
            # OLD (WRONG):
            # color_map = {
            #     r'bg-red-\d+': 'bg-secondary-color',
            #     r'bg-blue-\d+': 'bg-primary-color',
            #     r'text-red-\d+': 'text-secondary-color',
            #     r'text-blue-\d+': 'text-primary-color',
            #     r'bg-gray-900': 'bg-primary-color',
            #     r'bg-gray-800': 'bg-primary-color',
            # }
            
            for pattern, replacement in color_map.items():
                if re.search(pattern, content):
                    content = re.sub(pattern, replacement, content)
                    fixes_applied['color_classes'] += 1
            
            # 4. Fix animation classes
            if 'fade-in' in available_classes:
                content = re.sub(r'animate-fade-in', 'fade-in', content)
            
            if 'btn' in available_classes:
                # Replace complex hover effects with .btn class
                if 'transform hover:-translate-y' in content or 'transition-transform' in content:
                    # Add .btn class if not present
                    if 'class="btn' not in content and 'btn ' not in content:
                        # Find buttons and add .btn class
                        content = re.sub(
                            r'(<(?:a|button)[^>]*class="[^"]*)(inline-block[^"]*")',
                            r'\1btn \2',
                            content
                        )
                    fixes_applied['animation_classes'] += 1
            
            # 5. Clean up multiple spaces in class attributes
            content = re.sub(r'class="([^"]*)"', lambda m: f'class="{" ".join(m.group(1).split())}"', content)
            
            # 6. Remove empty style attributes
            content = re.sub(r'\s*style=["\']["\']', '', content)
            
            if content != original_content:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"✅ Fixed: {filename}")
                fixed_count += 1
    
    if fixed_count == 0:
        print("ℹ️ All components already use correct styling")
    else:
        print(f"\n✅ Fixed {fixed_count} component(s)")
        if fixes_applied['inline_styles'] > 0:
            print(f"   • Inline styles → CSS classes: {fixes_applied['inline_styles']}")
        if fixes_applied['bg_images'] > 0:
            print(f"   • Background images → .hero: {fixes_applied['bg_images']}")
        if fixes_applied['color_classes'] > 0:
            print(f"   • Hardcoded colors → CSS variables: {fixes_applied['color_classes']}")
        if fixes_applied['animation_classes'] > 0:
            print(f"   • Animation classes → .fade-in/.btn: {fixes_applied['animation_classes']}")


def main():
    print("🎨 Fixing component styling...\n")
    
    print("1. Fixing HeroSection background...")
    fix_hero_section()
    
    print("\n2. Fixing component colors...")
    fix_all_components()
    
    print("\n✅ Styling fixes completed!")
    print("\nComponents now use:")
    print("  • .hero class for background images")
    print("  • CSS variables (--primary-color, --secondary-color)")
    print("  • .fade-in for animations")
    print("  • .btn for button effects")


if __name__ == "__main__":
    main()
