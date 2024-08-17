
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from restbas.models import Employee
from .serializers import EmployeeSerializer


class EmployeeView(APIView):
    def get(self, request):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_staff:
            return Response(
                {"error": "Only admin can add employee"},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
