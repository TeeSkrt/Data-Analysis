import os
import pyodbc
import math
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BaseSerializer
from rest_framework import status
from azure.identity import ManagedIdentityCredential

class GetDataFromAzure(APIView):
    def get(self, request, *args, **kwargs):
        # Lấy các biến môi trường
        db_name = "amazon_sales"
        db_host = "amazon-sql-server.database.windows.net"
        db_user = "azure_sa"
        db_password = "@123456A"
        db_port = "1433"

        total_records = 436449  
        page_size = 500  

        total_pages = math.ceil(total_records / page_size)  

        # Lấy số trang từ request, mặc định là trang 1
        page_number = int(request.GET.get('page', 1))

        # Đảm bảo page_number không vượt quá tổng số trang
        if page_number > total_pages:
            page_number = total_pages

        # Tính toán offset cho truy vấn SQL
        offset = (page_number - 1) * page_size

        conn = None
        try:
            # Chuỗi kết nối với Azure SQL Database qua Managed Identity
            conn = pyodbc.connect(
                f'DRIVER={{ODBC Driver 18 for SQL Server}};'
                f'SERVER={db_host},{db_port};'
                f'DATABASE={db_name};'
                f'UID={db_user};'
                f'PWD={db_password};'
                'Encrypt=yes;'
                'TrustServerCertificate=no;'
                'Connection Timeout=30;'
            )
            cursor = conn.cursor()

            # Truy vấn dữ liệu (chỉ lấy 10 dòng đầu tiên)
            query = f"""
                SELECT * FROM Predictions 
                ORDER BY asin 
                OFFSET {offset} ROWS FETCH NEXT {page_size} ROWS ONLY
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            
            # Chuyển dữ liệu thành định dạng JSON
            data = []
            for row in rows:
                data.append({
                    'asin': row.Asin,
                    'product': row.Product,
                    'category_name': row.Category_name,
                    'image': row.Image,
                    'rating': row.Rating,
                    'avg_rating': row.Avg_rating,
                    'review': row.Review,
                    'avg_review': row.Avg_review,
                    'price': row.Price,
                    'avg_price': row.Avg_price,
                    'price_ratio': row.Price_Ratio,
                    'review_rating_ratio': row.Review_Rating_Ratio,
                    'relative_popularity': row.Relative_Popularity,
                    'review_avg_review_ratio': row.Review_Avg_Review_Ratio,
                    'price_amount_ratio': row.Price_Amount_Ratio,
                    'rating_review_ratio': row.Rating_Review_Ratio,
                    'popularity_global_ratio': row.Popularity_Global_Ratio,
                    'popularity_category_max_ratio': row.Popularity_Category_Max_Ratio,
                    'price_rating_interaction': row.Price_Rating_Interaction,
                    'review_amount_interaction': row.Review_Amount_Interaction,
                    'combined_interaction': row.Combined_Interaction,
                    'amount': row.Amount,
                    'predicted_best_seller': row.Predicted_Best_Seller,
                })

            # Dữ liệu đã chuyển đổi qua serializer
            serializer = BaseSerializer(data, many=True)

            # Đóng kết nối
            cursor.close()
            
            # Trả về dữ liệu dưới dạng JSON
            return Response({
                'total_records': total_records,
                'total_pages': total_pages,
                'current_page': page_number,
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        except pyodbc.Error as e:
            # Lỗi khi kết nối cơ sở dữ liệu
            error_message = f"Database connection failed: {str(e)}"
            return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            # Lỗi bất ngờ
            error_message = f"Unexpected error: {str(e)}"
            return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        finally:
            # Đảm bảo đóng kết nối cơ sở dữ liệu
            if conn:
                conn.close()