#!/bin/sh
set -eu

# Migrate first and refuse to start on failure: a newer LearnHouse on an
# unmigrated schema answers health checks while its API queries fail.
(cd /app/api && uv run python /usr/local/share/railway/learnhouse-migrate.py)

exec "$@"
