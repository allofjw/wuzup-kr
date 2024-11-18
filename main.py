import subprocess
import schedule
import time
import os

# headline_crawler.py 실행 함수
def run_headline_crawler():
    try:
        print("Running: crawlers/headline_crawler.py")
        subprocess.run(["python", "crawlers/headline_crawler.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running crawlers/headline_crawler.py: {e}")

# comment_crawler.py 실행 함수
def run_comment_crawler():
    try:
        print("Running: crawlers/comment_crawler.py")
        subprocess.run(["python", "crawlers/comment_crawler.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running crawlers/comment_crawler.py: {e}")

# headline_crawler와 comment_crawler를 순서대로 실행
def run_all_crawlers():
    print("Starting the crawlers...")
    run_headline_crawler()
    time.sleep(300)
    run_comment_crawler()
    print("Crawlers finished successfully.")

# 스케줄러 설정
def setup_scheduler():
    # 오전 10시 실행
    schedule.every().day.at("10:00").do(run_all_crawlers)
    print("Scheduler initialized. Tasks will run at the scheduled time (10:00).")
    # 오후 6시 30분 실행
    schedule.every().day.at("18:30").do(run_all_crawlers)
    print("Scheduler initialized. Tasks will run at the scheduled time (18:30).")

    print("Scheduler initialized. Tasks will run at the scheduled times (10:00 and 18:30).")
    while True:
        schedule.run_pending()
        time.sleep(1)

# 메인 실행
if __name__ == "__main__":
    setup_scheduler()
