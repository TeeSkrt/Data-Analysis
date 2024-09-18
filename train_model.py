import pandas as pd
import numpy as np
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score, learning_curve
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
from joblib import dump
import numpy as np
import matplotlib.pyplot as plt
import time

# PREPARATION DATASET
# Đọc dữ liệu
data = pd.read_csv('F:/VSCode/Python/Python385/Code Space/Analyst/amazon_merged.csv')
data_cat = pd.read_csv('F:/VSCode/Python/Python385/Code Space/Analyst/amazon_categories.csv')
categories_id_name = pd.read_csv('F:/VSCode/Python/Python385/Code Space/Analyst/amazon_categories.csv')

# Chuyển đổi các giá trị của cột isBestSeller sang chuỗi
data['isBestSeller'] = data['isBestSeller'].astype(str)

# Mã hóa cột isBestSeller
data['isBestSeller'] = data['isBestSeller'].map({'True': 1, 'False': 0})

# Xóa các dòng có giá trị trong cột 'price', 'stars', 'reviews', 'boughtInLastMonth'đồng thời bằng 0
condition = (data['price'] == 0) & (data['stars'] == 0) & (data['reviews'] == 0) & (data['boughtInLastMonth'] == 0)
data = data.drop(data[condition].index)

# Tính giá trị trung bình của cột 'price' theo từng danh mục 'category_name' và làm tròn đến 2 chữ số thập phân
avg_price_by_category = data.groupby('category_name')['price'].mean().round(2).rename('avg_price')
data = data.merge(avg_price_by_category, on='category_name', how='left')

# Thay thế các giá trị bằng 0 trong cột 'price' bằng giá trị trung bình của danh mục
data['price'] = data.apply(lambda row: row['avg_price'] if row['price'] == 0 else row['price'], axis=1)

# Tính giá trị trung bình của cột 'stars' theo từng danh mục 'category_name'
avg_star_by_category = data.groupby('category_name')['stars'].mean().round(1).rename('avg_star')
data = data.merge(avg_star_by_category, on='category_name', how='left')

# Tính giá trị trung bình của cột 'reviews' theo từng danh mục 'category_name'
avg_reviews_by_category = data.groupby('category_name')['reviews'].mean().round(2).rename('avg_reviews')
data = data.merge(avg_reviews_by_category, on='category_name', how='left')

# Kiểm tra các giá trị NaN và điền vào giá trị 0
data.fillna(0, inplace=True)

# Sắp xếp lại các cột
columns_order = ['asin', 'product', 'imgUrl', 'productURL', 'stars', 'avg_star', 
                 'reviews', 'avg_reviews', 'price', 'avg_price', 'listPrice', 'category_id', 
                 'category_name', 'boughtInLastMonth', 'isBestSeller']
data = data[columns_order]

# Kiểm tra tổng số dòng và số cột
num_rows, num_cols = data.shape
print(f"Tổng số dòng: {num_rows}")
print(f"Tổng số cột: {num_cols}")

# Kiểm tra thông tin chi tiết về dữ liệu
data_info = data.info()
print(data_info)

# Đánh giá mức độ tương quan giữ liệu
corr_matrix = data.drop(['asin', 'product', 'imgUrl', 'productURL', 'category_id', 'category_name'], axis=1)
correlation = corr_matrix.corr(method='spearman')
print(correlation)
# Tính toán xác suất thống kế
describe = data.describe().applymap(lambda x: round(x, 2))
print(describe)

# Kết hợp giá trị trung bình vào DataFrame
data_cat = data_cat.merge(avg_price_by_category, on='category_name', how='left')
data_cat = data_cat.merge(avg_star_by_category, on='category_name', how='left')

# Xuất DataFrame ra file CSV sau khi xóa
data.to_csv('F:/VSCode/Python/Python385/Code Space/Analyst/amazon_products_merged.csv', index=False)
data_cat.to_csv('F:/VSCode/Python/Python385/Code Space/Analyst/amazon_categories_merged.csv', index=False)

# DATA ANALYSIS
# Loại bỏ các cột không phải là đặc trưng
X = data.drop(['isBestSeller', 'category_name', 'imgUrl', 'productURL'], axis=1)

# Thêm cột chỉ mục để giữ nguyên thông tin gốc
X['original_index'] = X.index

# Lưu lại 'asin', 'product' và chỉ mục gốc
asin_product = X[['asin', 'product', 'original_index']]

# Loại bỏ 'asin', 'product' khỏi X trước khi huấn luyện
X = X.drop(['asin', 'product'], axis=1)

# Chọn cột isBestSeller làm biến mục tiêu
y = data['isBestSeller']

# Xử lý dữ liệu mất cân bằng
print("Resampling data...")
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)

# Lưu lại 'original_index' trước khi chia
X_resampled['original_index'] = asin_product['original_index']

