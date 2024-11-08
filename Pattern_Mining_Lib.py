import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

# Đọc dữ liệu từ tệp Excel
file_path = 'Chapter12-1a.xlsx'  # Đường dẫn đến tệp Excel
sheet_name = 'Sheet1'  # Tên sheet bạn muốn đọc (thay đổi nếu cần)

# Sử dụng pandas để đọc tệp Excel
df = pd.read_excel(file_path, sheet_name=sheet_name)

# Hiển thị dữ liệu giao dịch
print("Dữ liệu giao dịch ban đầu:")
print(df)
# Chuyển đổi dữ liệu thành One-Hot Encoding
# Đếm số lượng sản phẩm trong từng ReceiptNo và ItemCode (chỉ đánh dấu 1 nếu ItemCode có mặt trong ReceiptNo)
df_onehot = df.pivot_table(index='ReceiptNo', columns='ItemCode', aggfunc='size', fill_value=0)
df_onehot = df_onehot.applymap(lambda x: 1 if x > 0 else 0)  # Đưa về giá trị 0 hoặc 1

print("\nDữ liệu dạng One-Hot Encoding:")
print(df_onehot)

# Tìm các tập phổ biến với ngưỡng Support
frequent_itemsets = apriori(df_onehot, min_support=0.03, use_colnames=True)
print("\nTập phổ biến:")
print(frequent_itemsets)

# Khai thác các quy tắc kết hợp với ngưỡng Confidence
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.5, num_itemsets=len(frequent_itemsets))
print("\nCác quy tắc kết hợp:")
print(rules)
