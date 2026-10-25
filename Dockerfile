FROM redis:7.4.11-alpine@sha256:57e4255cc971b1c8d6f8a6ca283ac01bc3ecdd914273ef6bfaede87aaecd6541

LABEL org.opencontainers.image.source="https://github.com/monotykamary/railway-template-learnhouse"
LABEL org.opencontainers.image.version="7.4.11-learnhouse.1"
LABEL org.opencontainers.image.licenses="AGPL-3.0"

COPY redis-entrypoint.sh /usr/local/bin/railway-redis-entrypoint
RUN chmod 0755 /usr/local/bin/railway-redis-entrypoint

ENTRYPOINT ["/usr/local/bin/railway-redis-entrypoint"]
