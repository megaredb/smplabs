import logging
from http import HTTPStatus
from typing import TYPE_CHECKING

import aiosqlite
from fastapi import HTTPException

from app.core.config import settings

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

logger = logging.getLogger(__name__)


async def _setup_connection(connection: aiosqlite.Connection) -> aiosqlite.Connection:
    connection.row_factory = aiosqlite.Row
    await connection.execute("PRAGMA journal_mode=WAL")
    await connection.execute("PRAGMA synchronous=NORMAL")
    await connection.execute("PRAGMA foreign_keys=ON")
    return connection


async def get_db_connection() -> aiosqlite.Connection:
    try:
        connection = await aiosqlite.connect(settings.database_uri, timeout=30)
        return await _setup_connection(connection)
    except aiosqlite.Error as exc:
        log_msg = f"Failed to connect to database: {exc}"
        logger.exception(log_msg)

        raise HTTPException(
            status_code=HTTPStatus.SERVICE_UNAVAILABLE,
            detail="Database connection error. Please try again later.",
        ) from None


async def get_db_connection_with_context() -> AsyncGenerator[aiosqlite.Connection]:
    try:
        async with aiosqlite.connect(settings.database_uri, timeout=30) as connection:
            yield await _setup_connection(connection)
    except aiosqlite.Error as exc:
        log_msg = f"Failed to connect to database: {exc}"
        logger.exception(log_msg)

        raise HTTPException(
            status_code=HTTPStatus.SERVICE_UNAVAILABLE,
            detail="Database connection error. Please try again later.",
        ) from None
