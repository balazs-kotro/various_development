FROM --platform=linux/amd64 python:3.11.1-slim as builder

RUN apt-get update && apt-get install -y --no-install-recommends gcc g++ libpq-dev

RUN pip install --upgrade pip
RUN pip install numpy

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11.1-slim
RUN apt-get update \
    && apt-get install -y --no-install-recommends jq netcat dnsutils curl git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip


COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin/pytest /usr/local/bin/pytest
## COPY --from=builder /usr/local/lib/bin/mypy /usr/local/lib/bin/mypy
## COPY --from=builder /usr/local/lib/bin/coverage /usr/local/lib/bin/coverage 

WORKDIR /app
ENV PYTHONPATH "/app:/app/backtester"

CMD ["bash"]