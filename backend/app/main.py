"""
LexRam.AI — FastAPI Application Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import time

from .config import settings
from .database import engine, Base
from .routers import auth_router, chat_router, message_router, upload_router, feedback_router

app = FastAPI(
    title="LexRam.AI",
    description="A modern chatbot platform with authentication, streaming, uploads, and feedback.",
    version="1.0.0",
)

# Run DB creation safely after app starts with retries
@app.on_event("startup")
def startup():
    max_retries = 5
    retry_delay = 5
    for i in range(max_retries):
        try:
            Base.metadata.create_all(bind=engine)
            print("✅ Database connected")
            return
        except Exception as e:
            print(f"⚠️ Database connection attempt {i+1} failed: {e}")
            if i < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("❌ Max retries reached. Database might not be available.")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth_router.router)
app.include_router(chat_router.router)
app.include_router(message_router.router)
app.include_router(upload_router.router)
app.include_router(feedback_router.router)

@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "app": "LexRam.AI", "version": "1.0.0"}
