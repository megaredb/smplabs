import asyncio
import logging
from pathlib import Path

import aiosqlite

from app.core.config import settings

DB_PATH = settings.database_uri
MIGRATIONS_DIR = Path("migrations")

logger = logging.getLogger(__name__)


async def run_migrations() -> None:
    init_script = MIGRATIONS_DIR / "db-init.sql"

    if not init_script.exists():
        logger.warning(f"Migration script {init_script} not found.")
        return

    logger.info(f"Running migrations from {init_script}...")
    async with aiosqlite.connect(DB_PATH, timeout=30) as db:
        await db.execute("PRAGMA journal_mode=WAL")
        await db.execute("PRAGMA synchronous=NORMAL")

        sql_commands = init_script.read_text(encoding="utf-8")

        await db.executescript(sql_commands)
        await db.commit()
    logger.info("Migrations completed successfully.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(run_migrations())
