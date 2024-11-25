from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Base
from .serializers import BaseSerializer

class GetDataFromAzure(APIView):
    def get(self, request):
        # Phân trang
        paginator = PageNumberPagination()
        paginator.page_size = 100  # Số bản ghi trên mỗi trang
        predictions = Base.objects.all()
        result_page = paginator.paginate_queryset(predictions, request)
        
        # Serialize và trả dữ liệu
        serializer = BaseSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)