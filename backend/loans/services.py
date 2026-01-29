from datetime import date
from loans.models import Loan


def calculate_credit_score(customer):

    loans = Loan.objects.filter(customer=customer)

    if not loans.exists():
        return 50

    score = 0

    total_paid = sum(l.emis_paid_on_time for l in loans)
    total_tenure = sum(l.tenure for l in loans) or 1

    score += (total_paid / total_tenure) * 40
    score += min(loans.count() * 5, 20)

    current_year = date.today().year
    score += min(loans.filter(start_date__year=current_year).count() * 5, 20)

    total_amount = sum(l.loan_amount for l in loans)
    score += min(total_amount / 100000, 20)

    return min(int(score), 100)
