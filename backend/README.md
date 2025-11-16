# GenLaravel Backend

FastAPI backend server untuk GenLaravel dengan WebSocket support untuk real-time updates.

## 🚀 Quick Start

### Installation

```bash
# Install all dependencies (from project root)
pip install -r requirements.txt
```

### Run Server

```bash
# Development mode
python backend/main.py

# Or with uvicorn directly
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8080
```

Server akan berjalan di: **http://localhost:8080**

## 📡 API Endpoints

### REST API

#### `GET /`
Serve frontend index.html

#### `GET /health`
Health check endpoint
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00"
}
```

#### `GET /api/stats`
Get generation statistics
```json
{
  "total_generations": 15,
  "output_exists": true,
  "laravel_project_exists": true
}
```

#### `POST /api/clear-output`
Clear all generated output
```json
{
  "success": true,
  "message": "Output cleared successfully"
}
```

#### `GET /api/history`
Get generation history (last 10)
```json
{
  "history": [
    {
      "filename": "20240115-143022.json",
      "timestamp": "20240115-143022",
      "prompt": "Create a blog application...",
      "date": "2024-01-15T14:30:22"
    }
  ]
}
```

#### `GET /api/download/laravel`
Download Laravel project as ZIP file
- Returns: ZIP file with filename `genlaravel-project-{timestamp}.zip`
- Excludes: `node_modules`, `vendor`, `.git`, large storage folders
- Status 404 if project doesn't exist

#### `GET /api/download/output`
Download output directory as ZIP file
- Returns: ZIP file with filename `genlaravel-output-{timestamp}.zip`
- Contains: All draft HTML files and generated Blade files
- Status 404 if output doesn't exist

### WebSocket API

#### `WS /ws/generate`
Real-time generation with WebSocket

**Connect:**
```javascript
const ws = new WebSocket('ws://localhost:8080/ws/generate');
```

**Send Request:**
```json
{
  "prompt": "Create a blog application with posts and comments",
  "mode": "single"
}
```

**Receive Messages:**

1. **Start Message**
```json
{
  "type": "start",
  "message": "Starting generation process...",
  "mode": "single"
}
```

2. **Agent Start** (Single Page Mode)
```json
{
  "type": "agent_start",
  "agent_id": "draft-agent",
  "agent_name": "Draft Agent",
  "description": "Generating HTML draft..."
}
```

3. **Agent Complete**
```json
{
  "type": "agent_complete",
  "agent_id": "draft-agent",
  "agent_name": "Draft Agent",
  "duration": 2.5
}
```

4. **Phase Start** (Multi-Page Mode)
```json
{
  "type": "phase_start",
  "phase_id": "draft",
  "phase_name": "Draft Generation",
  "description": "Generating HTML drafts for all pages...",
  "current": 2,
  "total": 7
}
```

5. **Pages Detected** (Multi-Page Mode)
```json
{
  "type": "pages_detected",
  "count": 3,
  "pages": [
    {"name": "home", "description": "Landing page"},
    {"name": "about", "description": "About page"},
    {"name": "contact", "description": "Contact page"}
  ]
}
```

6. **Draft Ready**
```json
{
  "type": "draft_ready",
  "draft_path": "/output/draft.html",
  "message": "Draft generated. Please review."
}
```

**Send Confirmation:**
```json
{
  "action": "approve"
}
```
or
```json
{
  "action": "revise"
}
```

7. **Complete**
```json
{
  "type": "complete",
  "message": "Generation completed successfully!",
  "output_path": "/output/",
  "pages_count": 3
}
```

8. **Error**
```json
{
  "type": "error",
  "message": "Error description"
}
```

## 🏗️ Architecture

```
backend/
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
└── README.md           # This file

Frontend connects via:
- REST API for quick actions
- WebSocket for real-time generation
```

## 🔌 Frontend Integration

### JavaScript Example

```javascript
// Connect to WebSocket
const ws = new WebSocket('ws://localhost:8080/ws/generate');

// Send generation request
ws.onopen = () => {
    ws.send(JSON.stringify({
        prompt: "Create a blog application",
        mode: "single"
    }));
};

// Handle messages
ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    
    switch(data.type) {
        case 'agent_start':
            console.log(`Starting: ${data.agent_name}`);
            break;
        case 'agent_complete':
            console.log(`Completed: ${data.agent_name}`);
            break;
        case 'draft_ready':
            // Show draft preview
            showDraftModal(data.draft_path);
            break;
        case 'complete':
            console.log('Generation complete!');
            break;
        case 'error':
            console.error(data.message);
            break;
    }
};

// Send approval
function approveDraft() {
    ws.send(JSON.stringify({ action: 'approve' }));
}
```

## 🛠️ Development

### Project Structure

```
GenLaravel/
├── backend/
│   ├── main.py          # FastAPI server
│   └── requirements.txt
├── frontend/
│   ├── index.html       # Single page UI
│   └── multi-page.html  # Multi-page UI
├── agents/              # AI agents
├── utils/               # Utilities
└── output/              # Generated files
```

### Adding New Endpoints

```python
@app.get("/api/custom")
async def custom_endpoint():
    return {"message": "Custom endpoint"}
```

### Adding WebSocket Events

```python
await manager.send_message({
    "type": "custom_event",
    "data": "custom data"
}, websocket)
```

## 🔒 Security Notes

- CORS is currently set to allow all origins (`*`) for development
- In production, restrict CORS to specific domains
- Add authentication for sensitive endpoints
- Validate all user inputs
- Rate limit WebSocket connections

## 📝 Environment Variables

Create `.env` file in project root:

```env
# LLM Configuration
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here

# Server Configuration
HOST=0.0.0.0
PORT=8080
DEBUG=True
```

## 🐛 Troubleshooting

**Port already in use:**
```bash
# Change port
uvicorn backend.main:app --port 8081
```

**WebSocket connection failed:**
- Check if server is running
- Verify WebSocket URL (ws:// not http://)
- Check browser console for errors

**Import errors:**
```bash
# Ensure you're in project root
cd /path/to/GenLaravel
python backend/main.py
```

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [WebSocket Guide](https://fastapi.tiangolo.com/advanced/websockets/)
- [Uvicorn Documentation](https://www.uvicorn.org/)
