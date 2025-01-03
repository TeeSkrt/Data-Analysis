import shap
import pandas as pd
import numpy as np
import optuna
import matplotlib.pyplot as plt
import time
import random
import re
import pyodbc
from tqdm import tqdm
from imblearn.over_sampling import BorderlineSMOTE
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score, learning_curve, validation_curve
import lightgbm as lgb
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score

# PREPARATION DATASET
# Đọc dữ liệu
data = pd.read_csv('C:/Users/ADMIN/Desktop/DATN/Data/Analyst/master_file.csv')

# Đổi tên cột "Title" thành "Product"
data.rename(columns={'Title': 'Product'}, inplace=True)

# Chuyển đổi các giá trị của các cột sang chuỗi và mã hóa thành số
data['Best Seller'] = data['Best Seller'].astype(str)
data['Best Seller'] = data['Best Seller'].map({'Yes': 1, 'No': 0})

# Xử lý dữ liệu cột Rating
data['Rating'] = data['Rating'].str.extract(r'(\d+\.\d+|\d+)')[0]  # Lấy cả số nguyên và số thập phân
data['Rating'] = pd.to_numeric(data['Rating'], errors='coerce').fillna(0).round(1)  # Làm tròn đến 1 chữ số

# Xử lý dữ liệu cột Review
data['Review'] = pd.to_numeric(data['Review'], errors='coerce').fillna(0).astype(int)

# Hàm chuyển đổi các giá trị thành dạng số hoặc NaN nếu không phải giá tiền
def parse_price(price_str):
    if isinstance(price_str, str):
        # Loại bỏ các ký tự không phải số và dấu phẩy
        price_str = re.sub(r'[^\d.]', '', price_str)
        try:
            return float(price_str) if price_str else None
        except ValueError:
            return None
    return price_str

# Áp dụng hàm parse_price vào cột Price
data['Price'] = data['Price'].apply(parse_price)

# Chuyển đổi trực tiếp trên cột Amount
def parse_amount(amount_str):
    if isinstance(amount_str, str):
        match = re.match(r'(\d+)(K\+)?', amount_str)
        if match:
            base = int(match.group(1))  # Lấy số trước 'K'
            if match.group(2):  # Nếu có "K+"
                return random.randint(base * 1000, (base + 1) * 1000 - 1)
            else:  # Nếu không có "K+"
                return base  # Trả lại giá trị gốc
    return 0  # Nếu không đúng định dạng, trả về 0

# Áp dụng hàm parse_amount lên cột Amount
data['Amount'] = data['Amount'].apply(parse_amount)

# Xóa các dòng có giá trị trong cột 'Price', 'Rating', 'Review', 'Amount'đồng thời bằng 0
condition = (data['Price'] == 0) & (data['Rating'] == 0) & (data['Review'] == 0) & (data['Amount'] == 0)
data = data.drop(data[condition].index)

# Tính giá trị trung bình của cột 'price' theo từng danh mục 'Category name' và làm tròn đến 2 chữ số thập phân
avg_price_by_category = data.groupby('Category name')['Price'].mean().round(2).rename('Avg_price')
data = data.merge(avg_price_by_category, on='Category name', how='left')

# Tính giá trị trung bình của cột 'Rating' theo từng danh mục 'Category name'
avg_star_by_category = data.groupby('Category name')['Rating'].mean().round(1).rename('Avg_rating')
data = data.merge(avg_star_by_category, on='Category name', how='left')

# Tính giá trị trung bình của cột 'Review' theo từng danh mục 'Category name'
avg_reviews_by_category = data.groupby('Category name')['Review'].mean().round(0).rename('Avg_review')
data = data.merge(avg_reviews_by_category, on='Category name', how='left')

# Tính giá trị trung bình của cột "Amount" theo từng danh mục "Category name"
avg_amount_by_category = data.groupby('Category name')['Amount'].mean().round(0).rename('Avg_amount')
data = data.merge(avg_amount_by_category, on='Category name', how='left')

# Kiểm tra các giá trị NaN và điền vào giá trị 0
data.fillna(0, inplace=True)

# Thay thế các giá trị bằng 0 bằng giá trị trung bình của danh mục
data['Price'] = data['Price'].mask(data['Price'] == 0, data['Avg_price'])
data['Rating'] = data['Rating'].mask(data['Rating'] == 0, data['Avg_rating'])
data['Review'] = data['Review'].mask(data['Review'] == 0, data['Avg_review'])
data['Amount'] = data['Amount'].mask(data['Amount'] == 0, data['Avg_amount'])

