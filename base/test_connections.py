import pyodbc
import os

db_name = os.getenv('DB_NAME', 'amazon_sales')
db_user = os.getenv('DB_USER', 'azure_sa')
db_password = os.getenv('DB_PASSWORD', '@123456A')
db_host = os.getenv('DB_HOST', 'amazon-sql-server.database.windows.net')
db_port = os.getenv('DB_PORT', '1433')

try:
    # Cố gắng kết nối tới SQL Server
    conn = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={db_host},{db_port};'
        f'DATABASE={db_name};'
        f'UID={db_user};'
        f'PWD={db_password};'
        'TrustServerCertificate=yes;'
        'Connection Timeout=60;'
    )
    print("Kết nối thành công!")
except Exception as e:
    print(f"Không thể kết nối: {str(e)}")
