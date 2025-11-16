"""
GenLaravel FastAPI Backend
Real-time WebSocket server for AI Laravel generation
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse
import asyncio
import json
import os
import sys
import shutil
import zipfile
import io
from pathlib import Path
from typing import Dict, List
import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration from environment
BACKEND_HOST = os.getenv("BACKEND_HOST", "0.0.0.0")
BACKEND_PORT = int(os.getenv("BACKEND_PORT", "8080"))
LARAVEL_URL = os.getenv("LARAVEL_URL", "http://localhost:8000")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:8080")

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.a_prompt_expander import prompt_expander
from agents.b_draft_agent_v2 import draft_agent_multi
from agents.c_prompt_planner_v2 import plan_prompt_multi
from agents.d_page_architect import design_layout
from agents.e_generate_layout_app import generate_layout_app
from agents.f_ui_generator import generate_blade
from agents.g_route_agent_v2 import generate_routes_multi
from agents.h_component_agent import list_components
from agents.i_validator_agent import validate_with_reason, auto_fix
from agents.j_move_to_project import move_to_laravel_project


def clean_laravel_views():
    """Clean previous generated views from Laravel project"""
    laravel_views = "my-laravel/resources/views"
    
    # Paths to clean
    paths_to_clean = [
        os.path.join(laravel_views, "components"),
        os.path.join(laravel_views, "layouts"),
    ]
    
    # Clean components and layouts
    for path in paths_to_clean:
        if os.path.exists(path):
            shutil.rmtree(path)
            print(f"Cleaned: {path}")
    
    # Clean blade files in views root (except welcome.blade.php)
    if os.path.exists(laravel_views):
        for file in os.listdir(laravel_views):
            if file.endswith('.blade.php') and file != 'welcome.blade.php':
                file_path = os.path.join(laravel_views, file)
                os.remove(file_path)
                print(f"Removed: {file}")
    
    # Reset routes to welcome
    route_file = "my-laravel/routes/web.php"
    default_routes = """<?php

use Illuminate\\Support\\Facades\\Route;

