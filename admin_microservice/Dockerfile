# Use an official Python image as a base
FROM python:3.11-slim AS base

# Install system dependencies
RUN apt-get update \
    && apt-get -y install gcc curl gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_16.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g nodemon \
    && rm -rf /var/lib/apt/lists/*

# DEVELOPMENT
FROM base AS development
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
# copy requirements
COPY poetry.lock pyproject.toml ./

# add venv to path
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install Python packages
RUN poetry install --no-root

# Copy the rest of the application
COPY . .



# Set environment variables
#ENV PYTHONUNBUFFERED=1 \
#    POETRY_VIRTUALENVS_IN_PROJECT=true \
#    POETRY_NO_INTERACTION=1

# Set working directory
#WORKDIR /app

# Install system dependencies, Node.js, npm, nodemon, and Poetry
#RUN apt-get update && apt-get install -y --no-install-recommends \
#    curl \
#    gnupg \
#    && curl -fsSL https://deb.nodesource.com/setup_16.x | bash - \
#    && apt-get install -y nodejs \
#    && npm install -g nodemon \
#    && curl -sSL https://install.python-poetry.org | python3 - \
#    && rm -rf /var/lib/apt/lists/*

# Add Poetry to PATH
#ENV PATH="/root/.local/bin:$PATH"

# Copy only the dependency files first for better caching
#COPY pyproject.toml poetry.lock ./

# Install dependencies
#RUN poetry install --no-root

# Copy the rest of the application
#COPY . .

# Expose the application port
EXPOSE 8000

# Start the application using uvicorn directly
#CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Start the application using nodemon
CMD ["nodemon", "--exec", "poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
