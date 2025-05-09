import pandas as pd
import numpy as np

# Đọc dữ liệu
df = pd.read_csv("results.csv")

# Xác định các cột số
exclude_cols = ['Age', 'Standard_Min']
stat_cols = [col for col in df.select_dtypes(include=[np.number]).columns if col not in exclude_cols]

# Tính Median, Mean, Std 
overall = {"Team": "all"}
for col in stat_cols:
    overall[f"Median of {col}"] = df[col].median(skipna=True) if not df[col].dropna().empty else 0
    overall[f"Mean of {col}"] = df[col].mean(skipna=True) if not df[col].dropna().empty else 0
    overall[f"Std of {col}"] = df[col].std(skipna=True) if not df[col].dropna().empty else 0

# Tính theo từng đội
teams_stats = []
for team, group in df.groupby("Team"):
    row = {"Team": team}
    for col in stat_cols:
        row[f"Median of {col}"] = group[col].median(skipna=True) if not group[col].dropna().empty else 0
        row[f"Mean of {col}"] = group[col].mean(skipna=True) if not group[col].dropna().empty else 0
        row[f"Std of {col}"] = group[col].std(skipna=True) if not group[col].dropna().empty else 0
    teams_stats.append(row)

# Gộp tất cả kết quả vào DataFrame
result_df = pd.DataFrame([overall] + teams_stats)

# Thay thế toàn bộ NaN còn sót lại bằng 0
result_df.fillna(0, inplace=True)

# Ghi ra file
result_df.to_csv("results2.csv", index=False)
