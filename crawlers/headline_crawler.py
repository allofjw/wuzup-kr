import requests
from bs4 import BeautifulSoup
import json
import datetime
import os
from dotenv import load_dotenv
import boto3

# JSON 파일 이름 생성절차 
# 1. 오늘의 날짜 가져오기
today = datetime.datetime.now()
date_str = today.strftime("%m%d")  # MMDD 형식으로 날짜 생성

# 2. 오전/오후에 따라 파일 이름 설정
# 오전(전반기)은 1, 오후(후반기)는 2
if today.hour < 12:
    file_suffix = "1"  # 전반기
else:
    file_suffix = "2"  # 후반기

# 3. ../data 디렉토리 경로 생성
base_dir = "../data/headline_data"
date_dir = os.path.join(base_dir, date_str)  # ../headline_data/1117
json_filename = os.path.join(date_dir, f"headline_{date_str}_{file_suffix}.json")

os.makedirs(date_dir, exist_ok=True)  # ../headline_data 디렉토리가 없으면 생성

# 네이버 랭킹 뉴스 URL
url = 'https://news.naver.com/main/ranking/popularDay.naver'

# 요청 보내기
response = requests.get(url)
response.raise_for_status()  # 요청에 오류가 있을 경우 예외 발생

# BeautifulSoup을 사용해 HTML 파싱
soup = BeautifulSoup(response.text, 'html.parser')

# 뉴스 랭킹 목록 찾기
news_items = soup.select('.rankingnews_box .rankingnews_list .list_content .list_title')

# JSON 데이터 구조 초기화
news_data = []

# 뉴스 제목과 링크 저장
for i, item in enumerate(news_items, start=1):
    title = item.get_text(strip=True)
    link = item['href']
    
    # 링크가 상대 경로일 경우 'https://news.naver.com' 붙이기
    if link.startswith('/'):
        link = 'https://news.naver.com' + link

    news_data.append({
        "number": i,
        "title": title,
        "link": link
    })

# JSON 파일로 저장
with open(json_filename, 'w', encoding='utf-8') as json_file:
    json.dump(news_data, json_file, ensure_ascii=False, indent=4)
print(f"{json_filename} 파일이 생성되었습니다.")

# .env 파일 로드
load_dotenv()

# 환경 변수에서 AWS 설정 불러오기
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')
AWS_REGION = os.getenv('AWS_REGION')

# S3에 파일 업로드
def upload_to_s3(file_path, bucket_name, s3_key):
    """S3 버킷에 파일 업로드"""
    s3 = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION
    )
    try:
        s3.upload_file(file_path, bucket_name, s3_key)
        print(f"{file_path} 파일이 S3에 업로드되었습니다: s3://{bucket_name}/{s3_key}")
    except Exception as e:
        print(f"S3 업로드 중 오류 발생: {e}")

# S3 경로 지정 및 업로드 실행
s3_key = f"headline_data/{date_str}/headline_{date_str}_{file_suffix}.json"
upload_to_s3(json_filename, AWS_BUCKET_NAME, s3_key)
