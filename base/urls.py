from django.urls import path
from .views import GetDataFromAzure, SortBestSeller

urlpatterns = [
    path('getdata/', GetDataFromAzure.as_view(), name='getdata'),
    path('getdata/sort/', SortBestSeller.as_view(), name='sort'),
]