Route::get('/', function () {
    return view('welcome');
});
"""
    with open(route_file, "w", encoding="utf-8") as f:
        f.write(default_routes)
    print(f"Reset routes to welcome")

app = FastAPI(title="GenLaravel API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files with HTML support (auto-serve index.html)
app.mount("/frontend", StaticFiles(directory="frontend", html=True), name="frontend")

# Note: Output directory mounted dynamically in endpoint to avoid startup errors

# Active WebSocket connections
active_connections: List[WebSocket] = []


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.is_generating = False  # 🔒 Flag to prevent concurrent generations

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        
        # 🚫 REJECT if already generating
        if self.is_generating:
            await websocket.send_json({
                "type": "error",
                "message": "⚠️ Generation already in progress! Please wait..."
            })
            await websocket.close()
            print("🚫 Rejected connection: Generation already in progress")
            return False
        
        self.active_connections.append(websocket)
        self.is_generating = True  # 🔒 Lock generation
        print(f"✅ Connection accepted. Active: {len(self.active_connections)}")
        return True

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        self.is_generating = False  # 🔓 Unlock generation
        print(f"🔓 Connection closed. Generation unlocked. Active: {len(self.active_connections)}")

    async def send_message(self, message: dict, websocket: WebSocket):
        await websocket.send_json(message)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)


manager = ConnectionManager()


@app.get("/")
async def root():
    """Redirect to frontend"""
    return FileResponse("frontend/index.html")


@app.get("/output/{file_path:path}")
async def serve_output(file_path: str):
    """Serve output files dynamically"""
    output_file = Path("output") / file_path
    
    if not output_file.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(output_file)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.datetime.now().isoformat()}


@app.get("/api/stats")
async def get_stats():
    """Get generation statistics"""
    history_dir = Path("history")
    output_dir = Path("output")
    
    history_count = len(list(history_dir.glob("*.json"))) if history_dir.exists() else 0
    
    return {
        "total_generations": history_count,
        "output_exists": output_dir.exists(),
        "laravel_project_exists": Path("my-laravel").exists()
    }


@app.post("/api/clear-output")
async def clear_output():
    """Clear output directory"""
    import shutil
    
    try:
        if os.path.exists("output"):
            shutil.rmtree("output")
        
        # Clean Laravel views
        laravel_views = "my-laravel/resources/views"
        paths_to_clean = [
            os.path.join(laravel_views, "components"),
            os.path.join(laravel_views, "layouts"),
        ]
        
        for path in paths_to_clean:
            if os.path.exists(path):
                shutil.rmtree(path)
        
        # Clean blade files
        if os.path.exists(laravel_views):
            for file in os.listdir(laravel_views):
                if file.endswith('.blade.php') and file != 'welcome.blade.php':
                    os.remove(os.path.join(laravel_views, file))
        
        return {"success": True, "message": "Output cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/history")
async def get_history():
    """Get generation history"""
    history_dir = Path("history")
    
    if not history_dir.exists():
        return {"history": []}
    
    history_files = sorted(history_dir.glob("*.json"), reverse=True)
    history = []
    
    for file in history_files[:10]:  # Last 10
        try:
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                history.append({
                    "filename": file.name,
                    "timestamp": file.stem,
                    "prompt": data.get("prompt", "")[:100] + "...",
                    "date": datetime.datetime.strptime(file.stem, "%Y%m%d-%H%M%S").isoformat()
                })
        except:
            continue
    
    return {"history": history}


@app.get("/api/download/laravel")
async def download_laravel_project():
    """Download Laravel project as ZIP"""
    laravel_path = Path("my-laravel")
    
    if not laravel_path.exists():
        raise HTTPException(status_code=404, detail="Laravel project not found")
    
    # Create ZIP in memory
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Walk through Laravel directory
        for root, dirs, files in os.walk(laravel_path):
            # Skip node_modules, vendor, storage (except app), and other large dirs
            dirs[:] = [d for d in dirs if d not in ['node_modules', 'vendor', '.git', 'storage/logs', 'storage/framework']]
            
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, laravel_path.parent)
                zip_file.write(file_path, arcname)
    
    # Seek to beginning of buffer
    zip_buffer.seek(0)
    
    # Generate filename with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"genlaravel-project-{timestamp}.zip"
    
    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )


@app.get("/api/download/output")
async def download_output():
    """Download output directory as ZIP"""
    output_path = Path("output")
    
    if not output_path.exists():
        raise HTTPException(status_code=404, detail="Output directory not found")
    
    # Create ZIP in memory
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(output_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, output_path.parent)
                zip_file.write(file_path, arcname)
    
    zip_buffer.seek(0)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"genlaravel-output-{timestamp}.zip"
    
    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )


@app.websocket("/ws/generate/single")
async def websocket_generate_single(websocket: WebSocket):
    """WebSocket endpoint for SINGLE PAGE generation - follows main_single_page.py"""
    connected = await manager.connect(websocket)
    
    # 🚫 If rejected, stop here
    if not connected:
        return
    
    try:
        # Receive initial prompt
        data = await websocket.receive_json()
        prompt = data.get("prompt", "")
        
        if not prompt:
            await manager.send_message({
                "type": "error",
                "message": "Prompt is required"
            }, websocket)
            return
        
        await manager.send_message({
            "type": "start",
            "message": "Starting single-page generation...",
            "mode": "single"
        }, websocket)
        
        await generate_single_page(websocket, prompt)
        
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("Client disconnected")
    except Exception as e:
        print(f"Error in single page generation: {e}")
        await manager.send_message({
            "type": "error",
            "message": str(e)
        }, websocket)
        manager.disconnect(websocket)


@app.websocket("/ws/generate/multi")
async def websocket_generate_multi(websocket: WebSocket):
    """WebSocket endpoint for MULTI PAGE generation - follows main_multi_page.py"""
    connected = await manager.connect(websocket)
    
    # 🚫 If rejected, stop here
    if not connected:
        return
    
    try:
        # Receive initial prompt
        data = await websocket.receive_json()
        prompt = data.get("prompt", "")
        
        if not prompt:
            await manager.send_message({
                "type": "error",
                "message": "Prompt is required"
            }, websocket)
            return
        
        await manager.send_message({
            "type": "start",
            "message": "Starting multi-page generation...",
            "mode": "multi"
        }, websocket)
        
        await generate_multi_page(websocket, prompt)
        
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("Client disconnected")
    except Exception as e:
        print(f"Error in multi page generation: {e}")
        await manager.send_message({
            "type": "error",
            "message": str(e)
        }, websocket)
        manager.disconnect(websocket)


async def generate_single_page(websocket: WebSocket, prompt: str):
    """
    Generate SINGLE PAGE application
    Follows EXACT flow from main_single_page.py
    """
    
    try:
        # STEP 1: CLEAN OUTPUT AND LARAVEL VIEWS (first_run behavior)
        await manager.send_message({"type": "output", "message": "Cleaning output folder..."}, websocket)
        if os.path.exists("output"):
            shutil.rmtree("output")
        
        await manager.send_message({"type": "output", "message": "Cleaning Laravel views..."}, websocket)
        clean_laravel_views()
        await manager.send_message({"type": "output", "message": "✅ Cleaned successfully"}, websocket)
        
        # STEP 2: PROMPT EXPANDER
        await manager.send_message({"type": "agent_start", "agent_id": "prompt-expander", "agent_name": "Prompt Expander", "description": "Expanding user prompt..."}, websocket)
        from agents.a_prompt_expander import prompt_expander
        preprompt = prompt_expander(prompt)
        await manager.send_message({"type": "agent_complete", "agent_id": "prompt-expander", "agent_name": "Prompt Expander", "duration": 1.0}, websocket)
        
        # STEP 3: DRAFT AGENT (SINGLE PAGE - uses b_draft_agent NOT b_draft_agent_v2)
        await manager.send_message({"type": "agent_start", "agent_id": "draft-agent", "agent_name": "Draft Agent", "description": "Generating HTML draft..."}, websocket)
        from agents.b_draft_agent import draft_agent
        draft_result = draft_agent(preprompt)
        
        # STEP 4: SAVE DRAFT HTML (like CLI does)
        os.makedirs("output", exist_ok=True)
        draft_path = os.path.abspath("output/draft.html")
        with open(draft_path, "w", encoding="utf-8") as f:
            f.write(draft_result["draft"])
        await manager.send_message({"type": "output", "message": f"📁 Draft saved: {draft_path}"}, websocket)
        
        await manager.send_message({"type": "agent_complete", "agent_id": "draft-agent", "agent_name": "Draft Agent", "duration": 2.5}, websocket)
        
        # Send draft for confirmation
        await manager.send_message({
            "type": "draft_ready",
            "draft_path": "/output/draft.html",
            "message": "Draft generated. Please review."
        }, websocket)
        
        print("⏳ Waiting for user confirmation...")
        
        # REVISION LOOP - Allow unlimited revisions
        approved = False
        current_prompt = prompt
        
        while not approved:
            try:
                confirmation = await asyncio.wait_for(
                    websocket.receive_json(),
                    timeout=300.0
                )
                print(f"✅ Received confirmation: {confirmation}")
                
                action = confirmation.get("action")
                
                if action == "approve":
                    print("✅ User approved, continuing generation...")
                    approved = True
                    break
                    
                elif action == "revise":
                    print("User requested revision, waiting for new prompt...")
                    revised_prompt = confirmation.get("revised_prompt", "")
                    
                    if not revised_prompt:
                        await manager.send_message({
                            "type": "error",
                            "message": "No revised prompt provided."
                        }, websocket)
                        continue  # Ask for confirmation again
                    
                    try:
                        # Update current prompt
                        current_prompt = revised_prompt
                        
                        # Regenerate draft with revised prompt
                        print(f"Regenerating with revised prompt: {revised_prompt}")
                        await manager.send_message({
                            "type": "output",
                            "message": "Regenerating draft with your revisions..."
                        }, websocket)
                        
                        # Re-expand prompt first
                        await manager.send_message({"type": "agent_start", "agent_id": "prompt-expander", "agent_name": "Prompt Expander", "description": "Expanding revised prompt..."}, websocket)
                        from agents.a_prompt_expander import prompt_expander
                        preprompt = prompt_expander(revised_prompt)
                        await manager.send_message({"type": "agent_complete", "agent_id": "prompt-expander", "agent_name": "Prompt Expander", "duration": 1.0}, websocket)
                        
                        # Re-run draft agent with expanded prompt
                        await manager.send_message({"type": "agent_start", "agent_id": "draft-agent", "agent_name": "Draft Agent", "description": "Creating revised draft..."}, websocket)
                        from agents.b_draft_agent import draft_agent
                        draft_result = draft_agent(preprompt)
                        await manager.send_message({"type": "agent_complete", "agent_id": "draft-agent", "agent_name": "Draft Agent", "duration": 3.0}, websocket)
                        
                        # Save revised draft
                        with open("output/draft.html", "w", encoding="utf-8") as f:
                            f.write(draft_result['draft'])
                        
                        # Send new draft for approval (loop continues)
                        await manager.send_message({
                            "type": "draft_ready",
                            "draft_path": "/output/draft.html",
                            "message": "Revised draft generated. Please review."
                        }, websocket)
                        
                        print("⏳ Waiting for confirmation on revised draft...")
                        # Loop continues to wait for next confirmation
                        
                    except Exception as e:
                        print(f"❌ Error during revision: {e}")
                        await manager.send_message({
                            "type": "error",
                            "message": f"Failed to regenerate draft: {str(e)}"
                        }, websocket)
                        # Continue loop to ask for confirmation again
                        continue
                    
                else:
                    # Cancel or unknown action
                    print("❌ User cancelled generation")
                    await manager.send_message({
                        "type": "cancelled",
                        "message": "Generation cancelled by user."
                    }, websocket)
                    manager.disconnect(websocket)
                    await websocket.close()
                    return
                    
            except asyncio.TimeoutError:
                print("⏰ Confirmation timeout")
                await manager.send_message({
                    "type": "error",
                    "message": "Confirmation timeout. Please try again."
                }, websocket)
                # 🔓 UNLOCK before return (SINGLE PAGE)
                manager.disconnect(websocket)
                await websocket.close()
                return
        
        # STEP 5: CLEAN LARAVEL VIEWS BEFORE BUILD (after confirmation)
        await manager.send_message({"type": "output", "message": "Cleaning Laravel views before build..."}, websocket)
        clean_laravel_views()
        await manager.send_message({"type": "output", "message": "✅ Laravel views cleaned"}, websocket)
        
        # STEP 6: PROMPT PLANNER (SINGLE - uses c_prompt_planner NOT v2)
        await manager.send_message({"type": "agent_start", "agent_id": "prompt-planner", "agent_name": "Prompt Planner", "description": "Planning components..."}, websocket)
        from agents.c_prompt_planner import plan_prompt
        final_prompt = f"For UI design and materials, follow this draft reference: {draft_result['draft']}"
        plan = plan_prompt(final_prompt)
        await manager.send_message({"type": "agent_complete", "agent_id": "prompt-planner", "agent_name": "Prompt Planner", "duration": 1.5}, websocket)
        
        # STEP 7: PAGE ARCHITECT
        await manager.send_message({"type": "agent_start", "agent_id": "page-architect", "agent_name": "Page Architect", "description": "Designing layout..."}, websocket)
        layout = design_layout(plan)
        await manager.send_message({"type": "agent_complete", "agent_id": "page-architect", "agent_name": "Page Architect", "duration": 2.0}, websocket)
        
        # STEP 8: COMPONENT AGENT
        await manager.send_message({"type": "agent_start", "agent_id": "component-agent", "agent_name": "Component Agent", "description": "Listing components..."}, websocket)
        components = list_components(plan, draft_result['draft'])
        await manager.send_message({"type": "agent_complete", "agent_id": "component-agent", "agent_name": "Component Agent", "duration": 1.5}, websocket)
        
        # STEP 9: UI GENERATOR
        await manager.send_message({"type": "agent_start", "agent_id": "ui-generator", "agent_name": "UI Generator", "description": "Generating Blade views..."}, websocket)
        generate_blade(layout, components)
        await manager.send_message({"type": "agent_complete", "agent_id": "ui-generator", "agent_name": "UI Generator", "duration": 2.5}, websocket)
        
        # STEP 10: LAYOUT GENERATOR
        await manager.send_message({"type": "agent_start", "agent_id": "layout-generator", "agent_name": "Layout Generator", "description": "Creating app layout..."}, websocket)
        generate_layout_app(plan, draft_result['draft'])
        await manager.send_message({"type": "agent_complete", "agent_id": "layout-generator", "agent_name": "Layout Generator", "duration": 1.5}, websocket)
        
        # STEP 11: ROUTE AGENT (SINGLE - uses g_route_agent NOT v2)
        await manager.send_message({"type": "agent_start", "agent_id": "route-agent", "agent_name": "Route Agent", "description": "Generating route..."}, websocket)
        from agents.g_route_agent import generate_route
        generate_route(plan, draft_result['draft'])
        await manager.send_message({"type": "agent_complete", "agent_id": "route-agent", "agent_name": "Route Agent", "duration": 1.0}, websocket)
        
        # STEP 12: VALIDATOR AGENT (EXACT from main_single_page.py)
        await manager.send_message({"type": "agent_start", "agent_id": "validator-agent", "agent_name": "Validator Agent", "description": "Validating components..."}, websocket)
        from agents.i_validator_agent import validate_with_reason, auto_fix
        fixed_components = {}
        all_valid = True
        
        for name, blade_code in components.items():
            is_valid, reason = validate_with_reason(blade_code)
            if is_valid:
                await manager.send_message({"type": "output", "message": f"✅ {name} valid"}, websocket)
                fixed_components[name] = blade_code
            else:
                await manager.send_message({"type": "output", "message": f"❌ {name} - Error: {reason}"}, websocket)
                await manager.send_message({"type": "output", "message": f"Auto-fixing {name}..."}, websocket)
                
                fixed_code = auto_fix(blade_code, reason)
                
                # Validate fixed code
                is_fixed, _ = validate_with_reason(fixed_code)
                if is_fixed:
                    await manager.send_message({"type": "output", "message": f"✅ {name} fixed!"}, websocket)
                    fixed_components[name] = fixed_code
                    
                    # Update output file (EXACT from main_single_page.py)
                    output_path = f"output/components/{name}.blade.php"
                    if os.path.exists(output_path):
                        with open(output_path, "w", encoding="utf-8") as f:
                            f.write(fixed_code)
                else:
                    await manager.send_message({"type": "output", "message": f"❌ {name} fix failed, using original"}, websocket)
                    fixed_components[name] = blade_code
                    all_valid = False
        
        components = fixed_components
        await manager.send_message({"type": "output", "message": "✅ All Components Valid" if all_valid else "⚠️ Some components may have issues"}, websocket)
        await manager.send_message({"type": "agent_complete", "agent_id": "validator-agent", "agent_name": "Validator Agent", "duration": 1.0}, websocket)
        
        # STEP 13: PROJECT MOVER
        await manager.send_message({"type": "agent_start", "agent_id": "project-mover", "agent_name": "Project Mover", "description": "Moving to Laravel project..."}, websocket)
        move_to_laravel_project(layout)
        await manager.send_message({"type": "agent_complete", "agent_id": "project-mover", "agent_name": "Project Mover", "duration": 1.0}, websocket)
        
        # STEP 14: AUTO-FIX UTILITIES (single-page specific - EXACT from main_single_page.py)
        await manager.send_message({"type": "output", "message": "Auto-fixing CSS, routes, and styling (single-page mode)..."}, websocket)
        import sys
        sys.path.insert(0, 'utils')
        try:
            from fix_layout_css import extract_custom_css_from_draft, update_layout_css
            from fix_single_page import fix_component_routes_single_page
            from fix_component_styling import fix_hero_section, fix_all_components
            
            # Fix CSS
            custom_css = extract_custom_css_from_draft()
            if custom_css:
                update_layout_css(custom_css)
                await manager.send_message({"type": "output", "message": "  ✅ Custom CSS applied"}, websocket)
            
            # Fix routes - remove all route() calls for single-page
            await manager.send_message({"type": "output", "message": "  Removing route() calls (single-page)..."}, websocket)
            fix_component_routes_single_page()
            await manager.send_message({"type": "output", "message": "  ✅ Single-page fixes applied"}, websocket)
            
            # Fix component styling
            await manager.send_message({"type": "output", "message": "  Fixing component styling..."}, websocket)
            fix_hero_section()
            fix_all_components()
            await manager.send_message({"type": "output", "message": "  ✅ Styling fixes applied"}, websocket)
            
            # Fix component name mismatches (CRITICAL for single page!)
            await manager.send_message({"type": "output", "message": "  Fixing component names..."}, websocket)
            from fix_component_names import fix_component_includes
            fix_component_includes()
            await manager.send_message({"type": "output", "message": "  ✅ Component names fixed"}, websocket)
            
        except Exception as e:
            await manager.send_message({"type": "output", "message": f"  ⚠️ Auto-fix warning: {e}"}, websocket)
        
        # Send completion with Laravel URL and generation info (for localStorage)
        import datetime
        laravel_url = f"{LARAVEL_URL}{plan['route']}"
        await manager.send_message({"type": "output", "message": ""}, websocket)
        await manager.send_message({"type": "output", "message": "========================================"}, websocket)
        await manager.send_message({"type": "output", "message": f"🌐 Open Link: {laravel_url}"}, websocket)
        await manager.send_message({"type": "output", "message": "========================================"}, websocket)
        await manager.send_message({
            "type": "complete",
            "message": "Generation completed successfully!",
            "output_path": "/output/",
            "laravel_url": laravel_url,
            "route": plan['route'],
            "generation_info": {
                "timestamp": datetime.datetime.now().isoformat(),
                "mode": "single",
                "page": plan['page'],
                "route": plan['route'],
                "laravel_url": laravel_url,
                "components": list(components.keys()),
                "components_count": len(components)
            }
        }, websocket)
        
        # 🔒 CLOSE CONNECTION after completion
        print("✅ Single page generation completed. Closing connection.")
        manager.disconnect(websocket)
        await websocket.close()
        
    except Exception as e:
        print(f"❌ Error in single page generation: {e}")
        await manager.send_message({
            "type": "error",
            "message": f"Generation failed: {str(e)}"
        }, websocket)
        manager.disconnect(websocket)
        await websocket.close()


async def generate_multi_page(websocket: WebSocket, prompt: str):
    """
    Generate MULTI PAGE application
    Follows exact flow from main_multi_page.py
    """
    
    try:
        # STEP 1: CLEAN OUTPUT AND LARAVEL VIEWS
        await manager.send_message({"type": "output", "message": "Cleaning output folder..."}, websocket)
        if os.path.exists("output"):
            shutil.rmtree("output")
        
        await manager.send_message({"type": "output", "message": "Cleaning Laravel views..."}, websocket)
        clean_laravel_views()
        await manager.send_message({"type": "output", "message": "✅ Cleaned successfully"}, websocket)
        
        # STEP 2: PROMPT EXPANDER
        await manager.send_message({"type": "agent_start", "agent_id": "prompt-expander", "agent_name": "Prompt Expander", "description": "Expanding user prompt..."}, websocket)
        from agents.a_prompt_expander import prompt_expander
        preprompt = prompt_expander(prompt)
        await manager.send_message({"type": "agent_complete", "agent_id": "prompt-expander", "agent_name": "Prompt Expander", "duration": 1.0}, websocket)
        
        # STEP 3: DRAFT AGENT (MULTI - uses b_draft_agent_v2)
        await manager.send_message({"type": "agent_start", "agent_id": "draft-agent", "agent_name": "Draft Agent", "description": "Generating HTML drafts for all pages..."}, websocket)
        await manager.send_message({"type": "output", "message": "Analyzing prompt for multiple pages..."}, websocket)
        
        # Use queue for real-time communication between sync agent and async websocket
        import queue
        import threading
        message_queue = queue.Queue()
        
        def draft_callback(data):
            """Sync callback that puts messages in queue"""
            message_queue.put(data)
        
        # Run draft agent in separate thread
        from agents.b_draft_agent_v2 import draft_agent_multi
        draft_result = [None]  # Use list to store result from thread
        
        def run_draft():
            draft_result[0] = draft_agent_multi(preprompt, callback=draft_callback)
            message_queue.put({"type": "done"})  # Signal completion
        
        thread = threading.Thread(target=run_draft)
        thread.start()
        
        # Process messages from queue in real-time
        while True:
            try:
                data = message_queue.get(timeout=0.1)
                
                if data["type"] == "done":
                    break
                elif data["type"] == "pages_detected":
                    await manager.send_message({"type": "output", "message": f"Detected {data['count']} page(s) to generate"}, websocket)
                    await manager.send_message(data, websocket)
                elif data["type"] == "page_draft_start":
                    await manager.send_message({"type": "output", "message": f"Generating draft {data['index']}/{data['total']}: {data['page_name']}..."}, websocket)
                elif data["type"] == "page_draft_complete":
                    await manager.send_message({"type": "output", "message": f"✅ {data['page_name']} draft completed ({data['index']}/{data['total']})"}, websocket)
                    await manager.send_message({"type": "page_draft_complete", "page_name": data['page_name']}, websocket)
            except queue.Empty:
                await asyncio.sleep(0.1)  # Wait a bit and check again
        
        thread.join()  # Wait for thread to complete
        draft_result = draft_result[0]  # Get result from thread
        
        pages_count = len(draft_result.get("pages", []))
        
        await manager.send_message({"type": "output", "message": "✅ Draft generation completed"}, websocket)
        
        # Draft styling and consistency now handled by LLM in draft agent v2
        # Template-based generation ensures navbar/footer consistency from the start
        await manager.send_message({"type": "output", "message": "✅ Draft generation completed"}, websocket)
        
        # Page completion messages already sent via callback during generation
        
        await manager.send_message({"type": "agent_complete", "agent_id": "draft-agent", "agent_name": "Draft Agent", "duration": 2.5}, websocket)
        
        # Send draft for confirmation
        await manager.send_message({
            "type": "draft_ready",
            "draft_path": "/output/draft.html",
            "message": f"Generated {pages_count} pages. Please review."
        }, websocket)
        
        print("⏳ Waiting for user confirmation (multi-page)...")
        
        # REVISION LOOP - Allow unlimited revisions
        approved = False
        current_prompt = prompt
        
        while not approved:
            try:
                confirmation = await asyncio.wait_for(
                    websocket.receive_json(),
                    timeout=300.0
                )
                print(f"✅ Received confirmation: {confirmation}")
                
                action = confirmation.get("action")
                
                if action == "approve":
                    print("✅ User approved, continuing multi-page generation...")
                    approved = True
                    break
                    
                elif action == "revise":
                    print("User requested revision, waiting for new prompt...")
                    revised_prompt = confirmation.get("revised_prompt", "")
                    
                    if not revised_prompt:
                        await manager.send_message({
                            "type": "error",
                            "message": "No revised prompt provided."
                        }, websocket)
                        continue  # Ask for confirmation again
                    
                    try:
                        # Build context from previous draft (like CLI does)
                        prev_draft_info = {
                            "draft_html": draft_result["draft"],
                            "pages": draft_result.get("pages", []),
                            "drafts": draft_result.get("drafts", {})
                        }
                        
                        pages_list = ", ".join([p["name"] for p in prev_draft_info["pages"]])
                        pages_detail = "\n".join([
                            f"  - {p['name']}: {p.get('description', 'page')}"
                            for p in prev_draft_info["pages"]
                        ])
                        
                        # Build revision prompt with context
                        revision_context = f"""
