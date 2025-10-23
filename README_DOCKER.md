# Docker instructions

This repository contains a small Flask website. These instructions show how to build and run it using Docker.

Build the image:

```bash
docker build -t personal-website:latest .
```

Run the container:

```bash
docker run --rm -p 8000:8000 --name personal-website personal-website:latest
```

Or use docker-compose:

```bash
docker compose up --build
```

Notes:
- The container listens on port 8000 by default. You can change this with the `PORT` environment variable.
- `app.py` has been updated to respect `PORT`, `HOST`, and `FLASK_DEBUG` environment variables.
- The Dockerfile installs system libs that help Playwright/Headless browsers run. If you do not need Playwright, you can remove those packages to make the image smaller.
