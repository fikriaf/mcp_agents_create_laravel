# GenLaravel - Multi Page Mode

## 🎯 Overview
Generate multiple Laravel pages dengan AI agents dalam satu execution.

## 🚀 Quick Start

### Option 1: Web Interface with Backend (Recommended)
```bash
# 1. Install all dependencies
pip install -r requirements.txt

# 2. Start FastAPI server
python run_server.py

# 3. Open browser
# Navigate to: http://localhost:8080
```

**Features:**
- 🎨 Beautiful UI with real-time progress
- 📊 Live statistics and page preview
- ⚡ Daily limit tracker (5 generations/day)
- 🔄 Draft review and revision workflow
- 📱 Responsive design
- 🔌 WebSocket for real-time updates

### Option 2: Frontend Only (Static)
```bash
# Open the multi-page frontend directly
open frontend/multi-page.html
# or
start frontend/multi-page.html
```

**Note:** Static mode uses simulated data. For full functionality, use backend server.

### Option 3: Command Line
```bash
# Clean previous generation (recommended)
python utils/clean_project.py
# Choose option 4 (Everything)

# Then generate
python main_multi_page.py
# Auto-cleans output and Laravel views
```

**Example Prompts:**
```
"Create login and dashboard pages"
"Build e-commerce with home, products, cart, checkout"
"Make blog with posts list, post detail, about"
"Chat application with login page and chat interface"
```

## ⚡ Daily Limit

Multi-page generation is limited to **5 generations per day** to ensure:
- Optimal LLM performance
- Cost management
- Quality over quantity

The limit resets daily at midnight (local time).

## 🔍 Validation & Auto-Fix

### Validate Your Multi-Page App
```bash
# Run comprehensive validation
python validate_multi_page.py

# Checks:
# ✓ Routes & components
# ✓ Blade syntax
# ✓ Nested UI issues
# ✓ Duplicate JavaScript
# ✓ CSS consistency
```

### Auto-Fix Common Issues
```bash
# Fix nested UI & duplicate JS
python utils/fix_nested_ui.py

# Fix draft styling (Tailwind CDN, CSS)
python utils/fix_draft_styling.py

# Fix all issues at once
python utils/auto_fix_multi_page.py
```

**Common Issues Fixed:**
- ❌ Nested HTML structures (component with full `<html>` tags)
- ❌ Duplicate JavaScript blocks
- ❌ Component name mismatches
- ❌ Route synchronization errors
- ❌ CSS inconsistencies
- ❌ Draft styling broken (old Tailwind CDN, CSS conflicts)

## 📊 Output

```
output/
├── draft.html              ← Index dengan tabs
├── drafts/
│   ├── login.html         ← Individual draft 1
│   ├── dashboard.html     ← Individual draft 2
│   └── profile.html       ← Individual draft 3
├── login.blade.php
├── dashboard.blade.php
├── profile.blade.php
├── components/
│   ├── Navbar.blade.php   ← Shared components
│   ├── LoginForm.blade.php
│   └── StatsCard.blade.php
├── layouts/
│   └── app.blade.php      ← Shared layout
└── web.php                ← Multiple routes

my-laravel/
└── resources/views/
    ├── login.blade.php
    ├── dashboard.blade.php
    ├── profile.blade.php
    ├── components/...
    └── layouts/app.blade.php
```

## 🔄 Flow

```
1. User Input → Multi-page prompt
2. Prompt Expander → Enhanced prompt
3. Draft Agent V2 → Detect pages
   ├── Generate login.html
   ├── Generate dashboard.html
   └── Generate profile.html
4. Create draft index with tabs
5. User Approval → Continue/Revise
6. Multi Planner → Detect N pages
7. FOR EACH PAGE:
   ├── Page Architect → Layout
   ├── Component Agent → Components
   └── UI Generator → Blade view
8. Layout Generator → Shared app.blade.php
9. Route Agent V2 → Multiple routes
10. Validator → Check all components
11. Move to Laravel → Integration
```

## ✨ Features

### 1. Auto-Detection
System otomatis detect berapa pages yang dibutuhkan dari prompt.

### 2. Multiple Drafts
Setiap page punya draft HTML sendiri untuk preview.

