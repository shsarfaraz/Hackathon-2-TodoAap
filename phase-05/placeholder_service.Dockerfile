FROM python:3.11-slim

# Install necessary tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Create a simple placeholder service that listens on port 8000
RUN echo '#!/bin/bash' > /placeholder_service.sh && \
    echo 'echo "Starting placeholder service on port 8000..."' >> /placeholder_service.sh && \
    echo 'while true; do' >> /placeholder_service.sh && \
    echo '  echo -e "HTTP/1.1 200 OK\r\n\r\nPlaceholder service running" | nc -l -p 8000' >> /placeholder_service.sh && \
    echo 'done' >> /placeholder_service.sh && \
    chmod +x /placeholder_service.sh

CMD ["/placeholder_service.sh"]