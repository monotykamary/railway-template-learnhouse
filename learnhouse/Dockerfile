FROM ghcr.io/learnhouse/app:1.4.2@sha256:fbb8e10659d0726c8736360d0e63c13bedc398dd3a7a9c13cb312675d5b73380

LABEL org.opencontainers.image.source="https://github.com/monotykamary/railway-template-learnhouse"
LABEL org.opencontainers.image.version="1.4.2-railway.1"
LABEL org.opencontainers.image.licenses="AGPL-3.0"

COPY railway-migrate.py /usr/local/share/railway/learnhouse-migrate.py
COPY railway-entrypoint.sh /usr/local/bin/railway-learnhouse-entrypoint
RUN chmod 0755 /usr/local/bin/railway-learnhouse-entrypoint

ENTRYPOINT ["/usr/local/bin/railway-learnhouse-entrypoint"]
CMD ["sh", "/app/start.sh"]
