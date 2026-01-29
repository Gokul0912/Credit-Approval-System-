from django.contrib import admin
from django.urls import path, include
from core.views import (
    dashboard,
    register_ui,
    eligibility_ui,
    create_loan_ui,
    view_loan_ui,
    view_customer_loans_ui
)

urlpatterns = [
    path("", dashboard),
    path("register-ui/", register_ui),
    path("eligibility-ui/", eligibility_ui),
    path("create-loan-ui/", create_loan_ui),
    path("view-loan-ui/", view_loan_ui),
    path("view-customer-loans-ui/", view_customer_loans_ui),

    path("admin/", admin.site.urls),
    path("api/customers/", include("customers.urls")),
    path("api/loans/", include("loans.urls")),
]
