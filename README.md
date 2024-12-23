# Module 13 Mini-Project: Advanced E-commerce API
Requirements:

Customer and CustomerAccount: Create the CRUD (Create, Read, Update, Delete) endpoints for managing Customers and their associated CustomerAccounts:
Create Customer: Implement an endpoint to add a new customer to the database.
Read Customer: Develop an endpoint to retrieve customer details based on their unique identifier (ID).
Update Customer: Create an endpoint for updating customer details, allowing modifications to the customer's name, email, and phone number.
Delete Customer: Implement an endpoint to delete a customer from the system based on their ID.
Create CustomerAccount: Develop an endpoint to create a new customer account. This should include fields for a unique username and a secure password. The customerAccount have a customer ID with one-to-one relationship
Read CustomerAccount: Implement an endpoint to retrieve customer account details, including the associated customer's information.
Update CustomerAccount: Create an endpoint for updating customer account information, including the username and password.
Delete CustomerAccount: Develop an endpoint to delete a customer account.
Product Catalog: Create the CRUD (Create, Read, Update, Delete) endpoints for managing Products:
Create Product: Implement an endpoint to add a new product to the e-commerce database. 
Read Product: Develop an endpoint to retrieve product details based on the product's unique identifier (ID). 
Update Product: Create an endpoint for updating product details, allowing modifications to the product name and price.
Delete Product: Implement an endpoint to delete a product from the system based on its unique ID.
List Products: Develop an endpoint to list all available products in the e-commerce platform. Ensure that the list provides essential product information.
Order Processing: Develop the ability to place and retrieve an order.
Place Order: Create an endpoint for customers to place new orders, specifying the products they wish to purchase and providing essential order details. Each order should capture the order date and the associated customer.
Retrieve Order: Implement an endpoint that allows customers to retrieve details of a specific order based on its unique identifier (ID). Provide a clear overview of the order, including the order date and associated products.
Database Integration:
Utilize Flask-SQLAlchemy to integrate a MySQL database into the application.
Design and create the necessary Model to represent customers, orders, products, customer management, and any additional features.
Establish relationships between tables to model the application's core functionality.
Ensure proper database connections and interactions for data storage and retrieval.
Modularization code:
The code must be modularized using a layered architecture. We've used these during this module: Controllers, Models, Routes, Services, Utils, Test. We are open to your own interpretation and experimentation so long as it is organized and well thought out. A single file thousands of line long does not count.
The code must have a configuration file to configure all database connections, cache, etc.
Performance improvement with cache and limit implementation:
Use the cache logic only to get requests using the flask-caching library.
Use flask-limiter to limit request consumption to 100 per day for all endpoints generated.
Implement JWT Security
Use the jwt library and implement a token that has a time limit. Additionally, all endpoints except login should require the JWT.
Customer and CustomerAccount endpoints must have the administrator role to be consumed.
Unit test implementation with unittest:
Implement 3-5 tests. Use the unittest and mock library to be able to consider multiple scenarios.
Document API with Swagger library:
Use the Swagger library to be able to generate project documentation
Generate the swagger.yaml file with the documentation of each of the generated endpoints.

Function: Must run and make sure to look at blueprints to figure out which endpoint does what. just need to put the local address and whatever endpoint you would like to look at!
