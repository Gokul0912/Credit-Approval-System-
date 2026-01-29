from django.shortcuts import render

def dashboard(request):
    return render(request, "dashboard.html")

def register_ui(request):
    return render(request, "register.html")

def eligibility_ui(request):
    return render(request, "eligibility.html")

def create_loan_ui(request):
    return render(request, "create_loan.html")

def view_loan_ui(request):
    return render(request, "view_loan.html")

def view_customer_loans_ui(request):
    return render(request, "view_customer_loans.html")
