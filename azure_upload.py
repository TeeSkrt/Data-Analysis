import pyodbc
import pandas as pd
from tqdm import tqdm

# Đọc file CSV
df_combined = pd.read_csv('F:/VSCode/Python/Python385/Code Space/Analyst/best_seller.csv')

# Thông tin kết nối đến Azure SQL
print("Connecting to Azure SQL...")
server = 'amazon-sql-server.database.windows.net'
database = 'amazon_sales'
username = 'azure_sa'
password = '@123456A'
driver = 'ODBC Driver 17 for SQL Server'

conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Xóa bảng nếu tồn tại
drop_table_query = "DROP TABLE IF EXISTS BestSeller"
cursor.execute(drop_table_query)

# Tạo bảng mới
print("Creating table BestSeller...")
create_table_query = """
CREATE TABLE BestSeller (
    Asin VARCHAR(50),
    Product VARCHAR(500),
    Category_name VARCHAR(255),
    Image VARCHAR(255),
    Rating FLOAT,
    Avg_rating FLOAT,
    Review INT,
    Avg_review FLOAT,
    Price FLOAT,
    Avg_price FLOAT,
    Price_Ratio FLOAT,
    Review_Rating_Ratio FLOAT,
    Relative_Popularity FLOAT,
    Review_Avg_Review_Ratio FLOAT,
    Price_Amount_Ratio FLOAT,
    Rating_Review_Ratio FLOAT,
    Popularity_Global_Ratio FLOAT,
    Popularity_Category_Max_Ratio FLOAT,
    Price_Rating_Interaction FLOAT,
    Review_Amount_Interaction FLOAT,
    Combined_Interaction FLOAT,
    Amount INT,
    Predicted_Best_Seller VARCHAR(5) -- TRUE or FALSE
)
"""
cursor.execute(create_table_query)
conn.commit()

# Chuẩn bị câu lệnh INSERT
print("Uploading data to Azure SQL...")
insert_query = """
    INSERT INTO BestSeller (
        Asin, Product, Category_name, Image, Rating, Avg_rating, Review, Avg_review,
        Price, Avg_price, Price_Ratio, Review_Rating_Ratio, Relative_Popularity, 
        Review_Avg_Review_Ratio, Price_Amount_Ratio, Rating_Review_Ratio, 
        Popularity_Global_Ratio, Popularity_Category_Max_Ratio, 
        Price_Rating_Interaction, Review_Amount_Interaction, Combined_Interaction, 
        Amount, Predicted_Best_Seller
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

# Chuyển DataFrame thành danh sách tuple
print("Converting DataFrame to list of tuples...")
data_tuples = [
    (
        row['Asin'], row['Product'], row['Category name'], row['Image'],
        row['Rating'], row['Avg_rating'], row['Review'], row['Avg_review'],
        row['Price'], row['Avg_price'], row['Price_Ratio'], row['Review_Rating_Ratio'],
        row['Relative_Popularity'], row['Review_Avg_Review_Ratio'], row['Price_Amount_Ratio'],
        row['Rating_Review_Ratio'], row['Popularity_Global_Ratio'], row['Popularity_Category_Max_Ratio'],
        row['Price_Rating_Interaction'], row['Review_Amount_Interaction'], row['Combined_Interaction'],
        row['Amount'], row['Predicted Best Seller']
    )
    for _, row in df_combined.iterrows()
]

# Gửi dữ liệu theo batch với tqdm
batch_size = 1000
with tqdm(total=len(data_tuples), desc="Uploading to Azure SQL") as pbar:
    for i in range(0, len(data_tuples), batch_size):
        batch = data_tuples[i:i + batch_size]
        cursor.executemany(insert_query, batch)  # Gửi batch
        conn.commit()  # Commit sau mỗi batch
        pbar.update(len(batch))  # Cập nhật tiến trình

# Kết thúc
print("Data has been uploaded successfully.")
cursor.close()
conn.close()


