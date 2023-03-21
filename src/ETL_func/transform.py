# 2. 데이터 변환: ETL_func - transform.py
import re
import os
from b64uuid import B64UUID
from cryptography.fernet import Fernet
from dotenv import load_dotenv
load_dotenv()

# id
def b64_change_44(user_id):
    user_id_parts = [user_id[:32], user_id[32:]] # 32자리씩 나누기
    b64_uuid_parts = [B64UUID(u_id_part) for u_id_part in user_id_parts] # 32자리별로 B64UUID 모듈 활용하여 22자리로 변형
    b64_uuid_44 = str(b64_uuid_parts[0]) + str(b64_uuid_parts[1]) # 변형된 22자리 2개를 하나의 문자열로 합쳐준다.

    return b64_uuid_44

# method
def method_mapping(method):
    method_mapping = {'GET': 1, 'POST': 2}
    return method_mapping.get(method)

# inDate
def short_date(inDate):
    return re.sub(r'[^0-9]' ,'',''.join(inDate[2:]).replace(':','').replace('.',''))

# 문자열 압축 함수
def compress_log(log):
    tmp = log.copy()
    tmp['user_id'] = b64_change_44(tmp['user_id'])
    tmp['method'] = method_mapping(tmp['method'])
    tmp['inDate'] = short_date(tmp['inDate'])
    return tmp

# 키 생성
def transform_logs(data):
    print('==복호화 키 생성 중...')
    key = bytes(os.environ.get('f_key'), encoding='utf-8')
    fernet = Fernet(key)
    print('==키 생성 완료==')

    # 암호화-복호화 및 데이터 변환하기
    res = []
    print('==데이터 암호화-복호화 시작, 문자열 압축 중...')
    for log in data:
        target_data = fernet.decrypt(log['data'])
        decrypted_data = eval(target_data.decode('ascii'))
        res.append(compress_log(decrypted_data))
    print('==데이터 변환 완료==')
    return res