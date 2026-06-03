import logging

import aiosqlite
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api import api_router
from app.core.config import settings

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
)


@app.exception_handler(aiosqlite.Error)
async def aiosqlite_exception_handler(
    request: Request, exc: aiosqlite.Error
) -> JSONResponse:
    logger.exception("Database error occurred")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal database error"},
    )


@app.exception_handler(aiosqlite.IntegrityError)
async def aiosqlite_integrity_exception_handler(
    request: Request, exc: aiosqlite.IntegrityError
) -> JSONResponse:
    logger.warning(f"Database integrity error: {exc}")
    return JSONResponse(
        status_code=400,
        content={"detail": "Database integrity violation"},
    )


if settings.cors_origins:
    # noinspection PyTypeChecker
    app.add_middleware(
        middleware_class=CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get("/api/lab/xml-test", tags=["lab"])
def test_xml_parsing():
    from app.domain.lab_patterns import XMLCampaignAdapter

    adapter = XMLCampaignAdapter()
    return adapter.parse_xml()


app.include_router(api_router, prefix="/api", tags=["api"])

from app.api.ws import ws_router

app.include_router(ws_router)
