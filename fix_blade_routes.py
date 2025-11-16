import re
import glob

# Fix all blade files
blade_files = glob.glob('my-laravel/resources/views/**/*.blade.php', recursive=True)

for filepath in blade_files:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # Fix: {{ route('x') }}) }} → {{ route('x') }}
        content = re.sub(r"(\{\{\s*route\(['\"][^'\"]+['\"]\)\s*)\}\}\s*\)\s*\}\}", r'\1}}', content)
        
        # Fix: {{ route('x'}}text → {{ route('x') }}" class="text
        content = re.sub(r"(\{\{\s*route\(['\"][^'\"]+['\"])\}\}([a-zA-Z])", r'\1) }}" class="\2', content)
        
        # Fix missing closing parenthesis: {{ route('x' }} → {{ route('x') }}
        content = re.sub(r"(\{\{\s*route\(['\"][^'\"]+['\"])\s*\}\}", r'\1) }}', content)
        
        # Fix extra closing braces: {{ route('x') }}}} → {{ route('x') }}
        content = re.sub(r"(\{\{\s*route\(['\"][^'\"]+['\"]\)\s*\}\})\}\}", r'\1', content)
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'✅ Fixed: {filepath}')
        else:
            print(f'⏭️  Skipped: {filepath} (no issues)')
            
    except Exception as e:
        print(f'❌ Error fixing {filepath}: {e}')

print('\n✅ All blade files processed')
