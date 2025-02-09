import subprocess
import schedule
import time
import logging
from datetime import datetime

# 로깅 설정
logging.basicConfig(
    filename="crawler_status.log",  # 로그 파일 이름
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

# headline_crawler.py 실행 함수
def run_headline_crawler():
    """
    Run the headline_crawler.py script.
    Linux환경에 맞게 수정된 코드

    """
    try:
        print("Running: crawlers/headline_crawler.py")
        logging.info("Running: crawlers/headline_crawler.py")
        subprocess.run(["python3", "crawlers/headline_crawler.py"], check=True)
        logging.info("headline_crawler.py finished successfully.")
    except subprocess.CalledProcessError as e:
        error_message = f"Error running crawlers/headline_crawler.py: {e}"
        print(error_message)
        logging.error(error_message)

# comment_crawler.py 실행 함수
def run_comment_crawler():
    """
    Run the comment_crawler.py script.
    Linux환경에 맞게 수정된 코드
    
    """
    try:
        print("Running: crawlers/comment_crawler.py")
        logging.info("Running: crawlers/comment_crawler.py")
        subprocess.run(["python3", "crawlers/comment_crawler.py"], check=True)
        logging.info("comment_crawler.py finished successfully.")
    except subprocess.CalledProcessError as e:
        error_message = f"Error running crawlers/comment_crawler.py: {e}"
        print(error_message)
        logging.error(error_message)

# headline_crawler와 comment_crawler를 순서대로 실행
def run_all_crawlers():
    """
    Run the headline_crawler.py and comment_crawler.py scripts in sequence.
    헤드라인 크롤링결과가 AWS S3에 업로드가 되면, AWS Lambda Trigger에 의해 
    헤드라인 데이터 군집화 모델(약 1분간의 인프런스 과정 소모)이 작동하고,
    군집화된 헤드라인 데이터들에 대하여 댓글 크롤러 작동

    """
    logging.info("Starting the crawlers...")
    print("Starting the crawlers...")
    run_headline_crawler()
    time.sleep(300)  # 5분 대기
    run_comment_crawler()
    print("Crawlers finished successfully.")
    logging.info("Crawlers finished successfully.")

# 스케줄러 설정
def setup_scheduler():
    """
    오전, 오후로 스케줄러 설정을 통해
    뉴스 헤드라인, 댓글 크롤러를 실행하는 함수
    """
    # 작업 스케줄 설정
    schedule.every().day.at("10:00").do(run_all_crawlers)
    schedule.every().day.at("18:30").do(run_all_crawlers)
    print("Scheduler initialized. Tasks will run at the scheduled times (10:00 and 18:30).")

    while True:
        schedule.run_pending()
        time.sleep(1)

# 메인 실행
if __name__ == "__main__":
    setup_scheduler()
