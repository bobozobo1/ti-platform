"""
TI Investigation Platform — FastAPI application entry point.
All routes go through /api/v1/...
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

# Create the FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    # Disable automatic /docs in production for security
    docs_url="/docs" if settings.debug else None,
    redoc_url=None,
)

# Allow the frontend (React) to call the API
# In production, replace with the actual Vercel domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)


# ── Health check ────────────────────────────────────────────────────────────
# Used by Render to verify the service is alive.
# Returns 200 OK with basic info — no secrets, no sensitive data.
@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "service": settings.app_name,
        "version": settings.app_version,
    }


# ── Future routers (added in later waves) ───────────────────────────────────
# from app.api import auth, investigations, iocs
# app.include_router(auth.router,           prefix="/api/v1")
# app.include_router(investigations.router, prefix="/api/v1")
# app.include_router(iocs.router,           prefix="/api/v1")
