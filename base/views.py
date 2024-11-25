from django.http import JsonResponse
import pyodbc

def GetDataFromAzure(request):
    # Thiết lập kết nối đến cơ sở dữ liệu SQL Server trên Azure
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                          'SERVER=amazon-sql-server.database.windows.net;'
                          'PORT=1433;'
                          'DATABASE=amazon_sales;'
                          'UID=azure_sa;'
                          'PWD=@123456A')
    cursor = conn.cursor()

    # Truy vấn dữ liệu từ bảng Predictions, chỉ lấy 10 bản ghi
    cursor.execute("""
        SELECT Asin, Product, Category_name, Image, Rating, Avg_rating, Review, Avg_review, 
               Price, Avg_price, Price_Ratio, Review_Rating_Ratio, Relative_Popularity,
               Review_Avg_Review_Ratio, Price_Amount_Ratio, Rating_Review_Ratio,
               Popularity_Global_Ratio, Popularity_Category_Max_Ratio, Price_Rating_Interaction,
               Review_Amount_Interaction, Combined_Interaction, Amount, Predicted_Best_Seller
        FROM Predictions
        ORDER BY Amount DESC  
        OFFSET 0 ROWS FETCH NEXT 10 ROWS ONLY;  -- Chỉ lấy 10 sản phẩm
    """)

    # Lấy tất cả kết quả từ truy vấn
    rows = cursor.fetchall()

    # Đóng kết nối sau khi truy vấn xong
    cursor.close()
    conn.close()

    # Chuyển kết quả truy vấn thành danh sách các từ điển (JSON)
    products = []
    for row in rows:
        products.append({
            'Asin': row.Asin,
            'Product': row.Product,
            'Category_name': row.Category_name,
            'Image': row.Image,
            'Rating': row.Rating,
            'Avg_rating': row.Avg_rating,
            'Review': row.Review,
            'Avg_review': row.Avg_review,
            'Price': row.Price,
            'Avg_price': row.Avg_price,
            'Price_Ratio': row.Price_Ratio,
            'Review_Rating_Ratio': row.Review_Rating_Ratio,
            'Relative_Popularity': row.Relative_Popularity,
            'Review_Avg_Review_Ratio': row.Review_Avg_Review_Ratio,
            'Price_Amount_Ratio': row.Price_Amount_Ratio,
            'Rating_Review_Ratio': row.Rating_Review_Ratio,
            'Popularity_Global_Ratio': row.Popularity_Global_Ratio,
            'Popularity_Category_Max_Ratio': row.Popularity_Category_Max_Ratio,
            'Price_Rating_Interaction': row.Price_Rating_Interaction,
            'Review_Amount_Interaction': row.Review_Amount_Interaction,
            'Combined_Interaction': row.Combined_Interaction,
            'Amount': row.Amount,
            'Predicted_Best_Seller': row.Predicted_Best_Seller,
        })

    # Trả về kết quả dưới dạng JSON
    return JsonResponse({'products': products})