# Chia dữ liệu thành tập huấn luyện, tập xác thực và tập kiểm tra
print("Splitting data into training and test sets...")
X_train_full, X_valid, y_train_full, y_valid = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X_train_full, y_train_full, test_size=0.25, random_state=42)  # 0.25 x 0.8 = 0.2

# Lưu lại 'original_index' để sử dụng sau này
X_test_original_index = X_test['original_index']
X_train_original_index = X_train['original_index']
X_valid_original_index = X_valid['original_index']

# Loại bỏ 'original_index' trước khi huấn luyện
X_train = X_train.drop(['original_index'], axis=1)
X_valid = X_valid.drop(['original_index'], axis=1)
X_test = X_test.drop(['original_index'], axis=1)

# Các hyperparameter đã điều chỉnh
best_params = {
    'learning_rate': 0.07,  # Giảm learning_rate
    'max_depth': 4,  # Giảm max_depth
    'min_samples_leaf': 10,  # Tăng min_samples_leaf
    'min_samples_split': 20,  # Tăng min_samples_split
    'n_estimators': 150,  # Giảm số lượng cây
    'subsample': 0.7  # Giảm subsample
}


# Khởi tạo mô hình với hyperparameter tốt nhất
best_gb = GradientBoostingClassifier(**best_params, random_state=42)

# Huấn luyện mô hình
print("Training Gradient Boosting model...")
start = time.time()
best_gb.fit(X_train, y_train)
end = time.time()
print("Training time:", end - start)

# Đánh giá mô hình trên dữ liệu huấn luyện
print("Evaluating model on training data...")
y_train_pred = best_gb.predict(X_train)
print("Training Accuracy:", accuracy_score(y_train, y_train_pred))
print("Training Classification Report:\n", classification_report(y_train, y_train_pred))
print("Training ROC AUC Score:", roc_auc_score(y_train, y_train_pred))

# Đánh giá mô hình trên tập xác thực
print("Evaluating model on validation data...")
y_valid_pred = best_gb.predict(X_valid)
print("Validation Accuracy:", accuracy_score(y_valid, y_valid_pred))
print("Validation Classification Report:\n", classification_report(y_valid, y_valid_pred))
print("Validation ROC AUC Score:", roc_auc_score(y_valid, y_valid_pred))

# Đánh giá mô hình trên dữ liệu kiểm tra
print("Evaluating model on test data...")
y_test_pred = best_gb.predict(X_test)
print("Test Accuracy:", accuracy_score(y_test, y_test_pred))
print("Test Classification Report:\n", classification_report(y_test, y_test_pred))
print("Test ROC AUC Score:", roc_auc_score(y_test, y_test_pred))

# Cross-Validation với Stratified K-Fold
print("Performing Cross-Validation with Stratified K-Fold...")
k = 7
skf = StratifiedKFold(n_splits=k, shuffle=True, random_state=42)
cv_scores = cross_val_score(best_gb, X_resampled, y_resampled, cv=skf, scoring='accuracy')
print(f"Cross-Validation Scores: {cv_scores}")
print(f"Mean Cross-Validation Score: {np.mean(cv_scores)}")
print(f"Standard Deviation of Cross-Validation Scores: {np.std(cv_scores)}")

# Learning Curves
print("Plotting Learning Curves...")
train_sizes, train_scores, test_scores = learning_curve(
    best_gb, X_resampled, y_resampled, cv = 7, scoring='accuracy',
    train_sizes=np.linspace(0.1, 1.0, 10)
)

train_mean = np.mean(train_scores, axis=1)
train_std = np.std(train_scores, axis=1)
test_mean = np.mean(test_scores, axis=1)
test_std = np.std(test_scores, axis=1)

plt.figure(figsize=(10, 6))
plt.plot(train_sizes, train_mean, 'o-', color='blue', label='Training score')
plt.plot(train_sizes, test_mean, 'o-', color='red', label='Cross-validation score')
plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, color='blue', alpha=0.1)
plt.fill_between(train_sizes, test_mean - test_std, test_mean + test_std, color='red', alpha=0.1)
plt.title('Learning Curve')
plt.xlabel('Training Size')
plt.ylabel('Accuracy Score')
plt.legend(loc='best')
plt.grid()
plt.show()

# Sau khi dự đoán xong, khôi phục lại chỉ mục gốc của tập huấn luyện
X_train_with_original_index = pd.DataFrame(X_train)
X_train_with_original_index['original_index'] = X_train_original_index

# Sử dụng chỉ mục gốc để ghép lại với 'asin' và 'product'
X_train_with_asin_product = X_train_with_original_index.merge(asin_product, on='original_index', how='left')

