# Deploy and Host LearnHouse on Railway

## About Hosting LearnHouse

LearnHouse is an open-source platform for creating courses and collaborative learning experiences. This template deploys the single-tenant Community edition at stable release `1.3.4`, with durable PostgreSQL, Redis, and S3-compatible media storage.

## Common Use Cases

- Host an internal learning portal
- Build and publish structured courses
- Run collaborative learning activities and boards
- Manage learners, content, and progress from one application

## Dependencies for LearnHouse Hosting

### Deployment Dependencies

The template creates four Railway resources: the public `learnhouse` service, private `postgres` and `redis` services, and an `uploads` Railway Bucket. The database and Redis services use persistent volumes with backup schedules.

### Implementation Details

The LearnHouse service owns the public HTTPS domain and serves the web app, FastAPI API, and `/collab` WebSocket route from one origin. Initial database installation, organization creation, and administrator creation are driven by generated service variables. Find the initial email and generated password in the LearnHouse service variables, sign in, and rotate the password.

Do not change cross-service database, Redis, Bucket, public URL, cookie, or collaboration references independently. A custom domain requires updating the complete public-origin variable set.

This is the Community/OSS single-tenant edition. External credentials are required for AI, email, OAuth, analytics, and Judge0-backed code execution. The stack is not intended for tiny/free-tier memory limits.

### Why Deploy LearnHouse on Railway?

Railway provides a public HTTPS endpoint, private service networking, durable database volumes, managed object storage, backup schedules, and deliberate source/image versioning in one deployable topology.
