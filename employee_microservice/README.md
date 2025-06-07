# employee_microservice

The `employee_microservice` is the core service responsible for handling the majority of business logic within the KEA Cars system, carrying over much of the functionality from the original monolithic application. This microservice is designed to be used by all employees, including admins, managers, and sales people.

It provides endpoints for managing and retrieving data related to brands, models, colors, accessories, insurances, customers, cars, and purchases. While all employees can read from the system, only specific roles are permitted to perform certain write operations, such as creating or updating insurances, cars, and customers. Notably, direct modifications to employee records in the `mysqldb_employee` database are only performed by the service when it consumes messages from the `admin_microservice`, ensuring that employee data remains consistent and centrally managed.

The `employee_microservice` acts as both a consumer and producer of messages. It consumes messages from the `admin_exchange` (fanout type) using the `employee_microservice_queue`, processing routing keys like `employee.created`, `employee.updated`, `employee.deleted`, and `employee.undeleted` to keep its employee data synchronized with changes made in the admin service. Additionally, it publishes messages to the `employee_exchange` (direct type) with routing keys such as `insurance.created` and `insurance.updated`, allowing other services to stay updated on changes to insurance data.

The `mysqldb_employee` database connected to this microservice is structured to support a wide range of business operations. It contains tables for employees, customers, cars, brands, models, colors, accessories, insurances, and purchases, as well as the necessary relationships between these entities. This comprehensive schema enables efficient management of all aspects of the car sales process.

---

## API Overview

The employee_microservice exposes its API on **port 8003**.

Below is an overview of the available endpoints for managing business operations (all require authorization):

### Accessories

<details>
<summary><strong>GET <code>/accessories</code></strong> — Retrieve Accessories</summary>

- **Summary:** Retrieve Accessories - Requires authorization token in header.
- **Description:**  
  Retrieves all or a limited amount of Accessories from the MySQL Employee database and returns a list of `AccessoryReturnResource`.
- **Query Parameters:**
  - `limit` (optional, int): Set a limit for the amount of accessories that is returned.
- **Response:**  
  - Returns a list of `AccessoryReturnResource` objects.

</details>

<details>
<summary><strong>GET <code>/accessories/{accessory_id}</code></strong> — Retrieve an Accessory by ID</summary>

- **Summary:** Retrieve an Accessory by ID - Requires authorization token in header.
- **Description:**  
  Retrieves an Accessory by ID from the MySQL Employee database by giving a UUID in the path for the accessory and returns it as an `AccessoryReturnResource`.
- **Path Parameters:**
  - `accessory_id` (UUID): The UUID of the accessory to retrieve.
- **Response:**  
  - Returns an `AccessoryReturnResource` object.

</details>

### Brands

<details>
<summary><strong>GET <code>/brands</code></strong> — Retrieve Brands</summary>

- **Summary:** Retrieve Brands - Requires authorization token in header.
- **Description:**  
  Retrieves all or a limited amount of Brands from the MySQL Employee database and returns a list of `BrandReturnResource`.
- **Query Parameters:**
  - `limit` (optional, int): Set a limit for the amount of brands that is returned.
- **Response:**  
  - Returns a list of `BrandReturnResource` objects.

</details>

<details>
<summary><strong>GET <code>/brands/{brand_id}</code></strong> — Retrieve a Brand by ID</summary>

- **Summary:** Retrieve a Brand by ID - Requires authorization token in header.
- **Description:**  
  Retrieves a Brand by ID from the MySQL Employee database by giving a UUID in the path for the brand and returns it as a `BrandReturnResource`.
- **Path Parameters:**
  - `brand_id` (UUID): The UUID of the brand to retrieve.
- **Response:**  
  - Returns a `BrandReturnResource` object.

</details>

### Cars

<details>
<summary><strong>GET <code>/cars</code></strong> — Retrieve Cars</summary>

