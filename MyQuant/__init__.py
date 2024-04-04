from MyQuant.lib.DataManager import DataManager

class Quant(DataManager):
    def __init__(self, bsns_year, base_path = "./data") -> None:
        super().__init__(base_path, bsns_year)
        
    '''
    | DataManager 기반 함수 
    '''
    from MyQuant.lib.DartXML import corp_code_to_stock
    from MyQuant.lib.DartXML import set_stock_dic
    
    from MyQuant.lib.DataMining import mining_finance
    from MyQuant.lib.DataMining import mining_price
    from MyQuant.lib.DataMining import mining_stocknum
    from MyQuant.lib.DataMining import curving_finance
    