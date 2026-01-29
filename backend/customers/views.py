from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import RegisterCustomerSerializer
from .models import Customer
from .services import calculate_approved_limit


@api_view(["POST"])
def register_customer(request):

    serializer = RegisterCustomerSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    data = serializer.validated_data

    approved_limit = calculate_approved_limit(data["monthly_salary"])

    customer = Customer.objects.create(
        first_name=data["first_name"],
        last_name=data["last_name"],
        age=data["age"],
        phone_number=data["phone_number"],
        monthly_salary=data["monthly_salary"],
        approved_limit=approved_limit,
        current_debt=0
    )

    return Response(
        {
            "customer_id": customer.customer_id,
            "name": f"{customer.first_name} {customer.last_name}",
            "age": customer.age,
            "monthly_income": customer.monthly_salary,
            "approved_limit": customer.approved_limit,
            "phone_number": customer.phone_number
        },
        status=status.HTTP_201_CREATED
    )
