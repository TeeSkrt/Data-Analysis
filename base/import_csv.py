import csv
from base.models import Base  # Thay myapp bằng tên ứng dụng của bạn

file_path = 'F:/VSCode/Python/Python385/Code Space/Analyst/amazon_products.csv'  # Đường dẫn đến file CSV
def import_data(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            Base.objects.create(
                asin=row['Asin'],
                product=row['Product'],
                category_name=row['Category name'],
                image=row['Image'],
                rating=row['Rating'],
                avg_rating=row['Avg_rating'],
                review=row['Review'],
                avg_review=row['Avg_review'],
                price=row['Price'],
                avg_price=row['Avg_price'],
                price_ratio=row['Price_Ratio'],
                review_rating_ratio=row['Review_Rating_Ratio'],
                relative_popularity=row['Relative_Popularity'],
                review_avg_review_ratio=row['Review_Avg_Review_Ratio'],
                amount=row['Amount'],
                best_seller=row['Best Seller']
)
