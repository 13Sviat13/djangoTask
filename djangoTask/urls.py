"""
URL configuration for djangoTask project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import ObtainAuthToken

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView # noqa

from restbas.Auth.views import LoginView, RegisterView, UserView, LogoutView,  homepage # noqa
from restbas.restaurants.views import CreateRestaurantView, DeleteRestaurantView # noqa
from restbas.Menu.views import UploadMenuView, CurrentMenuView, VoteMenuView, CurrentMenuResultsView # noqa
from restbas.Employee.views import EmployeeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # noqa
    path('api-token-auth/', ObtainAuthToken.as_view(), name='api-token-auth'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # noqa
    path('api/v1/', include('rest_framework.urls')),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('user/', UserView.as_view(), name='user'),
    path('restaurants/', CreateRestaurantView.as_view(), name='restaurant'),
    path('restaurants/<pk>', DeleteRestaurantView.as_view(), name='restaurants'), # noqa
    path('restaurants/<pk>/menu', UploadMenuView.as_view(), name='upload'),
    path('restaurants/<pk>/menu/today', CurrentMenuView.as_view(), name='menu'), # noqa
    path('employees/', EmployeeView.as_view(), name='employee'),
    path('restaurants/<pk>/menu/<menu_pk>/vote', VoteMenuView.as_view(), name='vote'), # noqa
    path('restaurants/<pk>/menu/today/results', CurrentMenuResultsView.as_view(), name='result'), # noqa
    path('', homepage, name='home'),
]
