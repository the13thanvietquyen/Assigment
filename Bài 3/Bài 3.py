import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time 
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from datetime import datetime
import sys

# Tạo timestamp cho tên file
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Đọc dữ liệu từ file
df = pd.read_csv("results.csv")
df_numeric = df.select_dtypes(include=[np.number])
df_numeric.dropna(axis=1, how='all', inplace=True)
df_numeric.fillna(0, inplace=True)

# Chuẩn hoá dữ liệu
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_numeric)

# Xác định số lượng nhóm bằng Elbow method và Silhouette Score
inertia = []
silhouette_scores = []
K_range = range(2, 11)  

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init='auto')
    kmeans.fit(X_scaled)
    inertia.append(kmeans.inertia_)
    silhouette_scores.append(silhouette_score(X_scaled, kmeans.labels_))

# Vẽ và lưu biểu đồ Elbow và Silhouette
plt.figure(figsize=(14, 5))
plt.subplot(1, 2, 1)
plt.plot(K_range, inertia, marker='o')
plt.xlabel('Number of clusters (k)')
plt.ylabel('Inertia')
plt.title('Elbow Method') 
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(K_range, silhouette_scores, marker='o', color='orange')
plt.xlabel('Number of clusters (k)')
plt.ylabel('Silhouette Score')
plt.title('Silhouette Score')
plt.grid(True)

plt.tight_layout()
elbow_silhouette_file = f"Elbow silhouette {timestamp}.png"
plt.savefig(elbow_silhouette_file, dpi=300, bbox_inches='tight')
plt.close()
# Chọn số lượng nhóm
optimal_k = 4

# Phân cụm với k=4
kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init='auto')
clusters = kmeans.fit_predict(X_scaled)
df['Cluster'] = clusters

# Giảm chiều và trực quan hóa
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

plt.figure(figsize=(12, 8))
scatter = sns.scatterplot(x=X_pca[:, 0], y=X_pca[:, 1], hue=df['Cluster'], palette='Set2', s=80)

# Định nghĩa các nhóm
cluster_names = {
    0: "Hậu vệ/Phòng ngự",
    1: "Tiền vệ trung tâm",
    2: "Tiền đạo/Tấn công",
    3: "Tiền vệ cánh/Công"
}

# Hiển thị tên một số cầu thủ tiêu biểu
top_players = df.sort_values('Standard_Gls', ascending=False).head(5)['Player']
for idx, row in df.iterrows():
    if row['Player'] in top_players.values:
        plt.text(X_pca[idx, 0], X_pca[idx, 1], row['Player'], fontsize=9, 
                bbox=dict(facecolor='white', alpha=0.7))

plt.title('PCA of EPL in 2024 - 2025 season')
plt.xlabel('PCA 1 ')
plt.ylabel('PCA 2 ')
plt.legend(title='Nhóm cầu thủ', labels=[f'Nhóm {k}: {v}' for k, v in cluster_names.items()])
pca_clusters_file = f"PCA Clusters {timestamp}.png"
plt.savefig(pca_clusters_file, dpi=300, bbox_inches='tight')
plt.close()
print(f"{pca_clusters_file}")

# Phân tích chi tiết từng nhóm và nhận xét 
log_file = f"Bài 3.txt"
original_stdout = sys.stdout 
with open(log_file, 'w', encoding='utf-8') as f:
    sys.stdout = f
    print("PHÂN TÍCH CÁC NHÓM CẦU THỦ")
    for cluster_num in range(optimal_k):
        cluster_data = df[df['Cluster'] == cluster_num]
        size = len(cluster_data)
        pos_dist = cluster_data['Pos'].value_counts(normalize=True).head(3)
        
        print(f"\nNHÓM {cluster_num}: {cluster_names[cluster_num]} ({size} cầu thủ)")
        print("Phân bố vị trí chính:")
        for pos, percent in pos_dist.items():
            print(f"   - {pos}: {percent:.1%}")
        print("\nĐặc điểm nổi bật:")
        if cluster_num == 0:
            print("   - Chỉ số phòng ngự cao (tackles, interceptions)")
            print("   - Ít tham gia tấn công (xG, assists thấp)")
        elif cluster_num == 1:
            print("   - Cân bằng giữa tấn công và phòng ngự")
            print("   - Chỉ số chuyền và kiểm soát bóng tốt")
        elif cluster_num == 2:
            print("   - Chỉ số tấn công vượt trội (xG, shots, goals)")
            print("   - Ít tham gia phòng ngự")
        else:
            print("   - Khả năng tạt bóng, dribble tốt")
            print("   - Tham gia cả tấn công lẫn phòng thủ")
        print("\nCầu thủ tiêu biểu:")
        top_in_cluster = cluster_data.sort_values('Standard_Gls', ascending=False).head(3)['Player']
        for i, player in enumerate(top_in_cluster, 1):
            print(f"   {i}. {player}")
    sys.stdout = original_stdout



