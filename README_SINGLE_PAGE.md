# GenLaravel - Single Page Mode

## 🎯 Overview
Generate single Laravel page dengan AI agents.

## 🚀 Quick Start

```bash
python main.py
```

**Example Prompt:**
```
"Create a login page with email, password, and remember me checkbox"
```

## 📊 Output

```
output/
├── draft.html              ← Preview HTML
├── login.blade.php         ← Main view
├── components/
│   ├── LoginForm.blade.php
│   └── AuthCard.blade.php
├── layouts/
│   └── app.blade.php
└── web.php                 ← Route

my-laravel/
└── resources/views/
    ├── login.blade.php
    ├── components/...
    └── layouts/app.blade.php
```

## 🔄 Flow

```
1. User Input → Prompt
2. Prompt Expander → Enhanced prompt
3. Draft Agent → HTML preview
4. User Approval → Continue/Revise
5. Planner → Component list
6. Page Architect → Layout structure
7. Component Agent → Blade components
8. UI Generator → Main blade view
9. Layout Generator → app.blade.php
10. Route Agent → web.php
11. Validator → Check syntax
12. Move to Laravel → Integration
```

## ⚙️ Configuration

Edit `.env`:
```env
CEREBRAS_API_KEY=your_key
MISTRAL_API_KEY=your_key
```

## 📝 Tips

- Be specific in prompts
- Review draft before continuing
- Check validation results
- Auto-fix applies CSS and routes automatically ✨
- Test in browser after generation

## 🐛 Troubleshooting

**Issue: Draft tidak muncul**
```bash
# Check output folder
ls output/
```

**Issue: Validation failed**
```bash
# Check component syntax
cat output/components/*.blade.php
```

**Issue: Routes tidak bekerja**
```bash
# Run fix script
python fix_existing_views.py
```

## 📦 Files

- `main.py` - Main orchestrator
- `agents/` - All agent modules
- `output/` - Generated files
- `my-laravel/` - Laravel project