### 3. Tabbed Preview
Draft index dengan tab navigation untuk switch antar pages.

### 4. Smart Component Sharing
Components dengan nama sama otomatis di-merge.

### 5. Single Layout
Semua pages menggunakan 1 shared `app.blade.php`.

### 6. Multiple Routes
Generate semua routes sekaligus dalam 1 `web.php`.

## 🎨 Draft Preview

```
┌─────────────────────────────────────────┐
│ GenLaravel Draft Preview                │
│ [Login] [Dashboard] [Profile]  ← Tabs  │
├─────────────────────────────────────────┤
│                                         │
│     [Current Page Preview]              │
│     (Click tabs to switch)              │
│                                         │
└─────────────────────────────────────────┘
```

## 📈 Performance

| Pages | Time | LLM Calls | Files |
|-------|------|-----------|-------|
| 1 | ~30s | ~10 | ~5 |
| 3 | ~90s | ~28 | ~13 |
| 5 | ~150s | ~46 | ~21 |

## 🔧 Enhanced Agents

### 1. Draft Agent V2 (`b_draft_agent_v2.py`)
- Detect multiple pages
- Generate individual HTML drafts
- Create tabbed index

### 2. Planner V2 (`c_prompt_planner_v2.py`)
- Return array of pages
- Each page with components & route

### 3. Route Agent V2 (`g_route_agent_v2.py`)
- Generate multiple routes
- Named routes support

## 🐛 Common Issues & Fixes

### Issue 1: Draft Preview Navbar Menempel
**Problem:** Layout masih ada UI preview

**Fix:**
```bash
python utils/fix_existing_views.py
```

**Prevention:** Enhanced di `agents/e_generate_layout_app.py`

---

### Issue 2: Routes Tidak Bekerja
**Problem:** Links masih `href="index.html"` atau `Route [name] not defined`

**Fix:**
```bash
python utils/fix_existing_views.py
```

Script akan:
- Detect routes yang tersedia di `web.php`
- Convert HTML links ke Laravel routes yang ada
- Replace routes yang tidak ada dengan `#` (fallback)

**Prevention:** Enhanced di `agents/h_component_agent.py`

---

### Issue 3: Duplicate Routes
**Problem:** Routes di-append berkali-kali

**Fix:** Sudah fixed di `agents/j_move_to_project.py` (replace instead of append)

---

## 📝 Route Conversion

| HTML | Laravel |
|------|---------|
| `href="index.html"` | `href="{{ route('home') }}"` |
| `href="about.html"` | `href="{{ route('about') }}"` |
| `href="#section"` | `href="#section"` (unchanged) |

## 🎓 Examples

### Example 1: Auth System
```
Prompt: "Create login, register, forgot password pages"

Output:
- 3 HTML drafts
- 3 Blade views
- 3 routes
- Shared components (AuthCard, InputField)
```

### Example 2: E-commerce
```
Prompt: "Build shop with home, products, cart, checkout"

Output:
- 4 HTML drafts
- 4 Blade views
- 4 routes
- Shared components (ProductCard, Navbar)
```

### Example 3: Blog
```
Prompt: "Create blog with posts list, post detail, about"

Output:
- 3 HTML drafts
- 3 Blade views
- 3 routes
- Shared components (PostCard, Header)
```

## 🔄 Backward Compatibility

Multi-page mode tetap support single page:

```bash
python main_multi_page.py
```

Prompt: `"Create a login page"` → Generate 1 page (works!)

## 📦 File Structure

```
agents/
├── a_prompt_expander.py       ← Unchanged
├── b_draft_agent_v2.py        ← NEW: Multi-draft
├── c_prompt_planner_v2.py     ← NEW: Multi-page detection
├── d_page_architect.py        ← Unchanged
├── e_generate_layout_app.py   ← Enhanced
├── f_ui_generator.py          ← Unchanged
├── g_route_agent_v2.py        ← NEW: Multi-route
├── h_component_agent.py       ← Enhanced
├── i_validator_agent.py       ← Unchanged
└── j_move_to_project.py       ← Enhanced

main_multi_page.py             ← NEW: Multi-page orchestrator
fix_existing_views.py          ← Utility: Fix production issues
```

