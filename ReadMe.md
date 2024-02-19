# Grocery List Manager
The application you've described is a list management system that allows users to store and retrieve lists as needed. It's built with FastAPI as the backend framework, which provides a robust and high-performance API layer for your application. The backend is connected to a PostgreSQL database, which is a powerful open-source relational database system known for its reliability and scalability.

In this application, users can create, update, delete, and retrieve lists, which are stored in the PostgreSQL database. FastAPI handles the HTTP requests and responses, ensuring efficient communication between the frontend (client) and the backend (server). Overall, this architecture provides a solid foundation for a reliable and scalable list management application.

## How to start the project

### Setup

#### Python and Virtual Environment

- install Python 3.12.1

- Create a virtual environment 
```

python -m venv myenv

```
- Activate the virtual environment

```

 myenv\Scripts\activate
 
```
- install the required modules

```
pip install -r requirement.txt

```

## Features

- FastAPI (Python 3.12.1)

  - JWT authentication using OAuth2  and PyJWT

- PostgreSQL for the database
- SqlAlchemy for ORM
- Alembic for database migrations