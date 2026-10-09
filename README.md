# SmartFactory API

[![SmartFactory API Tests](https://github.com/Cellious/SmartFactoryAPI/actions/workflows/tests.yml/badge.svg)](https://github.com/Cellious/SmartFactoryAPI/actions/workflows/tests.yml)
Production and Inventory Management Backend built with Python and FastAPI.

SmartFactory API is a backend project designed for manufacturing environments to manage production records, machines, products, stock movements and customer orders through a secure REST API.

The project focuses on clean architecture, role-based authorization, testability and maintainable backend development.

---

## Features

- JWT-based authentication
- Role-based authorization
- Product management
- Production management
- Machine management
- Stock movement management
- Customer order management
- Machine performance reports
- Production statistics
- Dashboard summary
- Low-stock detection
- Stock valuation
- Order status filtering
- Input validation with Pydantic
- Repository / Service architecture
- Automated API tests with Pytest

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend development |
| FastAPI | REST API framework |
| Pydantic | Data validation and schemas |
| JWT | Authentication |
| Passlib + bcrypt | Password hashing |
| python-jose | JWT implementation |
| python-dotenv | Environment configuration |
| Pytest | Automated testing |
| HTTPX | API testing |
| Fake DB | Development data layer |

---

## Architecture

The project follows a layered architecture:

```text
Client
   |
   v
FastAPI API Layer
   |
   v
Service Layer
   |
   v
Repository Layer
   |
   v
Fake Database

API Layer
Responsible for:
- HTTP endpoints
- Request handling
- Authentication
- Authorization
- HTTP responses
Service Layer
Responsible for:
- Business rules
- Validation
- Calculations
- Application logic
Repository Layer
Responsible for:
- Data access
- CRUD operations
- Database abstraction
Database Layer
The current version uses an in-memory Fake DB for development and testing.
A real PostgreSQL implementation can be introduced later without changing the API contract.
Authentication
SmartFactory API uses JWT Bearer authentication.
Login
POST /api/auth/login

Example request:
{
  "username": "admin",
  "password": "Admin123!"
}

Example response:
{
  "access_token": "JWT_TOKEN",
  "token_type": "bearer"
}

Authenticated requests use:
Authorization: Bearer <token>

Current Users
The development environment contains two example roles:
Username	Role
admin	ADMIN
operator	OPERATOR


Example credentials are intended only for local development and testing. Production environments must use securely managed credentials.

Authorization
The API currently supports two roles.
ADMIN
Full access to the system.
OPERATOR
Read access and production-related operational access.
Module	Operation	ADMIN	OPERATOR
Products	Read	Yes	Yes
Products	Create	Yes	No
Products	Update	Yes	No
Products	Delete	Yes	No
Production	Read	Yes	Yes
Production	Create	Yes	Yes
Production	Update	Yes	Yes
Production	Delete	Yes	No
Machines	Read	Yes	Yes
Machines	Create	Yes	No
Machines	Update	Yes	No
Machines	Delete	Yes	No
Orders	Read	Yes	Yes
Orders	Create	Yes	No
Orders	Update	Yes	No
Orders	Delete	Yes	No
Stock	Read	Yes	Yes
Stock	Create Movement	Yes	No
Reports	Read	Yes	Yes
Dashboard	Read	Yes	Yes


API Endpoints
Authentication
POST /api/auth/login
GET  /api/auth/me

Products
GET    /api/products/
GET    /api/products/low-stock
GET    /api/products/{product_id}
POST   /api/products/
PUT    /api/products/{product_id}
DELETE /api/products/{product_id}

Production
GET    /api/production/
GET    /api/production/statistics
GET    /api/production/{production_id}
POST   /api/production/
PUT    /api/production/{production_id}
DELETE /api/production/{production_id}

Machines
GET    /api/machines/
GET    /api/machines/{machine_id}
POST   /api/machines/
PUT    /api/machines/{machine_id}
DELETE /api/machines/{machine_id}

Stock
GET  /api/stock/movements
POST /api/stock/movements
GET  /api/stock/balances
GET  /api/stock/value

Orders
GET    /api/orders/
GET    /api/orders/summary
GET    /api/orders/status/{status}
GET    /api/orders/{order_id}
POST   /api/orders/
PUT    /api/orders/{order_id}
DELETE /api/orders/{order_id}

Reports
GET /api/reports/machine-performance

Dashboard
GET /api/dashboard/summary

Project Structure
SmartFactoryAPI/
â”‚
â”œâ”€â”€ app/
â”‚   â”œâ”€â”€ api/
â”‚   â”‚   â”œâ”€â”€ auth.py
â”‚   â”‚   â”œâ”€â”€ dashboard.py
â”‚   â”‚   â”œâ”€â”€ machines.py
â”‚   â”‚   â”œâ”€â”€ orders.py
â”‚   â”‚   â”œâ”€â”€ production.py
â”‚   â”‚   â”œâ”€â”€ products.py
â”‚   â”‚   â”œâ”€â”€ reports.py
â”‚   â”‚   â””â”€â”€ stock.py
â”‚   â”‚
â”‚   â”œâ”€â”€ auth/
â”‚   â”‚   â”œâ”€â”€ dependencies.py
â”‚   â”‚   â””â”€â”€ security.py
â”‚   â”‚
â”‚   â”œâ”€â”€ database/
â”‚   â”‚   â””â”€â”€ fake_db.py
â”‚   â”‚
â”‚   â”œâ”€â”€ repositories/
â”‚   â”‚   â”œâ”€â”€ machine_repository.py
â”‚   â”‚   â”œâ”€â”€ order_repository.py
â”‚   â”‚   â”œâ”€â”€ production_repository.py
â”‚   â”‚   â”œâ”€â”€ product_repository.py
â”‚   â”‚   â””â”€â”€ user_repository.py
â”‚   â”‚
â”‚   â”œâ”€â”€ schemas/
â”‚   â”‚   â”œâ”€â”€ auth.py
â”‚   â”‚   â”œâ”€â”€ dashboard.py
â”‚   â”‚   â”œâ”€â”€ machine.py
â”‚   â”‚   â”œâ”€â”€ order.py
â”‚   â”‚   â”œâ”€â”€ production.py
â”‚   â”‚   â”œâ”€â”€ product.py
â”‚   â”‚   â”œâ”€â”€ report.py
â”‚   â”‚   â””â”€â”€ stock.py
â”‚   â”‚
â”‚   â”œâ”€â”€ services/
â”‚   â”‚   â”œâ”€â”€ auth_service.py
â”‚   â”‚   â”œâ”€â”€ dashboard_service.py
â”‚   â”‚   â”œâ”€â”€ order_service.py
â”‚   â”‚   â”œâ”€â”€ production_service.py
â”‚   â”‚   â”œâ”€â”€ report_service.py
â”‚   â”‚   â””â”€â”€ stock_service.py
â”‚   â”‚
â”‚   â””â”€â”€ main.py
â”‚
â”œâ”€â”€ tests/
â”‚   â”œâ”€â”€ conftest.py
â”‚   â”œâ”€â”€ test_auth.py
â”‚   â”œâ”€â”€ test_authorization.py
â”‚   â”œâ”€â”€ test_dashboard.py
â”‚   â”œâ”€â”€ test_dashboard_authorization.py
â”‚   â”œâ”€â”€ test_machines.py
â”‚   â”œâ”€â”€ test_machine_authorization.py
â”‚   â”œâ”€â”€ test_orders.py
â”‚   â”œâ”€â”€ test_order_authorization.py
â”‚   â”œâ”€â”€ test_production.py
â”‚   â”œâ”€â”€ test_products.py
â”‚   â”œâ”€â”€ test_reports.py
â”‚   â”œâ”€â”€ test_report_authorization.py
â”‚   â”œâ”€â”€ test_stock.py
â”‚   â””â”€â”€ test_stock_authorization.py
â”‚
â”œâ”€â”€ .env.example
â”œâ”€â”€ .gitignore
â”œâ”€â”€ README.md
â””â”€â”€ requirements.txt

Installation
Clone the repository:
git clone <repository-url>
cd SmartFactoryAPI

Create a virtual environment:
Windows
python -m venv .venv
.venv\Scripts\Activate.ps1

Install dependencies:
pip install -r requirements.txt

Environment Configuration
Create a .env file in the project root:
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

Never commit the .env file to source control.
The repository contains .env.example as a configuration template.
Running the API
Start the development server:
uvicorn app.main:app --reload

The API will be available at:
http://127.0.0.1:8000

API Documentation
FastAPI automatically provides interactive API documentation.
Swagger UI
http://127.0.0.1:8000/docs

ReDoc
http://127.0.0.1:8000/redoc

Testing
The project uses Pytest for automated testing.
Run the complete test suite:
pytest -q

Current test status:
84 passed

The test suite covers:
- Authentication
- JWT validation
- Role-based authorization
- Product CRUD
- Production CRUD
- Machine CRUD
- Stock operations
- Order management
- Reports
- Dashboard
- Business rules
- Input validation
- Unauthorized access scenarios
- Role-based access control
Security
The project includes:
- JWT authentication
- Password hashing with bcrypt
- Role-based authorization
- Protected API endpoints
- Environment-based secret configuration
- .env excluded from Git
- Pydantic input validation
Production deployments should additionally use:
- Strong randomly generated secrets
- HTTPS
- Secure secret management
- Production database
- Centralized logging
- Monitoring
- Rate limiting
- Secure credential management
Current Database Strategy
The current version intentionally uses an in-memory Fake DB.
This approach makes the project:
- Easy to run locally
- Easy to test
- Independent of external database infrastructure
- Suitable for demonstrating API architecture
PostgreSQL is planned as a future implementation.
The Repository / Service architecture allows the persistence layer to be replaced without changing the API layer.
Roadmap
- [ ] PostgreSQL integration
- [ ] SQLAlchemy
- [ ] Database migrations
- [ ] Docker support
- [ ] GitHub Actions CI/CD
- [ ] Centralized error handling
- [ ] Pagination
- [ ] Advanced filtering
- [ ] API logging
- [ ] Pandas production analytics
- [ ] AI-assisted production analysis
- [ ] Ollama integration
- [ ] React dashboard
- [ ] Production monitoring
Development Philosophy
The project is developed with the following principles:
- Separation of concerns
- Explicit business rules
- Automated test validation
- Secure authentication
- Role-based authorization
- Maintainable code
- API-first design
- Incremental architecture evolution
- Testable business logic
Project Status
The current version includes:
- Secure JWT authentication
- Role-based authorization
- Production management
- Machine management
- Product management
- Stock management
- Order management
- Reporting
- Dashboard
- Automated test coverage
Current automated test result:
84 passed

Author
Professional backend portfolio project demonstrating:
- Python
- FastAPI
- REST API design
- JWT authentication
- Role-based authorization
- Pydantic
- Automated testing
- Layered architecture
- Manufacturing-domain business logic

