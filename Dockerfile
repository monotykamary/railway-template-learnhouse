FROM redis:7.2.3-alpine@sha256:090276da2603db19b154602c374f505d94c10ea57e9749fc3e68e955284bf0fd

LABEL org.opencontainers.image.source="https://github.com/monotykamary/railway-template-learnhouse"
LABEL org.opencontainers.image.version="7.2.3-learnhouse.1"
LABEL org.opencontainers.image.licenses="AGPL-3.0"

COPY redis-entrypoint.sh /usr/local/bin/railway-redis-entrypoint
RUN chmod 0755 /usr/local/bin/railway-redis-entrypoint

ENTRYPOINT ["/usr/local/bin/railway-redis-entrypoint"]