- **Summary:** Retrieve Cars - Requires authorization token in header.
- **Description:**  
  Retrieves all or a limited amount of Cars from the MySQL Employee database, potentially filtered by cars belonging to a customer and/or employee, if the cars are purchased and/or are past their purchase deadline, and returns a list of `CarReturnResource`.
  - If the token is from an employee with the role: `SALES_PERSON`, only cars from that employee will be returned.
- **Query Parameters:**
  - `customer_id` (optional, UUID): Filter cars by customer.
  - `employee_id` (optional, UUID): Filter cars by employee.
  - `is_purchased` (optional, bool): Filter by purchase status.
  - `is_past_purchase_deadline` (optional, bool): Filter by purchase deadline status.
  - `limit` (optional, int): Set a limit for the amount of cars returned.
- **Response:**  
  - Returns a list of `CarReturnResource` objects.

</details>

<details>
<summary><strong>GET <code>/cars/{car_id}</code></strong> — Retrieve a Car by ID</summary>

- **Summary:** Retrieve a Car by ID - Requires authorization token in header.
- **Description:**  
  Retrieves a Car by ID from the MySQL Employee database by giving a UUID in the path for the car and returns it as a `CarReturnResource`.
  - The endpoint requires an authorization token in the header and is accessible by all roles.
  - If the token is from an employee with the role: `SALES_PERSON` and the car does not belong to that employee, an error with a specific error code (HTTP_403_FORBIDDEN) will be returned.
- **Path Parameters:**
  - `car_id` (UUID): The UUID of the car to retrieve.
- **Response:**  
  - Returns a `CarReturnResource` object.

</details>

<details>
<summary><strong>POST <code>/cars</code></strong> — Create a Car</summary>

- **Summary:** Create a Car - Requires authorization token in header.
- **Description:**  
  Creates a Car within the MySQL Employee database by giving a request body `CarCreateResource` and returns it as a `CarReturnResource`.
  - If the token is from an employee with the role: `SALES_PERSON`, that employee will be set as the owner.
  - If no employee is given in the request body, the employee that created the car will be set as the owner.
- **Request Body:**  
  - `CarCreateResource`: The car data to create.
- **Response:**  
  - Returns the created `CarReturnResource` object.

</details>

<details>
<summary><strong>DELETE <code>/car/{car_id}</code></strong> — Delete a Car</summary>

- **Summary:** Delete a Car - Requires authorization token in header.
- **Description:**  
  Deletes a Car within the MySQL Employee database by giving a UUID in the path for the car and returns a 204 status code.
  - If the token is from an employee with the role: `SALES_PERSON` and the car is not of that employee, an error with status code HTTP_403_FORBIDDEN will be thrown.
- **Path Parameters:**
  - `car_id` (UUID): The UUID of the car to delete.
- **Query Parameters:**
  - `delete_purchase_too` (bool, default False): Whether to also delete the purchase associated with the car.
- **Response:**  
  - Returns 204 No Content.

</details>

### Colors

<details>
<summary><strong>GET <code>/colors</code></strong> — Retrieve Colors</summary>

- **Summary:** Retrieve Colors - Requires authorization token in header.
- **Description:**  
  Retrieves all or a limited amount of Colors from the MySQL Employee database and returns a list of `ColorReturnResource`.
- **Query Parameters:**
  - `limit` (optional, int): Set a limit for the amount of colors that is returned.
- **Response:**  
  - Returns a list of `ColorReturnResource` objects.

</details>

<details>
<summary><strong>GET <code>/colors/{color_id}</code></strong> — Retrieve a Color by ID</summary>

- **Summary:** Retrieve a Color by ID - Requires authorization token in header.
- **Description:**  
  Retrieves a Color by ID from the MySQL Employee database and returns it as a `ColorReturnResource`.
- **Path Parameters:**
  - `color_id` (UUID): The UUID of the color to retrieve.
- **Response:**  
  - Returns a `ColorReturnResource` object.

