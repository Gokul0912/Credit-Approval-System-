from datetime import date
from loans.models import Loan



def calculate_credit_score(customer):
    """
    Score Range: 0 - 100

    Factors:
    - Past loans count
    - Repayment history
    - Total loan exposure
    """

    loans = Loan.objects.filter(customer=customer)

    # New customer gets base score
    if not loans.exists():
        return 50

    score = 0

    #  On-time EMI payments
    total_emis_paid = sum(l.emis_paid_on_time for l in loans)
    total_tenure = sum(l.tenure for l in loans) or 1
    payment_ratio = total_emis_paid / total_tenure
    score += payment_ratio * 40

    #  Number of previous loans
    score += min(loans.count() * 5, 20)

    #  Loans taken in current year
    current_year = date.today().year
    yearly_loans = loans.filter(start_date__year=current_year).count()
    score += min(yearly_loans * 5, 20)

    #  Total borrowed amount
    total_amount = sum(l.loan_amount for l in loans)
    score += min(total_amount / 100000, 20)

    return min(int(score), 100)



def calculate_emi(amount, interest_rate, tenure):
    monthly_rate = float(interest_rate) / (12 * 100)

    emi = (
        float(amount)
        * monthly_rate
        * (1 + monthly_rate) ** int(tenure)
    ) / ((1 + monthly_rate) ** int(tenure) - 1)

    return round(emi, 2)




def check_loan_eligibility(customer, loan_amount, interest_rate, tenure):
    credit_score = calculate_credit_score(customer)

    # Decision Rules
    if credit_score >= 70:
        approved = True
    elif credit_score >= 50 and loan_amount <= 500000:
        approved = True
    else:
        approved = False

    emi = calculate_emi(loan_amount, interest_rate, tenure)

    return {
        "customer_id": customer.id,
        "approval": approved,
        "credit_score": credit_score,
        "interest_rate": interest_rate,
        "corrected_interest_rate": interest_rate,
        "tenure": tenure,
        "monthly_installment": emi
    }
