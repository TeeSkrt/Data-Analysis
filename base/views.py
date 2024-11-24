from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Base
from .serializers import BaseSerializer

class BaseList(APIView):
    def get(self, request):
        # Lấy tất cả dữ liệu từ bảng Base
        bases = Base.objects.all()
        # Sử dụng serializer để chuyển đổi dữ liệu
        serializer = BaseSerializer(bases, many=True)
        return Response(serializer.data)