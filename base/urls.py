from django.urls import path
from .views import BaseList

urlpatterns = [
    path('api/bases/', BaseList.as_view(), name='base-list'),  # Endpoint của API
]