# Tính tỷ lệ Price so với Avg_price
data['Price_Ratio'] = data['Price'] / data['Avg_price']

# Tính tỷ lệ Review so với Rating
data['Review_Rating_Ratio'] = data['Review'] / (data['Rating'] + 1e-5)  # Thêm 1e-5 để tránh chia cho 0

# Tính mức độ phổ biến tương đối của sản phẩm trong từng danh mục
data['Relative_Popularity'] = data['Amount'] / data['Avg_amount']

# Tính số lượng đánh giá so với trung bình của danh mục
data['Review_Avg_Review_Ratio'] = data['Review'] / data['Avg_review']

# Tính tỷ lệ số lượng bán ra
data['Price_Amount_Ratio'] = data['Price'] / (data['Amount'] + 1e-5)

# Tỷ lệ giữa Rating và Review
data['Rating_Review_Ratio'] = data['Rating'] / (data['Review'] + 1e-5)

# Tỷ lệ số lượng bán và tổng số lượng
total_amount = data['Amount'].sum()
data['Popularity_Global_Ratio'] = data['Amount'] / total_amount

# Tỷ lệ số lượng bán và số lượng bán lớn nhất trong cùng danh mục
max_amount_by_category = data.groupby('Category name')['Amount'].max().rename('Max_amount')
data = data.merge(max_amount_by_category, on='Category name', how='left')
data['Popularity_Category_Max_Ratio'] = data['Amount'] / data['Max_amount']
data.drop('Max_amount', axis=1, inplace=True)  # Xóa cột không cần thiết sau khi tính

# Mức độ phổ biến tương đối
data['Price_Rating_Interaction'] = data['Price'] * data['Rating']
data['Review_Amount_Interaction'] = data['Review'] * data['Amount']
data['Combined_Interaction'] = data['Review_Rating_Ratio'] * data['Price_Ratio']

# Sắp xếp lại các cột
columns_order = ['Asin', 'Product','Category name', 'Image', 'Rating', 'Avg_rating',
                'Review', 'Avg_review', 'Price', 'Avg_price','Price_Ratio', 'Review_Rating_Ratio',
                'Relative_Popularity', 'Review_Avg_Review_Ratio', 'Price_Amount_Ratio', 
                'Rating_Review_Ratio', 'Popularity_Global_Ratio', 'Popularity_Category_Max_Ratio', 
                'Price_Rating_Interaction', 'Review_Amount_Interaction', 
                'Combined_Interaction', 'Amount', 'Best Seller']
data = data[columns_order]

# Kiểm tra tổng số dòng và số cột
num_rows, num_cols = data.shape
print(f"Tổng số dòng: {num_rows}")
print(f"Tổng số cột: {num_cols}")

# Kiểm tra thông tin chi tiết về dữ liệu
data_info = data.info()
print(data_info)

# Đánh giá mức độ tương quan giữ liệu
corr_matrix = data.drop(['Asin', 'Product', 'Image', 'Category name'], axis=1)
correlation = corr_matrix.corr(method='spearman')
print(correlation)

# Tính toán xác suất thống kế
describe = data.describe().round(2)
print(describe)


# Xuất DataFrame ra file CSV sau khi xóa
data.to_csv('C:/Users/ADMIN/Desktop/DATN/Data/Analyst/amazon_products.csv', index=False)


# DATA ANALYSIS
# Chia dữ liệu thành tập huấn luyện, tập kiểm tra và tập xác thực
X = data.drop(['Best Seller'], axis=1) # Loại bỏ các cột không phải là đặc trưng

X['original_index'] = X.index # Thêm cột chỉ mục để giữ nguyên thông tin gốc

asin_product = X[['Asin', 'Product', 'Category name', 'Image', 'original_index']] # Lưu lại 'Asin', 'Product' và chỉ mục gốc

X = X.drop(['Asin', 'Product', 'Category name', 'Image'], axis=1) # Loại bỏ 'Asin', 'Product' khỏi X trước khi huấn luyện

y = data['Best Seller'] # Chọn cột Best Seller làm biến mục tiêu

# Xử lý dữ liệu mất cân bằng
print("Resampling data...")
smote = BorderlineSMOTE(sampling_strategy=1, random_state=42)
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

