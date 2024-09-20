import pandas as pd
import re
from datetime import datetime
import matplotlib.pyplot as plt

def main():
    # 로그 파일 경로 설정
    log_file_path = 'archive/access_log_Jul95.txt'
    df = load_log_file(log_file_path)

    min_timestamp = df['Timestamp'].min()
    max_timestamp = df['Timestamp'].max()

    print("시작일시:", min_timestamp)
    print("종료일시:", max_timestamp)
    print("Count  :", df.shape[0])

    # DataFrame 출력
    # print(df.shape[0])
    print(df.head())


    filter_df = filter_top_count(df, 'URL', 20)
    graph_with_percentage('TOP_20 URL Count', 'URL', filter_df['Request Count'], filter_df['Percentage'])
    
    
    # 시간 단위로 요청 횟수를 계산 (Timestamp 컬럼을 기준으로)
    hourly_requests, hourly_percentage = calculate_and_graph_time_unit(df, 'hour')
    graph_with_percentage('Hour Count', 'Hour', hourly_requests, hourly_percentage)
    
    minutely_requests, minutely_percentage = calculate_and_graph_time_unit(df, 'minute')
    graph_with_percentage('Minute Count', 'Minute', minutely_requests, minutely_percentage)

    plt.show()
    
# 함수 정의: Day, Hour, Minute 단위로 모듈화
def calculate_and_graph_time_unit(df, time_unit):
    # 주어진 단위로 요청 횟수를 계산
    time_requests = df['Timestamp'].dt.__getattribute__(time_unit).value_counts().sort_index()

    # 각 단위별 요청 횟수가 전체에서 차지하는 비율 계산
    total_requests = time_requests.sum()
    percentage_requests = (time_requests / total_requests) * 100
    
    return time_requests, percentage_requests

def filter_top_count(df, field, count):
    field_requests = df[field].value_counts()
    top_count_requests = field_requests.head(count)
    total_requests = field_requests.sum()
    percentage_top_count = (top_count_requests / total_requests) * 100
    combined_df = pd.DataFrame({
        'Request Count': top_count_requests,
        'Percentage': percentage_top_count
    })

    return combined_df

def load_log_file(log_file_path):

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

    return df

def graph_with_percentage(name, xlabel, counts, percentages):
    # 새로운 figure 생성
    plt.figure()

    # 요청 횟수 시각화 (막대 그래프)
    ax = counts.plot(kind='bar', color='skyblue')

    # 그래프 레이블 설정
    plt.xlabel(f'{xlabel}')
    plt.ylabel('Number of Requests')
    plt.title(f'{name} Request Distribution')
    
    # 막대 그래프 끝에 비율 값 표시
    for i, (count, percentage) in enumerate(zip(counts, percentages)):
        ax.text(i, count + 0.5, f'{percentage:.2f}%', ha='center')

    # y축에만 그리드 표시
    plt.grid(True, axis='y')

    # # 그래프 보여주기
    # plt.show()
    
def graph(name, time_requests):
    # 새로운 figure 생성
    plt.figure()
    
    # 요청 횟수 시각화
    time_requests.plot(kind='bar', color='skyblue')
    plt.xlabel(f'{name} of Day')
    # x축 레이블 가로로 표시 (회전 0도)
    # plt.xticks(rotation=0)
    plt.ylabel('Number of Requests')
    plt.title(f'{name} Request Distribution')

    # y축에만 그리드 표시
    plt.grid(True, axis='y')


if __name__ == "__main__":
    main()