# 1. 데이터 추출: ETL_func - extract.py
import os
import requests
from dotenv import load_dotenv
load_dotenv()

# 데이터 받아오기
def extract_logs():
    print('==데이터 추출...')
    url = os.environ.get('log_url')
    print('==데이터 추출 완료==')
    return requests.get(url).json()
    


    