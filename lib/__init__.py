import pandas as pd
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
    filtered_df = df[df['날짜'] > date_str]
    
    # 만약 주어진 날짜 이후의 데이터가 없다면 None 반환
    if filtered_df.empty:
        return None
    
    # 가장 가까운 다음 날짜의 인덱스 찾기
    next_date_idx = filtered_df['날짜'].idxmin()
    
    date_diff = (pd.to_datetime(filtered_df.at[next_date_idx, '날짜']) - pd.to_datetime(date)).days
    
    if date_diff >= 10:
        return None
    
    
    return df.at[next_date_idx, '종가']


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