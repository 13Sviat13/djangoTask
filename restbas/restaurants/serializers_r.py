
from rest_framework import serializers
from restbas.models import Restaurant


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'kitchen', 'phone_number', 'owner']

    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError(
                "Name must be at least 3 characters"
            )
        return value

    def validate_address(self, value):
        if not value:
            raise serializers.ValidationError("Address is required")
        return value
