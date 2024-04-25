# from MyDart import DART
# from MyQuant import Quant

# import os

# def quant_init():
#     newDart.save_corp_code()
#     newQuant.set_stock_dic() # code를 stock에 저장

# def data_crolling():
#     if newDart.loadFlag("DataCrolling") == 'Off':
#         newDart.get_corp_finance(newQuant.stock_dic)
#         newDart.get_corp_stocknum(newQuant.stock_dic)
#         newDart.get_corp_price(newQuant.stock_dic)
#     newDart.saveFlag("DataCrolling")
    

# def data_mining():
#     if newQuant.loadFlag("DataMining") == 'Off':
#         newQuant.mining_finance()
#         newQuant.mining_stocknum()
#         newQuant.mining_price()
#         newQuant.curving_finance()
#     newQuant.saveFlag("DataMining")

# def qaunt():
#     newQuant.set_score()
#     newQuant.quant_stratgy()
    

# if __name__ == "__main__":
#     bsns_year = "2023"
#     rebalancing_date = '.04.05'
#     base_path = f"./data/data_{bsns_year}"
#     if not os.path.exists(base_path): os.makedirs(base_path)
    
#     newDart = DART(rebalancing_date= rebalancing_date, bsns_year = bsns_year, base_path = base_path)
#     newQuant = Quant(rebalancing_date= rebalancing_date, bsns_year = bsns_year, base_path = base_path) 
    
#     # Qaunt init phase
#     quant_init()

#     # Data crolling phase
#     data_crolling()

#     # Data mining phase
#     data_mining()

#     #get starage
#     qaunt()
    
    