</details>

### Customers

<details>
<summary><strong>GET <code>/customers</code></strong> — Retrieve Customers</summary>

- **Summary:** Retrieve Customers - Requires authorization token in header.
- **Description:**  
  Retrieves all or a limited amount of Customers from the MySQL Employee database, potentially filtered by email, and returns a list of `CustomerReturnResource`.
- **Query Parameters:**
  - `email_filter` (optional, str): Filter customers by their email.
  - `limit` (optional, int): Set a limit for the amount of customers that is returned.
- **Response:**  
  - Returns a list of `CustomerReturnResource` objects.

</details>

<details>
<summary><strong>GET <code>/customers/{customer_id}</code></strong> — Retrieve a Customer by ID</summary>

- **Summary:** Retrieve a Customer by ID - Requires authorization token in header.
- **Description:**  
  Retrieves a Customer by ID from the MySQL Employee database and returns it as a `CustomerReturnResource`.
- **Path Parameters:**
  - `customer_id` (UUID): The UUID of the customer to retrieve.
- **Response:**  
  - Returns a `CustomerReturnResource` object.

</details>

<details>
<summary><strong>POST <code>/customers</code></strong> — Create a Customer</summary>

- **Summary:** Create a Customer - Requires authorization token in header.
- **Description:**  
  Creates a Customer within the MySQL Employee database by giving a request body `CustomerCreateResource` and returns it as a `CustomerReturnResource`.
- **Request Body:**  
  - `CustomerCreateResource`: The customer data to create.
- **Response:**  
  - Returns the created `CustomerReturnResource` object.

</details>

<details>
<summary><strong>PUT <code>/customers/{customer_id}</code></strong> — Update a Customer</summary>

- **Summary:** Update a Customer - Requires authorization token in header.
- **Description:**  
  Updates a Customer within the MySQL Employee database by giving a UUID in the path for the customer and a request body `CustomerUpdateResource`, and returns it as a `CustomerReturnResource`.
- **Path Parameters:**
  - `customer_id` (UUID): The UUID of the customer to update.
- **Request Body:**  
  - `CustomerUpdateResource`: The updated customer data.
- **Response:**  
  - Returns the updated `CustomerReturnResource` object.

</details>

<details>
<summary><strong>DELETE <code>/customers/{customer_id}</code></strong> — Delete a Customer</summary>

- **Summary:** Delete a Customer - Requires authorization token in header.
- **Description:**  
  Deletes a Customer within the MySQL Employee database by giving a UUID in the path for the customer and returns a 204 status code.
  - Only accessible by employees with the role: `ADMIN` or `MANAGER`.
- **Path Parameters:**
  - `customer_id` (UUID): The UUID of the customer to delete.
- **Response:**  
  - Returns 204 No Content.

</details>

### Employees

<details>
<summary><strong>GET <code>/employees</code></strong> — Retrieve Employees</summary>

- **Summary:** Retrieve Employees - Requires authorization token in header.
- **Description:**  
  Retrieves a list of employees from the MySQL Employee database based on the provided query parameters.
  - If the token is from an employee with the role: `SALES_PERSON`, a list with only that employee will be returned.
- **Query Parameters:**
  - `limit` (optional, int): Set a limit for the amount of employees that is returned.
  - `deleted` (optional, bool): Filter for deleted employees.
- **Response:**  
  - Returns a list of `EmployeeReturnResource` objects.

</details>

<details>
<summary><strong>GET <code>/employees/{employee_id}</code></strong> — Retrieve an Employee by ID</summary>

- **Summary:** Retrieve an Employee by ID - Requires authorization token in header.
- **Description:**  
  Retrieves an Employee by ID from the MySQL Employee database by giving a UUID in the path for the employee and returns it as an `EmployeeReturnResource`.
  - If the token is from an employee with the role: `SALES_PERSON`, that employee will be returned.
