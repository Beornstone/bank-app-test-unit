from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import os
from dotenv import load_dotenv

from routes.user import router as user_router
from routes.webhooks import router as webhooks_router
from routes.carer import router as carer_router
from routes.payments import router as payments_router
from routes.issuing import router as issuing_router

load_dotenv()

app = FastAPI(title="Alma API", version="1.0.0")

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET_KEY", "alma-dev-secret-change-in-prod")
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(webhooks_router)
app.include_router(carer_router)
app.include_router(payments_router)
app.include_router(issuing_router)

@app.get("/")
async def root():
    return {"status": "Alma API is running", "mode": "test"}