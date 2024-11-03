# import thư viện 
from bs4 import BeautifulSoup as bs
from bs4 import Comment
import requests
import pandas as pd

# hàm thu thập dữ liệu từ trang web
def crawler(url, id_div):
    print(url,id_div)
    r = requests.get(url)
    soup = bs(r.content, 'html.parser')
    table = soup.find('div', {'id': id_div})
    comment = table.find_all(string=lambda text: isinstance(text, Comment))
    data = bs(comment[0], 'html.parser').find_all('tr') 
    # Tạo dictionary để lưu trữ dữ liệu được lấy ra
    ans = {}
    # lấy tên cột
    for i, g in enumerate(data[1].find_all('th')):
        if i !=0:
            ans[g.get('data-stat')] = []
    # lấy dữ liệu 
    for i in range(2, len(data)):
        tmp = data[i].find_all('td')
        for j, x in enumerate(tmp):
            if x.get('data-stat') in ans.keys():
                if x.get('data-stat') == 'nationality':
                    s = x.getText().split(" ")
                    ans[x.get('data-stat')].append(s[0])
                else:
                    ans[x.get('data-stat')].append(x.getText())
    df = pd.DataFrame(ans)
    return df

if __name__=='__main__':
    # Danh sách các URL cần lấy dữ liệu
    urls = [
            'https://fbref.com/en/comps/9/2023-2024/stats/2023-2024-Premier-League-Stats',
            'https://fbref.com/en/comps/9/2023-2024/keepers/2023-2024-Premier-League-Stats',
            'https://fbref.com/en/comps/9/2023-2024/shooting/2023-2024-Premier-League-Stats',
            'https://fbref.com/en/comps/9/2023-2024/passing/2023-2024-Premier-League-Stats',
            'https://fbref.com/en/comps/9/2023-2024/passing_types/2023-2024-Premier-League-Stats',
            'https://fbref.com/en/comps/9/2023-2024/gca/2023-2024-Premier-League-Stats',
            'https://fbref.com/en/comps/9/2023-2024/defense/2023-2024-Premier-League-Stats',
            'https://fbref.com/en/comps/9/2023-2024/possession/2023-2024-Premier-League-Stats',
            'https://fbref.com/en/comps/9/2023-2024/playingtime/2023-2024-Premier-League-Stats',
            'https://fbref.com/en/comps/9/2023-2024/misc/2023-2024-Premier-League-Stats'
            ]
    # Các ID của thẻ div tương ứng cho mỗi URL
    ids = ['all_stats_standard','all_stats_keeper', 
           'all_stats_shooting', 'all_stats_passing', 
           'all_stats_passing_types', 'all_stats_gca',
           'all_stats_defense','all_stats_possession', 
           'all_stats_playing_time', 'all_stats_misc']
        
    # Thu thập dữ liệu
    result=crawler(urls[0],ids[0])
    # Lần lượt gộp dữ liệu từ các URL khác
    df1=crawler(urls[1],ids[1])
    common_columns = list(result.columns.intersection(df1.columns))
    result=pd.merge(result,df1,on=common_columns,how='left')
    for i in range(2,len(urls)):
        tmp_df=pd.DataFrame(crawler(urls[i],ids[i]))
        tmp_common_columns = list(result.columns.intersection(tmp_df.columns)) 
        result=pd.merge(result,tmp_df,on=tmp_common_columns,how='inner')
    #  lọc các hàng có giá trị minutes lớn hơn 90.
    result['minutes'] = result['minutes'].apply( lambda x : int(''.join(x.split(','))))
    result = result [result['minutes']>90]
    # Đổi tên và loại bỏ các cột không cần thiết: 
    result.rename(columns={'goals_pens': 'non-Penalty Goals', 'pens_made': 'Penalty Goals'},inplace=True)
    result.drop(labels=['goals','goals_assists','birth_year',
                        'pens_att','npxg_xg_assist','minutes_90s',
                        'matches','gk_games', 'gk_games_starts',
                          'gk_minutes'],axis=1,inplace=True)
    
    print(result.head().to_string())
    # Lưu kết quả vào CSV:
    result.to_csv('result.csv',index=False)
                