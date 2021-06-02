# URL Checker

## Overview

The URL Checker is an application designed to allow the user to monitor the status of various HTTP endpoints. The frontend is build in React, and the backend API is built in Python using FastAPI. 

## Features

- Fully asynchronous backend
- OpenAPI compliant API design with interactive documentation provided via SwaggerUI
- SQLAlchemy ORM models
- Pydantic models for API input/output response validation
- APIKey and HTTP Basic authentication
- CRUD operations through React Admin dashboard
- Full-Stack Docker container for ease of deployment


## Getting Started with Docker (fastest method)

1. Clone the GitHub repository to an empty folder on your local machine

	```
    git clone https://github.com/hunter-young/url-checker.git .
    ```
2. Create a dotenv (.env) file for credentials and app configurations in the top level directory of the repository (same as main.py)

	```
    touch .env
    ```  
3. Add the required values to the .env file

	```
    # required environment variables
    ADMIN_EMAIL='dummyuser@acmecorp.com'
	SMTP_SERVER='email-smtp.us-east-1.amazonaws.com'
	SMTP_PORT=465
	SMTP_USERNAME='dummyuser'
	SMTP_PASSWORD='dummypass'
	SENDER_EMAIL='dummyuser@acmecorp.com'
    
    # optional environment variables (default values shown)
    MAX_FAILURES=3
    API_KEY='supersecretkey123'
    ADMIN_USERNAME='admin'
    ADMIN_PASSWORD='admin
    BUILD_DIRECTORY='ui/url-checker/build'
    ```
4. Build the docker container
	
    ```
    docker build -t url-checker:demo .
    ```
5. Run the docker container

	```
    docker run -p 80:80 url-checker:demo
    ```
6. Navigate to <http://localhost> and login with the admin username and password set in the .env file


## Manual Build on Your Local Machine

1. Clone the GitHub repository to an empty folder on your local machine

	```
    git clone https://github.com/hunter-young/url-checker.git .
    ```
2. Create a dotenv (.env) file for credentials and app configurations in the top level directory of the repository (same as main.py)

	```
    touch .env
    ```  
3. Add the required values to the .env file and modify any optional values you desire

	```
    # required environment variables
    ADMIN_EMAIL='dummyuser@acmecorp.com'
	SMTP_SERVER='email-smtp.us-east-1.amazonaws.com'
	SMTP_PORT=465
	SMTP_USERNAME='dummyuser'
	SMTP_PASSWORD='dummypass'
	SENDER_EMAIL='dummyuser@acmecorp.com'
    
    # optional environment variables (default values shown)
    MAX_FAILURES=3
    API_KEY='supersecretkey123'
    ADMIN_USERNAME='admin'
    ADMIN_PASSWORD='admin
    BUILD_DIRECTORY='ui/url-checker/build'
    ```
4. Change the working directory for the React app
	
    ```
    cd ui/url-checker
    ```
5. Install dependencies

	```
    npm install
    ```
6. Build artifacts

	```
    npm run build
    ```
7. Change back to the main directory

	```
    cd ../..
    ```
8. Install Python dependencies

	```
    pip install -r requirements.txt
    ```
9. Run main.py
	
    ```
    python main.py
    ```
10. Navigate to <http://localhost> and login with the admin username and password set in the .env file



