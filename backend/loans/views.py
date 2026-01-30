from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from datetime import date, timedelta
from django.views.decorators.csrf import csrf_exempt


from customers.models import Customer
from loans.models import Loan
from loans.services import calculate_credit_score
from common.utils import calculate_emi




@api_view(["POST"])
def check_eligibility(request):

    customer_id = request.data.get("customer_id")
    loan_amount = request.data.get("loan_amount")
    interest_rate = request.data.get("interest_rate")
    tenure = request.data.get("tenure")

    if not all([customer_id, loan_amount, interest_rate, tenure]):
        return Response({"error": "Missing fields"}, status=400)

    customer = get_object_or_404(Customer, customer_id=customer_id)

    loan_amount = float(loan_amount)
    interest_rate = float(interest_rate)
    tenure = int(tenure)

    loans = Loan.objects.filter(customer=customer)
    total_emi = sum(l.monthly_installment for l in loans)

    if total_emi > 0.5 * customer.monthly_salary:
        return Response({"approval": False})

    total_debt = sum(l.loan_amount for l in loans)

    credit_score = 0 if total_debt > customer.approved_limit else calculate_credit_score(customer)

    approval = False
    corrected_rate = interest_rate

    if credit_score > 50:
        approval = True
    elif 30 < credit_score <= 50:
        approval = True
        corrected_rate = max(interest_rate, 12)
    elif 10 < credit_score <= 30:
        approval = True
        corrected_rate = max(interest_rate, 16)

    emi = calculate_emi(loan_amount, corrected_rate, tenure)

    return Response({
        "customer_id": customer_id,
        "approval": approval,
        "interest_rate": interest_rate,
        "corrected_interest_rate": corrected_rate,
        "tenure": tenure,
        "monthly_installment": emi
    })


@csrf_exempt
@api_view(["POST"])
def create_loan(request):

    customer_id = request.data.get("customer_id")
    loan_amount = request.data.get("loan_amount")
    interest_rate = request.data.get("interest_rate")
    tenure = request.data.get("tenure")

    if not all([customer_id, loan_amount, interest_rate, tenure]):
        return Response({"error": "Missing fields"}, status=400)

    customer = get_object_or_404(Customer, customer_id=customer_id)

    loan_amount = float(loan_amount)
    interest_rate = float(interest_rate)
    tenure = int(tenure)

    existing = Loan.objects.filter(
        customer=customer,
        loan_amount=loan_amount,
        interest_rate=interest_rate,
        tenure=tenure
    ).first()

    if existing:
        return Response({
            "loan_id": existing.loan_id,
            "loan_approved": True,
            "monthly_installment": existing.monthly_installment,
            "message": "Loan already exists"
        })

    loans = Loan.objects.filter(customer=customer)
    total_emi = sum(l.monthly_installment for l in loans)

    if total_emi > 0.5 * customer.monthly_salary:
        return Response({"loan_approved": False, "message": "EMI limit exceeded"}, status=400)

    credit_score = calculate_credit_score(customer)

    if credit_score <= 10:
        return Response({"loan_approved": False, "message": "Low credit score"}, status=400)

    if 30 < credit_score <= 50:
        interest_rate = max(interest_rate, 12)
    elif 10 < credit_score <= 30:
        interest_rate = max(interest_rate, 16)

    emi = calculate_emi(loan_amount, interest_rate, tenure)

    start = date.today()
    end = start + timedelta(days=30 * tenure)

    loan = Loan.objects.create(
        customer=customer,
        loan_amount=loan_amount,
        interest_rate=interest_rate,
        tenure=tenure,
        monthly_installment=emi,
        emis_paid_on_time=0,
        start_date=start,
        end_date=end,
        is_active=True
    )

    return Response({
        "loan_id": loan.loan_id,
        "customer_id": customer.customer_id,
        "loan_approved": True,
        "monthly_installment": emi
    }, status=201)



@api_view(["GET"])
def view_loan(request, loan_id):

    loan = get_object_or_404(Loan, loan_id=loan_id)
    customer = loan.customer

    return Response({
        "loan_id": loan.loan_id,
        "customer": {
            "id": customer.customer_id,
            "first_name": customer.first_name,
            "last_name": customer.last_name,
            "phone_number": customer.phone_number,
            "age": customer.age
        },
        "loan_amount": loan.loan_amount,
        "interest_rate": loan.interest_rate,
        "monthly_installment": loan.monthly_installment,
        "tenure": loan.tenure
    })




@api_view(["GET"])
def view_loans_by_customer(request, customer_id):

    loans = Loan.objects.filter(customer__customer_id=customer_id)

    data = []

    for loan in loans:
        data.append({
            "loan_id": loan.loan_id,
            "loan_amount": loan.loan_amount,
            "interest_rate": loan.interest_rate,
            "monthly_installment": loan.monthly_installment,
            "repayments_left": loan.tenure - loan.emis_paid_on_time
        })

    return Response(data)
