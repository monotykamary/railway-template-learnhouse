# LearnHouse on Railway

A pinned Railway deployment for [LearnHouse](https://github.com/learnhouse/learnhouse), the open-source platform for building learning experiences.

[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/deploy/learnhouse?referralCode=ZqgrJ0)

## What this deploys

- LearnHouse Community Edition `1.3.4`
- PostgreSQL 16 with pgvector `0.8.0`
- Redis `7.2.3`
- A Railway Bucket for uploaded learning content

The LearnHouse application serves its frontend, API, real-time collaboration endpoint, and reverse proxy from one public service. PostgreSQL and Redis stay on Railway private networking. A narrow Redis adapter enables append-only persistence and requires the generated Redis password.

## First login

The template creates the initial administrator from `LEARNHOUSE_INITIAL_ADMIN_EMAIL` and the generated `LEARNHOUSE_INITIAL_ADMIN_PASSWORD`. Read both values from the LearnHouse service variables after deployment and rotate the password after signing in.

## Important limits

- This is the Community/OSS single-tenant edition, not LearnHouse Enterprise.
- Code execution needs an external Judge0 API. A privileged Judge0 stack is intentionally not included.
- AI, outbound email, analytics, and OAuth integrations need their own external credentials.
- LearnHouse recommends at least 2 GB RAM and 4 GB for comfortable use.
- Use Railway backups and the upstream migration procedure instead of the Docker-oriented LearnHouse CLI backup/update commands.
- When adding a custom domain, update all public URL, cookie, CORS, NextAuth, and WebSocket variables together.

## Version pins

See [`versions.env`](versions.env). Every production image is pinned by version and immutable registry digest; no service uses `latest`.

## Updating

1. Back up PostgreSQL and the media Bucket.
2. Review the upstream release and migration notes.
3. Update the application image tag and digest deliberately.
4. Validate admin login, uploads, collaboration WebSockets, migrations, persistence, and logs on a disposable Railway project.

## Upstream and license

- Source: https://github.com/learnhouse/learnhouse
- Release: https://github.com/learnhouse/learnhouse/releases/tag/1.3.4
- Documentation: https://docs.learnhouse.app/self-hosting
- License: AGPL-3.0; see [`LICENSE`](LICENSE) and [`NOTICE`](NOTICE)
