import json
import os
from MyQuant.lib.stock.stock import stock


def set_stock_dic(self):
    '''
    set_stock_dic은 저장된 stock_dic json file을 불러와 stock_dic에 저장하거나
    CORPCODE.xml을 통해 불러온다 
    '''
    data_path = self.base_path + "/stock_dic"
    if os.path.exists(data_path):
        self.load_stock_dic(data_path = data_path)
    else:
        self.corp_code_to_stock()

def corp_code_to_stock(self):
    """
    CORPCODE.xml 파일을 stock_dic에 옮긴 후 dictionary를 json dump
    이때, stock code가 있는 (상장주)만 stock_dic에 포함된다.
    """
    data_path = self.base_path + "/CORPCODE.xml"
    root = self.openfile(data_path).getroot()
    for child in root:
        new_stock = node_to_stock(child)
        if new_stock: self.stock_dic[new_stock.corp_code] = new_stock
    self.save_stock_dic()



#############################################################################################
#                                   UTILS                                                   #
#############################################################################################  
              
def node_to_stock(xmlnode)->stock:
    """
    |
    | xml 노드를 읽어 stock을 return 이때, stock code가 있는 stock만 return 한다
    |
    """
    for child in xmlnode:
        if child.tag == "corp_code": corp_code = child.text  
        if child.tag == "corp_name": corp_name = child.text  
        if child.tag == "stock_code": stock_code = child.text  
        if child.tag == "modify_date": modify_date = child.text
    if len(stock_code) > 5:
        return stock(corp_code = corp_code ,corp_name= corp_name,stock_code= stock_code,modify_date= modify_date)
    else:
        return None      

