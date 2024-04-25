import os
import json

def node_to_stock(xmlnode):
    """
    |
    | xml 노드를 읽어 stock을 return 이때, stock code가 있는 stock만 return 한다
    |
    """
    for child in xmlnode:
        if child.tag == "corp_code": corp_code = child.text  
        if child.tag == "stock_code": stock_code = child.text  
        
    if len(stock_code) > 5:
        return {"corp_code":corp_code, "stock_code":stock_code}
    else:
        return None  
    
def saveFlag(self, flag: str, value = None):
        flag_path = self.base_path + '/flags'
        if os.path.exists(flag_path):
            with open(flag_path, 'r') as f:
                flag_dic = json.load(f)
            if value:
                flag_dic[flag] = value
            else:
                flag_dic[flag] = 'On'
        else:
            flag_dic = {}
            if value:
                flag_dic[flag] = value
            else:
                flag_dic[flag] = 'On'
        with open(flag_path, 'w') as f:
            json.dump(flag_dic, f)

def loadFlag(self, flag: str):
    flag_path = self.base_path + '/flags'
    if os.path.exists(flag_path):
        with open(flag_path, 'r') as f:
            flag_dic = json.load(f)
        if flag in flag_dic:
            return flag_dic[flag]
        else:
            return 'Off'
    else:
        return 'Off'




