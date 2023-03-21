# 3. 데이터 적재: ETL_func - load.py
import os
import io
import gzip
import boto3
import json
from dotenv import load_dotenv
load_dotenv()

# 키 지정 함수: 도전과제, dynamic partitioning
def get_s3_key(in_date, file_name):
    """
    주어진 in_date와 file_name 값으로 s3 객체의 key를 생성하는 함수
    """
    key_prefix = 'data'
    year = '20' + in_date[0:2]
    month = in_date[2:4]
    day = in_date[4:6]
    hour = in_date[6:8]

    return f'{key_prefix}/{year}/{month}/{day}/{hour}/{file_name}'

# 압축 및 업로드 기능
def upload_to_s3(in_date, file_name, log_data):
    """
    주어진 in_date 값으로 s3 객체를 생성하고 log_data를 압축하여 file_name 으로 업로드하는 함수
    """

    # 필요키 지정
    s3_aws_access_key_id = os.environ.get('s3_aws_access_key_id')
    s3_aws_secret_access_key = os.environ.get('s3_aws_secret_access_key')
    s3_bucket_name = os.environ.get('s3_bucket_name')

    s3_client = boto3.client('s3',
                  aws_access_key_id = s3_aws_access_key_id,
                  aws_secret_access_key=s3_aws_secret_access_key,
                  region_name='ap-northeast-2')

    bucket_path = f"s3://{s3_bucket_name}/{get_s3_key(in_date, file_name)}"
    
    # 압축알고리즘, gzip활용
    with io.BytesIO() as output:
        with gzip.GzipFile(fileobj=output, mode='w') as gzip_output:
            gzip_output.write(log_data.encode('ascii'))
        compressed_content = output.getvalue()

    # 압축된 파일을 s3에 업로드: 키 지정 함수 호출
    s3_client.upload_fileobj(io.BytesIO(compressed_content), s3_bucket_name, get_s3_key(in_date, f'{file_name}'))

    # 업로드 후 확인메시지 출력
    print(f"Upload completed: {file_name} to {bucket_path}")
    

# 주어진 데이터를 분류하여 압축 후 적재 실행
def load_logs(logs_data):
    """
    주어진 logs_data를 시간 단위별로 분류하여 압축하여 s3에 업로드하는 함수
    """
    print('==데이터 적재 시작==')
    # 시간 단위별로 분류하기 위해 딕셔너리 초기화
    logs_by_hour = {}

    # 각 로그 데이터를 시간 단위로 분류
    for log_data in logs_data:
        in_date = log_data['inDate']
        hour = in_date[6:8]
        if hour not in logs_by_hour:
            logs_by_hour[hour] = []
        logs_by_hour[hour].append(log_data)
    
    # 분류한 시간 단위별로 로그 데이터를 압축하여 업로드 함수 호출
    for hour, logs in logs_by_hour.items():
        # 해당 시간의 첫번째 로그 데이터의 inDate 값을 가져옵니다.
        first_log_in_date = logs[0]['inDate']
        # 해당 시간의 마지막 로그 데이터의 inDate 값을 가져옵니다.
        last_log_in_date = logs[-1]['inDate']

        # 압축 파일의 이름: 첫로그 분단위 이하_끝로그 분단위 이하.gz 형태
        file_name = f"{first_log_in_date[8:]}_{last_log_in_date[8:]}.gz"
        
        # 시간 단위 폴더에 로그 데이터를 저장합니다.
        upload_to_s3(first_log_in_date[:8], file_name, json.dumps(logs))
    
    print('==데이터 적재 완료==')