# Built-in imports
import os
import sys

sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), "./src")))

# Third-party imports
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Local imports
from base.config import logger
from api.routes import user, account, wallet, pay

load_dotenv(override=True)

# Create FastAPI app at module level
app = FastAPI()

# Configure CORS
origins = [
    f"http://{os.getenv('HOST')}.tiangolo.com",
    f"https://{os.getenv('HOST')}.tiangolo.com",
    f"http://{os.getenv('HOST')}",
    f"http://{os.getenv('HOST')}:{os.getenv('PORT')}",
    "*",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user.router)
app.include_router(account.router)
app.include_router(wallet.router)
app.include_router(pay.router)


if __name__ == "__main__":
    host = os.getenv("HOST")
    port = int(os.getenv("PORT"))
    reload = os.getenv("RELOAD").lower() == "true"

    logger.info(f"Starting FastAPI server at http://{host}:{port} (reload={reload})")
    uvicorn.run(
        "start_restapi:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info",
    )
