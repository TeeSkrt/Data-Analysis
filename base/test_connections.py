import pyodbc
import os

# Lấy các biến môi trường từ hệ thống
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')

# Chuỗi kết nối ODBC
connection_string = f'Driver={{ODBC Driver 17 for SQL Server}};Server=tcp:{db_host},1433;Database={db_name};Uid={db_user};Pwd={db_password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'

try:
    # Cố gắng kết nối tới SQL Server
    conn = pyodbc.connect(connection_string)
    print("Kết nối thành công!")
except Exception as e:
    print(f"Không thể kết nối: {str(e)}")

