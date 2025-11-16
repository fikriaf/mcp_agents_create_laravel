# GenLaravel Frontend

Web interface untuk GenLaravel AI Laravel Generator.

## 📁 Files

### 1. `index.html` - Single Page Mode
Frontend untuk generate single-page Laravel application.

**Features:**
- 10 AI agents pipeline visualization
- Real-time terminal output
- Draft preview and approval workflow
- Statistics tracking
- Unlimited generations

**Usage:**
```bash
open frontend/index.html
```

### 2. `multi-page.html` - Multi-Page Mode
Frontend untuk generate multi-page Laravel application.

**Features:**
- 7 phase pipeline (optimized for multi-page)
- Multiple pages preview
- Daily limit tracker (5 generations/day)
- Page-by-page preview
- Enhanced statistics (pages, components, routes)

**Usage:**
```bash
open frontend/multi-page.html
```

## 🎨 Design System

### Colors

**Single Page Mode:**
- Primary: Slate (700-900)
- Accent: Red (500-600)
- Success: Green (500-600)
- Warning: Yellow (500-600)

**Multi-Page Mode:**
- Primary: Purple (600-700)
- Accent: Purple (500-600)
- Success: Green (500-600)
- Warning: Yellow (500-600)

### Components

1. **Header**
   - Logo and title
   - Mode switcher
   - Daily limit badge (multi-page only)

2. **Input Panel**
   - Prompt textarea
   - Generate button
   - Statistics card
   - Quick actions (single-page)
   - Daily limit info (multi-page)

3. **Output Panel**
   - Progress bar
   - Agent pipeline / Phase tracker
   - Terminal output
   - Pages preview (multi-page only)

4. **Draft Modal**
   - Iframe preview
   - Approve/Revise buttons
   - Close button

## 🔄 Workflow

### Single Page Mode
1. User enters prompt
2. Click "Generate Laravel App"
3. Watch 10 agents execute
4. Review draft in modal
5. Approve or request revision
6. Continue to completion

### Multi-Page Mode
1. User enters multi-page prompt
2. Check daily limit (5/day)
3. Click "Generate Multi-Page App"
4. Watch 7 phases execute
5. Review all pages in modal
6. Approve or request revision
7. Continue to completion

## 💾 Local Storage

### Multi-Page Mode
Stores daily usage count:
```javascript
{
  "date": "Mon Jan 01 2024",
  "count": 3
}
```

Key: `genlaravel_multi_usage`

Resets automatically at midnight.

## 🔌 Backend Integration

Currently uses **simulated data** for demo purposes.

To connect to real backend:

1. Replace `simulateAgentWork()` with WebSocket/SSE connection
2. Update `processAgent()` to handle real agent output
3. Connect `showDraftConfirmation()` to actual draft files
4. Implement real-time progress updates

### WebSocket Example
```javascript
const ws = new WebSocket('ws://localhost:8000/generate');

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    
    if (data.type === 'agent_start') {
        updateAgentStatus(data.agent, 'running');
    } else if (data.type === 'agent_complete') {
        updateAgentStatus(data.agent, 'success', data.duration);
    } else if (data.type === 'output') {
        addTerminalOutput(data.message);
    }
};
```

## 🎬 Quick Actions

Both frontends include Quick Actions for common tasks:

### Single Page Mode
1. **Open Output Folder** - View generated files
2. **Preview Draft** - Open draft.html in modal
3. **Open Laravel** - Launch localhost:8000
4. **View History** - See past generations
5. **Clear Output** - Clean all generated files

### Multi-Page Mode
1. **Open Output Folder** - View all page drafts
2. **Preview All Pages** - Open multi-page draft index
3. **Open Laravel** - Launch localhost:8000
4. **Validate Multi-Page** - Run validation checks
5. **Clear Output** - Clean all generated files

**UI Components:**
- **Toast Notifications** - Slide-in notifications for quick feedback
- **Info Modals** - Detailed information with formatted content
- **No more alerts!** - Modern, non-intrusive UI

**Note:** Some actions require backend integration and will show instructions in beautiful modals instead of alerts.

## 🎯 Future Enhancements

- [ ] Real backend integration (WebSocket/SSE)
- [ ] Actual file system operations
- [ ] User authentication
- [ ] Project history viewer
- [ ] Template library
- [ ] Export/import prompts
- [ ] Dark mode
- [ ] Mobile optimization
- [ ] Collaborative editing
- [ ] AI suggestions
- [ ] Cost tracking

## 📝 Notes

- Both frontends are **standalone HTML files** (no build process)
- Uses **Tailwind CDN** for styling
- Uses **Font Awesome CDN** for icons
- **No dependencies** required
- Works in all modern browsers

## 🐛 Troubleshooting

**Issue: Daily limit not resetting**
- Clear localStorage: `localStorage.removeItem('genlaravel_multi_usage')`

**Issue: Modal not showing**
- Check browser console for errors
- Ensure JavaScript is enabled

**Issue: Styling broken**
- Check internet connection (CDN required)
- Clear browser cache

## 📄 License

Same as main project (see root LICENSE file)
