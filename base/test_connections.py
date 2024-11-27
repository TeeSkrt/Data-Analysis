import pymssql
import os

db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT', '1433')

try:
    # Cố gắng kết nối tới SQL Server
    conn = pymssql.connect(
        server=db_host, 
        user=db_user, 
        password=db_password, 
        database=db_name, 
        port=int(db_port)
    )
    print("Kết nối thành công!")
except Exception as e:
    print(f"Không thể kết nối: {str(e)}")
