# Manpower Management System — Backend

A FastAPI backend providing secure REST APIs for managing employees, contracts, customers, work shifts, attendance, and incidents.

The backend uses PostgreSQL, SQLAlchemy ORM, JWT Authentication, and Pydantic validation.

---

## Live API

API

https://manpower-management-app-backend.onrender.com

Swagger Documentation

https://manpower-management-app-backend.onrender.com/docs

Frontend

https://manpower-management-app-frontend.vercel.app/

Frontend Repository

https://github.com/VD400/manpower-management-app-frontend

---

## Features

- FastAPI
- SQLAlchemy ORM
- PostgreSQL
- JWT Authentication
- Password Hashing
- Pydantic Validation
- REST API
- CRUD Operations
- Environment Variables
- Render Deployment

---

## Database Schema

Tables

- Users
- Employees
- Customers
- Contracts
- Shifts
- Attendance
- Incidents

Relationships

```
Employees
    │
Contracts
    │
 Shifts
    │
Attendance

Customers
    │
Contracts

Employees
    │
Incidents
```

---

## REST API

### Authentication

- POST /register
- POST /token

### Employees

- GET
- POST
- PUT
- DELETE

### Customers

- GET
- POST
- PUT
- DELETE

### Contracts

- GET
- POST
- PUT
- DELETE

### Shifts

- GET
- POST
- PUT
- DELETE

### Attendance

- GET
- POST
- PUT
- DELETE

### Incidents

- GET
- POST
- PUT
- DELETE

---

## Technologies

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- JWT
- Pwdlib
- Uvicorn

---

## Running Locally

```bash
git clone https://github.com/VD400/manpower-management-app-backend

pip install -r requirements.txt

uvicorn main:app --reload
```

---

## Environment Variables

```
DATABASE_URL=

SECRET_KEY=

ALGORITHM=

ACCESS_TOKEN_EXPIRE_MINUTES=
```

---

## Skills Demonstrated

- REST API Development
- Backend Architecture
- Authentication & Authorization
- Relational Database Design
- SQLAlchemy ORM
- CRUD APIs
- Deployment
- PostgreSQL
- API Documentation
- Data Validation

---

## API Documentation

Swagger UI

https://manpower-management-app-backend.onrender.com/docs

---

## Author

Vishesh Dubey

GitHub:
https://github.com/VD400