## 🚀 Production Checklist

### Before Generation
- [ ] Run `python clean_project.py` (option 4)
- [ ] Or answer 'y' when prompted to clean

### During Generation
- [ ] Review all drafts in browser
- [ ] Click each tab to check pages
- [ ] Approve or request revision

### After Generation
- [ ] Run `python fix_existing_views.py`
- [ ] Check `php artisan route:list`
- [ ] Test `php artisan serve`
- [ ] Click all navigation links
- [ ] Verify no 404 errors
- [ ] Check no "Route not defined" errors

## 💡 Tips

1. **Auto-clean:** Script otomatis clean output & Laravel views
2. **Be explicit:** "Create login AND dashboard pages"
3. **Group related pages:** "Auth pages: login, register"
4. **Check drafts individually:** Click each tab
5. **Test routes:** Click all links after generation
6. **Auto-fix:** CSS and routes fixed automatically after generation ✨
7. **Manual fix (if needed):** If auto-fix fails:
   ```bash
   python utils/fix_existing_views.py
   python utils/fix_layout_css.py
   ```
8. **Manual clean:** Use `clean_project.py` untuk control lebih detail

## 🎨 Design Consistency

GenLaravel ensures consistent design across multi-page:

### Automatic Consistency:
- ✅ **Navbar:** Same design, colors, layout on all pages
- ✅ **Footer:** Identical across all pages
- ✅ **Color Scheme:** Consistent primary, secondary, accent colors
- ✅ **Typography:** Same fonts, sizes, weights
- ✅ **Buttons:** Same styles and hover effects
- ✅ **Spacing:** Consistent layout patterns

### How It Works:
1. Draft agent generates pages with **shared design theme**
2. CSS variables ensure **color consistency**
3. Component extraction preserves **shared navbar/footer**
4. Layout CSS applies **global styles**

### Result:
Professional, cohesive multi-page application! 🎨

## ⚙️ Configuration

Same as single page mode - edit `.env`:
```env
CEREBRAS_API_KEY=your_key
MISTRAL_API_KEY=your_key
```

## 🎯 When to Use

**Use Single Page (`main.py`):**
- Simple one-page apps
- Landing pages
- Single forms

**Use Multi Page (`main_multi_page.py`):**
- Complete applications
- Multiple related pages
- Full websites
- Admin panels
- E-commerce sites

## 🔄 Common Workflows

### Workflow 1: Fresh Start (Recommended)
```bash
# 1. Clean everything
python utils/clean_project.py
# Choose: 4 (Everything)

# 2. Generate
python main_multi_page.py
# Prompt: "Create home, about, contact pages"

# 3. Fix routes & CSS
python utils/fix_existing_views.py
python utils/fix_layout_css.py

# 4. Test
cd my-laravel
php artisan serve
```

### Workflow 2: Quick Iteration (Recommended)
```bash
# 1. Generate (auto-cleans & auto-fixes)
python main_multi_page.py
# Prompt: "Create home, about, contact pages"
# ✅ Auto-fixes CSS and routes after generation

# 2. Test
cd my-laravel
php artisan serve
```

## 🛠️ Utility Scripts

### `utils/clean_project.py`
Clean project before generation
```bash
python utils/clean_project.py
```
Options:
- 1: Clean output/ only
- 2: Clean Laravel views only
- 3: Reset routes only
- 4: Clean everything (recommended)

### `utils/fix_existing_views.py`
Fix production issues after generation
```bash
python utils/fix_existing_views.py
```
Fixes:
- Remove draft preview UI
- Convert HTML links to Laravel routes
- Handle missing routes
- Fix route view names (auth.login → login)

### `utils/fix_layout_css.py`
Copy custom CSS from draft to layout
```bash
python utils/fix_layout_css.py
```
Fixes:
- Extract custom CSS from draft HTML
- Update app.blade.php with custom styles
- Preserve design quality

### `utils/fix_routes.py`
Fix route view names only
```bash
python utils/fix_routes.py
```

### `utils/utils_clean.py`
Reusable utility functions (imported by other scripts)

---

**Ready to generate multi-page Laravel apps!** 🚀
