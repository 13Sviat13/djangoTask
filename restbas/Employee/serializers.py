from rest_framework import serializers
from restbas.models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'user', 'restaurant', 'role']
