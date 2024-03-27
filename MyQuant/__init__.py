from MyQuant.lib.DataManager import DataManager

class Quant(DataManager):
    def __init__(self, base_path = "./data") -> None:
        super().__init__(base_path)
    '''
    | DataManager 기반 함수 
    '''
    from MyQuant.lib.DartXML import corp_code_to_stock
    from MyQuant.lib.DartXML import set_stock_dic