# Tuning hyperparameters với Optuna
def objective(trial):
    params = {
        'objective': 'binary',
        'metric': 'auc',
        'boosting_type': 'gbdt', 
        'learning_rate': trial.suggest_loguniform('learning_rate', 0.0005, 0.005),  
        'num_leaves': trial.suggest_int('num_leaves', 5, 20),  
        'max_depth': trial.suggest_int('max_depth', 3, 7),  
        'min_child_samples': trial.suggest_int('min_child_samples', 150, 300),  
        'min_child_weight': trial.suggest_loguniform('min_child_weight', 20.0, 200.0),
        'min_gain_to_split': trial.suggest_loguniform('min_gain_to_split', 0.01, 0.1),  
        'subsample': trial.suggest_uniform('subsample', 0.4, 0.6),  
        'feature_fraction': trial.suggest_uniform('feature_fraction', 0.4, 0.7),  
        'reg_alpha': trial.suggest_loguniform('reg_alpha', 1.0, 20.0),  
        'reg_lambda': trial.suggest_loguniform('reg_lambda', 1.0, 15.0),  
    }
    
    # Dataset cho LightGBM
    dtrain = lgb.Dataset(X_train, label=y_train)
    dvalid = lgb.Dataset(X_valid, label=y_valid)

    # Huấn luyện mô hình
    gbm = lgb.train(
        params,
        dtrain,
        num_boost_round=500,  # Số vòng lặp
        valid_sets=[dtrain, dvalid],
        callbacks=[
            lgb.early_stopping(stopping_rounds=50),  
            lgb.log_evaluation(50)  
        ]
    )

    # Dự đoán và tính AUC
    y_pred = gbm.predict(X_valid)
    score = roc_auc_score(y_valid, y_pred)
    return score

# # Tuning với Optuna
# print("Tuning hyperparameters using Optuna...")
# study = optuna.create_study(direction='maximize')
# study.optimize(objective, n_trials=100)
# best_params = study.best_params
# best_params['n_estimators'] = 500  

# Các hyperparameter đã điều chỉnh nhằm giảm overfitting
best_params = {
    'objective': 'binary',
    'metric': 'auc',
    'boosting_type': 'gbdt',  
    'learning_rate': 0.005, 
    'num_leaves': 15,  
    'max_depth': 7,  
    'min_child_samples': 250,  
    'min_child_weight': 23.912911702470137,
    'min_gain_to_split': 0.05705170953518958,  
    'subsample': 0.5,  
    'feature_fraction': 0.5,  
    'reg_alpha': 7,  
    'reg_lambda': 15, 
    'n_estimators': 700  
}

# Khởi tạo mô hình với các hyperparameters đã điều chỉnh
print("Training model with the best parameters...")
lgb_model = lgb.LGBMClassifier(**best_params, verbose=-1)
start = time.time()
lgb_model.fit(X_train, y_train)
end = time.time()
print("Training time:", end - start)

# Hàm đánh giá chung cho bất kỳ tập dữ liệu nào
def evaluate_model(model, X_data, y_data, dataset_name):
    y_pred = model.predict(X_data)
    y_prob = model.predict_proba(X_data)[:, 1]  # Lấy xác suất của lớp 1
    
    print(f"Evaluating model on {dataset_name} data...")
    print(f"{dataset_name} Accuracy:", accuracy_score(y_data, y_pred))
    print(f"{dataset_name} Classification Report:\n", classification_report(y_data, y_pred))
    print(f"{dataset_name} ROC AUC Score:", roc_auc_score(y_data, y_prob))
    print("-" * 50)

# Đánh giá mô hình cho 3 tập dữ liệu
evaluate_model(lgb_model, X_train, y_train, "Training")
evaluate_model(lgb_model, X_valid, y_valid, "Validation")
evaluate_model(lgb_model, X_test, y_test, "Test")

# SHAP: Phân tích tầm quan trọng của đặc trưng
print("Explaining model predictions with SHAP...")
# Sử dụng TreeExplainer cho mô hình LightGBM
explainer = shap.TreeExplainer(lgb_model)

# Tạo giá trị SHAP cho tập kiểm tra
shap_values = explainer.shap_values(X_test)

# Kiểm tra và xử lý định dạng SHAP values
if isinstance(shap_values, list):
    if len(shap_values) == 2:  # Trường hợp định dạng cũ
        shap_values_class_1 = shap_values[1]  # Giá trị SHAP cho lớp 1 (Best Seller = 1)
        expected_value_class_1 = explainer.expected_value[1]
    elif len(shap_values) == 1:  # Trường hợp định dạng mới
        shap_values_class_1 = shap_values[0]  # Giá trị SHAP duy nhất cho lớp 1
        expected_value_class_1 = explainer.expected_value
    else:
        raise ValueError("SHAP values có số lượng không hợp lệ!")
