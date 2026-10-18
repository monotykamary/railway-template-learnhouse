# LearnHouse on Railway

A pinned Railway deployment for [LearnHouse](https://github.com/learnhouse/learnhouse), the open-source platform for building learning experiences.

[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/deploy/learnhouse?referralCode=ZqgrJ0)

## What this deploys

- LearnHouse Community Edition `1.4.0`
- PostgreSQL 16 with pgvector `0.8.6`
- Redis `7.2.16`
- A Railway Bucket for uploaded learning content

The LearnHouse application serves its frontend, API, real-time collaboration endpoint, and reverse proxy from one public service. PostgreSQL and Redis stay on Railway private networking. A narrow Redis adapter enables append-only persistence and requires the generated Redis password.

The `learnhouse` service is built from [`learnhouse/`](learnhouse/): the pinned upstream image plus a start adapter that brings the database to the image's Alembic head before the application starts. LearnHouse itself only creates missing tables on boot and never alters existing ones, so without this step a newer release runs against an older schema. The `redis` service is built from the repository root.

## First login

The template creates the initial administrator from `LEARNHOUSE_INITIAL_ADMIN_EMAIL` and the generated `LEARNHOUSE_INITIAL_ADMIN_PASSWORD`. Read both values from the LearnHouse service variables after deployment and rotate the password after signing in.

## Important limits

- This is the Community/OSS single-tenant edition, not LearnHouse Enterprise.
- Code execution needs an external Judge0 API. A privileged Judge0 stack is intentionally not included.
- AI, outbound email, analytics, and OAuth integrations need their own external credentials.
- LearnHouse `1.4.0` queues courses for AI-search indexing shortly after start and every three hours. Until an embedding provider key is configured, each pass logs `RAG: indexing failed` errors per course; the application is unaffected. Set `LEARNHOUSE_RAG_BACKFILL_HOURS=0` to turn the pass off.
- LearnHouse recommends at least 2 GB RAM and 4 GB for comfortable use.
- Use Railway backups and the upstream migration procedure instead of the Docker-oriented LearnHouse CLI backup/update commands.
- When adding a custom domain, update all public URL, cookie, CORS, NextAuth, and WebSocket variables together.

## Version pins

See [`versions.env`](versions.env). Every production image is pinned by version and immutable registry digest; no service uses `latest`.

## Updating

1. Back up PostgreSQL and the media Bucket.
2. Review the upstream release and migration notes.
3. Update the application image tag and digest in [`learnhouse/Dockerfile`](learnhouse/Dockerfile) and `versions.env` deliberately.
4. Validate admin login, uploads, collaboration WebSockets, migrations, persistence, and logs on a disposable Railway project.

On every start the adapter logs lines prefixed `[railway-migrate]` and ends with `database is at head <revision>` (`b6e199d023f8` for `1.4.0`). If a migration fails the container exits instead of starting LearnHouse, and Railway keeps the previous deployment active.

### Upgrading a deployment created from LearnHouse `1.3.x`

Deployments created before `1.4.0` run the upstream image directly, and Railway does not update image-sourced services when a template changes. Changing only the image to `ghcr.io/learnhouse/app:1.4.0` starts LearnHouse on an unmigrated schema (for example, `assignmenttask.order` is missing) while the service health check still passes. Back up PostgreSQL, then do one of the following on the `learnhouse` service. Variables, volumes, and the Bucket stay as they are.

- Recommended: in the service settings, replace the Docker image source with this repository (`monotykamary/railway-template-learnhouse`, or your fork of it) and set the root directory to `/learnhouse`. The next deploy migrates the existing database in place, and so does every later version bump.
- To stay on the upstream image: change the image to the `1.4.0` reference in `versions.env`, then run the migration once in the running container (for example through `railway ssh`):

  ```sh
  cd /app/api
  uv run alembic current
  # only when the previous command prints no revision:
  uv run alembic stamp b1n2u3d4g5e6
  uv run alembic upgrade heads
  ```

  Repeat `uv run alembic upgrade heads` after each later image change.

Databases created by this template carry no Alembic revision because LearnHouse built them with `create_all`. `b1n2u3d4g5e6` is the baseline for a database first created by LearnHouse `1.3.4`, `1.3.5`, or `1.3.6`; every later migration checks for the columns it adds, so the same baseline is correct for all three.

## Upstream and license

- Source: https://github.com/learnhouse/learnhouse
- Release: https://github.com/learnhouse/learnhouse/releases/tag/1.4.0
- Documentation: https://docs.learnhouse.app/self-hosting
- License: AGPL-3.0; see [`LICENSE`](LICENSE) and [`NOTICE`](NOTICE)
