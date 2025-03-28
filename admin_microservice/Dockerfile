# Use an official Python image as a base
FROM python:3.11-slim AS base

# Install system dependencies
RUN apt-get update \
    && apt-get -y install gcc curl \
    && rm -rf /var/lib/apt/lists/*

# DEVELOPMENT
ENV\
    PIP_NO_CACHE_DIR=off\
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PYTHONDONTWRITEBYTECODE=1 \
    VIRTUAL_ENV=/pybay-venv
ENV\
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_NO_INTERACTION=1 \
    POETRY_VERSION=2.1.1

# install poetry
RUN pip install "poetry==$POETRY_VERSION"

# Set working directory
WORKDIR /app

# copy requirements
COPY poetry.lock pyproject.toml ./

# add venv to path
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install Python packages
RUN poetry install --no-root

# Copy the rest of the application
COPY . .


# Expose the application port
EXPOSE 8000

# Run the application with uvicorn and enable hot-reloading
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
