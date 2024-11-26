from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Base
from .serializers import BaseSerializer
import logging

class GetDataFromAzure(APIView):
    def get(self, request):
        try:
            # Lấy dữ liệu từ ORM
            products = Base.objects.all().order_by('-amount')[:10]
            logging.info(f"Fetched {len(products)} records from database.")
            serializer = BaseSerializer(products, many=True)
            return Response(serializer.data)
        except Exception as e:
            logging.error(f"Error in GetDataFromAzure: {e}")
            return Response({"error": "Internal Server Error"}, status=500)