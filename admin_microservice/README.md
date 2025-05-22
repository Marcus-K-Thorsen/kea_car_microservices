# admin_microservice

The `admin_microservice` is responsible for managing all employee records within the KEA Cars system. It provides a secure API for users with the admin role to create, view, update, delete, and undelete employee accounts. All operations are strictly limited to employees with administrative privileges, ensuring that only authorized personnel can manage sensitive employee data.

This microservice connects to a dedicated MySQL database (`mysqldb_admin`) that stores comprehensive employee information, including unique IDs, email addresses, hashed passwords, first and last names, roles (admin, manager, or sales person), deletion status, and timestamps for creation and updates. The `admin_microservice` is the only service permitted to read from and write to the employee table in this database, maintaining strict control over data integrity and security.

Whenever employee records are created, updated, deleted, or undeleted, the service publishes corresponding messages to the `admin_exchange` in RabbitMQ (fanout exchange type). These messages use routing keys such as `employee.created`, `employee.updated`, `employee.deleted`, and `employee.undeleted`, allowing other microservices to stay synchronized with changes to employee data.

Additionally, the service securely hashes passwords when new employees are registered or when existing employees update their passwords, ensuring that sensitive credentials are never stored in plain text.

In summary, the `admin_microservice` acts as the central authority for employee management, enforcing access control, data consistency, and secure communication with other parts of the KEA Cars system.

---

## API Overview

The admin_microservice exposes its API on **port 8000**.

Below is an overview of the available endpoints for managing employees (all require admin authorization):

### Employees

<details>
<summary><strong>GET <code>/employees</code></strong> — Retrieve a list of employees</summary>

- **Summary:** Retrieve Employees - Requires authorization token in header.
- **Description:**  
  Retrieves a list of employees from the MySQL Admin database based on the provided query parameters.
  - If no query parameters are provided, returns all active employees.
  - The `limit` query parameter can restrict the number of employees returned.
  - The `deleted` query parameter allows filtering employees based on their deletion status:
    - `None` (default): Only active employees.
    - `True`: Only deleted employees.
    - `False`: Both active and deleted employees.
- **Query Parameters:**
  - `limit` (optional, int): Set a limit for the number of employees returned.
  - `deleted` (optional, bool): Filter for deleted employees.
- **Response:**  
  - Returns a list of `EmployeeReturnResource` objects.

</details>

<details>
<summary><strong>GET <code>/employees/{employee_id}</code></strong> — Retrieve an employee by ID</summary>

- **Summary:** Retrieve an Employee by ID - Requires authorization token in header.
- **Description:**  
  Retrieves an employee by UUID from the MySQL Admin database and returns it as an `EmployeeReturnResource`.
- **Path Parameters:**
  - `employee_id` (UUID): The UUID of the employee to retrieve.
- **Response:**  
  - Returns an `EmployeeReturnResource` object.

</details>

<details>
<summary><strong>POST <code>/employees</code></strong> — Create an employee</summary>

- **Summary:** Create an Employee - Requires authorization token in header.
- **Description:**  
  Creates an employee within the MySQL Admin database by providing a request body `EmployeeCreateResource` and returns it as an `EmployeeReturnResource`.  
  If successful, a message will be sent to the `auth_microservice` and the `employee_microservice` to create that employee in their databases as well.
- **Request Body:**  
  - `EmployeeCreateResource`: The employee data to create.
- **Response:**  
  - Returns the created `EmployeeReturnResource` object.

</details>

<details>
<summary><strong>PUT <code>/employees/{employee_id}</code></strong> — Update an employee</summary>

- **Summary:** Update an Employee - Requires authorization token in header.
- **Description:**  
  Updates an employee within the MySQL Admin database by providing a UUID in the path and a request body `EmployeeUpdateResource`.  
  If successful, a message will be sent to the `auth_microservice` and the `employee_microservice` to update that employee in their databases as well.
- **Path Parameters:**
  - `employee_id` (UUID): The UUID of the employee to update.
- **Request Body:**  
  - `EmployeeUpdateResource`: The updated employee data.
- **Response:**  
  - Returns the updated `EmployeeReturnResource` object.

</details>

<details>
<summary><strong>DELETE <code>/employees/{employee_id}</code></strong> — Delete an employee</summary>

- **Summary:** Delete an Employee - Requires authorization token in header.
- **Description:**  
  Soft-deletes an employee within the MySQL Admin database by providing a UUID in the path.  
  If successful, a message will be sent to the `auth_microservice` and the `employee_microservice` to delete that employee in their databases as well.
- **Path Parameters:**
  - `employee_id` (UUID): The UUID of the employee to delete.
- **Response:**  
  - Returns the deleted `EmployeeReturnResource` object.

</details>

<details>
<summary><strong>PATCH <code>/employees/{employee_id}/undelete</code></strong> — Undelete an employee</summary>

- **Summary:** Undelete an Employee - Requires authorization token in header.
- **Description:**  
  Undeletes (reactivates) an employee within the MySQL Admin database by providing a UUID in the path.  
  If successful, a message will be sent to the `auth_microservice` and the `employee_microservice` to undelete that employee in their databases as well.
- **Path Parameters:**
  - `employee_id` (UUID): The UUID of the employee to undelete.
- **Response:**  
  - Returns the undeleted `EmployeeReturnResource` object.

</details>

All endpoints require a valid authorization token in the header and are accessible only by employees with the `ADMIN` role.
