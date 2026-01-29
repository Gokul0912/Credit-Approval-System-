import pandas as pd
from django.core.management.base import BaseCommand
from customers.models import Customer
from django.db import connection


class Command(BaseCommand):
    help = "Import customers from Excel"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **kwargs):

        file_path = kwargs["file_path"]
        df = pd.read_excel(file_path)

        for _, row in df.iterrows():
            Customer.objects.get_or_create(
                customer_id=row["Customer ID"],
                defaults={
                    "first_name": row["First Name"],
                    "last_name": row["Last Name"],
                    "age": row["Age"],
                    "phone_number": str(row["Phone Number"]),
                    "monthly_salary": row["Monthly Salary"],
                    "approved_limit": row["Approved Limit"],
                    "current_debt": 0
                }
            )

        # reset sequence
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT setval(pg_get_serial_sequence('customers_customer','customer_id'), MAX(customer_id)) FROM customers_customer;"
            )

        self.stdout.write(self.style.SUCCESS("Customers imported successfully"))
