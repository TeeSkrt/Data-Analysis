from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Base
from .serializers import BaseSerializer

class GetDataFromAzure(APIView):
    def get(self, request):
        # Lấy 10 sản phẩm từ bảng Predictions, sắp xếp theo Amount giảm dần
        products = Base.objects.all().order_by('-amount')[:10]
        serializer = BaseSerializer(products, many=True)
        return Response(serializer.data)