elif isinstance(shap_values, np.ndarray):  # Một số phiên bản SHAP chỉ trả về mảng numpy
    shap_values_class_1 = shap_values
    expected_value_class_1 = explainer.expected_value
else:
    raise ValueError("SHAP values không đúng định dạng mong đợi!")

# 1. Hiển thị force plot cho 5 mẫu đầu tiên và lưu thành HTML
print("Generating SHAP force plots for the first 5 samples...")
for i in range(5):
    force_plot_path = f"shap_force_plot_sample_{i + 1}.html"
    shap.save_html(force_plot_path, shap.force_plot(
        expected_value_class_1,
        shap_values_class_1[i, :],
        X_test.iloc[i, :]
    ))
    print(f"SHAP force plot for sample {i + 1} saved to {force_plot_path}")

# Tầm quan trọng trung bình của các đặc trưng
print("Generating SHAP summary plot (bar)...")
plt.figure()
shap.summary_plot(shap_values_class_1, X_test, plot_type="bar", show=False)
plt.savefig("shap_summary_bar.png", bbox_inches='tight')
print("SHAP summary plot (bar) saved to shap_summary_bar.png")

# Đóng góp của từng đặc trưng
print("Generating SHAP summary plot (detailed scatter)...")
plt.figure()
shap.summary_plot(shap_values_class_1, X_test, show=False)
plt.savefig("shap_summary_scatter.png", bbox_inches='tight')
print("SHAP summary plot (scatter) saved to shap_summary_scatter.png")

# Dependence plot cho một số đặc trưng quan trọng
print("Generating SHAP dependence plots for selected features...")
important_features = ["Rating", "Popularity_Global_Ratio", "Relative_Popularity"]
for feature in important_features:
    plt.figure()
    shap.dependence_plot(feature, shap_values_class_1, X_test, show=False)
    plot_path = f"shap_dependence_{feature}.png"
    plt.savefig(plot_path, bbox_inches='tight')
    print(f"SHAP dependence plot for feature {feature} saved to {plot_path}")

# Tính độ quan trọng trung bình của từng đặc trưng
shap_importance = np.abs(shap_values_class_1).mean(axis=0)
importance_df = pd.DataFrame({
    'Feature': X_test.columns,
    'Mean SHAP Value': shap_importance
}).sort_values(by='Mean SHAP Value', ascending=False)

importance_csv_path = "shap_feature_importance.csv"
importance_df.to_csv(importance_csv_path, index=False)
print(f"Feature importance exported to {importance_csv_path}")

# Phân tích các mẫu dự đoán là "Best Seller" và không phải "Best Seller"
print("Analyzing SHAP values for predicted groups...")
y_pred = lgb_model.predict(X_test)
group_1 = shap_values_class_1[y_pred == 1]  # Mẫu dự đoán là Best Seller
group_0 = shap_values_class_1[y_pred == 0]  # Mẫu không phải Best Seller

mean_shap_group_1 = np.abs(group_1).mean(axis=0)
mean_shap_group_0 = np.abs(group_0).mean(axis=0)
group_analysis_df = pd.DataFrame({
    'Feature': X_test.columns,
    'Mean SHAP (Best Seller)': mean_shap_group_1,
    'Mean SHAP (Non-Best Seller)': mean_shap_group_0
}).sort_values(by='Mean SHAP (Best Seller)', ascending=False)

group_analysis_csv_path = "shap_group_analysis.csv"
group_analysis_df.to_csv(group_analysis_csv_path, index=False)
print(f"Group analysis exported to {group_analysis_csv_path}")

# Cross-Validation với Stratified K-Fold
print("Performing Cross-Validation with Stratified K-Fold...")
k = 7
skf = StratifiedKFold(n_splits=k, shuffle=True, random_state=42)
cv_scores = cross_val_score(lgb_model, X_resampled, y_resampled, cv=skf, scoring='accuracy')
print(f"Cross-Validation Scores: {cv_scores}")
print(f"Mean Cross-Validation Score: {np.mean(cv_scores)}")
print(f"Standard Deviation of Cross-Validation Scores: {np.std(cv_scores)}")

