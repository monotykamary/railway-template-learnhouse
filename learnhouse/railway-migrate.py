"""Bring the LearnHouse database to this image's Alembic head before the app starts.

LearnHouse only runs ``create_all`` on boot: it creates missing tables and never
alters existing ones, and the image does not run Alembic. A database created by
``create_all`` also carries no ``alembic_version`` row, so a plain
``alembic upgrade heads`` would replay the whole history against it.

Three database states are handled, each of them safe to repeat on every start:

* stamped            -> ``alembic upgrade heads``
* tables, no stamp   -> stamp LEGACY_BASELINE, then ``alembic upgrade heads``
* empty              -> stamp heads; the API then creates the current schema

Run from /app/api with the application environment (see railway-entrypoint.sh).
"""
import os
import sys
import time

from alembic import command
from alembic.config import Config
from alembic.script import ScriptDirectory
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.pool import NullPool

# Last revision that cannot be replayed over a create_all schema: it creates the
# nudge tables unconditionally, and create_all supplies them anyway. Every later
# revision checks for the table, column, or index it adds, so upgrading from
# here repairs a database first created by LearnHouse 1.3.4, 1.3.5, or 1.3.6
# (the releases this template has shipped) whichever of them it last ran.
LEGACY_BASELINE = "b1n2u3d4g5e6"
DB_WAIT_SECONDS = 120


def log(message: str) -> None:
    print(f"[railway-migrate] {message}", flush=True)


def versions(connection) -> list[str]:
    if "alembic_version" not in inspect(connection).get_table_names():
        return []
    return sorted(r[0] for r in connection.execute(text("SELECT version_num FROM alembic_version")))


def main() -> int:
    url = os.environ.get("LEARNHOUSE_SQL_CONNECTION_STRING")
    if not url:
        log("LEARNHOUSE_SQL_CONNECTION_STRING is not set")
        return 1
    # Same normalisation as migrations/env.py: Alembic uses the sync driver.
    engine = create_engine(url.replace("postgresql+asyncpg://", "postgresql://", 1), poolclass=NullPool)

    deadline = time.monotonic() + DB_WAIT_SECONDS
    while True:
        try:
            with engine.connect() as connection:
                current = versions(connection)
                has_schema = "organization" in inspect(connection).get_table_names()
            break
        except OperationalError as error:
            if time.monotonic() > deadline:
                log(f"database not reachable after {DB_WAIT_SECONDS}s: {error.orig}")
                return 1
            time.sleep(3)

    config = Config("alembic.ini")
    heads = sorted(ScriptDirectory.from_config(config).get_heads())
    if current:
        log(f"database is at {', '.join(current)}")
    elif has_schema:
        log(f"existing database has no Alembic revision; stamping baseline {LEGACY_BASELINE}")
        command.stamp(config, LEGACY_BASELINE)
    else:
        log(f"empty database; stamping {', '.join(heads)} for the schema the API creates on start")
        command.stamp(config, "heads")
    command.upgrade(config, "heads")

    with engine.connect() as connection:
        current = versions(connection)
    if current != heads:
        log(f"database is at {', '.join(current) or 'no revision'}, expected {', '.join(heads)}")
        return 1
    log(f"database is at head {', '.join(current)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
