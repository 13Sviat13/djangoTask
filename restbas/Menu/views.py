import datetime

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from restbas.models import Menu, MenuItem, Restaurant, Vote, Employee
from .serializers import MenuSerializer, MenuItemSerializer


class UploadMenuView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        restaurant = get_object_or_404(Restaurant, pk=pk)
        if not request.user.is_staff or request.user != restaurant.owner:
            return Response(
                {"error": "Only the restaurant owner can upload menus"},
                status=status.HTTP_403_FORBIDDEN
            )

        menu_data = request.data.get('menu')
        if not menu_data:
            return Response(
                {"error": "Menu data is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        menu_serializer = MenuSerializer(data=menu_data)
        if menu_serializer.is_valid():
            menu = menu_serializer.save(restaurant=restaurant)
            menu_items_data = request.data.get('menu_items')
            if menu_items_data:
                for item_data in menu_items_data:
                    item_serializer = MenuItemSerializer(data=item_data)
                    if item_serializer.is_valid():
                        item_serializer.save(menu=menu)
            return Response(
                {"message": "Menu uploaded successfully"},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"error": "Invalid menu data"},
            status=status.HTTP_400_BAD_REQUEST
        )


class CurrentMenuView(APIView):
    def get(self, request, pk):
        restaurant = get_object_or_404(Restaurant, pk=pk)
        today = datetime.date.today()
        today_menu = Menu.objects.filter(
            restaurant=restaurant,
            date=today.strftime("%A").upper()).first()
        if today_menu:
            menu_serializer = MenuSerializer(today_menu)
            menu_items = MenuItem.objects.filter(menu=today_menu)
            menu_items_serializer = MenuItemSerializer(menu_items, many=True)
            return Response({
                'menu': menu_serializer.data,
                'menu_items': menu_items_serializer.data
            })
        return Response({"error": "Menu not found for today"}, status=404)


class VoteMenuView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, menu_pk):
        employee = Employee.objects.get(admin=request.user)
        menu = get_object_or_404(Menu, pk=menu_pk)
        if Vote.objects.filter(employee=employee, menu=menu).exists():
            return Response(
                {"error": "You have already voted for this menu"},
                status=400
            )
        vote = Vote(employee=employee, menu=menu)
        vote.save()
        return Response({"message": "Vote cast successfully"})


class CurrentMenuResultsView(APIView):
    def get(self, request, pk):
        restaurant = get_object_or_404(Restaurant, pk=pk)
        today = datetime.date.today()
        today_menu = Menu.objects.filter(
            restaurant=restaurant,
            date=today.strftime("%A").upper()).first()
        if today_menu:
            votes = Vote.objects.filter(menu=today_menu).count()
            menu_serializer = MenuSerializer(today_menu)
            return Response({
                'menu': menu_serializer.data,
                'votes': votes
            })
        return Response({"error": "Menu not found for today"}, status=404)
