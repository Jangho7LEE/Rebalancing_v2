import pandas as pd
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta

def get_next_closest_price(df, date, Ptype = '종가'):
    """
    DataFrame(df)에서 주어진 날짜(date) 이후의 가장 가까운 다음 날짜의 Ptype('종가') 값을 반환하는 함수.
    
    :param df: 날짜와 종가가 포함된 DataFrame
    :param date: 찾고자 하는 날짜 (예: '2023.12.31' 형식의 문자열)
    :return: 주어진 날짜 이후의 가장 가까운 다음 날짜의 종가 (존재하지 않을 경우 None 반환)
    """
    # 날짜를 문자열로 변환하여 비교
    date_str = pd.to_datetime(date).strftime('%Y.%m.%d')
    
    # 주어진 날짜 이후의 데이터만 필터링
    filtered_df = df[df['날짜'] >= date_str]
    
    # 만약 주어진 날짜 이후의 데이터가 없다면 None 반환
    if filtered_df.empty:
        return None
    
    # 가장 가까운 다음 날짜의 인덱스 찾기
    next_date_idx = filtered_df['날짜'].idxmin()
    
    date_diff = (pd.to_datetime(filtered_df.at[next_date_idx, '날짜']) - pd.to_datetime(date)).days
    
    if date_diff >= 10:
        return None
    
    
    return df.at[next_date_idx, Ptype]

def get_next_ymd(ymd = '1999.01.01', nexttype ='M', offset = 1):
    '''
    nexttype: Y: year
              M: month
              D: day
    '''
    date = datetime.strptime(ymd, '%Y.%m.%d')
    if nexttype == 'Y': next_date = date + relativedelta(years=offset)
    if nexttype == 'M': next_date = date + relativedelta(months=offset)
    if nexttype == 'D': next_date = date + relativedelta(days=offset)
    return next_date.strftime('%Y.%m.%d')

    


def cal_momentum(a, b):
    """
    주어진 두 값에 대한 백분율 변화를 계산하여 소수점 두 자리까지 반환하는 함수.

    :param a: 초기값
    :param b: 최종값
    :return: 백분율 변화 값 (예: 10.50)
    """
    # 백분율 변화 계산
    percentage_change = ((b - a) / abs(a)) * 100
    
    # 소수점 둘째 자리까지 반올림하여 반환
    return round(percentage_change, 2)

def get_stock_price(corp_code: str, ymd: str, market_pass = './data/market/price', offset: int = None):
    '''
    ymd : e.g. '2024.04.01'
    '''
    if offset:
        date = datetime.strptime(ymd, '%Y.%m.%d')
        next_month_date = date - relativedelta(months=offset)
        ymd = next_month_date.strftime('%Y.%m.%d')

    corp_price_path = market_pass + f"/{corp_code}.csv"
    if os.path.exists(corp_price_path):
        df = pd.read_csv(corp_price_path)
        price = get_next_closest_price(df= df, date = ymd, Ptype= '종가')
        if price: return float(price)
        else: return None
    else:
        return None

def get_index_price(index_name: str, ymd: str, index_path = './data/market/index', offset: int = None):
    '''
    ymd : e.g. '2024.04.01'
    '''
    if offset:
        date = datetime.strptime(ymd, '%Y.%m.%d')
        next_month_date = date - relativedelta(months=offset)
        ymd = next_month_date.strftime('%Y.%m.%d')

    index_price_path = index_path + f"/{index_name}.csv"
    if os.path.exists(index_price_path):
        df = pd.read_csv(index_price_path)
        price = get_next_closest_price(df= df, date = ymd, Ptype= '체결가')
        if price: return float(price)
        else: return None
    else:
        return None

def get_corp_profit(corp_code: str, start_ymd: str, end_ymd: str):
    a = get_stock_price(corp_code = corp_code,ymd= start_ymd)
    b = get_stock_price(corp_code= corp_code, ymd= end_ymd)
    if a and b: return cal_momentum(a,b)
    else: return None
    
def get_index_profit(index_name: str, start_ymd: str, end_ymd: str):    
    a = get_index_price(index_name = index_name,ymd= start_ymd)
    b = get_index_price(index_name= index_name, ymd= end_ymd)
    if a and b: return cal_momentum(a,b)
    else: return None