CRITICAL: This is a MULTI-PAGE project with {len(prev_draft_info["pages"])} pages.

EXISTING PAGES (DO NOT CHANGE):
{pages_detail}

You MUST generate these EXACT {len(prev_draft_info["pages"])} pages:
{pages_list}

PREVIOUS DRAFT (for reference):
{prev_draft_info["draft_html"][:2000]}...

USER REVISION REQUEST:
{revised_prompt}

IMPORTANT:
- Keep the SAME {len(prev_draft_info["pages"])} pages structure
- Do NOT merge into single page
- Do NOT add or remove pages
- Only improve based on user feedback
"""
                        
                        current_prompt = revision_context
                        
                        print(f"Regenerating with context: {len(prev_draft_info['pages'])} pages")
                        await manager.send_message({
                            "type": "output",
                            "message": f"Regenerating {len(prev_draft_info['pages'])} pages with your revisions..."
                        }, websocket)
                        
                        # Re-expand prompt with context
                        await manager.send_message({"type": "agent_start", "agent_id": "prompt-expander", "agent_name": "Prompt Expander", "description": "Expanding revised prompt..."}, websocket)
                        from agents.a_prompt_expander import prompt_expander
                        preprompt = prompt_expander(revision_context)
                        await manager.send_message({"type": "agent_complete", "agent_id": "prompt-expander", "agent_name": "Prompt Expander", "duration": 1.0}, websocket)
                        
                        # Re-run draft agent with expanded prompt (with real-time updates)
                        await manager.send_message({"type": "agent_start", "agent_id": "draft-agent", "agent_name": "Draft Agent", "description": "Creating revised multi-page draft..."}, websocket)
                        
                        # Use queue for real-time communication
                        import queue
                        import threading
                        message_queue = queue.Queue()
                        
                        def draft_callback(data):
                            message_queue.put(data)
                        
                        from agents.b_draft_agent_v2 import draft_agent_multi
                        draft_result_container = [None]
                        
                        def run_draft():
                            draft_result_container[0] = draft_agent_multi(preprompt, callback=draft_callback)
                            message_queue.put({"type": "done"})
                        
                        thread = threading.Thread(target=run_draft)
                        thread.start()
                        
                        # Process messages from queue in real-time
                        while True:
                            try:
                                data = message_queue.get(timeout=0.1)
                                
                                if data["type"] == "done":
                                    break
                                elif data["type"] == "pages_detected":
                                    await manager.send_message({"type": "output", "message": f"Detected {data['count']} page(s) to generate"}, websocket)
                                    await manager.send_message(data, websocket)
                                elif data["type"] == "page_draft_start":
                                    await manager.send_message({"type": "output", "message": f"Generating draft {data['index']}/{data['total']}: {data['page_name']}..."}, websocket)
                                elif data["type"] == "page_draft_complete":
                                    await manager.send_message({"type": "output", "message": f"✅ {data['page_name']} draft completed ({data['index']}/{data['total']})"}, websocket)
                                    await manager.send_message({"type": "page_draft_complete", "page_name": data['page_name']}, websocket)
                            except queue.Empty:
                                await asyncio.sleep(0.1)
                        
                        thread.join()
                        draft_result = draft_result_container[0]
                        pages_count = len(draft_result.get("pages", []))
                        await manager.send_message({"type": "agent_complete", "agent_id": "draft-agent", "agent_name": "Draft Agent", "duration": 3.0}, websocket)
                        
                        # Save revised draft
                        with open("output/draft.html", "w", encoding="utf-8") as f:
                            f.write(draft_result['draft'])
                        
                        # Send new draft for approval (loop continues)
                        await manager.send_message({
                            "type": "draft_ready",
                            "draft_path": "/output/draft.html",
                            "message": f"Revised draft with {pages_count} pages. Please review."
                        }, websocket)
                        
                        print("⏳ Waiting for confirmation on revised draft...")
                        # Loop continues to wait for next confirmation
                        
                    except Exception as e:
                        print(f"❌ Error during revision: {e}")
                        await manager.send_message({
                            "type": "error",
                            "message": f"Failed to regenerate draft: {str(e)}"
                        }, websocket)
                        # Continue loop to ask for confirmation again
                        continue
                    
                else:
                    # Cancel or unknown action
                    print("❌ User cancelled generation")
                    await manager.send_message({
                        "type": "cancelled",
                        "message": "Generation cancelled by user."
                    }, websocket)
                    manager.disconnect(websocket)
                    await websocket.close()
                    return
                    
            except asyncio.TimeoutError:
                print("⏰ Confirmation timeout")
                await manager.send_message({
                    "type": "error",
                    "message": "Confirmation timeout. Please try again."
                }, websocket)
                # 🔓 UNLOCK before return (MULTI PAGE)
                manager.disconnect(websocket)
                await websocket.close()
                return
        
        # STEP 4: PROMPT PLANNER (MULTI - uses c_prompt_planner_v2)
        await manager.send_message({"type": "agent_start", "agent_id": "prompt-planner", "agent_name": "Prompt Planner", "description": "Planning components for each page..."}, websocket)
        from agents.c_prompt_planner_v2 import plan_prompt_multi
        multi_plan = plan_prompt_multi(f"For UI design: {draft_result['draft']}")
        pages_from_planner = multi_plan.get("pages", [])
        await manager.send_message({"type": "agent_complete", "agent_id": "prompt-planner", "agent_name": "Prompt Planner", "duration": 1.5}, websocket)
        
        # STEP 5: PAGE ARCHITECT - Loop each page
        await manager.send_message({"type": "agent_start", "agent_id": "page-architect", "agent_name": "Page Architect", "description": "Designing layouts for all pages..."}, websocket)
        all_layouts = []
        all_components = {}
        
        pages_from_draft = draft_result.get("pages", [])
        total_pages = len(pages_from_draft)
        
        for idx, draft_page in enumerate(pages_from_draft):
            page_name = draft_page["name"]
            await manager.send_message({"type": "output", "message": f"🔨 Generating page {idx+1}/{total_pages}: {page_name}"}, websocket)
            
            page_plan = {
                "page": page_name,
                "route": f"/{page_name}",
                "components": pages_from_planner[idx].get("components", []) if idx < len(pages_from_planner) else []
            }
            
            # Design layout for this page
            layout = design_layout(page_plan)
            all_layouts.append(layout)
            
            # Get draft for this page
            page_draft_html = draft_result.get("drafts", {}).get(page_name, draft_result["draft"])
            
            # Generate components
            components = list_components(page_plan, page_draft_html)
            all_components.update(components)
            
            # Generate blade
            generate_blade(layout, components)
            
            await manager.send_message({"type": "output", "message": f"  ✅ {page_name} completed"}, websocket)
        
        await manager.send_message({"type": "agent_complete", "agent_id": "page-architect", "agent_name": "Page Architect", "duration": 2.0}, websocket)
        
        # STEP 6: BLADE GENERATION (already done in loop above)
        await manager.send_message({"type": "agent_start", "agent_id": "blade-generator", "agent_name": "Blade Generator", "description": "Generating shared layout..."}, websocket)
        # Generate shared layout
        generate_layout_app({"page": pages_from_draft[0]["name"], "components": list(all_components.keys())}, draft_result['draft'])
        await manager.send_message({"type": "agent_complete", "agent_id": "blade-generator", "agent_name": "Blade Generator", "duration": 1.0}, websocket)
        
        # STEP 7: ROUTE GENERATION (MULTI - uses g_route_agent_v2)
        await manager.send_message({"type": "agent_start", "agent_id": "route-generator", "agent_name": "Route Generator", "description": "Generating routes for all pages..."}, websocket)
        await manager.send_message({"type": "output", "message": f"Generating routes for {len(pages_from_draft)} pages..."}, websocket)
        
        try:
            from agents.g_route_agent_v2 import generate_routes_multi
            pages_for_routes = [{"page": p["name"], "route": f"/{p['name']}"} for p in pages_from_draft]
            generate_routes_multi(pages_for_routes)
            await manager.send_message({"type": "output", "message": "✅ Routes generated"}, websocket)
        except Exception as e:
            await manager.send_message({"type": "output", "message": f"⚠️ Route generation warning: {e}"}, websocket)
        
        await manager.send_message({"type": "agent_complete", "agent_id": "route-generator", "agent_name": "Route Generator", "duration": 1.0}, websocket)
        
        # Small delay to ensure frontend renders progress
        await asyncio.sleep(0.1)
        
        # STEP 8: VALIDATION & AUTO-FIX (Combined into one agent)
        await manager.send_message({
            "type": "agent_start",
            "agent_id": "validator-fixer",
            "agent_name": "Validator & Auto-Fixer",
            "description": "Validating, fixing, and optimizing..."
        }, websocket)
        from agents.i_validator_agent import validate_with_reason, auto_fix
        
        all_valid = True
        fixed_components = {}
        
        await manager.send_message({"type": "output", "message": "[VALIDATOR AGENT] Validating all components..."}, websocket)
        
        try:
            for name, blade_code in all_components.items():
                try:
                    is_valid, reason = validate_with_reason(blade_code)
                    
                    if is_valid:
                        await manager.send_message({"type": "output", "message": f"✅ {name}"}, websocket)
                        fixed_components[name] = blade_code
                    else:
                        await manager.send_message({"type": "output", "message": f"❌ {name} - Error: {reason}"}, websocket)
                        await manager.send_message({"type": "output", "message": f"Auto-fixing {name}..."}, websocket)
                        
                        fixed_code = auto_fix(blade_code, reason)
                        
                        # Validate fixed code
                        is_fixed, _ = validate_with_reason(fixed_code)
                        if is_fixed:
                            await manager.send_message({"type": "output", "message": f"✅ {name} fixed!"}, websocket)
                            fixed_components[name] = fixed_code
                            
                            # Update output file
                            output_path = f"output/components/{name}.blade.php"
                            if os.path.exists(output_path):
                                with open(output_path, "w", encoding="utf-8") as f:
                                    f.write(fixed_code)
                        else:
                            await manager.send_message({"type": "output", "message": f"❌ {name} fix failed, using original"}, websocket)
                            fixed_components[name] = blade_code
                            all_valid = False
                except Exception as e:
                    await manager.send_message({"type": "output", "message": f"⚠️ Error validating {name}: {e}"}, websocket)
                    fixed_components[name] = blade_code
                    all_valid = False
            
            all_components = fixed_components
            await manager.send_message({"type": "output", "message": "✅ All Components Valid" if all_valid else "⚠️ Some components may have issues"}, websocket)
        except Exception as e:
            await manager.send_message({"type": "output", "message": f"⚠️ Validation error: {e}"}, websocket)
        
        # Move all layouts to project
        for layout in all_layouts:
            move_to_laravel_project(layout)
        
        # Multi-Page Validation (CRITICAL from main_multi_page.py)
        await manager.send_message({"type": "output", "message": "Running multi-page validation..."}, websocket)
        try:
            from utils.multi_page_validator import validate_multi_page_app
            is_valid = validate_multi_page_app("my-laravel")
            if not is_valid:
                await manager.send_message({"type": "output", "message": "⚠️ Validation found issues. Attempting auto-fix..."}, websocket)
            else:
                await manager.send_message({"type": "output", "message": "✅ Multi-page validation passed"}, websocket)
        except Exception as e:
            await manager.send_message({"type": "output", "message": f"⚠️ Validation warning: {e}"}, websocket)
        
        # Continue with auto-fix utilities (same agent)
        await manager.send_message({"type": "output", "message": "\n[AUTO-FIX] Applying optimizations..."}, websocket)
        await manager.send_message({"type": "output", "message": "Auto-fixing CSS, routes, and styling (multi-page mode)..."}, websocket)
        import sys
        sys.path.insert(0, 'utils')
        
        try:
            # Fix nested UI first (critical)
            from fix_nested_ui import fix_nested_ui
            fix_nested_ui()
            await manager.send_message({"type": "output", "message": "  ✅ Nested UI fixed"}, websocket)
            
            from fix_layout_css import extract_custom_css_from_draft, update_layout_css
            from fix_layout_js import extract_javascript_from_drafts, update_layout_js
            from fix_existing_views import fix_component_routes
            from fix_component_styling import fix_hero_section, fix_all_components
            
            # Fix CSS
            custom_css = extract_custom_css_from_draft()
            if custom_css:
                update_layout_css(custom_css)
                await manager.send_message({"type": "output", "message": "  ✅ Custom CSS applied to layout"}, websocket)
            
            # Fix JavaScript
            await manager.send_message({"type": "output", "message": "  Merging JavaScript from all pages..."}, websocket)
            custom_js = extract_javascript_from_drafts()
            if custom_js:
                update_layout_js(custom_js)
                await manager.send_message({"type": "output", "message": "  ✅ JavaScript merged to layout"}, websocket)
            
            # Smart route sync (preserves valid routes)
            await manager.send_message({"type": "output", "message": "  Syncing routes with web.php..."}, websocket)
            from smart_route_sync import sync_navbar_routes
            sync_navbar_routes()
            await manager.send_message({"type": "output", "message": "  ✅ Routes synced"}, websocket)
            
            # Fix component styling
            await manager.send_message({"type": "output", "message": "  Fixing component styling..."}, websocket)
            fix_hero_section()
            fix_all_components()
            await manager.send_message({"type": "output", "message": "  ✅ Styling fixes applied"}, websocket)
            
            # Fix component name mismatches
            await manager.send_message({"type": "output", "message": "  Fixing component names..."}, websocket)
            from fix_component_names import fix_component_includes
            fix_component_includes()
            await manager.send_message({"type": "output", "message": "  ✅ Component names fixed"}, websocket)
            
            # Final structure validation with LLM (part of auto-fixer agent)
            await manager.send_message({"type": "output", "message": "  AI validating structure and styling..."}, websocket)
            
            from agents.k_validator_agent_v2 import validate_all_with_llm
            
            # Run validator in thread with callback
            import queue
            import threading
            validator_queue = queue.Queue()
            
            def validator_sync_callback(message):
                validator_queue.put(message)
            
            validator_result = [None]
            
            def run_validator():
                validator_result[0] = validate_all_with_llm(callback=validator_sync_callback)
                validator_queue.put({"type": "done"})
            
            validator_thread = threading.Thread(target=run_validator)
            validator_thread.start()
            
            # Process validator messages in real-time
            while True:
                try:
                    data = validator_queue.get(timeout=0.1)
                    
                    if isinstance(data, dict) and data.get("type") == "done":
                        break
                    else:
                        # It's a log message
                        await manager.send_message({"type": "output", "message": data}, websocket)
                except queue.Empty:
                    await asyncio.sleep(0.1)
            
            validator_thread.join()
            is_valid = validator_result[0]
            
            if is_valid:
                await manager.send_message({"type": "output", "message": "  ✅ AI validation passed"}, websocket)
            else:
                await manager.send_message({"type": "output", "message": "  ✅ AI validation completed with auto-fixes"}, websocket)
            
        except Exception as e:
            await manager.send_message({"type": "output", "message": f"  ⚠️ Auto-fix warning: {e}"}, websocket)
        
        # Send agent_complete AFTER ALL validation and fixes done
        await manager.send_message({
            "type": "agent_complete",
            "agent_id": "validator-fixer",
            "agent_name": "Validator & Auto-Fixer",
            "duration": 5.0
        }, websocket)
        
        # Prepare generation metadata for frontend (saved in localStorage)
        pages_list = [{"page": p["name"], "route": f"/{p['name']}"} for p in pages_from_draft]
        first_route = pages_list[0]['route'] if pages_list else '/'
        laravel_url = f"{LARAVEL_URL}{first_route}"
        
        # Send completion with Laravel URL (EXACT from main_multi_page.py)
        await manager.send_message({"type": "output", "message": ""}, websocket)
        await manager.send_message({"type": "output", "message": "========================================"}, websocket)
        await manager.send_message({"type": "output", "message": "✅ Multi-page Laravel application generated!"}, websocket)
        await manager.send_message({"type": "output", "message": "========================================"}, websocket)
        await manager.send_message({"type": "output", "message": ""}, websocket)
        await manager.send_message({"type": "output", "message": "📄 Generated Pages:"}, websocket)
        for page in pages_list:
            await manager.send_message({"type": "output", "message": f"  • {page['route']} → {page['page']}.blade.php"}, websocket)
        await manager.send_message({"type": "output", "message": ""}, websocket)
        await manager.send_message({"type": "output", "message": f"🌐 Opening: {laravel_url}"}, websocket)
        
        import datetime
        await manager.send_message({
            "type": "complete",
            "message": f"Multi-page application with {pages_count} pages completed!",
            "output_path": "/output/",
            "pages_count": pages_count,
            "laravel_url": laravel_url,
            "pages": pages_list,
            "generation_info": {
                "timestamp": datetime.datetime.now().isoformat(),
                "mode": "multi",
                "pages_count": pages_count,
                "pages": pages_list,
                "laravel_url": laravel_url,
                "components": list(all_components.keys()),
                "components_count": len(all_components)
            }
        }, websocket)
        
        # 🔒 CLOSE CONNECTION after completion
        print("✅ Multi-page generation completed. Closing connection.")
        manager.disconnect(websocket)
        await websocket.close()
        
    except Exception as e:
        print(f"❌ Error in multi-page generation: {e}")
        await manager.send_message({
            "type": "error",
            "message": f"Generation failed: {str(e)}"
        }, websocket)
        manager.disconnect(websocket)
        await websocket.close()


async def send_agent_start(websocket: WebSocket, agent_info: tuple):
    """Send agent start message"""
    agent_id, agent_name, description = agent_info
    await manager.send_message({
        "type": "agent_start",
        "agent_id": agent_id,
        "agent_name": agent_name,
        "description": description
    }, websocket)


async def send_agent_complete(websocket: WebSocket, agent_info: tuple, duration: float = 0):
    """Send agent complete message"""
    agent_id, agent_name, _ = agent_info
    await manager.send_message({
        "type": "agent_complete",
        "agent_id": agent_id,
        "agent_name": agent_name,
        "duration": duration
    }, websocket)


async def send_phase_start(websocket: WebSocket, phase_info: tuple, current: int, total: int):
    """Send phase start message"""
    phase_id, phase_name, description = phase_info
    await manager.send_message({
        "type": "phase_start",
        "phase_id": phase_id,
        "phase_name": phase_name,
        "description": description,
        "current": current + 1,
        "total": total
    }, websocket)


async def send_phase_complete(websocket: WebSocket, phase_info: tuple, current: int, total: int):
    """Send phase complete message"""
    phase_id, phase_name, _ = phase_info
    await manager.send_message({
        "type": "phase_complete",
        "phase_id": phase_id,
        "phase_name": phase_name,
        "current": current + 1,
        "total": total
    }, websocket)


if __name__ == "__main__":
    import uvicorn
    print(f"🚀 Starting GenLaravel Backend on {BACKEND_HOST}:{BACKEND_PORT}")
    print(f"📍 Laravel URL: {LARAVEL_URL}")
    print(f"🌐 Frontend URL: {FRONTEND_URL}")
    uvicorn.run(app, host=BACKEND_HOST, port=BACKEND_PORT, log_level="info")
