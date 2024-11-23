import json
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from dotenv import load_dotenv
import boto3
# Chrome WebDriver 경로 설정
#driver_path = '/usr/local/bin/chromedriver-linux64/chromedriver'  # ChromeDriver가 있는 실제 경로로 변경하세요.

# Chrome WebDriver 경로 설정
driver_path = 'c:/Users/JW/Desktop/chromedriver-win64/chromedriver.exe'  # ChromeDriver 경로
service = Service(driver_path)
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # UI 없이 실행
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=service, options=options)

# datetime에 맞는 JSON 파일 이름 설정
today = datetime.datetime.now()
date_str = today.strftime("%m%d")
file_suffix = "1" if today.hour < 12 else "2"  # 오전은 1, 오후는 2

comments_base_dir = "../comment_data"
comments_date_dir = os.path.join(comments_base_dir, date_str)
os.makedirs(comments_date_dir, exist_ok=True)  # ../comments_data/date 디렉토리가 없으면 생성

# JSON 파일 경로
comments_json_filename = os.path.join(comments_date_dir, f"comments_{date_str}_{file_suffix}.json")

# 입력 JSON 파일 경로 설정
head_base_dir = "../headline_data"
head_date_dir = os.path.join(head_base_dir, date_str)
head_json_filename = os.path.join(head_date_dir, f"headline_{date_str}_{file_suffix}.json")

# JSON 데이터 구조 초기화
all_comments = []

# JSON 파일에서 뉴스 링크 읽기
with open(head_json_filename, 'r', encoding='utf-8') as infile:
    headlines = json.load(infile)  # JSON 데이터 읽기

    for item in headlines:
        number = item['number']  # 뉴스 번호
        news_url = item['link']  # 뉴스 URL
        driver.get(news_url)
        print(f"현재 뉴스 링크({number}): {news_url}")

        # 페이지가 완전히 로드될 때까지 대기
        wait = WebDriverWait(driver, 10)
        try:
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'u_cbox')))
        except:
            print(f"댓글 창이 로드되지 않는 뉴스입니다. 번호: {number}")
            continue

        # 첫 번째 "댓글 더보기" 버튼 클릭
        try:
            initial_more_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'u_cbox_btn_view_comment')))
            initial_more_button.click()
            time.sleep(1)
            print("첫 번째 '댓글 더보기' 버튼 클릭 성공.")
        except Exception as e:
            print("첫 번째 '댓글 더보기' 버튼을 찾을 수 없습니다:", e)
            continue

        # "더보기" 버튼 반복 클릭 200회까지
        comments_data = []
        total_comments = 0  # 총 댓글 수
        try:
            while total_comments < 200:
                more_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'u_cbox_btn_more')))
                more_button.click()
                time.sleep(1)
                print("댓글 '더보기' 버튼 클릭 성공.")
                # 댓글 수 업데이트
                comments = driver.find_elements(By.CLASS_NAME, 'u_cbox_comment')
                total_comments = len(comments)
                print(f"현재까지 수집된 댓글 수: {total_comments}")
                 # 댓글이 200개 이상이면 루프 종료
                if total_comments >= 200:
                    print("댓글이 200개를 초과하여 수집을 종료합니다.")
                    break
        except Exception as e:
            print("더 이상 클릭할 '더보기' 버튼이 없습니다:", e)

        try:
            comments = driver.find_elements(By.CLASS_NAME, 'u_cbox_comment')
            for element in comments[:200]:
                # 원래의 try-except 구조 그대로 유지
                try:
                    content = element.find_element(By.CLASS_NAME, 'u_cbox_text_wrap').text
                except Exception:
                    content = "댓글 내용을 가져올 수 없습니다."

                try:
                    upvotes = element.find_element(By.CLASS_NAME, 'u_cbox_cnt_recomm').text
                    upvotes = int(upvotes) if upvotes.isdigit() else 0
                except Exception:
                    upvotes = 0

                try:
                    downvotes = element.find_element(By.CLASS_NAME, 'u_cbox_cnt_unrecomm').text
                    downvotes = int(downvotes) if downvotes.isdigit() else 0
                except Exception:
                    downvotes = 0

                comments_data.append({
                    "content": content,
                    "upvotes": upvotes,
                    "downvotes": downvotes
                })
        except Exception as e:
            print(f"댓글 로드 중 오류 발생: {e}")

        # 뉴스 댓글 데이터 저장
        all_comments.append({
            "news_number": number,
            "url": news_url,
            "comments": comments_data
        })

        # 중간 저장 추가 (구조는 그대로 유지)
        with open(comments_json_filename, 'w', encoding='utf-8') as json_file:
            json.dump(all_comments, json_file, ensure_ascii=False, indent=4)
        print(f"Intermediate save: {comments_json_filename}")

print(f"모든 댓글 데이터가 JSON 파일로 저장되었습니다: {comments_json_filename}")

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
s3_key = f"comments_data/{date_str}/comments_{date_str}_{file_suffix}.json"
upload_to_s3(comments_json_filename, AWS_BUCKET_NAME, s3_key)
