FROM ghcr.io/astral-sh/uv:debian

WORKDIR /app

COPY . . 

RUN uv sync

EXPOSE 8000

CMD ["./bin/start.sh"]