- **Path Parameters:**
  - `employee_id` (UUID): The UUID of the employee to retrieve.
- **Response:**  
  - Returns an `EmployeeReturnResource` object.

</details>

### Insurances

<details>
<summary><strong>GET <code>/insurances</code></strong> — Retrieve Insurances</summary>

- **Summary:** Retrieve Insurances - Requires authorization token in header.
- **Description:**  
  Retrieves all or a limited amount of Insurances from the MySQL Employee database and returns a list of `InsuranceReturnResource`.
- **Query Parameters:**
  - `limit` (optional, int): Set a limit for the amount of insurances that is returned.
- **Response:**  
  - Returns a list of `InsuranceReturnResource` objects.

</details>

<details>
<summary><strong>GET <code>/insurances/{insurance_id}</code></strong> — Retrieve an Insurance by ID</summary>

- **Summary:** Retrieve an Insurance by ID - Requires authorization token in header.
- **Description:**  
  Retrieves an Insurance by ID from the MySQL Employee database by giving a UUID in the path for the insurance and returns it as an `InsuranceReturnResource`.
- **Path Parameters:**
  - `insurance_id` (UUID): The UUID of the insurance to retrieve.
- **Response:**  
  - Returns an `InsuranceReturnResource` object.

</details>

<details>
<summary><strong>POST <code>/insurances</code></strong> — Create an Insurance</summary>

- **Summary:** Create an Insurance - Requires authorization token in header.
- **Description:**  
  Creates an Insurance in the MySQL Employee database and returns it as an `InsuranceReturnResource`.
  - If successful, a message will be sent to the `synch_microservice` to create that insurance in the Customer database as well.
  - Only accessible by employees with the role: `ADMIN` or `MANAGER`.
- **Request Body:**  
  - `InsuranceCreateResource`: The insurance data to create.
- **Response:**  
  - Returns the created `InsuranceReturnResource` object.

</details>

<details>
<summary><strong>PUT <code>/insurances/{insurance_id}</code></strong> — Update an Insurance</summary>

- **Summary:** Update an Insurance - Requires authorization token in header.
- **Description:**  
  Updates an Insurance in the MySQL Employee database and returns it as an `InsuranceReturnResource`.
  - If successful, a message will be sent to the `synch_microservice` to update that insurance in the Customer database as well.
  - Only accessible by employees with the role: `ADMIN` or `MANAGER`.
- **Path Parameters:**
  - `insurance_id` (UUID): The UUID of the insurance to update.
- **Request Body:**  
  - `InsuranceUpdateResource`: The updated insurance data.
- **Response:**  
  - Returns the updated `InsuranceReturnResource` object.

</details>

### Models

<details>
<summary><strong>GET <code>/models</code></strong> — Retrieve Models</summary>

- **Summary:** Retrieve Models - Requires authorization token in header.
- **Description:**  
  Retrieves all or a limited amount of Models from the MySQL Employee database, potentially filtered by models belonging to a brand, and returns a list of `ModelReturnResource`.
- **Query Parameters:**
  - `brand_id` (optional, UUID): The UUID of the brand, to retrieve models belonging to that brand.
  - `limit` (optional, int): Set a limit for the amount of models that is returned.
- **Response:**  
  - Returns a list of `ModelReturnResource` objects.

</details>

<details>
<summary><strong>GET <code>/models/{model_id}</code></strong> — Retrieve a Model by ID</summary>

- **Summary:** Retrieve a Model by ID - Requires authorization token in header.
- **Description:**  
  Retrieves a Model by ID from the MySQL Employee database by giving a UUID in the path for the model and returns it as a `ModelReturnResource`.
- **Path Parameters:**
  - `model_id` (UUID): The UUID of the model to retrieve.
- **Response:**  
  - Returns a `ModelReturnResource` object.

</details>

<details>
<summary><strong>POST <code>/models</code></strong> — Create a Model</summary>

