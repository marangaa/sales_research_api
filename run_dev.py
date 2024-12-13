import uvicorn
from app.main import app
from app.core.logging import setup_logging

if __name__ == "__main__":
    # Set up logging
    setup_logging()

    # Run the API with hot reload
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["app"],
        log_level="debug"
    )