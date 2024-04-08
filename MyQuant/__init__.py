from MyQuant.lib.DataManager import DataManager
from scipy.stats import percentileofscore
import pandas as pd

class Quant(DataManager):
    def __init__(self, bsns_year, base_path = "./data") -> None:
        super().__init__(base_path, bsns_year)
        self.value_list_low_good = ['PBR', 'PER', 'PSR', 'EE', 'PCR',]
        self.value_list_high_good = ['DIV',]
        self.score_df = None

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

    def _stockdic_to_df(self,rlist):
        df_dic = {}
        for s in self.stock_dic:
            df_dic[self.stock_dic[s].corp_name] = self._rlist_to_dic(self.stock_dic[s], rlist)
        self.score_df = pd.DataFrame(df_dic).transpose()
        self._cal_total_score(rlist)
        self.score_df = self.score_df.sort_values(by= 'Total Score', ascending= False)
        print(self.score_df.head())

    def _rlist_to_dic(self,stock,rlist):
        temp_dic = {}
        for v in rlist:
            temp_dic[v] = stock.valuestate[v]['value']
            temp_dic[v + ' score'] = stock.valuestate[v]['score']
        return temp_dic

    def _cal_total_score(self, rlist):
        self.score_df['Total Score'] = 0
        for v in rlist:
            self.score_df['Total Score'] += self.score_df[v + ' score']
        

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
            if self.stock_dic[s].valuestate[value]['value'] > 0 and lowhigh == 'low':
                temp_dic[s] = 999
                
        percentiles = {key: percentileofscore(list(temp_dic.values()), value) for key, value in temp_dic.items()}
        
        if lowhigh == 'low':
            points_dict = {key: 100 - percentile for key, percentile in percentiles.items()}
        elif lowhigh == 'high':
            points_dict = {key: percentile for key, percentile in percentiles.items()}

        for s in points_dict:
            self.stock_dic[s].valuestate[value]['score'] = points_dict[s]
            
    def quant_stratgy(self, st ='VC2'):
        if st == 'VC2':
            self.quant_VC2()
            

    def quant_VC2(self):
        rlist =['PBR', 'PER', 'PSR', 'EE', 'PCR','DIV']
        self._ceck_required_value(rlist)
        self._stockdic_to_df(rlist)

