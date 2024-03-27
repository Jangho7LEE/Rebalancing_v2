import json
import os
import xml.etree.ElementTree as ET

from MyQuant.lib.stock.stock import stock

class DataManager(object):
    def __init__(self,base_path) -> None:
        if os.path.isdir(base_path) :self.base_path = base_path
        else: raise ValueError("Wrong path")
        self.stock_dic = {}
    
    def openfile(self, data_path):
        """
        openfile is for open various type of files
        """
        if not os.path.exists(data_path): raise ValueError("no such path")
        chunks = data_path.split('.')
        if len(chunks) == 1:
            fileType = 'json'
        else:
            fileType = chunks[-1]

        return {
            "xml": self.openXML,
            "json": self.openJson,
        }.get(fileType, self.openXML)(data_path)
    
    def openXML(self, path):
        """
        openXML is for open XML and return ElementTree
        """
        return ET.parse(path)    
    
    def openJson(self, path):
        '''
        openJson은 json file을 읽어 반환
        '''
        with open(path, 'r') as f:
            return json.load(f)    

    def save_stock_dic(self):
        """
        self.stock_dic 을 json dump형태로 base_path + "stockdic"형태로 저장 
        """
        dic = {}
        for s in self.stock_dic:
            dic[s] = self.stock_dic[s].export_dic()

        save_path = self.base_path + "/stock_dic"
        with open(save_path, 'w') as f:
            json.dump(dic, f)
    
    def load_stock_dic(self, data_path):
        """
        load_stock_dic은 'data_path'에 존재하는 json file를 load하여 stock_dic에 저장 
        input param: data_path = base_path + corp_code   
        """
        dic = self.openfile(data_path=data_path)
        for s in dic:
            self.stock_dic[s] = stock(**dic[s])
    
    def get_corp_code_list(self):
        '''
        get_corp_code_list는 stock dic에 저장된 stock의 corp_code (stock code와 다름)
        를 list형태로 반환한다
        '''
        sl = []
        for s in self.stock_dic:
            sl.append(self.stock_dic[s].corp_code)
        return sl
    
    # 나중에 mining.py 로 옮기기
    def read_finance(self,data_path):
        '''
        read_finance는 path에 명시된 json file을 읽어온다
        '''
        dic = self.openfile(data_path=data_path)
        pass