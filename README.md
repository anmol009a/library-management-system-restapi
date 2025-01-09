# Library Management System API

This project is a Flask-based REST API for managing books and members in a library. It supports CRUD operations, search functionality, pagination, and token-based authentication without using any third-party libraries.

---
## Table of Contents

- [Features](#features)
- [Setup and Running the Project](#setup-and-running-the-project)
  - [Prerequisites](#prerequisites)
  - [Steps to Run](#steps-to-run)
- [API Endpoints](#api-endpoints)
  - [Authentication](#authentication)
  - [Members](#members)
  - [Books](#books)
- [Design Choices](#design-choices)
- [Assumptions and Limitations](#assumptions-and-limitations)
- [Testing](#testing)
  - [Running Automated Tests](#running-automated-tests)

- [Features](#features)
- [Setup and Running the Project](#setup-and-running-the-project)
  - [Prerequisites](#prerequisites)
  - [Steps to Run](#steps-to-run)
- [API Endpoints](#api-endpoints)
  - [Authentication](#authentication)
  - [Members](#members)
  - [Books](#books)
- [Design Choices](#design-choices)
- [Assumptions and Limitations](#assumptions-and-limitations)
- [Testing](#testing)
  - [Running Automated Tests](#running-automated-tests)

---

## Features

1. **CRUD Operations**:
   - Create, Read, Update, and Delete (CRUD) operations for both books and members.

2. **Search**:
   - Search books by title or author using query parameters.

3. **Pagination**:
   - Paginated listing of books with customizable page size.

4. **Authentication**:
   - Secured with token-based authentication for most operations.

5. **Simple Design**:
   - Self-contained and uses only Python's built-in capabilities and Flask.

---

## Setup and Running the Project

### Prerequisites
- Python 3.11 or higher

### Steps to Run

1. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```

2. **Create Virtual Environment**:
   ```bash
   python venv .venv
   ```

3. **Activate Virtual Environment**:
   ```bash
   # For Unix-based systems
   source .venv/bin/activate

   # For Windows
   .venv\Scripts\activate
   ```

4. **Install Requirements**:
   Use Python's built-in `pip` to install Requirements:
   ```bash
   python -m pip install -r requirements.txt
   ```

5. **Running Tests**
   ```bash
   pytest
   ```

6. **Initialize the Database**:
   ```bash
   flask --app library init-db
   ```

7. **Run the Application**:
   ```bash
   flask --app library run 
   ```

   The server will start on `http://127.0.0.1:5000` by default.

8. **Use the API Endpoints**:
   - You can interact with the API using tools like Postman or `curl`.
   - Refer to the endpoint documentation below for details.

---

## API Endpoints

The API has the following endpoints for different operations:

### Authentication
`/api/auth`
- **Login**: `/login` (POST)
  - Input: `{ "email": "<email>" }`
  - Output: `{ "token": "<auth_token>" }`

- **Register**: `/register` (POST)
  - Input: `{"email": <email>, "name": <name>}`
  - Output: `HTTP 201`

### Books
API Endpoint: `/api/books`

Requires: `Authorization: Bearer <token>`

- **Create Book**: (POST)
  - Input: `{"title":<title>, "author":<author>, "year":<year>}`
  - Output: `HTTP 201`

- **Get Book**: `/<book_id>` (GET)
  - Output: `{"title":<title>, "author":<author>, "year":<year>}`

- **Search Book**: `/<book_field>` (GET)
  - Output: `{
              "books": [
                    {
                      "title":<title>, 
                      "author":<author>, 
                      "year":<year>
                      },
                    ...
              ]
            }`

- **List Book**: (GET)
  - Output: `{
      "books": [
          {
            "title":<title>, 
            "author":<author>, 
            "year":<year>
            },
          ...
      ]
    }`

- **Update Book**: `<book_id>` (PUT)
  - Input: `{"title":<title>, "author":<author>, "year":<year>}`
    - Output: `HTTP 204`

- **Delete Book**: `<book_id>` (DELETE)
  - Output: `HTTP 201`

### Members
API Endpoint: `/api/member`

Requires: `Authorization: Bearer <token>`

- **Get Member**: `/<member_id>` (GET)
  - Output: `{"id":<member_id>, "name": <member_name>, "email":<email>}`

- **List Member**: (GET)
  - Output: `{
      "members": [
          {"id":<member_id>, "name": <member_name>, "email":<email>},
          ...
      ]
    }`

- **Update Member**: `<member_id>` (PUT)
  - Input: `{"name": <member_name>, "email":<email>}`
    - Output: `HTTP 204`

- **Delete Member**: `<member_id>` (DELETE)
  - Output: `HTTP 204`


---

## Design Choices

The following design choices were made during the implementation:

1. **Framework**:
   - The application is built using the Flask framework for simplicity and ease of use.

2. **Authentication**:
   - Token-based authentication using the `pyjwt` library.
   - Tokens are generated and validated using JWT (JSON Web Tokens).

3. **Database**:
   - SQLite is used as the database for simplicity and ease of setup.

4. **Error Handling**:
   - Custom error handling is implemented to provide meaningful error messages to the client.

5. **Pagination**:
   - Basic slicing is used for paginated responses to keep implementation lightweight.

6. **Configuration**:
   - Configuration settings are managed using environment variables and a configuration file.

---

## Assumptions and Limitations

1. **Data Persistence**:
   - The application persist data after a restart. Data is stored in an SQLite database.

2. **Security**:
   - The application uses a simple token-based authentication mechanism. For production use, additional security measures should be implemented.

3. **Scalability**:
   - The application is designed for simplicity and may not scale well for large datasets or high traffic without further optimization.

4. **Testing**:
   - Basic unit tests are provided, but comprehensive testing is recommended for production use.

---

## Testing

1. **Automated Tests**:
   - Test cases include validation of CRUD operations, authentication, search, and pagination.

2. **Manual Testing**:
   - Test with tools like Postman or `curl`.

### Running Automated Tests
```bash
pytest
```