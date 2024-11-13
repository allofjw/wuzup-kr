import requests
from bs4 import BeautifulSoup
import csv
import datetime

# CSV 파일 이름 생성절차 
# 1. 오늘의 날짜 가져오기
today = datetime.datetime.now()
date_str = today.strftime("%m%d")  # MMDD 형식으로 날짜 생성

# 2. 오전/오후에 따라 파일 이름 설정
# 오전(전반기)은 1, 오후(후반기)는 2
if today.hour < 12:
    file_suffix = "1"  # 전반기
else:
    file_suffix = "2"  # 후반기

# 3. CSV 파일 이름 생성
csv_filename = f"headline_{date_str}_{file_suffix}.csv"


# 네이버 랭킹 뉴스 URL
url = 'https://news.naver.com/main/ranking/popularDay.naver'

# 요청 보내기
response = requests.get(url)
response.raise_for_status()  # 요청에 오류가 있을 경우 예외 발생

# BeautifulSoup을 사용해 HTML 파싱
soup = BeautifulSoup(response.text, 'html.parser')

# 뉴스 랭킹 목록 찾기
news_items = soup.select('.rankingnews_box .rankingnews_list .list_content .list_title')

# CSV 파일 작성
with open(csv_filename, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['번호', '제목', '링크'])  # 헤더 작성

    # 뉴스 제목과 링크 저장
    for i, item in enumerate(news_items, start=1):
        title = item.get_text(strip=True)
        link = item['href']
        
        # 링크가 상대 경로일 경우 'https://news.naver.com' 붙이기
        if link.startswith('/'):
            link = 'https://news.naver.com' + link

        writer.writerow([i, title, link])
print(f"{csv_filename} 파일이 생성되었습니다.")
