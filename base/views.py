from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Base
from .serializers import BaseSerializer

class GetDataFromAzure(APIView):
    def get(self, request):
        # Trả về 100 bản ghi đầu tiên
        predictions = Base.objects.all()[:100]
        serializer = BaseSerializer(predictions, many=True)
        return Response(serializer.data)