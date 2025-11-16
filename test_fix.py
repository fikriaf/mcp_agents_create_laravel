import re

filepath = "my-laravel/resources/views/home.blade.php"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

print("File content:")
print(repr(content))
print("\n" + "="*60)

include_pattern = r"@include\(['\"]components\.([^'\"]+)['\"]\)"
includes = re.findall(include_pattern, content)

print(f"\nPattern: {include_pattern}")
print(f"Includes found: {includes}")
print(f"Length: {len(includes)}")

if includes:
    print("\nTesting replacement:")
    for inc in includes:
        print(f"  - {inc}")
        no_dash = inc.replace('-', '')
        print(f"    no_dash: {no_dash}")
