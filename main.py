from app.lib.Env import environment
import logging
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import api_router
import sys
from app.lib import JsonSchemas

app = FastAPI()

# Configure CORS for both development and production
origins = [
    "http://localhost:5173",  # Development frontend
    "http://localhost:10000", # Preview frontend
    "https://lyrics-thing-frontend.onrender.com",  # Your production frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API prefix configuration
prefix = ""
if environment == "dev":
    prefix = "/api"
    logger = logging.getLogger("uvicorn")
    logger.warning("Running in development mode")

app.include_router(api_router, prefix=prefix)

if __name__ == "__main__":
    if "--save-json-schemas" in sys.argv:
        JsonSchemas.save_all()
    else:
        uvicorn.run(app="main:app", host="0.0.0.0", reload=True)