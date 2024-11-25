from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Base
from .serializers import BaseSerializer

class BaseList(APIView):
    def get(self, request):
        try:
            # Lấy tất cả dữ liệu từ bảng Base
            bases = Base.objects.all()
            # Sử dụng serializer để chuyển đổi dữ liệu thành JSON
            serializer = BaseSerializer(bases, many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)