- **Summary:** Create a Model - Requires authorization token in header.
- **Description:**  
  Creates a Model within the MySQL Employee database by accepting form data and an image file. The endpoint validates the image file (must be PNG or JPEG, not exceeding 2MB, and a valid image), uploads it to DigitalOcean Spaces, and saves the resulting image URL along with the model data in the database. The request body should match the structure of `ModelCreateResource`, and the response will be a `ModelReturnResource`.
  - Only accessible by employees with the role: `ADMIN` or `MANAGER`.
- **Form Data:**  
  - `id` (UUID): The UUID of the model to create.
  - `name` (str): The name of the model.
  - `brands_id` (UUID): The UUID of the brand for the model.
  - `price` (float): The price of the model.
  - `color_ids` (List[UUID]): List of UUIDs for the colors available for the model.
  - `model_image` (file): The image file for the model (PNG or JPEG, max 2MB).
- **Response:**  
  - Returns the created `ModelReturnResource` object, including the image URL.

</details>

### Purchases

<details>
<summary><strong>GET <code>/purchases</code></strong> — Retrieve Purchases</summary>

- **Summary:** Retrieve Purchases - Requires authorization token in header.
- **Description:**  
  Retrieves all or a limited amount of Purchases and/or purchases belonging to a specific employee from the MySQL Employee database and returns a list of `PurchaseReturnResource`.
  - If the token is from an employee with the role: `SALES_PERSON`, only purchases from that employee will be returned.
- **Query Parameters:**
  - `employee_id` (optional, UUID): The UUID of the employee to retrieve purchases for.
  - `limit` (optional, int): Set a limit for the amount of purchases that is returned.
- **Response:**  
  - Returns a list of `PurchaseReturnResource` objects.

</details>

<details>
<summary><strong>GET <code>/purchases/{purchase_id}</code></strong> — Retrieve a Purchase by ID</summary>

- **Summary:** Retrieve a Purchase by ID - Requires authorization token in header.
- **Description:**  
  Retrieves a Purchase by ID from the MySQL Employee database by giving a UUID in the path for the purchase and returns it as a `PurchaseReturnResource`.
  - If the token is from an employee with the role:  `SALES_PERSON` and the purchase is not of that employee, an error with status code HTTP_403_FORBIDDEN will be thrown.
- **Path Parameters:**
  - `purchase_id` (UUID): The UUID of the purchase to retrieve.
- **Response:**  
  - Returns a `PurchaseReturnResource` object.

</details>

<details>
<summary><strong>GET <code>/purchases/car/{cars_id}</code></strong> — Retrieve a Purchase by Car ID</summary>

- **Summary:** Retrieve a Purchase by Car ID - Requires authorization token in header.
- **Description:**  
  Retrieves a Purchase by Car ID from the MySQL Employee database by giving a UUID in the path for the car of the purchase and returns it as a `PurchaseReturnResource`.
  - If the token is from an employee with the role: `SALES_PERSON` and the car is not of that employee, an error with status code HTTP_403_FORBIDDEN will be thrown.
- **Path Parameters:**
  - `cars_id` (UUID): The UUID of the car to retrieve the purchase for.
- **Response:**  
  - Returns a `PurchaseReturnResource` object.

</details>

<details>
<summary><strong>POST <code>/purchase</code></strong> — Create a Purchase</summary>

- **Summary:** Create a Purchase - Requires authorization token in header.
- **Description:**  
  Creates a Purchase within the MySQL Employee database by giving a request body `PurchaseCreateResource` and returns it as a `PurchaseReturnResource`.
  - If the token is from an employee with the role: `SALES_PERSON` and the car being purchased is not of that employee, an error with status code HTTP_403_FORBIDDEN will be thrown.
- **Request Body:**  
  - `PurchaseCreateResource`: The purchase data to create.
- **Response:**  
  - Returns the created `PurchaseReturnResource` object.

</details>
