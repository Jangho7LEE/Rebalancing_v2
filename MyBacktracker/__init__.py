import os
import pandas as pd
import requests
import json
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup as bs
from io import StringIO
import xml.etree.ElementTree as ET

from MyBacktracker.lib import node_to_stock
from MyDart import DART
from MyQuant import Quant
from lib import get_corp_profit, get_index_profit, get_next_ymd
class Backtracker(object):
    def __init__(self, stratgy = 'VC2',rebalancing_date = '.04.15', base_path = './data/market') -> None:
        self.base_path = base_path
        self.data_path = './data'
        self.price_path = base_path + '/price'
        self.index_path = base_path + '/index'
        self.corp_dic = {}
        self.rebalancing_date = rebalancing_date
        self.stratgy = stratgy
        self.make_dirs()

    def make_dirs(self):
        if not os.path.exists(self.price_path): os.makedirs(self.price_path)
        if not os.path.exists(self.index_path): os.makedirs(self.index_path)

################################################################################################################
    
    def set_market_data(self):
        corp_list = self.get_corp_list()
        corp_update_list = []
        self.update_index_data(index_name= 'KOSPI')
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
    
    def update_market_datas(self):
        self.get_corp_list()
        corp_update_list = []
        self.update_index_data(index_name= 'KOSPI')
        for file in os.listdir(self.price_path):
            corp_update_list.append(file.replace(".csv",""))

        for corp_code in corp_update_list:
            if corp_code.startswith("p"):
                self.update_preffered_market_data(corp_code = corp_code)
            else:
                self.update_market_data(corp_code = corp_code) 

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
        df.to_csv(self.price_path + f'/{corp_code}.csv')     

    def update_market_data(self, corp_code):
        stock_code =  self.corp_dic[corp_code]
        df = pd.read_csv(self.price_path + f'/{corp_code}.csv')
        last_date = df['날짜'][0]
        page = 1
        page_exist = True  
        date_checker = True
        while(date_checker and page_exist):
            new_page, page_exist = self.get_market_data_page(stock_code= stock_code, page= page)
            if page_exist:
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
    
    def update_index_data(self, index_name):
        if not os.path.exists(self.index_path + f'/{index_name}.csv'):
            self.get_index_data(index_name= index_name)
        else:
            df = pd.read_csv(self.index_path + f'/{index_name}.csv')
            last_date = df['날짜'][0]
            page = 1
            page_exist = True  
            date_checker = True
            while(date_checker and page_exist):
                new_page, page_exist = self.get_index_data_page(index_name= index_name, page= page)
                date_checker, new_page = self.update_checker(new_page,last_date)
                df = pd.concat([new_page.dropna(),df]).reset_index(drop=True)
                page += 1
            df.to_csv(self.index_path + f'/{index_name}.csv')
    
    def get_index_data(self, index_name):
        df = pd.DataFrame()
        page = 1  
        page_exist = True
        while(page_exist):
            new_page, page_exist = self.get_index_data_page(index_name= index_name, page= page)
            df = pd.concat([df,new_page.dropna()]).reset_index(drop=True)
            if len(df)>0:  
                if int(df.at[df.index[-1], '날짜'].split('.')[0]) < 2019:
                    if page > 1: break
                    else: return
            page += 1
        if page > 10: df.to_csv(self.index_path + f'/{index_name}.csv')

    def get_index_data_page(self,index_name,page:int):
        sise_url = f'https://finance.naver.com/sise/sise_index_day.naver?code={index_name}'
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
################################################################################################################
    '''
    set_dart_qaunt_ready
    Data crolling과 Qaunt stratgy를 결정하게 된다.
    '''
    
    def set_dart_qaunt_ready(self, bsns_year: str):
        base_path = f"./data/data_{bsns_year}"
        if not os.path.exists(base_path): os.makedirs(base_path)
        self.newDart = DART(rebalancing_date= self.rebalancing_date,bsns_year = bsns_year, base_path = base_path)
        self.newQuant = Quant(rebalancing_date= self.rebalancing_date, bsns_year = bsns_year, base_path = base_path) 
        market_corp_list = self.get_market_corp_list()
        # Qaunt init phase
        self.quant_init(market_corp_list)

        # Data crolling phase
        self.data_crolling()

        # Data mining phase
        self.data_mining()

        #get starage
        self.qaunt()

    def get_market_corp_list(self):
        clist = os.listdir(self.price_path)
        returnlist = []
        for corp_code in clist:
            if not corp_code.startswith('p'): returnlist.append(corp_code.replace(".csv",""))
        return returnlist

    def quant_init(self, market_corp_list):
        self.newDart.save_corp_code()
        self.newQuant.set_stock_dic(market_corp_list= market_corp_list) # code를 stock에 저장

    def data_crolling(self):
        if self.newDart.loadFlag("DataCrolling") == 'Off':
            self.newDart.get_corp_finance(self.newQuant.stock_dic, reset= 1)
            self.newDart.get_corp_stocknum(self.newQuant.stock_dic, reset= 1)
            self.newDart.saveFlag("DataCrolling")
        if not self.newDart.loadFlag(f"PriceCrolling") == self.rebalancing_date:
            self.newDart.get_corp_price(self.newQuant.stock_dic, reset= 1)
            self.newDart.saveFlag(flag= f"PriceCrolling", value=self.rebalancing_date)
        
    def data_mining(self):
        if self.newQuant.loadFlag("DataMining") == 'Off':
            self.newQuant.mining_finance()
            self.newQuant.mining_stocknum()
            self.newQuant.saveFlag("DataMining")
        if not self.newQuant.loadFlag("MiningPrice") == self.rebalancing_date:
            self.newQuant.mining_price()
            self.newQuant.curving_finance()
            self.newDart.saveFlag(flag= "MiningPrice", value=self.rebalancing_date)
        # self.newQuant.curving_finance()
        # self.newDart.saveFlag(flag= "MiningPrice", value=self.rebalancing_date)

    def qaunt(self):
        if not self.newQuant.loadFlag("Stratgy") == self.stratgy:
            self.newQuant.set_score()
            self.newQuant.quant_stratgy(st = self.stratgy)
            self.newDart.saveFlag(flag= "Stratgy", value=self.stratgy)

