
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from restbas.models import Restaurant
from restbas.restaurants.serializers_r import RestaurantSerializer


class CreateRestaurantView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        if not request.user.is_staff:
            return Response(
                {"error": "Only admin can create restaurants"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = RestaurantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteRestaurantView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        if not request.user.is_staff:
            return Response(
                {"error": "Only admin can delete restaurants"},
                status=status.HTTP_403_FORBIDDEN
            )

        restaurant = get_object_or_404(Restaurant, pk=pk)
        restaurant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
