"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 04/05/2025
"""

import os
import sys

from fastapi.middleware.cors import CORSMiddleware

from aimlpy.api import health_router, recommendation_router, notes_router
from aimlpy.setting import Settings
from aimlpy.util import loggerutil

sys.path.append(os.getcwd())

import uvicorn
import nest_asyncio

nest_asyncio.apply()

from fastapi import FastAPI

logger = loggerutil.get_logger(__name__)
app = FastAPI(
    title="Python AI/ML API",
    description="Demo API",
    version="1.0.0",
    author="Ashok Pant",
    email="ashok@treeleaf.ai",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(health_router.router)
app.include_router(recommendation_router.router, prefix="")
app.include_router(notes_router.router)


if __name__ == "__main__":
    loggerutil.setup_logging()
    logger.info("🚀 Starting API server...")
    logger.info(f"🌐 Docs available at: http://localhost:{Settings.API_PORT}/docs")
    logger.info(f"📘 ReDoc available at: http://localhost:{Settings.API_PORT}/redoc")

    uvicorn.run(
        "aimlpy.main:app",  # ✅ fixed import path
        host="0.0.0.0",
        port=Settings.API_PORT,
        reload=False,
        loop="asyncio",
    )
