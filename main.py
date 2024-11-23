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
    logging.info("Starting the crawlers...")
    print("Starting the crawlers...")
    run_headline_crawler()
    time.sleep(300)  # 5분 대기
    run_comment_crawler()
    print("Crawlers finished successfully.")
    logging.info("Crawlers finished successfully.")

# 상태 기록 함수
def log_heartbeat():
    message = f"Heartbeat: Process is running. Current time: {datetime.now()}"
    print(message)
    logging.info(message)

# 스케줄러 설정
def setup_scheduler():
    # 작업 스케줄 설정
    schedule.every().day.at("10:00").do(run_all_crawlers)
    schedule.every().day.at("18:30").do(run_all_crawlers)
    schedule.every(10).minutes.do(log_heartbeat)  # 10분마다 상태 기록
    print("Scheduler initialized. Tasks will run at the scheduled times (10:00 and 18:30).")

    while True:
        schedule.run_pending()
        time.sleep(1)

# 메인 실행
if __name__ == "__main__":
    setup_scheduler()
