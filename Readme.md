
# 프로젝트: ETL 기초 파이프라인 구축

## 개요
- 주어진 서버(url)에 주기적으로 생성되고 있는 임의의 로그데이터를 스케줄러를 활용하여 추출하고,
- 이를 효율적으로 압축변환하여 AWS S3 객체로 폴더화하여 저장하는 프로젝트

## 수행 절차
- 0. 데이터 추출
    - url로부터 가져온 데이터에서 'data' 부분이 바이트형태로 암호화 되어있음
    - 해당 'data'를 암호화, 복호화 진행
    ```python
    # json으로 디코딩 함수
    def decrypt_to_json(log):
    ```
- 1. 데이터 변환
    - 로그데이터는 json형식으로 구성되어있음
    - 'user_id' : b64uuid 모듈 활용하여 64자리 -> 44자리로 길이 축소
    - 'method' : 'GET' 이나 'POST' -> mapping 활용하여 1과 2로 구분하여 크기 축소
    - 'inDate' : 정보의 손실없이 기존의 날짜 형식을 문자열 형식으로 압축
    ```python
    
    # 문자열 압축하여 반환
    def compress_log(log):
	    tmp = log.copy()
	    
	    def b64_change_44(user_id): # id
	    def method_mapping(method): # method
	    def short_date(inDate): # inDate

	    tmp['user_id'] = b64_change_44(tmp['user_id'])
	    tmp['method'] = method_mapping(tmp['method'])
	    tmp['inDate'] = short_date(tmp['inDate'])
	    return tmp
    ```
    
- 2. 데이터 적재
    - AWS IAM 계정의 액세스키를 생성, S3 버킷을 만들어 변환된 데이터를 적재
        - 적재 방식은 데이터의 inDate의 시단위 정보까지 구분하여 gzip 적용 후 적재
    ```python
	def get_s3_key(in_date, file_name): # 키 지정
	def upload_to_s3(in_date, file_name, log_data): # gzip압축 및 업로드
	def process_logs(logs_data): # 시단위로 데이터 분류하여 작업 수행
    ```
- 3. 스케줄링 적용
    - 원본 데이터는 3분에 1번씩 100개의 데이터가 갱신됨
    - 3분마다 데이터를 추출하도록 apscheduler 객체 구현
        - cron을 활용하여 원본이 생성되는 직후 시간대로 지정하면 손실 최소화 가능
    ```python
	def ETL(): # 스케줄러에 들어갈 ETL 작업
	def main(): # 메인함수
	# 스케줄링 테스트 10초
	sched = BackgroundScheduler()
	sched.add_job(ETL, 'interval', seconds=10, id='test_cron')
	# sched.add_job(ETL, 'cron', minute='0,10,20,30,40,50', id='test_cron')
	sched.start()
    ```

## 수행 결과
- AWS EC2 계정으로 콘솔 로그인하여 S3 버킷 확인
- 폴더명, 파일명 확인
   ![image](https://user-images.githubusercontent.com/59263935/226332246-986177d4-7e0a-4ffa-9862-cabc29710d79.png)
   ![image](https://user-images.githubusercontent.com/59263935/226332349-e6ef2ca6-915a-4ad8-8e3a-fed2ca7272d8.png)



### 개선할 부분
- AWS Athena 로 검색하는 것까지 완성하지 못함. 학습 중..
- 스케줄링 추가 학습 필요
