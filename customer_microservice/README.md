Remember to start a MongoDB database, you can find information about the env values in the .env.example

Remember to create users within the MongoDB by using these commands in mongo shell:
```sh
# Connect to the locally running MongoDB server
mongosh --host localhost --port 27017

# Switch to the admin database and create an admin user
use admin
db.createUser({
  user: "adminUser",
  pwd: "adminPassword",
  roles: [{ role: "root", db: "admin" }]
})

# Authenticate as the admin user
db.auth("adminUser", "adminPassword")

# Switch to the kea_cars_customer_dev database and create a read-only user
use kea_cars_customer_dev
db.createUser({
  user: "readOnlyUser",
  pwd: "readOnlyPassword",
  roles: [{ role: "read", db: "kea_cars_customer_dev" }]
})
```

You can insert initial data in to the database by following this command:
```sh
cd customer_microservice/scripts
poetry shell
poetry run python seed_mongodb.py
```

To start the project use commands:

```sh
cd customer_microservice
poetry shell
poetry run python main.py
```

The customer API will run default on localhost:8002
you can find information about the available endpoints on localhost:8002/docs