# Hàm vẽ Validation Curve cho num_leaves
def plot_validation_curve_num_leaves():
    param_range = np.arange(10, 51, 10)  # Giảm số giá trị kiểm tra của num_leaves

    train_scores, valid_scores = validation_curve(
        lgb.LGBMClassifier(**best_params, verbose=-1),
        X_train, y_train,
        param_name="num_leaves",
        param_range=param_range,
        scoring="roc_auc",
        cv=7  # Giảm số lượng cv để tăng tốc độ
    )

    train_mean = np.mean(train_scores, axis=1)
    valid_mean = np.mean(valid_scores, axis=1)

    plt.figure(figsize=(8, 6))
    plt.plot(param_range, train_mean, label="Training score", color="blue", marker='o')
    plt.plot(param_range, valid_mean, label="Validation score", color="red", marker='o')
    plt.title("Validation Curve for num_leaves")
    plt.xlabel("num_leaves")
    plt.ylabel("ROC AUC Score")
    plt.legend(loc="best")
    plt.grid()

# Hàm vẽ Validation Curve cho learning_rate
def plot_validation_curve_learning_rate():
    param_range = np.logspace(-3, -1, 5)  # Các giá trị learning_rate từ 0.001 đến 0.1

    train_scores, valid_scores = validation_curve(
        lgb.LGBMClassifier(**best_params, verbose=-1),
        X_train, y_train,
        param_name="learning_rate",
        param_range=param_range,
        scoring="roc_auc",
        cv=7 
    )

    train_mean = np.mean(train_scores, axis=1)
    valid_mean = np.mean(valid_scores, axis=1)

    plt.figure(figsize=(8, 6))
    plt.plot(param_range, train_mean, label="Training score", color="blue", marker='o')
    plt.plot(param_range, valid_mean, label="Validation score", color="red", marker='o')
    plt.xscale('log')  # Sử dụng log scale cho learning_rate
    plt.title("Validation Curve for learning_rate")
    plt.xlabel("learning_rate")
    plt.ylabel("ROC AUC Score")
    plt.legend(loc="best")
    plt.grid()

# Hàm vẽ Learning Curve
def plot_learning_curve():
    train_sizes, train_scores, valid_scores = learning_curve(
        lgb.LGBMClassifier(**best_params), X_resampled, y_resampled, 
        cv=7, scoring='accuracy', train_sizes=np.linspace(0.1, 1.0, 5)
    )

    train_mean = np.mean(train_scores, axis=1)
    valid_mean = np.mean(valid_scores, axis=1)

    plt.figure(figsize=(10, 6))
    plt.plot(train_sizes, train_mean, 'o-', color='blue', label='Training score')
    plt.plot(train_sizes, valid_mean, 'o-', color='red', label='Cross-validation score')
    plt.title('Learning Curve')
    plt.xlabel('Training Size')
    plt.ylabel('Accuracy Score')
    plt.legend(loc='best')
    plt.grid()

# Vẽ tất cả các biểu đồ
print("Plotting Validation and Learning Curves...")
plot_validation_curve_num_leaves()
plot_validation_curve_learning_rate()
plot_learning_curve()
plt.show()

# Thêm các cột dữ đoán
y_train_pred = lgb_model.predict(X_train)
y_valid_pred = lgb_model.predict(X_valid)
y_test_pred = lgb_model.predict(X_test)

