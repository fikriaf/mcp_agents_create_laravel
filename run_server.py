"""
GenLaravel Server Runner
Quick script to start the FastAPI backend server
"""

import sys
import os

def main():
    print("="*60)
    print("🚀 GenLaravel Backend Server")
    print("="*60)
    print()
    
    # Check if FastAPI is installed
    try:
        import fastapi
        import uvicorn
        print("✅ FastAPI installed")
    except ImportError:
        print("❌ FastAPI not installed!")
        print()
        print("Please install dependencies:")
        print("  pip install -r backend/requirements.txt")
        print()
        return 1
    
    # Check if .env exists
    if not os.path.exists(".env"):
        print("⚠️  Warning: .env file not found")
        print("   Create .env with your API keys")
        print()
    
    print("📡 Starting server...")
    print("   URL: http://localhost:8080")
    print("   WebSocket: ws://localhost:8080/ws/generate")
    print()
    print("Press Ctrl+C to stop")
    print("="*60)
    print()
    
    # Run server
    try:
        uvicorn.run(
            "backend.main:app",
            host="0.0.0.0",
            port=8080,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped")
        return 0
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
