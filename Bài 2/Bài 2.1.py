import pandas as pd
import numpy as np

# Đọc dữ liệu từ file CSV
df = pd.read_csv("results.csv")  

# Lọc các cột chứa số liệu thống kê 
numeric_df = df.select_dtypes(include=[np.number])

# Loại bỏ các cột không cần thống kê xếp hạng
exclude_cols = ['Age', 'Standard_Min']
stat_cols = [col for col in numeric_df.columns if col not in exclude_cols]

# Chuẩn bị thông tin cầu thủ để kết hợp
player_info = df[['Player', 'Team']]
top_3_results = []

# Duyệt qua từng cột thống kê
for col in stat_cols:
    top3 = df.nlargest(3, col)[['Player', 'Team', col]]
    bottom3 = df.nsmallest(3, col)[['Player', 'Team', col]]

    # Ghi vào danh sách kết quả
    top_3_results.append(f"Statistic: {col}\nTop 3:")
    top_3_results.extend(top3.to_string(index=False).split('\n'))
    top_3_results.append("Bottom 3:")
    top_3_results.extend(bottom3.to_string(index=False).split('\n'))


# Ghi kết quả ra file
with open("top_3.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(top_3_results))