# Ghép dữ liệu sau khi dự đoán
def merge_and_add_predictions(X, y_pred, asin_product, X_original_index):
    # Khôi phục lại chỉ mục gốc
    X_with_original_index = pd.DataFrame(X)
    X_with_original_index['original_index'] = X_original_index
    
    # Ghép với asin_product và các thông tin khác
    X_with_asin_product = X_with_original_index.merge(asin_product, on='original_index', how='left')
    
    # Thêm cột dự đoán vào DataFrame
    predictions = pd.DataFrame({
        'Asin': X_with_asin_product['Asin'],  
        'Product': X_with_asin_product['Product'],
        'Category name': X_with_asin_product['Category name'],  
        'Image': X_with_asin_product['Image'], 
        'Rating': X_with_asin_product['Rating'],  
        'Avg_rating': X_with_asin_product['Avg_rating'],
        'Review': X_with_asin_product['Review'],
        'Avg_review': X_with_asin_product['Avg_review'],
        'Price': X_with_asin_product['Price'],
        'Avg_price': X_with_asin_product['Avg_price'],
        'Price_Ratio': X_with_asin_product['Price_Ratio'],  
        'Review_Rating_Ratio': X_with_asin_product['Review_Rating_Ratio'],  
        'Relative_Popularity': X_with_asin_product['Relative_Popularity'],
        'Review_Avg_Review_Ratio': X_with_asin_product['Review_Avg_Review_Ratio'],  
        'Price_Amount_Ratio': X_with_asin_product['Price_Amount_Ratio'],  
        'Rating_Review_Ratio': X_with_asin_product['Rating_Review_Ratio'],  
        'Popularity_Global_Ratio': X_with_asin_product['Popularity_Global_Ratio'],  
        'Popularity_Category_Max_Ratio': X_with_asin_product['Popularity_Category_Max_Ratio'],  
        'Price_Rating_Interaction': X_with_asin_product['Price_Rating_Interaction'],  
        'Review_Amount_Interaction': X_with_asin_product['Review_Amount_Interaction'],  
        'Combined_Interaction': X_with_asin_product['Combined_Interaction'],  
        'Amount': X_with_asin_product['Amount'],
        'Predicted Best Seller': y_pred
    })
    
    return predictions

# Sử dụng hàm trên cho từng tập dữ liệu
train_predictions = merge_and_add_predictions(X_train, y_train_pred, asin_product, X_train_original_index)
valid_predictions = merge_and_add_predictions(X_valid, y_valid_pred, asin_product, X_valid_original_index)
test_predictions = merge_and_add_predictions(X_test, y_test_pred, asin_product, X_test_original_index)

# Lưu kết quả vào file CSV
train_predictions.dropna(subset=['Asin', 'Product'], inplace=True)
valid_predictions.dropna(subset=['Asin', 'Product'], inplace=True)
test_predictions.dropna(subset=['Asin', 'Product'], inplace=True)

# Gộp 3 DataFrame lại với nhau
df_combined = pd.concat([test_predictions, valid_predictions, train_predictions], ignore_index=True)

# Lọc sản phẩm bán chạy
best_seller = df_combined[df_combined['Predicted Best Seller'] == 1]

# Mapping lại cột "Predicted Best Seller" thành True/False
df_combined['Predicted Best Seller'] = df_combined['Predicted Best Seller'].map({1: 'True', 0: 'False'})
best_seller['Predicted Best Seller'] = best_seller['Predicted Best Seller'].map({1: 'True', 0: 'False'})

# Xuất file csv
best_seller.to_csv('C:/Users/ADMIN/Desktop/DATN/Data/Analyst/best_seller.csv', index=False)
df_combined.to_csv('C:/Users/ADMIN/Desktop/DATN/Data/Analyst/final.csv', index=False)

# Lưu mô hình đã huấn luyện
lgb_model.booster_.save_model('lgb_model.txt')
print(f"Model and data are saved")

# UPLOAD TO AZURE SQL SERVER
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

# Danh sách các file CSV và tên bảng tương ứng
files_and_tables = [
    ('F:/VSCode/Python/Python385/Code Space/Analyst/final.csv', 'Predictions'),
    ('F:/VSCode/Python/Python385/Code Space/Analyst/best_seller.csv', 'BestSeller')
    
]

# Hàm xử lý từng file
def process(file_path, table_name):
    print(f"Processing file: {file_path}")

    # Đọc file CSV
    df_combined = pd.read_csv(file_path)

    # Xóa bảng nếu tồn tại
    drop_table_query = f"DROP TABLE IF EXISTS {table_name}"
    cursor.execute(drop_table_query)

    # Tạo bảng mới
    print(f"Creating table {table_name}...")
    create_table_query = f"""
    CREATE TABLE {table_name} (
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
    print(f"Uploading data to table {table_name}...")
    insert_query = f"""
        INSERT INTO {table_name} (
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
    with tqdm(total=len(data_tuples), desc=f"Uploading to {table_name}") as pbar:
        for i in range(0, len(data_tuples), batch_size):
            batch = data_tuples[i:i + batch_size]
            cursor.executemany(insert_query, batch)  # Gửi batch
            conn.commit()  # Commit sau mỗi batch
            pbar.update(len(batch))  # Cập nhật tiến trình

    print(f"Data has been uploaded to table {table_name} successfully.")

# Xử lý từng file và bảng
for file_path, table_name in files_and_tables:
    process(file_path, table_name)

# Kết thúc
cursor.close()
conn.close()
print("All files have been processed.")