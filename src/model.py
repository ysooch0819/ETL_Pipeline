import ETL_func
import time
from apscheduler.schedulers.background import BackgroundScheduler

import warnings
warnings.filterwarnings(action='ignore')

def ETL():
    # 데이터 추출하기
    data = ETL_func.extract_logs()
    # 데이터 변환하기
    data_test = ETL_func.transform_logs(data)
    # 데이터 적재
    ETL_func.load_logs(data_test)

def main():
    # 4. 스케줄링 매 시 3의 배수 분 5초마다 ETL 수행
    sched = BackgroundScheduler()
    sched.add_job(ETL, 'cron', minute='0,3,6,9,12,15,18,21,24,27,30,33,36,39,42,45,48,51,54,57', second='5', id='test_cron')
    sched.start()
    count=0
    while True:
        count += 1
        print(f'Running {count}회차 ETL process....')
        time.sleep(180)
        if count == 100: # ctrl+c 수동 종료..
            print(f'{count}번째 작업까지 완료')
            sched.remove_job('test_cron')
            sched.pause()


if __name__ == '__main__':
    main()