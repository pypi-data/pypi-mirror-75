DOCKERFILE = """
# syntax = docker/dockerfile:1.1.7-experimental
FROM gcr.io/long-state-279014/catacomb-base

# Copy project dependencies
COPY Pipfile* /app/
COPY requirements* /app/

# Install project dependencies
RUN --mount=type=cache,target=/root/.cache /scripts/install_deps.sh

# Copy project files
COPY . /app/

RUN /scripts/run_custom.sh
""".strip()
