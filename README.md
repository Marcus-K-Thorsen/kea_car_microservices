## What you can run

Be in the root of the project while running the commands.

### admin_microservice
- Run the admin endpoints on port 8000:
- ```sh
    poetry run python -m employee_microservice.main
    ```
  - Root endpoint: "/" gives {"Hello": "Admin Service"}
  - Send message endpoint "/send_message/{message}" sends a Trial BaseModel to the fanout exchange: "trial_admin_exchange"
- Start the admin main publisher to send a Trial BaseModel to the fanout exhange: "trial_admin_exchange":
- ```sh
    poetry run python -m admin_microservice.main_publisher
    ```

### auth_microservice
- Run the authentication endpoints on port 8001:
- ```sh
    poetry run python -m auth_microservice.main
    ```
  - Root endpoint: "/" gives {"Hello": "Auth Service"}
- Run the authentication main consumer to consume Trial BaseModels from fanout exchange: "trial_admin_exchange" on queue "trial_queue_auth":
- ```sh
    poetry run python -m auth_microservice.main_consumer
    ```

### customer_microservice
- Run the customer endpoints on port 8002:
- ```sh
    poetry run python -m customer_microservice.main
    ```
  - Root endpoint: "/" gives {"Hello": "Customer Service"}

### employee_microservice
- Run the employee endpoints on port 8003:
- ```sh
    poetry run python -m employee_microservice.main
    ```
  - Root endpoint: "/" gives {"Hello": "Employee Service"}
  - Send message endpoint: "/send_message/{message}" sends a Trial BaseModel to the fanout exchange: "trial_employee_exchange"
- Run the employee main consumer to consume Trial BaseModels from fanout exchange: "trial_admin_exchange" on queue "trial_queue_employee":
- ```sh
    poetry run python -m employee_microservice.main_consumer
    ```

### synch_microservice
- Run the synchronizer main consumer to consume Tiral BaseModels from fanout exchange: "trial_employee_exchange" on queue "trial_queue_synch":
- ```sh
    poetry run python -m synch_microservice.main_consumer
    ```