# Credit Approval System API

A Django REST Framework backend for a credit approval workflow. The service imports customer and loan data, calculates credit limits and credit scores, evaluates loan eligibility, creates approved loans, and exposes customer/loan lookup APIs.

## What This Demonstrates

- Django and Django REST Framework API design
- PostgreSQL-backed domain models with Docker Compose
- Service-layer business logic for credit scoring and EMI calculation
- Excel import commands for initial customer and loan data
- Simple server-rendered dashboard for manual API testing

## Tech Stack

- Python
- Django
- Django REST Framework
- PostgreSQL
- Docker and Docker Compose
- Pandas / OpenPyXL

## Features

- Register customers and calculate approved credit limits
- Import customer and loan records from Excel files
- Check loan eligibility using historical repayment behavior
- Create loans with corrected interest rates where required
- View a loan by ID
- View all loans for a customer
- Admin dashboard for manual data inspection

## Run Locally

```bash
docker compose up --build
```

The app runs at:

```text
http://localhost:8000
```

Create an admin user:

```bash
docker compose exec web python manage.py createsuperuser
```

Import sample data:

```bash
docker compose exec web python manage.py import_customers backend/customer_data.xlsx
docker compose exec web python manage.py import_loans backend/loan_data.xlsx
```

## API Overview

```text
POST /api/register/
POST /api/check-eligibility/
POST /api/create-loan/
GET  /api/view-loan/<loan_id>/
GET  /api/view-loans/<customer_id>/
```

## Portfolio Notes

This project is intentionally backend-focused. The strongest parts are the domain modeling, API endpoints, import commands, and credit decision logic. Future improvements would include authentication, fuller test coverage, OpenAPI docs, and replacing the simple HTML dashboard with a separate frontend.
