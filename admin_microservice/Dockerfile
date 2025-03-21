# Use an official Python image as a base
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

# Set working directory
WORKDIR /app

# Install system dependencies, Node.js, npm, nodemon, and Poetry
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_16.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g nodemon \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && rm -rf /var/lib/apt/lists/*

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy only the dependency files first for better caching
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry install --no-root

# Copy the rest of the application
COPY . .

# Expose the application port
EXPOSE 8000

# Start the application using uvicorn directly
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Start the application using nodemon
# CMD ["nodemon", "--exec", "poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
