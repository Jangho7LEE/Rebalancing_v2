import os
from MyBacktracker import Backtracker
# print(len(os.listdir("./data/market/price")))
myback = Backtracker()
myback.set_market_data()
# myback.corp_dic['00126380'] = '005930'
# myback.get_market_data(corp_code='00126380')