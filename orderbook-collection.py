import requests
import pandas as pd
from datetime import *
import time
timestamp = last_update_time = datetime.now()
switch = 0 # 데이터 초기화용 변수
while True:
    response = requests.get('https://api.bithumb.com/public/orderbook/BTC_KRW/?count=5')
# 빗썸에서 거래 매수층과 매도층을 불러옴(각각 현재매수가 기준 5개까지)
    book = response.json()
    data = book['data'] # json 형식으로 표현된 것
    timestamp = datetime.now() # 현재시각 저장
    if ((timestamp - last_update_time).total_seconds() < 1.0):
        continue
# 현재시각과 최근 업데이트된 시각 사이의 간격이 1초 이상이 될 때까지 반복
    last_update_time = timestamp # 마지막 업데이트 시각을 현재시각으로 변경
    req_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S.%f') # 시간 형식
    bids = (pd.DataFrame(data['bids'])).apply(pd.to_numeric, errors='ignore')
    bids.sort_values('price', ascending=True, inplace=True)
    bids = bids.reset_index()
    bids['type'] = 0
# 매수 주문에 대한 데이터 처리
    asks = (pd.DataFrame(data['asks'])).apply(pd.to_numeric, errors='ignore')
    asks.sort_values('price', ascending=True, inplace=True)
    asks['type'] = 1
# 매도 주문에 대한 데이터 처리
    df = pd.concat([bids, asks])
    df['quantity'] = df['quantity'].round(decimals=4)
    df['timestamp'] = req_timestamp
# 매수량/매도량 관련 데이터는 소수점 아래 넷째 자리까지 표시
# 타임스탬프 표시
    del df['index'] # 인덱스 삭제
    print(df) # 자료가 어떤 식으로 나오는지?

    if (switch == 0): # 맨 처음에는 데이터 초기화(덮어쓰기)
        switch = 1
        df.to_csv("2022-05-20-bithumb-BTC-orderbook.csv", mode='w')
    else: # 그 다음부터는 아래에 채워나감
        df.to_csv("2022-05-20-bithumb-BTC-orderbook.csv", mode='a', header=False)

    time.sleep(1)



