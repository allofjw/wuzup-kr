import csv
import time
import datetime 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Chrome WebDriver 경로 설정
driver_path = r'D:\chromedriver-win64\chromedriver.exe'  # ChromeDriver가 있는 실제 경로로 변경하세요.
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

# datetime에 맞는 csv 파일 불러오기 
# 날짜와 오전/오후 구분으로 CSV 파일 이름 설정
today = datetime.datetime.now()
date_str = today.strftime("%m%d")
file_suffix = "1" if today.hour < 12 else "2"  # 오전은 1, 오후는 2
csv_filename = f"headline_{date_str}_{file_suffix}.csv"


# CSV 파일에서 뉴스 링크를 읽어들이기
with open('naver_news_ranking.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # 헤더 스킵

    for row in reader:
        # 링크가 있는 열 가져오기 (CSV 구조에 따라 인덱스 확인)
        news_url = row[2]  # CSV 파일에서 세 번째 열이 링크라 가정
        driver.get(news_url)
        print(f"현재 뉴스 링크: {news_url}")

        # 페이지가 완전히 로드될 때까지 대기
        wait = WebDriverWait(driver, 10)
        
        # 댓글 섹션이 로드되는지 확인
        try:
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'u_cbox')))
        except:
            print("댓글 창이 로드되지 않는 뉴스입니다. 다음 뉴스로 넘어갑니다.")
            continue  # 댓글 창이 없으면 다음 뉴스로 이동

        # 첫 번째 "댓글 더보기" 버튼 클릭
        try:
            initial_more_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'u_cbox_btn_view_comment')))
            initial_more_button.click()
            time.sleep(1)  # 댓글이 로드될 시간 대기
            print("첫 번째 '댓글 더보기' 버튼 클릭 성공.")
        except Exception as e:
            print("첫 번째 '댓글 더보기' 버튼을 찾을 수 없습니다:", e)
            continue  # 다음 뉴스 링크로 이동

        # 댓글 로드
        prev_comment_count = 0
        total_comments = 0  # 총 수집된 댓글 수 초기화
        while total_comments < 200:
            try:
                comments = driver.find_elements(By.CLASS_NAME, 'u_cbox_comment')
                current_comment_count = len(comments)

                # "더보기" 버튼 클릭 시도
                more_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'u_cbox_btn_more')))
                more_button.click()
                time.sleep(1)  # 댓글 로딩 시간 대기

                # 클릭 후 댓글 개수 확인
                comments = driver.find_elements(By.CLASS_NAME, 'u_cbox_comment')
                current_comment_count = len(comments)

                # 댓글 개수가 동일하면 모든 댓글이 로드된 것으로 간주
                if current_comment_count == prev_comment_count:
                    print("더 이상 로드할 댓글이 없습니다.")
                    break
                else:
                    new_comments = current_comment_count - prev_comment_count
                    total_comments += new_comments
                    print(f"댓글이 {new_comments}개 추가로 로드되었습니다.")
                    prev_comment_count = current_comment_count

            except:
                print("모든 댓글이 로드되었습니다.")
                break
            # 댓글 수가 200개를 초과하면 루프 종료
            if total_comments >= 200:
                print("댓글 수가 200개를 초과하여 수집을 종료합니다.")
                break

        # 최종 댓글 리스트 수집
        comments = driver.find_elements(By.CLASS_NAME, 'u_cbox_comment')

        # 각 댓글의 작성자와 내용 출력
        for comment in comments:
            content = comment.find_element(By.CLASS_NAME, 'u_cbox_text_wrap').text
            try:
                upvotes = comment.find_element(By.CLASS_NAME, 'u_cbox_cnt_recomm').text
                downvotes = comment.find_element(By.CLASS_NAME, 'u_cbox_cnt_unrecomm').text
            except:
                upvotes, downvotes = '0', '0'  # 값이 없을 경우 0으로 설정
            print(f"댓글 내용: {content}\n추천수: {upvotes}, 비추천수: {downvotes}\n")

        # 다음 뉴스 기사로 이동하기 전 약간의 대기
        time.sleep(2)

# 모든 작업 완료 후 브라우저 종료
