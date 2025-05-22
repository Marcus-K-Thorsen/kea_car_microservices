# synch_microservice

The `synch_microservice` is a background service dedicated to keeping non-critical data in sync between the employee and customer domains within the KEA Cars system. It does not expose any API endpoints and operates solely as a message consumer.

The `synch_microservice` subscribes to the `employee_exchange` (direct type) via the `synch_microservice_queue`, receiving messages from the `employee_microservice` about changes such as new or updated insurances, brands, models, colors, and accessories. Upon receiving these messages, it updates the `mongodb_customer` database, which is shared with the `customer_microservice`.

This design follows the CQRS (Command Query Responsibility Segregation) pattern, where the `synch_microservice` is the only service allowed to write to the `mongodb_customer` database, while the `customer_microservice` is responsible for reading from it. This ensures that customers always have access to up-to-date, non-sensitive information—such as available brands, models, colors, accessories, and insurances—without exposing any private or critical data related to employees, customers, or purchases.

The `synch_microservice` thus plays a crucial role in maintaining data consistency and security across the system by ensuring that public-facing data is always current and accurate, while internal and sensitive data remains protected.