# Kết hợp kết quả dự đoán với 'asin', 'product'
train_predictions = pd.DataFrame({
    'asin': X_train_with_asin_product['asin'],
    'product': X_train_with_asin_product['product'],
    'category_id': X_train_with_asin_product['category_id'],
    'stars': X_train_with_asin_product['stars'],
    'avg_star': X_train_with_asin_product['avg_star'],
    'reviews': X_train_with_asin_product['reviews'],
    'avg_reviews': X_train_with_asin_product['avg_reviews'],
    'price': X_train_with_asin_product['price'],
    'avg_price': X_train_with_asin_product['avg_price'],
    'listPrice': X_train_with_asin_product['listPrice'],
    'boughtInLastMonth': X_train_with_asin_product['boughtInLastMonth'],
    'PredictedIsBestSeller': y_train_pred
})

# Lưu kết quả dự đoán vào file CSV
train_predictions.dropna(subset=['asin', 'product'], inplace=True)

# Sau khi dự đoán xong, khôi phục lại chỉ mục gốc của tập xác thực
X_valid_with_original_index = pd.DataFrame(X_valid)
X_valid_with_original_index['original_index'] = X_valid_original_index

# Sử dụng chỉ mục gốc để ghép lại với 'asin' và 'product'
X_valid_with_asin_product = X_valid_with_original_index.merge(asin_product, on='original_index', how='left')

# Kết hợp kết quả dự đoán với 'asin', 'product'
valid_predictions = pd.DataFrame({
    'asin': X_valid_with_asin_product['asin'],
    'product': X_valid_with_asin_product['product'],
    'category_id': X_valid_with_asin_product['category_id'],
    'stars': X_valid_with_asin_product['stars'],
    'avg_star': X_valid_with_asin_product['avg_star'],
    'reviews': X_valid_with_asin_product['reviews'],
    'avg_reviews': X_valid_with_asin_product['avg_reviews'],
    'price': X_valid_with_asin_product['price'],
    'avg_price': X_valid_with_asin_product['avg_price'],
    'listPrice': X_valid_with_asin_product['listPrice'],
    'boughtInLastMonth': X_valid_with_asin_product['boughtInLastMonth'],
    'PredictedIsBestSeller': y_valid_pred
})

# Lưu kết quả dự đoán vào file CSV
valid_predictions.dropna(subset=['asin', 'product'], inplace=True)

# Sau khi dự đoán xong, khôi phục lại chỉ mục gốc của tập kiểm tra
X_test_with_original_index = pd.DataFrame(X_test)
X_test_with_original_index['original_index'] = X_test_original_index

# Sử dụng chỉ mục gốc để ghép lại với 'asin' và 'product'
X_test_with_asin_product = X_test_with_original_index.merge(asin_product, on='original_index', how='left')

# Kết hợp kết quả dự đoán với 'asin', 'product'
test_predictions = pd.DataFrame({
    'asin': X_test_with_asin_product['asin'],
    'product': X_test_with_asin_product['product'],
    'category_id': X_test_with_asin_product['category_id'],
    'stars': X_test_with_asin_product['stars'],
    'avg_star': X_test_with_asin_product['avg_star'],
    'reviews': X_test_with_asin_product['reviews'],
    'avg_reviews': X_test_with_asin_product['avg_reviews'],
    'price': X_test_with_asin_product['price'],
    'avg_price': X_test_with_asin_product['avg_price'],
    'listPrice': X_test_with_asin_product['listPrice'],
    'boughtInLastMonth': X_test_with_asin_product['boughtInLastMonth'],
    'PredictedIsBestSeller': y_test_pred
})

# Lưu kết quả dự đoán vào file CSV
test_predictions.dropna(subset=['asin', 'product'], inplace=True)
# 
# Gộp 3 DataFrame lại với nhau
df_combined = pd.concat([test_predictions, valid_predictions, train_predictions], ignore_index=True)

# Ghép "category_name" vào DataFrame kết quả
df_combined = df_combined.merge(categories_id_name, on='category_id', how='left')
order = ['asin', 'product', 'category_id', 'category_name', 'stars', 'avg_star', 'reviews', 
         'avg_reviews', 'price', 'avg_price', 'listPrice', 'boughtInLastMonth', 'PredictedIsBestSeller']
df_combined = df_combined[order]

# Mapping lại cột "PredictedIsBestSeller" thành True/False
df_combined['PredictedIsBestSeller'] = df_combined['PredictedIsBestSeller'].map({1: 'True', 0: 'False'})

# Lọc sản phẩm bán chạy
best_seller = df_combined[df_combined['PredictedIsBestSeller'] == 1]

# Xuất file csv
best_seller.to_csv('F:/VSCode/Python/Python385/Code Space/Analyst/best_seller.csv', index=False)
df_combined.to_csv('F:/VSCode/Python/Python385/Code Space/Analyst/final.csv', index=False)

# Lưu mô hình đã huấn luyện
dump(best_gb, 'gradient_boosting_model.pkl')
print(f"Model and data are saved")


