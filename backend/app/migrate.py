import asyncio
from pathlib import Path

import aiosqlite

from app.core.config import settings

DB_PATH = settings.database_uri
MIGRATIONS_DIR = Path("migrations")


async def run_migrations() -> None:
    init_script = MIGRATIONS_DIR / "db-init.sql"

    if not init_script.exists():
        return

    async with aiosqlite.connect(DB_PATH) as db:
        sql_commands = init_script.read_text(encoding="utf-8")

        await db.executescript(sql_commands)
        await db.commit()


if __name__ == "__main__":
    asyncio.run(run_migrations())
