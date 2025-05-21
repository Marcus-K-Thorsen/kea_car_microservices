# KEA Cars Microservices

Welcome to the KEA Cars Microservices project! This repository contains a set of microservices for managing car sales, customers, employees, and authentication for KEA CARS™.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Step 1: Clone the Repository](#step-1-clone-the-repository)
- [Step 2: Create Environment Files](#step-2-create-environment-files)
- [Step 3: Install Poetry (if needed)](#step-3-install-poetry-if-needed)
- [Step 4: Install Dependencies (Optional)](#step-4-install-dependencies-optional)
- [Step 5: Start the Project with Docker Compose](#step-5-start-the-project-with-docker-compose)
- [Step 6: Seed Databases (Optional)](#step-6-seed-databases-optional)
- [Step 7: Running with Kubernetes](#step-7-running-with-kubernetes)
- [Useful Commands](#useful-commands)
- [Documentation](#documentation)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [Poetry](https://python-poetry.org/) (for local development and scripts)
- Python 3.10+ (for local development)

---

## Project Structure

```
.
├── admin_microservice/
├── auth_microservice/
├── customer_microservice/
├── employee_microservice/
├── synch_microservice/
├── init_db/
├── kubernetes/
├── scripts/
├── code_documentation/
├── docker-compose.yaml
├── .env.example
└── README.md
```

---

## Step 1: Clone the Repository

```sh
git clone <your-repo-url>
cd kea_car_microservices
```

---

## Step 2: Create Environment Files

For each microservice and the root folder, copy the `.env.example` file to `.env` and fill in the required values.

```sh
cp .env.example .env
cp admin_microservice/.env.example admin_microservice/.env
cp auth_microservice/.env.example auth_microservice/.env
cp customer_microservice/.env.example customer_microservice/.env
cp employee_microservice/.env.example employee_microservice/.env
```

> **Note:** Edit each `.env` file and provide the necessary environment variables (database credentials, secrets, etc.).

---

## Step 3: Install Poetry (if needed)

If you want to run scripts or services locally (outside Docker), install [Poetry](https://python-poetry.org/docs/#installation):

```sh
pip install poetry
```

---

## Step 4: Install Dependencies (Optional)

If you want to run a microservice locally:

```sh
cd <microservice-folder>
poetry install
```

---

## Step 5: Start the Project with Docker Compose

From the project root:

```sh
docker-compose build
docker-compose up -d
```

- All services will start in the background.
- To stop all services:

```sh
docker-compose down
```

- To remove all containers, images, and volumes:

```sh
docker-compose down --volumes --remove-orphans
```

---

## Step 6: Seed Databases (Optional)

Some services require initial data. For example, to seed the customer MongoDB:

```sh
cd customer_microservice/scripts
poetry shell
poetry run python seed_mongodb.py
```

> See each microservice's `README.md` for specific seeding instructions.

---

## Step 7: Running with Kubernetes

To deploy all services to your Kubernetes cluster:

```sh
kubectl apply -R -f kubernetes/
```

To remove all resources:

```sh
kubectl delete -R -f kubernetes/
```

---

## Useful Commands

- Access API docs for each service (when running):

  - Admin: http://localhost:8001/docs
  - Customer: http://localhost:8002/docs
  - Employee: http://localhost:8003/docs
  - Auth: http://localhost:8004/docs

- Check logs for a service (Docker Compose):

```sh
docker-compose logs <service-name>
```

---

## Documentation

To generate and view code documentation:

```sh
cd code_documentation/docs
poetry run sphinx-apidoc -o source ../../customer_microservice
poetry run make html
```

Open the generated HTML files in `code_documentation/docs/build/html/`.

---

## Troubleshooting

- Ensure all `.env` files are present and correctly configured.
- Make sure Docker and Docker Compose are running.
- For database issues, check connection strings and credentials in your `.env` files.
- For Kubernetes, ensure your context is set to the correct cluster.

---

## License

This project is for educational purposes at KEA and is not intended for production use.

---
