"""
Standalone Multi-Page Validator
Run this script to validate your multi-page Laravel application
"""

import sys
from utils.multi_page_validator import validate_multi_page_app

def main():
    print("="*60)
    print("🔍 MULTI-PAGE VALIDATOR")
    print("="*60)
    print()
    
    laravel_path = sys.argv[1] if len(sys.argv) > 1 else "my-laravel"
    
    print(f"📂 Validating Laravel project: {laravel_path}\n")
    
    is_valid = validate_multi_page_app(laravel_path)
    
    if is_valid:
        print("\n🎉 SUCCESS! Your multi-page application is ready to use.")
        return 0
    else:
        print("\n❌ FAILED! Please fix the errors above before proceeding.")
        print("\n💡 Tips:")
        print("  • Check route definitions in routes/web.php")
        print("  • Verify component files exist in resources/views/components")
        print("  • Ensure all @include references are correct")
        print("  • Run auto-fix utilities in utils/ folder")
        return 1

if __name__ == "__main__":
    sys.exit(main())
