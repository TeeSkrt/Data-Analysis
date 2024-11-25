from django.urls import path
from .views import GetDataFromAzure

urlpatterns = [
    path('getdata/', GetDataFromAzure.as_view(), name='get-data-from-azure'),
]