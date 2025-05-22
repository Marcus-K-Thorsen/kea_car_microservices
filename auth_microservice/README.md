# auth_microservice

The `auth_microservice` is responsible for authentication within the KEA Cars system. It issues JSON Web Tokens (JWT) to employees, enabling secure access to protected endpoints in both the `admin_microservice` and `employee_microservice`. When an employee logs in, the service verifies their credentials and generates a JWT if authentication is successful.

This microservice connects to a dedicated MongoDB database (`mongodb_auth`), which stores employee records including emails and hashed passwords. The data structure in this database mirrors that of the admin MySQL database, but with a key difference: deleted employees are fully removed from `mongodb_auth`, ensuring that only active employees can authenticate and receive tokens.

The `auth_microservice` also subscribes to the `admin_exchange` in RabbitMQ, consuming messages via the `auth_microservice_queue`. It listens for events such as employee creation, updates, deletions, and undeletions from the `admin_microservice`, and updates its MongoDB database accordingly to stay synchronized with the latest employee data. While the message consumer can both read from and write to the database, the API endpoints used for authentication only have read access, further enhancing security.

This microservice is the central point for any frontend or client application to obtain a JWT, which is required for accessing secured endpoints across the system. Additionally, the `auth_microservice` is configured for observability: Promtail scrapes its logs and forwards them to Loki, making them available for monitoring and analysis in Grafana. This setup ensures robust authentication, up-to-date employee data, and comprehensive logging for operational visibility.

---

## API Overview

The auth_microservice exposes its API on **port 8001**.

Below is an overview of the available authentication endpoints:

### Login

<details>
<summary><strong>POST <code>/token</code></strong> — Create an Access Token for an Employee</summary>

- **Summary:** Create an Access Token for an Employee.
- **Description:**  
  This endpoint is primarily used by Swagger UI and similar tools to authorize access to protected endpoints. It creates an access token for an employee by accepting form data for the employee's email (`username`) and password (`password`). Upon successful authentication, it returns a JWT token and employee information.
- **Request:**  
  - Form fields:
    - `username` (string): The email of the employee.
    - `password` (string): The password of the employee.
- **Response:**  
  - Returns a `Token` object containing the access token, token type, and employee details.

</details>

<details>
<summary><strong>POST <code>/login</code></strong> — Logs in as an Employee</summary>

- **Summary:** Logs in as an Employee.
- **Description:**  
  This endpoint works similarly to `/token`, but expects a JSON request body instead of form data. It is intended for frontend or client applications to log in and obtain a JWT for accessing protected endpoints. The request body should be an `EmployeeLoginResource` containing the employee's email and password.
- **Request:**  
  - JSON body:
    - `email` (string): The email of the employee.
    - `password` (string): The password of the employee.
- **Response:**  
  - Returns a `Token` object containing the access token, token type, and employee details.

</details>

Both endpoints return a JWT token that must be used to access secured endpoints in other microservices.
