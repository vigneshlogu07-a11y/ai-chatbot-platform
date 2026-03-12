"""
LexRam.AI — FastAPI Application Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .database import engine, Base
from .routers import auth_router, chat_router, message_router, upload_router, feedback_router

# Create all tables (if not using schema.sql manually)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="LexRam.AI",
    description="A modern chatbot platform with authentication, streaming, uploads, and feedback.",
    version="1.0.0",
)

# CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth_router.router)
app.include_router(chat_router.router)
app.include_router(message_router.router)
app.include_router(upload_router.router)
app.include_router(feedback_router.router)


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "app": "LexRam.AI", "version": "1.0.0"}
