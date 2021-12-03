# 위에 다 있는 내용이라 없어도 무방 할 듯
#     basic_dataframe.to_csv('/content/' + category + '.csv', mode='a', header=False)
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import pandas as pd

domain = 'https://socialerus.com'

arr = "https://socialerus.com/Ranking/?ChCategory="
url_list = []

for num in range(1,20) :
    url = arr + str(num)
    url_list.append(url)

print("전체 카테고리 :", url_list)


for upper_url in url_list:
    print("현재 소셜러스 카테고리 주소 :", upper_url)
    upper = urlopen(upper_url)
    upper_obj = bs(upper, 'html.parser')
    social_youtubers = []


    # 각 장르별 유튜버들 소셜러스 주소 출력
    for tag in upper_obj.find_all('div', {'class': 'ranking_info'}):
        category = tag.find('span', {'class': 'category'}).get_text()
        temp_link = tag.get('onclick').split()
        pre_pro = temp_link[-1]
        target_url = domain + eval(pre_pro)
        social_youtubers.append([target_url, category])
        category = category.replace("/", "_")
    print(social_youtubers)

    df_array = []
    # 데이터 프레임 생성
    i = 0
    pd.DataFrame()
    basic_dataframe = pd.DataFrame({'No': [], 'Genre': [], 'youtube_link': []})
    basic_dataframe = basic_dataframe.set_index('No')

    # 소셜러스 페이지에서 유튜브 링크 추출
    for link in social_youtubers:
        print("유튜브 채널 :",link)
        temp = urlopen(link[0])
        youtuber_obj = bs(temp, 'html.parser')
        chanel_link = youtuber_obj.select_one('a.shortcuts.youtube')
        link[1] = link[1].replace("/", "_")
        basic_dataframe.loc[i] = [link[1], chanel_link['href']]
        i += 1
    df_array.append([basic_dataframe, category])

    # 장르별 csv파일 만들기
    for df in df_array:
        df[0].to_csv('D:/Python/JBNU_BigData_Analyze/content/' + df[1] + '.csv', mode='a', header=False)