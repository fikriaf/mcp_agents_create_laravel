import re

content = open('my-laravel/resources/views/home.blade.php', 'r', encoding='utf-8').read()
pattern = r"@include\(['\"]components\.([^'\"]+)['\"]\)"

print("Content:")
print(content)
print("\nPattern:", pattern)
print("\nMatches:", re.findall(pattern, content))