################################################################################################################
    
    def Profit_and_Loss(self, start_year, end_year):
        index_list = ['KOSPI']
        if self.check_ready(start_year= start_year, end_year= end_year) == True:
            Tot_PNL_dic = {}
            for market_year in range(start_year, end_year): # endyear-1 만큼만 시뮬가능하니까,
                Tot_PNL_dic.update(self.get_corps_year_profit(market_year= str(market_year), index_list= index_list))
            self.plot_profit_Dic(Tot_PNL_dic, index_list= index_list)
        else:
            print('Stratgy is not ready')
            for market_year in range(start_year, end_year+1):
                bsns_year = str(market_year-1) 
                self.set_dart_qaunt_ready(bsns_year=bsns_year)
            self.Profit_and_Loss(start_year, end_year)
    
    def plot_profit_Dic(self, Tot_PNL_dic, index_list):
        x = []
        y = {'Total_PNL':[]}
        for key in Tot_PNL_dic:
            x.append(key)    
            y['Total_PNL'].append(Tot_PNL_dic[key]['Total_PNL'])
            for index_name in index_list:
                if index_name in y: y[index_name].append(Tot_PNL_dic[key][index_name])
                else:
                    y[index_name] =[Tot_PNL_dic[key][index_name]]
                    
        plt.figure(1, figsize=(15, 6))
        color_list = ['r', 'k', 'b', 'g', 'm']
        color_len = len(color_list)
        width = 0.8
        for i,key in enumerate(y):
            width *= 0.9
            plt.bar(x, y[key], color=color_list[i%color_len],label = key,  width=width, alpha = 0.7)
        # 그래프 제목과 축 레이블 추가
        plt.title('Total_PNL')
        plt.xlabel(f'1 month')
        plt.ylabel('PNL')
        plt.xticks(rotation=80)
        plt.legend()
        plt.grid(True, which='both')

        plt.figure(2, figsize=(15, 6))
        color_list = ['r', 'k', 'b', 'g', 'm']
        color_len = len(color_list)
        cum_y = self.cal_cum_pnl(y)
        for i,key in enumerate(cum_y):
            plt.plot(x, cum_y[key], color=color_list[i%color_len], linewidth=2, linestyle='--', marker='o', markersize=8, label = key)
        # 그래프 제목과 축 레이블 추가
        plt.title('Total_PNL')
        plt.xlabel('1 month')
        plt.ylabel('Cumulative PNL')
        plt.xticks(rotation=80)
        plt.legend()
        plt.grid(True, which='both')

        plt.show()    

    def cal_cum_pnl(self, y):
        r_y ={}
        for key in y:
            pnl =100
            r_y[key] = []
            for item in y[key]:
                pnl *= (1 + item / 100)
                r_y[key].append(pnl)
        return r_y
    
    def check_ready(self, start_year, end_year):
        for market_year in range(start_year, end_year+1):
            bsns_year = str(market_year-1)
            if not self.stratgy_ready(bsns_year = bsns_year, rebalancing_date = self.rebalancing_date): return False
        
        return True
    
    def stratgy_ready(self, bsns_year,rebalancing_date):
        flag_path = self.data_path + f'/data_{bsns_year}/flags'
        if os.path.exists(flag_path):
            if os.path.exists(flag_path):
                with open(flag_path, 'r') as f:
                    flag_dic = json.load(f)
                if 'Stratgy' in flag_dic and 'MiningPrice' in flag_dic and 'PriceCrolling' in flag_dic:
                    if flag_dic['Stratgy'] == self.stratgy and flag_dic['MiningPrice'] == rebalancing_date and flag_dic['PriceCrolling'] == rebalancing_date: 
                        return True
        return False    
    
    def del_all_flag(self, start_year, end_year, flag_name):
        for market_year in range(start_year, end_year+1):
            bsns_year = str(market_year-1)        
            self.del_flag(bsns_year= bsns_year, flag_name = flag_name)

    def del_flag(self, bsns_year, flag_name):
        flag_path = self.data_path + f'/data_{bsns_year}/flags'
        if os.path.exists(flag_path):
            with open(flag_path, 'r') as f:
                flag_dic = json.load(f)
            if  flag_name in flag_dic: del flag_dic[flag_name]
            with open(flag_path, 'w') as f:
                json.dump(flag_dic, f)    
