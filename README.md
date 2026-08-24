# Python FastAPI RESTful API Boilerplate

A modern, scalable, and production-ready **FastAPI** backend boilerplate designed specifically for timed technical coding interviews. It features automatic interactive documentation, type-safe request validation, pre-configured testing suites, global error handling, and flexible database integration.

---

## 🚀 Key Features

* **Framework**: FastAPI (built on ASGI standard, high performance).
* **ORM & Database**: SQLAlchemy configured with a fallback to SQLite. Running the app/tests requires zero external database installation, but PostgreSQL or MySQL can be attached instantly via `.env`.
* **Testing Suite**: Out-of-the-box integration testing setup with `pytest` and `FastAPI.testclient`.
* **Validation**: Request/Response models using `pydantic`.
* **Error Handling**: Global exception interception delivering consistent JSON error response schemas.
* **Auto-generated Documentation**: Swagger interactive documentation available automatically at `/docs`.

---

## 📁 Folder Structure

```text
backend-interview/
│
├── src/
│   ├── config/
│   │   └── db.py            # Database connections, SessionLocal engine & declarative Base
│   │
│   ├── controllers/
│   │   └── health.py        # Controller logic (orchestrating database queries & business logic)
│   │
│   ├── models/
│   │   └── .gitkeep         # Database ORM models defined here
│   │
│   ├── routes/
│   │   └── index.py         # Main routes router mapping paths to controllers
│   │
│   ├── services/
│   │   └── .gitkeep         # Business logic separate from controllers
│   │
│   ├── middleware/
│   │   ├── error_handler.py # Custom global exception handlers (Validation, HTTP, and 500s)
│   │   └── not_found.py     # 404 handler fallback route
│   │
│   ├── utils/
│   │   └── .gitkeep         # Helpers & common utility functions
│   │
│   ├── app.py               # Application factory setup (cors, middlewares, routes mounting)
│   └── main.py              # Server entry point (launches Uvicorn and initiates DB schema creation)
│
├── tests/
│   ├── conftest.py          # Pytest fixtures: setup/teardown in-memory test database & TestClient
│   └── test_health.py       # Integration tests checking health and route responses
│
├── .env.example             # Template for configuration environment variables
├── .gitignore               # Standard python gitignore parameters
├── requirements.txt         # Core dependencies
└── README.md                # This manual
```

---

## ⚙️ Quick Start Setup

### Prerequisites

Ensure you have **Python 3.8 or higher** installed.

### 1. Create a Virtual Environment

Open your terminal in the project directory and create a virtual environment:

```bash
# Windows
python -m venv venv

# macOS / Linux
python3 -m venv venv
```

### 2. Activate the Virtual Environment

```bash
# Windows (Command Prompt)
venv\Scripts\activate.bat

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Copy the environment template:

```bash
# Windows
copy .env.example .env

# macOS / Linux / Git Bash
cp .env.example .env
```

By default, the `.env` is configured to use a local SQLite database (`sqlite:///./dev.db`). The server will automatically create this database file on startup.

---

## 🏃 Running the Application

Start the development server with reload enabled (meaning changes to your code will automatically restart the server):

```bash
python -m src.main
```

Once running, you can access the server at **`http://127.0.0.1:8000`**.

### 📖 API Documentation

Navigate to the following URLs in your browser to inspect or test routes interactively:
* **Interactive Swagger Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **ReDoc (Alternative static docs)**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🧪 Running Tests

Verify your API works correctly using pytest. The test suite automatically launches a sandboxed in-memory SQLite database connection for isolation:

```bash
pytest
```

For verbose output:
```bash
pytest -v
```

---

## ✍️ Coding Guidelines (How to expand)

During your coding interview, follow this clean architecture flow to add a new resource (e.g., `Items`):

1. **Model**: Define your database schema inside `src/models/item.py` using SQLAlchemy:
   ```python
   from sqlalchemy import Column, Integer, String
   from src.config.db import Base

   class Item(Base):
       __tablename__ = "items"
       id = Column(Integer, primary_key=True, index=True)
       title = Column(String, index=True)
   ```
2. **Schemas**: Create your input/output validation models in `src/models/schemas.py` using Pydantic:
   ```python
   from pydantic import BaseModel

   class ItemCreate(BaseModel):
       title: str

   class ItemResponse(BaseModel):
       id: int
       title: str
       class Config:
           from_attributes = True
   ```
3. **Controller/Service**: Add querying logic or database transactions inside `src/controllers/item.py` or `src/services/item.py`.
4. **Routes**: Create the routing paths inside `src/routes/items.py` and register it on the primary router in `src/routes/index.py` using:
   ```python
   from src.routes.items import router as items_router
   router.include_router(items_router, prefix="/items", tags=["Items"])
   ```
5. **Auto-DB Updates**: Since `Base.metadata.create_all` runs on server startup, your database schema will update automatically next time you start the app!
