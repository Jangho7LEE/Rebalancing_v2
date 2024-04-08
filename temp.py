import pandas as pd

def dict_to_dataframe(dic, keys):
    # DataFrame으로 변환할 딕셔너리 항목 선택
    selected_data = {key: dic[key] for key in keys if key in dic}
    
    # DataFrame으로 변환
    df = pd.DataFrame(selected_data).transpose()
    
    return df

# 예시 딕셔너리
dic = {
    'key1': {'A': 1, 'B': 2, 'C': 3},
    'key2': {'A': 4, 'B': 5, 'C': 6},
    'key3': {'A': 7, 'B': 8, 'C': 9}
}

# 변환할 키 선택
keys_to_convert = ['key1', 'key3']

# DataFrame으로 변환
df = dict_to_dataframe(dic, keys_to_convert)
print(df)