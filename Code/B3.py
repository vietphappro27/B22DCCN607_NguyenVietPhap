from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
import pandas as pd

# lấy dữ liệu từ result
df=pd.read_csv("result.csv")

# 3.1
# Xóa cột không cần thiết
tmp_df = df.drop(columns='player')
# Điền giá trị thiếu bằng 0
tmp_df = tmp_df.fillna(0)
# Chuyển đổi dữ liệu dạng String thành one-hot encoding
ct = ColumnTransformer(
    transformers=[('encode', OneHotEncoder(), ['nationality', 'position', 'team'])],
    remainder='passthrough'
)
transformed_data = ct.fit_transform(tmp_df)

encoded_columns = ct.named_transformers_['encode'].get_feature_names_out(['nationality', 'position', 'team'])
all_columns = list(encoded_columns) + [col for col in tmp_df.columns if col not in ['nationality', 'position', 'team']]
tmp_df_transformed = pd.DataFrame(transformed_data, columns=all_columns)

scaler = StandardScaler()
df_scaled = scaler.fit_transform(tmp_df_transformed)

wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
    kmeans.fit(df_scaled)
    wcss.append(kmeans.inertia_)


plt.figure(figsize=(10,6))
plt.plot(range(1, 11), wcss,'bx-')
plt.xlabel("K")
plt.ylabel("Distorsion")
plt.title("Elbow")
plt.show()

n_clusters=5
kmeans = KMeans(n_clusters=n_clusters, init='k-means++', random_state=42)
y_kmeans = kmeans.fit_predict(df_scaled)
tmp_df_transformed['Cluster'] = y_kmeans

# 3.2
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# Áp dụng PCA
pca = PCA(n_components=2)
data_pca = pca.fit_transform(df_scaled)

# Tạo DataFrame với các thành phần chính và nhãn cụm
df_pca = pd.DataFrame(data_pca, columns=['PC1', 'PC2'])
df_pca['Cluster'] = tmp_df_transformed['Cluster']



# Vẽ biểu đồ các cụm
plt.figure(figsize=(8, 6))
colors = ['r', 'g', 'b','c','m']  
for i in range(n_clusters):
    plt.scatter(df_pca[df_pca['Cluster'] == i]['PC1'], 
                df_pca[df_pca['Cluster'] == i]['PC2'], 
                s=100, 
                c=colors[i], 
                label=f'Cluster {i}')

plt.title('K-Means Clustering with PCA')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.legend()
plt.grid()
plt.show()

# 3.3 
print("Danh sách tên cầu thủ: ",list(df['player']),sep='\n')
p1=input("Mời bạn nhập tên cầu thủ thứ nhất: ").strip()
p2=input("Mời bạn nhập tên cầu thủ thứ hai: ").strip()
list_att=list(df.drop(columns=['player','nationality','position','team'],axis=1).columns)
print("Danh sách các thuộc tính: ",list_att,sep='\n')
Attributes=list(i for i in input("Mời bạn nhập những thuộc tính cần so sánh: ").split())
# p1: Levi Colwill
# p2: Marc Cucurella 
# Attributes= xg npxg xg_assist assists_per90 xg_assist_per90 xg_xg_assist_per90 npxg_xg_assist_per90 shots_per90 shots_on_target_per90 npxg_per_shot
radar_df = df.loc[df['player'].isin([p1,p2]),list(['player']+Attributes)]
print(radar_df.to_string())
import numpy as np
import matplotlib.pyplot as plt
from math import pi

players=[p1,p2]
N = len(Attributes)

# Tính góc cho từng trục
theta = [n / float(N) * 2 * pi for n in range(N)]
theta += theta[:1]  # Đóng vòng tròn cho các góc
# Tạo giá trị cho từng cầu thủ và đóng vòng tròn
values = []
for player in players:
    player_values = radar_df.loc[radar_df['player'] == player, Attributes].values.flatten().tolist()
    values.append(player_values + player_values[:1])  # Đóng vòng tròn

# Tạo biểu đồ radar
fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
colors = ['b', 'r']

# Vẽ dữ liệu cho từng cầu thủ
for i, player_values in enumerate(values):
    ax.plot(theta, player_values, color=colors[i], linewidth=2, label=players[i])
    ax.fill(theta, player_values, facecolor=colors[i], alpha=0.25)

max_value = radar_df.drop(columns='player').max().max()

# Thiết lập các trục và tiêu đề
ax.set_xticks(theta[:-1])
ax.set_xticklabels(Attributes, fontsize=10)
ax.set_title('Player Attribute Comparison', weight='bold', size=16, position=(0.5, 1.1))
ax.set_rgrids([2*max_value/10, 4*max_value/10, 6*max_value/10, 8*max_value/10, 10*max_value/10])  # Điều chỉnh các giá trị trục theo nhu cầu

# Thêm chú thích
ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

# Hiển thị biểu đồ
plt.show()
