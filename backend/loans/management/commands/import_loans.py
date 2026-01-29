import pandas as pd
from django.core.management.base import BaseCommand
from loans.models import Loan
from customers.models import Customer
from django.db import connection


class Command(BaseCommand):
    help = "Import loans from Excel"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **kwargs):

        file_path = kwargs["file_path"]
        df = pd.read_excel(file_path)

        for _, row in df.iterrows():

            customer = Customer.objects.get(
                customer_id=row["Customer ID"]
            )

            Loan.objects.get_or_create(
                loan_id=row["Loan ID"],
                defaults={
                    "customer": customer,
                    "loan_amount": row["Loan Amount"],
                    "tenure": row["Tenure"],
                    "interest_rate": row["Interest Rate"],
                    "monthly_installment": row["Monthly payment"],
                    "emis_paid_on_time": row["EMIs paid on Time"],
                    "start_date": row["Date of Approval"],
                    "end_date": row["End Date"],
                    "is_active": True
                }
            )

        # reset sequence
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT setval(pg_get_serial_sequence('loans_loan','loan_id'), MAX(loan_id)) FROM loans_loan;"
            )

        self.stdout.write(self.style.SUCCESS("Loans imported successfully"))
