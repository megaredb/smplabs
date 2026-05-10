import logging
from typing import AsyncGenerator

import aiosqlite

from app.core.config import settings

logger = logging.getLogger(__name__)


async def get_db_connection() -> aiosqlite.Connection:
    connection = await aiosqlite.connect(settings.database_uri)
    connection.row_factory = aiosqlite.Row
    return connection


async def get_db_connection_with_context() -> AsyncGenerator[aiosqlite.Connection]:
    async with aiosqlite.connect(settings.database_uri) as connection:
        connection.row_factory = aiosqlite.Row
        yield connection
