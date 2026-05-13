FROM python:3.11-slim AS builder

WORKDIR /build
COPY pyproject.toml .
COPY varoascii/ varoascii/
RUN pip install --no-cache-dir --prefix=/install .

FROM python:3.11-slim

COPY --from=builder /install /usr/local
WORKDIR /app

ENTRYPOINT ["python", "-m", "varoascii"]
