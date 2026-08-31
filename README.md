# 📝 Blog API

A RESTful Blog API built using **FastAPI** and **SQLAlchemy**.  
This project provides CRUD operations for blogs along with JWT-based authentication, search, and pagination.

## 🚀 Features

- User authentication using JWT
- Create a blog
- Get all blogs
- Get a blog by ID
- Update a blog
- Delete a blog
- Search blogs by title
- Pagination for blogs
- SQLite database
- SQLAlchemy ORM
- Automatic API documentation with Swagger UI

## 🛠️ Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- JWT (`python-jose`)
- Uvicorn
- Passlib / Bcrypt

## 📂 Project Structure

```text
Blog-API/
│
├── main.py
├── auth.py
├── database.py
├── models.py
├── schemas.py
├── test.db
├── requirements.txt
└── README.md
