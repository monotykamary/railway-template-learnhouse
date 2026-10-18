FROM redis:7.2.16-alpine@sha256:29e8589c3f9ba699b5f7aa4b3c7733c58852a3626439e619aa0ee78de08c6ca0

LABEL org.opencontainers.image.source="https://github.com/monotykamary/railway-template-learnhouse"
LABEL org.opencontainers.image.version="7.2.16-learnhouse.1"
LABEL org.opencontainers.image.licenses="AGPL-3.0"

COPY redis-entrypoint.sh /usr/local/bin/railway-redis-entrypoint
RUN chmod 0755 /usr/local/bin/railway-redis-entrypoint

ENTRYPOINT ["/usr/local/bin/railway-redis-entrypoint"]
