Credit Approval System – Backend Assignment

Hi, This project is a Credit Approval System that I built as part of a backend internship assignment. The goal of this project is to design and implement a backend service that can register customers, evaluate loan eligibility based on historical data, create loans, and allow viewing of loan and customer details.

I have used Django, Django Rest Framework, PostgreSQL, and Docker to build and containerize the entire system. The application also supports importing initial customer and loan data from Excel files.

TECH STACK

Python - Django 5 - Django Rest Framework - PostgreSQL - Docker & Docker Compose - Pandas
FEATURES IMPLEMENTED

Register new customers Automatically calculate approved credit limit based on salary Import customers and loans from Excel files Check loan eligibility based on historical loan data Create new loans after eligibility check View loan details by loan ID View all loans for a specific customer Django Admin panel for managing customers and loans Simple HTML/CSS dashboard for interacting with APIs
HOW TO RUN

docker compose up –build

Open: http://localhost:8000

CREATE ADMIN USER

docker compose exec web python manage.py createsuperuser

Open: http://localhost:8000/admin/

IMPORT INITIAL DATA

docker compose exec web python manage.py importcustomers customerdata.xlsx docker compose exec web python manage.py importloans loandata.xlsx

CREDIT LOGIC (SUMMARY)

Past loan repayment history - Number of loans - Current loan activity - Total loan volume - EMI vs salary

If total EMI > 50% of salary → reject If total loans > approved limit → reject

UI

Simple HTML/CSS dashboard inside Django templates.

WHY I BUILT IT THIS WAY

Clean separation of apps - Production-like database - Dockerized environment - Easy to extend
FUTURE IMPROVEMENTS

Authentication Better scoring model Unit tests React frontend