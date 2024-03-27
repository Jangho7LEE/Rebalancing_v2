from MyDart import DART
from MyQuant import Quant





    
def quant_init():
    newDart.save_corp_code()
    newQuant.set_stock_dic() # code를 stock에 저장

def data_crolling():
    newDart.get_corp_finance(newQuant.get_corp_code_list())

def data_mining():
    pass
if __name__ == "__main__":
    newDart = DART(bsns_year = "2023")
    newQuant = Quant() # declare

    # Qaunt init phase
    quant_init()

    # Data crolling phase
    # data_crolling()

    # Data mining phase
    data_mining()
