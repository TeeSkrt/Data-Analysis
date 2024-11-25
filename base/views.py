from django.http import JsonResponse
from django.views import View
from django.db import connection

class GetDataFromAzure(View):
    def get(self, request, *args, **kwargs):
        # Kết nối với cơ sở dữ liệu Azure SQL Server
        with connection.cursor() as cursor:
            # Truy vấn dữ liệu từ bảng Predictions
            cursor.execute("""
                SELECT Asin, Product, Category_name, Image, Rating, Avg_rating, Review, Avg_review, 
                       Price, Avg_price, Price_Ratio, Review_Rating_Ratio, Relative_Popularity,
                       Review_Avg_Review_Ratio, Price_Amount_Ratio, Rating_Review_Ratio,
                       Popularity_Global_Ratio, Popularity_Category_Max_Ratio, Price_Rating_Interaction,
                       Review_Amount_Interaction, Combined_Interaction, Amount, Predicted_Best_Seller
                FROM Predictions
            """)
            rows = cursor.fetchall()

        # Chuyển dữ liệu truy vấn thành định dạng JSON
        data = []
        for row in rows:
            data.append({
                'Asin': row[0],
                'Product': row[1],
                'Category_name': row[2],
                'Image': row[3],
                'Rating': row[4],
                'Avg_rating': row[5],
                'Review': row[6],
                'Avg_review': row[7],
                'Price': row[8],
                'Avg_price': row[9],
                'Price_Ratio': row[10],
                'Review_Rating_Ratio': row[11],
                'Relative_Popularity': row[12],
                'Review_Avg_Review_Ratio': row[13],
                'Price_Amount_Ratio': row[14],
                'Rating_Review_Ratio': row[15],
                'Popularity_Global_Ratio': row[16],
                'Popularity_Category_Max_Ratio': row[17],
                'Price_Rating_Interaction': row[18],
                'Review_Amount_Interaction': row[19],
                'Combined_Interaction': row[20],
                'Amount': row[21],
                'Predicted_Best_Seller': row[22],
            })

        # Trả về dữ liệu dưới dạng JSON
        return JsonResponse(data, safe=False)
