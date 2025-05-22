# customer_microservice

The `customer_microservice` is designed to provide public, read-only access to non-critical data within the KEA Cars system. It connects to a shared MongoDB database (`mongodb_customer`), which is maintained and updated exclusively by the `synch_microservice`. This microservice does not interact with RabbitMQ and does not require any form of authentication or authorization, allowing unauthenticated users—such as potential customers—to freely access its endpoints.

Through its API, the `customer_microservice` enables users to retrieve information about available insurances, accessories, colors, brands, and car models (including filtering models by brand). This allows customers to explore the options offered by the KEA Cars company and make informed decisions before engaging with a salesperson to initiate a purchase.

The `customer_microservice` is strictly limited to reading data; it cannot modify or add any information in the database, ensuring the integrity and security of the underlying data. This approach makes it easy for customers to browse offerings while maintaining a clear separation between public and internal system operations.

---

## API Overview

The customer_microservice exposes its API on **port 8002**.

Below is an overview of the available endpoints for public data access:

### Accessories

<details>
<summary><strong>GET <code>/accessories</code></strong> — Retrieve Accessories</summary>

- **Summary:** Retrieve Accessories.
- **Description:**  
  Retrieves all or a limited amount of Accessories from the Customer database and returns a list of `AccessoryReturnResource`.
- **Query Parameters:**
  - `limit` (optional, int): Set a limit for the amount of accessories that is returned.
- **Response:**  
  - Returns a list of `AccessoryReturnResource` objects.

</details>

<details>
<summary><strong>GET <code>/accessories/{accessory_id}</code></strong> — Retrieve an Accessory by ID</summary>

- **Summary:** Retrieve an Accessory by ID.
- **Description:**  
  Retrieves an Accessory by ID from the Customer database by giving a UUID in the path for the accessory and returns it as an `AccessoryReturnResource`.
- **Path Parameters:**
  - `accessory_id` (UUID): The UUID of the accessory to retrieve.
- **Response:**  
  - Returns an `AccessoryReturnResource` object.

</details>

### Brands

<details>
<summary><strong>GET <code>/brands</code></strong> — Retrieve Brands</summary>

- **Summary:** Retrieve Brands.
- **Description:**  
  Retrieves all or a limited amount of Brands from the Customer database and returns a list of `BrandReturnResource`.
- **Query Parameters:**
  - `limit` (optional, int): Set a limit for the amount of brands that is returned.
- **Response:**  
  - Returns a list of `BrandReturnResource` objects.

</details>

<details>
<summary><strong>GET <code>/brands/{brand_id}</code></strong> — Retrieve a Brand by ID</summary>

- **Summary:** Retrieve a Brand by ID.
- **Description:**  
  Retrieves a Brand by ID from the Customer database by giving a UUID in the path for the brand and returns it as a `BrandReturnResource`.
- **Path Parameters:**
  - `brand_id` (UUID): The UUID of the brand to retrieve.
- **Response:**  
  - Returns a `BrandReturnResource` object.

</details>

### Colors

<details>
<summary><strong>GET <code>/colors</code></strong> — Retrieve Colors</summary>

- **Summary:** Retrieve Colors.
- **Description:**  
  Retrieves all or a limited amount of Colors from the Customer database and returns a list of `ColorReturnResource`.
- **Query Parameters:**
  - `limit` (optional, int): Set a limit for the amount of colors that is returned.
- **Response:**  
  - Returns a list of `ColorReturnResource` objects.

</details>

<details>
<summary><strong>GET <code>/colors/{color_id}</code></strong> — Retrieve a Color by ID</summary>

- **Summary:** Retrieve a Color by ID.
- **Description:**  
  Retrieves a Color by ID from the Customer database by giving a UUID in the path for the color and returns it as a `ColorReturnResource`.
- **Path Parameters:**
  - `color_id` (UUID): The UUID of the color to retrieve.
- **Response:**  
  - Returns a `ColorReturnResource` object.

</details>

### Insurances

<details>
<summary><strong>GET <code>/insurances</code></strong> — Retrieve Insurances</summary>

- **Summary:** Retrieve Insurances.
- **Description:**  
  Retrieves all or a limited amount of Insurances from the Customer database and returns a list of `InsuranceReturnResource`.
- **Query Parameters:**
  - `limit` (optional, int): Set a limit for the amount of insurances that is returned.
- **Response:**  
  - Returns a list of `InsuranceReturnResource` objects.

</details>

<details>
<summary><strong>GET <code>/insurances/{insurance_id}</code></strong> — Retrieve an Insurance by ID</summary>

- **Summary:** Retrieve an Insurance by ID.
- **Description:**  
  Retrieves an Insurance by ID from the Customer database by giving a UUID in the path for the insurance and returns it as an `InsuranceReturnResource`.
- **Path Parameters:**
  - `insurance_id` (UUID): The UUID of the insurance to retrieve.
- **Response:**  
  - Returns an `InsuranceReturnResource` object.

</details>

### Models

<details>
<summary><strong>GET <code>/models</code></strong> — Retrieve Models</summary>

- **Summary:** Retrieve Models.
- **Description:**  
  Retrieves all or a limited amount of Models from the Customer database, potentially filtered by models belonging to a brand, and returns a list of `ModelReturnResource`.
- **Query Parameters:**
  - `brand_id` (optional, UUID): The UUID of the brand, to retrieve models belonging to that brand.
  - `limit` (optional, int): Set a limit for the amount of models that is returned.
- **Response:**  
  - Returns a list of `ModelReturnResource` objects.

</details>

<details>
<summary><strong>GET <code>/models/{model_id}</code></strong> — Retrieve a Model by ID</summary>

- **Summary:** Retrieve a Model by ID.
- **Description:**  
  Retrieves a car Model by ID from the Customer database by giving a UUID in the path for the model and returns it as a `ModelReturnResource`.
- **Path Parameters:**
  - `model_id` (UUID): The UUID of the model to retrieve.
- **Response:**  
  - Returns a `ModelReturnResource` object.

</details>
