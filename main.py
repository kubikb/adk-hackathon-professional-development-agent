import os

from google.adk.cli.fast_api import get_fast_api_app
import uvicorn

# Call the function to get the FastAPI app instance
app = get_fast_api_app(
    agents_dir=os.path.dirname(os.path.abspath(__file__)),
    allow_origins=["http://localhost", "http://localhost:8080", "*"],
    web=True,
)

if __name__ == "__main__":
    # Use the PORT environment variable provided by Cloud Run, defaulting to 8080
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
