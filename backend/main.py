from fastapi import FastAPI, HTTPException
import logging
from fastapi.middleware.cors import CORSMiddleware
from .routes import upload, chat

app = FastAPI(title="AI Chatbot", version="1.0.0")

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(upload.router)
app.include_router(chat.router)

@app.get("/")
async def root():
    # Root message displayed to user
    logging.info("Root endpoint accessed!")
    return {"message": "Welcome to the AI Chatbot API"}

@app.get("/ping")
async def ping():
    logging.info("Ping endpoint accessed!")
    return {"status": "ok", "ping": "pong"}