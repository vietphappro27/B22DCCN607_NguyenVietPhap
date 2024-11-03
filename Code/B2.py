import matplotlib.pyplot as plt
import pandas as pd
import os


# lấy dữ liệu từ result
df=pd.read_csv("result.csv")

# 2.1  
# Tạo thư mục để lưu trữ các bảng top 3
output_dir = 'top_3_tables'
os.makedirs(output_dir, exist_ok=True)

# Tạo dictionary để lưu top 3 giá trị cao nhất và thấp nhất cho mỗi chỉ số
top_3_highest = {}
top_3_lowest = {}

# Duyệt qua từng cột (chỉ số) trong DataFrame, bỏ qua cột đầu tiên ('player')
for col in df.columns[1:]:
    df_sorted = df.sort_values(by=col, ascending=False)
    top_3_highest[col] = df_sorted[['player', col]].head(3)
    top_3_lowest[col] = df_sorted[['player', col]].tail(3)

# Lưu top 3 cầu thủ có điểm cao nhất cho mỗi chỉ số
for col, top in top_3_highest.items():
    plt.figure(figsize=(6, 2))
    plt.axis('tight')
    plt.axis('off')
    plt.title(f'Top 3 cầu thủ có điểm cao nhất ở chỉ số: {col}')
    table_data = top.values
    columns = ['Cầu thủ', col]
    plt.table(cellText=table_data, colLabels=columns, cellLoc='center', loc='center')
    
    # Lưu hình
    filename = f"{output_dir}/top_3_highest_{col}.png"
    plt.savefig(filename, bbox_inches='tight')
    plt.close()  # Đóng hình để tiết kiệm bộ nhớ

# Lưu top 3 cầu thủ có điểm thấp nhất cho mỗi chỉ số
for col, bottom in top_3_lowest.items():
    plt.figure(figsize=(6, 2))
    plt.axis('tight')
    plt.axis('off')
    plt.title(f'Top 3 cầu thủ có điểm thấp nhất ở chỉ số: {col}')
    table_data = bottom.values
    columns = ['Cầu thủ', col]
    plt.table(cellText=table_data, colLabels=columns, cellLoc='center', loc='center')
    
    # Lưu hình
    filename = f"{output_dir}/top_3_lowest_{col}.png"
    plt.savefig(filename, bbox_inches='tight')
    plt.close()  # Đóng hình để tiết kiệm bộ nhớ

# 2.2
# Hàm thêm giá trị thống kê cho từng team
def add_statistics_for_team(team_name, numeric_df, table):
    table['Team'].append(team_name)
    for att in numeric_df.columns:
        table['Median of ' + att].append(float(numeric_df[att].median()))
        table['Mean of ' + att].append(float(numeric_df[att].mean()))
        table['Std of ' + att].append(float(numeric_df[att].std()))

if __name__=='__main__':
    numeric_df = df.select_dtypes(include=['float', 'int'])
    # Tạo dictionary để lưu kết quả
    table = {'Team': []}
    # Khởi tạo các cột cho Median, Mean, Std của từng thuộc tính số
    for att in numeric_df.columns:
        table['Median of ' + att] = []
        table['Mean of ' + att] = []
        table['Std of ' + att] = []
    # Tính toán cho tất cả các đội (team 'all')
    add_statistics_for_team('all', numeric_df, table)

    teams=['all']
    teams.extend(df['team'].unique())

    # Tính toán cho từng đội
    for team in teams[1:]:  
        # Bỏ qua 'all' vì đã tính toán trước
        filtered_df = df[df['team'] == team]
        numeric_df = filtered_df.select_dtypes(include=['float', 'int'])
        add_statistics_for_team(team, numeric_df, table)

    # Tạo DataFrame từ dictionary 'table'
    result2 = pd.DataFrame(table)

    # lưu vào result2.csv 
    result2.to_csv('result2.csv', index=False)

# 2.3
import matplotlib.pyplot as plt
import os

# Tạo một thư mục để lưu trữ hình ảnh histogram
output_dir = 'histograms'
os.makedirs(output_dir, exist_ok=True)

# Chọn các cột số
numeric_df = df.select_dtypes(include=['float', 'int'])

# Khởi tạo bộ đếm
cnt = 0

# Lưu histogram cho toàn bộ giải đấu
for att in numeric_df.columns:
    cnt += 1
    print("Đang lưu histogram:", cnt)
    plt.figure(figsize=(5, 3))
    plt.hist(numeric_df[att], bins=10, alpha=0.7, color='blue', edgecolor='black')
    plt.title(f'Hình chóp của {att} (Tất cả các đội)')
    plt.xlabel(att)
    plt.ylabel('Tần suất')
    plt.grid(axis='y', alpha=0.75)
    
    # Lưu hình
    filename = f"{output_dir}/histogram_{att}_all_teams.png"
    plt.savefig(filename)
    plt.close()  # Đóng hình để tiết kiệm bộ nhớ

# Lưu histogram cho mỗi đội
teams = df['team'].unique()

for team in teams:
    # Lọc cầu thủ cho mỗi đội
    filtered_df = df[df['team'] == team]
    numeric_df_team = filtered_df.select_dtypes(include=['float', 'int'])
    
    # Lưu histogram cho các thuộc tính của mỗi đội
    for att in numeric_df_team.columns:
        cnt += 1
        print("Đang lưu histogram:", cnt)
        plt.figure(figsize=(5, 3))
        plt.hist(numeric_df_team[att], bins=10, alpha=0.7, color='green', edgecolor='black')
        plt.title(f'Hình chóp của {att} ({team})')
        plt.xlabel(att)
        plt.ylabel('Tần suất')
        plt.grid(axis='y', alpha=0.75)
        
        # Lưu hình
        filename = f"{output_dir}/histogram_{att}_{team}.png"
        plt.savefig(filename)
        plt.close()  # Đóng hình để tiết kiệm bộ nhớ

# 2.4
df2=pd.read_csv('result2.csv')
df2.drop(index=0,inplace=True)
numeric_columns = df2.select_dtypes(include=['float', 'int']).columns

# Tạo danh sách để lưu kết quả cho mỗi thuộc tính
highest_team_per_stat = []

for column in numeric_columns:
    # Tìm chỉ số dòng có giá trị lớn nhất cho thuộc tính
    max_idx = df2[column].idxmax()
    
    # Lấy tên đội bóng và giá trị của thuộc tính tại chỉ số này
    max_team = df2.loc[max_idx, 'Team']
    max_score = df2.loc[max_idx, column]
    
    # Thêm kết quả vào danh sách
    highest_team_per_stat.append({
        'Attribute': column,
        'Team': max_team,
        'Highest Score': max_score
    })

# Chuyển đổi danh sách kết quả thành DataFrame
highest_team_per_stat_df = pd.DataFrame(highest_team_per_stat)

# Hiển thị kết quả
print(highest_team_per_stat_df.to_string())
# đếm  xem mỗi đội bóng có bao nhiêu chỉ số điểm cao nhất 
print(highest_team_per_stat_df['Team'].value_counts())

# Lấy đội bóng có số lượng chỉ số điểm cao nhất
team_counts = highest_team_per_stat_df['Team'].value_counts()
highest_team = team_counts.idxmax()
highest_count = team_counts.max()

# Hiển thị kết quả
print(f"Đội bóng có số chỉ số điểm cao nhất: {highest_team} với {highest_count} chỉ số.")

