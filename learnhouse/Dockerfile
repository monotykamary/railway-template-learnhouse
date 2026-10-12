FROM ghcr.io/learnhouse/app:1.4.0@sha256:4b9839320a05a3737bd9bb48f7ef8a38f0933af668b1377ff70393f40d36e574

LABEL org.opencontainers.image.source="https://github.com/monotykamary/railway-template-learnhouse"
LABEL org.opencontainers.image.version="1.4.0-railway.1"
LABEL org.opencontainers.image.licenses="AGPL-3.0"

COPY railway-migrate.py /usr/local/share/railway/learnhouse-migrate.py
COPY railway-entrypoint.sh /usr/local/bin/railway-learnhouse-entrypoint
RUN chmod 0755 /usr/local/bin/railway-learnhouse-entrypoint

ENTRYPOINT ["/usr/local/bin/railway-learnhouse-entrypoint"]
CMD ["sh", "/app/start.sh"]
