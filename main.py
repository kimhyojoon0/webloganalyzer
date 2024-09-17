import pandas as pd
import re
from datetime import datetime

# 로그 파일 경로 설정
log_file_path = 'archive/access_log_Jul95.txt'

# 로그 파일의 각 줄을 파싱하기 위한 정규 표현식
log_pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - \[(.*?)\] "(.*?) (.*?) (.*?)" (\d{3}) (\d+)'

# 로그 데이터를 저장할 리스트 생성
log_data = []

# 로그 파일 읽기 및 파싱
with open(log_file_path, 'r') as log_file:
    for line in log_file:
        match = re.match(log_pattern, line)
        if match:
            ip_address = match.group(1)
            timestamp = match.group(2)
            method = match.group(3)
            url = match.group(4)
            http_version = match.group(5)
            status_code = int(match.group(6))
            response_size = int(match.group(7))
            
            # 날짜와 시간 변환
            timestamp = datetime.strptime(timestamp, "%d/%b/%Y:%H:%M:%S %z")
            
            # 로그 데이터를 리스트에 추가
            log_data.append([ip_address, timestamp, method, url, status_code, response_size])

# DataFrame 생성
df = pd.DataFrame(log_data, columns=['IP Address', 'Timestamp', 'Method', 'URL', 'Status Code', 'Response Size'])

# DataFrame 출력
print(df.shape)
print(df.head())
