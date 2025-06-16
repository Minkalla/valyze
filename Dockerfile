# Stage 1: Build the dependencies
FROM python:3.10-slim as builder

# Set working directory
WORKDIR /app

# Install poetry
RUN pip install poetry

# Copy only the dependency configuration files
COPY poetry.lock pyproject.toml ./

# Install dependencies, but not the project itself
# --no-root prevents installing our local app code in this stage
RUN poetry install --no-root --no-dev


# Stage 2: Create the final production image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy the virtual environment with all dependencies from the builder stage
COPY --from=builder /app/.venv .venv

# Activate the virtual environment for subsequent commands
ENV PATH="/app/.venv/bin:$PATH"

# Copy our application source code into the final image
COPY ./app /app/app

# Command to run the Uvicorn server when the container starts
# Binds to 0.0.0.0 to be accessible from outside the container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
