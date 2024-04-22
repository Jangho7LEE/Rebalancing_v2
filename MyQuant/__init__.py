from MyQuant.lib.DataManager import DataManager
from scipy.stats import percentileofscore
import pandas as pd

class Quant(DataManager):
    def __init__(self, rebalancing_date, bsns_year, base_path = "./data") -> None:
        super().__init__(base_path, bsns_year)
        self.value_list_low_good = ['PBR', 'PER', 'PSR', 'EE', 'PCR',]
        self.value_list_high_good = ['DIV',]
        self.score_df = None
        self.stratgy_df = None
        self.rebalancing_date = rebalancing_date

    '''
    | DataManager 기반 함수 
    '''
    from MyQuant.lib.DartXML import corp_code_to_stock
    from MyQuant.lib.DartXML import set_stock_dic
    
    from MyQuant.lib.DataMining import mining_finance
    from MyQuant.lib.DataMining import mining_price
    from MyQuant.lib.DataMining import mining_stocknum
    from MyQuant.lib.DataMining import curving_finance
    
    def _ceck_required_value(self, rlist):
        for v in rlist:
            if not (v in self.value_list_low_good or v in self.value_list_high_good): raise KeyError()

    def _stockdic_to_df(self,rlist, addlist, adjust_val):
        df_dic = {}
        for s in self.stock_dic:
            df_dic[self.stock_dic[s].corp_name] = self._lists_to_dic(self.stock_dic[s], rlist, addlist)
        self.score_df = pd.DataFrame(df_dic).transpose()
        self._cal_total_score(rlist, adjust_val)
        self.score_df = self.score_df.sort_values(by= 'Total Score', ascending= False)
        

    def _lists_to_dic(self,stock,rlist, addlist):
        temp_dic = {}
        for v in rlist:
            temp_dic[v] = stock.valuestate[v]['value']
            temp_dic[v + ' score'] = stock.valuestate[v]['score']
        for v in addlist:
            temp_dic[v] = stock.financestate[v]
        return temp_dic

    def _cal_total_score(self, rlist, adjust_val):
        self.score_df['Total Score'] = 0
        for i,v in enumerate(rlist):
            self.score_df['Total Score'] += self.score_df[v + ' score']*adjust_val[i]
        

    def set_score(self):
        self.set_low_scores()
        self.set_high_scores()
        self.save_stock_dic()

    def set_low_scores(self):
        for val in self.value_list_low_good:
            self.cal_score(value= val, lowhigh= 'low')

    def set_high_scores(self):
        for val in self.value_list_high_good:
            self.cal_score(value= val, lowhigh= 'high')
    
    def cal_score(self, value, lowhigh):
        temp_dic = {}
        for s in self.stock_dic:
            temp_dic[s] = self.stock_dic[s].valuestate[value]['value']
            if self.stock_dic[s].valuestate[value]['value'] < 0 and lowhigh == 'low':
                temp_dic[s] = 999
                
        percentiles = {key: percentileofscore(list(temp_dic.values()), value) for key, value in temp_dic.items()}
        
        if lowhigh == 'low':
            points_dict = {key: 100 - percentile for key, percentile in percentiles.items()}
        elif lowhigh == 'high':
            points_dict = {key: percentile for key, percentile in percentiles.items()}

        for s in points_dict:
            self.stock_dic[s].valuestate[value]['score'] = points_dict[s]
            
    def quant_stratgy(self, st ='VC2'):
        if st == 'VC2': # 추세형 가치주 포트폴리오(전체 주식 VC2 상위 10%, 6개월 가격 모멘텀 (상위 25종목)
            self.quant_VC2()
        elif st == 'TGS':
            pass
            

    def quant_VC2(self):
        # rlist =['PBR', 'PER', 'PSR', 'EE', 'PCR','DIV'] # in valuestate
        # adjust_val = [1.105929355280393, 0.9430336648179733, 1.4643396915758484, 2.352206654626052, 1.153208866905027, 0.2610796835633595]
        rlist =['PER', 'PSR', 'EE', 'PCR'] # in valuestate
        adjust_val = [ 0.9430336648179733, 1.4643396915758484, 2.352206654626052, 1.153208866905027]
        addlist =['6M momentum'] # in financestate
        self._ceck_required_value(rlist)
        self._stockdic_to_df(rlist, addlist, adjust_val)
        score_cutline = self.score_df['Total Score'].quantile(0.9)
        self.stratgy_df = self.score_df[self.score_df['Total Score'] >= score_cutline]
        self.stratgy_df = self.stratgy_df.sort_values(by= '6M momentum', ascending= False)
        print(self.stratgy_df.head(25).to_csv('VC2.csv'))

    def quant_TGS(self):
        pass