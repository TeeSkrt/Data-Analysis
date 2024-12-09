import pandas as pd
import glob
import os

# Chỉ định đường dẫn đến các tệp CSV
csv_files = glob.glob("F:/VSCode/Python/Python385/Code Space/Scraping/*.csv")

# Lặp qua từng tệp CSV để thêm cột "category name" và lưu lại
for file in csv_files:
    # Lấy tên danh mục từ tên tệp (bỏ phần mở rộng .csv)
    category_name = os.path.splitext(os.path.basename(file))[0]
    
    # Đọc file CSV và xóa cột "Category name" cũ nếu có
    df = pd.read_csv(file)
    if 'Category name' in df.columns:
        df = df.drop(columns=['Category name'])
    
    # Thêm cột "Category name" mới
    df['Category name'] = category_name  # Thêm cột "category name"
    
    # Ghi đè tệp CSV với cột mới này
    df.to_csv(file, index=False)  # Ghi đè tệp CSV hiện tại

# Sau khi xử lý xong từng file, đọc lại tất cả và tổng hợp vào file tổng
merged_data = pd.concat([pd.read_csv(file) for file in csv_files], ignore_index=True)

# Xóa cột "Category name" trùng lặp nếu có
if 'category name' in merged_data.columns and merged_data.columns.duplicated().any():
    merged_data = merged_data.loc[:, ~merged_data.columns.duplicated()]


# Kiểm tra số lượng sản phẩm ban đầu
initial_count = merged_data.shape[0]

# Xóa các sản phẩm bị trùng dựa trên cột "Asin"
data = merged_data.drop_duplicates(subset='Asin', keep='first')

# Kiểm tra số lượng sản phẩm sau khi xóa
final_count = data.shape[0]

# Tính số sản phẩm đã bị xóa
removed_count = initial_count - final_count

# In ra số lượng sản phẩm đã bị xóa
print(f'Số sản phẩm đã xóa: {removed_count}')

# Lưu tệp CSV sau khi xóa sản phẩm trùng lặp
data.to_csv("master_file.csv", index=False)
