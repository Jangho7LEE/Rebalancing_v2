import os
from MyBacktracker import Backtracker
# print(len(os.listdir("./data/market/price")))


rebalancing_date = '.04.05'
base_path = './data/market'
myback = Backtracker(stratgy = 'VC2',rebalancing_date = rebalancing_date, base_path = base_path)

#2023
start_year = 2020
end_year = 2024
for market_year in range(start_year, end_year+1):
    bsns_year = str(market_year-1) 
    myback.set_dart_qaunt_ready(bsns_year=bsns_year)