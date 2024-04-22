import os
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from io import StringIO
import xml.etree.ElementTree as ET
from MyBacktracker.lib import node_to_stock
from MyDart import DART
from MyQuant import Quant

class Backtracker(object):
    def __init__(self, rebalancing_date = '.04.15', base_path = './data/market') -> None:
        self.base_path = base_path
        self.price_path = base_path + '/price'
        self.corp_dic = {}
        self.rebalancing_date = rebalancing_date

    def getProfit(self, target_stocks: dict, duration: int, datenow: str):
        '''
        target_stocks: target_stocks['corp_code'] = stock_code
        duration: int 23 (23 days)
        datenow: str 2024.04.12
        '''
        for corp_code in target_stocks:
            pass

    def get_price(self, corp_code: str, date: str):
        corp_price_csv_path = self.price_path + f'/{corp_code}.csv'
        df = pd.read_csv(corp_price_csv_path)
        closest_date = self.find_closest_date()
        return df[df['날짜'] == closest_date]['종가'] 
    
    def find_closest_date(self, df: pd.DataFrame, date: str):
        pass

    def set_market_data(self):
        corp_list = self.get_corp_list()
        corp_update_list = []
        for file in os.listdir(self.price_path):
            corp_update_list.append(file.replace(".csv",""))
        corp_new_list = [x for x in corp_list if x not in corp_update_list]

        for corp_code in corp_update_list:
            if corp_code.startswith("p"):
                self.update_preffered_market_data(corp_code = corp_code)
            else:
                self.update_market_data(corp_code = corp_code)
        
        for corp_code in corp_new_list:
            self.get_market_data(corp_code = corp_code)
            self.get_preffered_market_data(corp_code = corp_code)
    
    def get_corp_list(self):
        '''
        기업 corp_code list 반환, stock_dic 생성
        '''
        returnlist = []
        data_path = self.base_path + "/CORPCODE.xml"
        root = ET.parse(data_path).getroot()
        for child in root:
            new_stock = node_to_stock(child)
            if new_stock: 
                self.corp_dic[new_stock["corp_code"]] = new_stock['stock_code']
                returnlist.append(new_stock["corp_code"])
        return returnlist
    
    def update_preffered_market_data(self, corp_code):
        stock_code =  self.corp_dic[corp_code[1:]][:-1]+'5'
        df = pd.read_csv(self.price_path + f'/{corp_code}.csv')
        last_date = df['날짜'][0]
        page = 1
        page_exist = True  
        date_checker = True
        while(date_checker and page_exist):
            new_page, page_exist = self.get_market_data_page(stock_code= stock_code, page= page)
            date_checker, new_page = self.update_checker(new_page,last_date)
            df = pd.concat([new_page.dropna(),df]).reset_index(drop=True)
            page += 1
        df.to_csv(self.price_path + f'/p{corp_code}.csv')     

    def update_market_data(self, corp_code):
        stock_code =  self.corp_dic[corp_code]
        df = pd.read_csv(self.price_path + f'/{corp_code}.csv')
        last_date = df['날짜'][0]
        page = 1
        page_exist = True  
        date_checker = True
        while(date_checker and page_exist):
            new_page, page_exist = self.get_market_data_page(stock_code= stock_code, page= page)
            date_checker, new_page = self.update_checker(new_page,last_date)
            df = pd.concat([new_page.dropna(),df]).reset_index(drop=True)
            page += 1
        df.to_csv(self.price_path + f'/{corp_code}.csv') 

    def update_checker(self,df,last_date):
        # column에서 value와 일치하는 첫 번째 인덱스 찾기
        index = df[df['날짜'] == last_date].index
        if len(index) == 0:
            return True, df
        else:
            index = index[0]
            return False, df.iloc[:index]
        
    def get_market_data(self, corp_code):
        stock_code =  self.corp_dic[corp_code]
        df = pd.DataFrame()
        page = 1  
        page_exist = True
        while(page_exist):
            new_page, page_exist = self.get_market_data_page(stock_code= stock_code, page= page)
            df = pd.concat([df,new_page.dropna()]).reset_index(drop=True)
            if len(df)>0:  
                if int(df.at[df.index[-1], '날짜'].split('.')[0]) < 2019:
                    if page > 1: break
                    else: return
            page += 1
        if page > 10: df.to_csv(self.price_path + f'/{corp_code}.csv') 
    
    def get_preffered_market_data(self, corp_code):
        stock_code =  self.corp_dic[corp_code][:-1] + '5'
        df = pd.DataFrame()
        page = 1  
        page_exist = True
        while(page_exist):
            new_page, page_exist = self.get_market_data_page(stock_code= stock_code, page= page)
            df = pd.concat([df,new_page.dropna()]).reset_index(drop=True)
            if len(df)>0:  
                if int(df.at[df.index[-1], '날짜'].split('.')[0]) < 2019:
                    if page > 1: break
                    else: return
            page += 1
        if page > 10: df.to_csv(self.price_path + f'/p{corp_code}.csv')
    
    def get_market_data_page(self, stock_code, page:int):
        sise_url = f'https://finance.naver.com/item/sise_day.nhn?code={stock_code}'
        headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'}
        page_url = '{}&page={}'.format(sise_url, page)
        response = requests.get(page_url, headers=headers)
        if response.text and '올바른 종목이 아닙니다' not in response.text and '접속장애' not in response.text:
            html = bs(response.text, 'html.parser')
            html_table = html.select("table")
            table = pd.read_html(StringIO(str(html_table)))
            if not (table[1].iloc[0] == page).any(): return pd.DataFrame(), False
            else: return table[0], True
        else:
            return pd.DataFrame(), False

    def set_dart_qaunt_ready(self,bsns_year):
        base_path = f"./data/data_{bsns_year}"
        os.makedirs(base_path)
        self.newDart = DART(rebalancing_date= self.rebalancing_date,bsns_year = bsns_year, base_path = base_path)
        self.newQuant = Quant(rebalancing_date= self.rebalancing_date, bsns_year = bsns_year, base_path = base_path) 

        # Qaunt init phase
        self.quant_init()

        # Data crolling phase
        self.data_crolling()

        # Data mining phase
        self.data_mining()

        #get starage
        self.qaunt()

    def quant_init(self):
        self.newDart.save_corp_code()
        self.newQuant.set_stock_dic() # code를 stock에 저장

    def data_crolling(self):
        if self.newDart.loadFlag("DataCrolling") == 'Off':
            self.newDart.get_corp_finance(self.newQuant.stock_dic)
            self.newDart.get_corp_stocknum(self.newQuant.stock_dic)
        self.newDart.saveFlag("DataCrolling")
        if self.newDart.loadFlag(f"PriceCrolling") == self.rebalancing_date:
            self.newDart.get_corp_price(self.newQuant.stock_dic)
        self.newDart.saveFlag(flag= f"PriceCrolling", value=self.rebalancing_date)
        
    def data_mining(self):
        if self.newQuant.loadFlag("DataMining") == 'Off':
            self.newQuant.mining_finance()
            self.newQuant.mining_stocknum()
        self.newQuant.saveFlag("DataMining")
        if self.newQuant.loadFlag("MiningPrice") == self.rebalancing_date:
            self.newQuant.mining_price()
            self.newQuant.curving_finance()
        self.newDart.saveFlag(flag= "MiningPrice", value=self.rebalancing_date)

    def qaunt(self):
        self.newQuant.set_score()
        self.newQuant.quant_stratgy()