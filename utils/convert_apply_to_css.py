"""
Convert Tailwind @apply directives to pure CSS
Because @apply doesn't work with CDN version
"""

import re


# Mapping of common Tailwind classes to CSS
TAILWIND_TO_CSS = {
    # Padding
    r'px-(\d+)': lambda m: f'padding-left: {int(m.group(1)) * 0.25}rem; padding-right: {int(m.group(1)) * 0.25}rem;',
    r'py-(\d+)': lambda m: f'padding-top: {int(m.group(1)) * 0.25}rem; padding-bottom: {int(m.group(1)) * 0.25}rem;',
    r'p-(\d+)': lambda m: f'padding: {int(m.group(1)) * 0.25}rem;',
    
    # Margin
    r'mx-auto': lambda m: 'margin-left: auto; margin-right: auto;',
    r'mb-(\d+)': lambda m: f'margin-bottom: {int(m.group(1)) * 0.25}rem;',
    r'mt-(\d+)': lambda m: f'margin-top: {int(m.group(1)) * 0.25}rem;',
    
    # Flex
    r'flex': lambda m: 'display: flex;',
    r'flex-1': lambda m: 'flex: 1 1 0%;',
    r'flex-col': lambda m: 'flex-direction: column;',
    r'flex-row': lambda m: 'flex-direction: row;',
    r'flex-row-reverse': lambda m: 'flex-direction: row-reverse;',
    r'items-center': lambda m: 'align-items: center;',
    r'justify-between': lambda m: 'justify-content: space-between;',
    r'space-x-(\d+)': lambda m: f'gap: {int(m.group(1)) * 0.25}rem;',
    
    # Width/Height
    r'w-full': lambda m: 'width: 100%;',
    r'w-64': lambda m: 'width: 16rem;',
    r'h-screen': lambda m: 'height: 100vh;',
    r'max-w-2xl': lambda m: 'max-width: 42rem;',
    
    # Border
    r'rounded-lg': lambda m: 'border-radius: 0.5rem;',
    r'rounded-full': lambda m: 'border-radius: 9999px;',
    r'border-t': lambda m: 'border-top-width: 1px;',
    r'border-gray-300': lambda m: 'border-color: #d1d5db;',
    
    # Background
    r'bg-gray-100': lambda m: 'background-color: #f3f4f6;',
    r'bg-gray-200': lambda m: 'background-color: #e5e7eb;',
    r'bg-white': lambda m: 'background-color: #ffffff;',
    r'bg-opacity-20': lambda m: 'background-color: rgba(255, 255, 255, 0.2);',
    
    # Text
    r'text-lg': lambda m: 'font-size: 1.125rem; line-height: 1.75rem;',
    r'text-xl': lambda m: 'font-size: 1.25rem; line-height: 1.75rem;',
    r'text-2xl': lambda m: 'font-size: 1.5rem; line-height: 2rem;',
    r'text-xs': lambda m: 'font-size: 0.75rem; line-height: 1rem;',
    r'text-white': lambda m: 'color: #ffffff;',
    r'text-gray-500': lambda m: 'color: #6b7280;',
    r'font-bold': lambda m: 'font-weight: 700;',
    r'font-semibold': lambda m: 'font-weight: 600;',
    
    # Transitions
    r'transition-all': lambda m: 'transition-property: all;',
    r'duration-300': lambda m: 'transition-duration: 300ms;',
    r'ease-in-out': lambda m: 'transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);',
    
    # Transform
    r'transform': lambda m: '',  # Already implied
    r'hover:scale-105': lambda m: '',  # Handle separately
    r'hover:bg-opacity-90': lambda m: '',  # Handle separately
    
    # Overflow
    r'overflow-y-auto': lambda m: 'overflow-y: auto;',
    r'overflow-x-auto': lambda m: 'overflow-x: auto;',
    
    # Cursor
    r'cursor-pointer': lambda m: 'cursor: pointer;',
}


def convert_apply_line(apply_line):
    """Convert a single @apply line to pure CSS"""
    # Extract classes from @apply
    classes = apply_line.replace('@apply', '').strip().rstrip(';').split()
    
    css_properties = []
    
    for cls in classes:
        matched = False
        for pattern, converter in TAILWIND_TO_CSS.items():
            match = re.match(pattern + '$', cls)
            if match:
                result = converter(match)
                if result:
                    css_properties.append(result)
                matched = True
                break
        
        if not matched:
            # Keep as comment for manual review
            css_properties.append(f'/* TODO: Convert {cls} */')
    
    return '\n            '.join(css_properties)


def convert_apply_in_css(css_content):
    """Convert all @apply directives in CSS content"""
    lines = css_content.split('\n')
    result = []
    
    for line in lines:
        if '@apply' in line:
            indent = len(line) - len(line.lstrip())
            converted = convert_apply_line(line)
            result.append(' ' * indent + converted)
        else:
            result.append(line)
    
    return '\n'.join(result)


def main():
    print("🔄 Converting @apply to pure CSS...\n")
    print("This is a helper tool. Manual review recommended.")
    print("\nExample:")
    print("  Input:  @apply px-6 py-3 rounded-full font-semibold;")
    print("  Output: padding-left: 1.5rem; padding-right: 1.5rem;")
    print("          padding-top: 0.75rem; padding-bottom: 0.75rem;")
    print("          border-radius: 9999px;")
    print("          font-weight: 600;")


if __name__ == "__main__":
    main()