#-----------------------------------------------------------------------------------------------------------------
    def load_stratgy_corp_code(self, bsns_year):
        stratgy_path = self.data_path + f'/data_{bsns_year}/stratgy/{self.stratgy}.csv'
        df = pd.read_csv(stratgy_path, dtype= {'corp_code': str})
        return df['corp_code'].tolist()
    
    def get_corps_year_profit(self, market_year, index_list =['KOSTPI']):
        bsns_year = str(int(market_year)-1)
        corp_list = self.load_stratgy_corp_code(bsns_year)
        return_dic ={}
        init_ymd = market_year + self.rebalancing_date
        for i in range(1,13):
            profit_dic = {'Total_PNL': 0.0}
            start_ymd = get_next_ymd(ymd = init_ymd, nexttype='M', offset= i-1)
            end_ymd = get_next_ymd(ymd = init_ymd, nexttype='M', offset= i)
            count = 0
            for corp in corp_list:
                profit = get_corp_profit(corp_code= corp, start_ymd= start_ymd, end_ymd= end_ymd)
                if not profit == None:
                    count +=1
                    profit_dic[corp] = profit
                    profit_dic['Total_PNL'] += profit
                else:
                    print(corp)
                    get_corp_profit(corp_code= corp, start_ymd= start_ymd, end_ymd= end_ymd)
            for index_name in index_list:
                index_profit = get_index_profit(index_name= index_name, start_ymd= start_ymd, end_ymd= end_ymd)
                if index_profit:
                    profit_dic[index_name] = index_profit
            profit_dic['Total_PNL'] /= count
            return_dic[end_ymd] = profit_dic
        return return_dic
    
################################################################################################################
     