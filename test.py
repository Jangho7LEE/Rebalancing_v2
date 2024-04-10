from MyDart import DART
from MyQuant import Quant


def quant_init():
    newDart.save_corp_code()
    newQuant.set_stock_dic() # code를 stock에 저장

def data_crolling():
    newDart.get_corp_finance(newQuant.stock_dic)
    newDart.get_corp_stocknum(newQuant.stock_dic)
    newDart.get_corp_price(newQuant.stock_dic)
    

def data_mining():
    newQuant.mining_finance()
    newQuant.mining_stocknum()
    newQuant.mining_price()
    newQuant.curving_finance()
    newQuant.set_score()

def qaunt():
    newQuant.quant_stratgy()
    

if __name__ == "__main__":
    bsns_year = "2023"
    newDart = DART(bsns_year = bsns_year, base_path = f"./data_{bsns_year}")
    newQuant = Quant(bsns_year = bsns_year, base_path = f"./data_{bsns_year}") # declare

    # Qaunt init phase
    quant_init()

    # Data crolling phase
    # data_crolling()

    # Data mining phase
    # data_mining()

    #get starage
    qaunt()
    
    

