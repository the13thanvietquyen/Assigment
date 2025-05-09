import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import re

# Hàm làm sạch tên file
def sanitize_filename(name):
    return re.sub(r'[^a-zA-Z0-9_]', '_', name)

df = pd.read_csv("results.csv")
os.makedirs("histograms", exist_ok=True)

# Chỉ lấy các cột cụ thể (3 tấn công và 3 phòng thủ)
attack_stats = {
    'shots_on_target_percent': ('Shooting_SoT%', float),
    'shots_on_target_per90': ('Shooting_SoT/90', float),
    'goals_per_shot': ('Shooting_G/Sh', float)
}

defense_stats = {
    'tackles': ('Defense_Tkl', int),
    'tackles_won': ('Defense_TklW', int),
    'dribblers_tackled': ('Defense_Att', int)
}

# Kết hợp tất cả các chỉ số cần vẽ
selected_stats = {**attack_stats, **defense_stats}

# Toàn giải
for stat_name, (col_name, col_type) in selected_stats.items():
    plt.figure(figsize=(8, 5))
    plt.hist(df[col_name].dropna(), bins=20, color='skyblue', edgecolor='black')
    plt.title(f"Histogram of {stat_name} ({col_name}) - All Players")
    plt.xlabel(stat_name)
    plt.ylabel("Frequency")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout(pad=2.0)
    safe_col = sanitize_filename(col_name)
    plt.savefig(f"histograms/{safe_col}_all.png")
    plt.show()
    plt.close()

# Từng đội
for team in df["Team"].dropna().unique():
    team_df = df[df["Team"] == team]
    for stat_name, (col_name, col_type) in selected_stats.items():
        plt.figure(figsize=(8, 5))
        plt.hist(team_df[col_name].dropna(), bins=20, color='lightcoral', edgecolor='black')
        plt.title(f"Histogram of {stat_name} ({col_name}) - {team}")
        plt.xlabel(stat_name)
        plt.ylabel("Frequency")
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout(pad=2.0)
        safe_col = sanitize_filename(col_name)
        safe_team = sanitize_filename(team)
        plt.savefig(f"histograms/{safe_col}_{safe_team}.png")
        plt.show()
        plt.close()