import pandas as pd
from itertools import combinations

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

# Tính Support cho từng sản phẩm
support = df_onehot.mean()

# Tính Support cho các cặp sản phẩm (2-itemset)
pair_support = {}
pairs = combinations(df_onehot.columns, 2)
for pair in pairs:
    pair_support[pair] = (df_onehot[list(pair)].all(axis=1).sum()) / len(df_onehot)

# Tính Confidence cho các quy tắc kết hợp
pair_confidence = {}
for pair in pair_support:
    support_ab = pair_support[pair]
    support_a = support[pair[0]]
    confidence = support_ab / support_a
    pair_confidence[pair] = confidence

# Đặt ngưỡng Support và Confidence
support_threshold = 0.03
confidence_threshold = 0.5

# Lọc ra các quy tắc kết hợp thỏa mãn ngưỡng
rules = [(pair, support_ab, support[pair[0]], confidence) 
         for pair, support_ab, confidence in zip(pair_support.keys(), pair_support.values(), pair_confidence.values()) 
         if support_ab >= support_threshold and confidence >= confidence_threshold]

print("\nCác quy tắc kết hợp thỏa mãn ngưỡng:")
for rule in rules:
    print(f"Quy tắc: {rule[0]} - Support: {rule[1]:.2f} - Confidence: {rule[3]:.2f}")