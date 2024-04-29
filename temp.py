import os
from MyBacktracker import Backtracker
# print(len(os.listdir("./data/market/price")))


rebalancing_date = '.04.26'
base_path = './data/market'
myback = Backtracker(stratgy = 'VC2',rebalancing_date = rebalancing_date, base_path = base_path)

# myback.update_market_datas()
#2023
start_year = 2020
end_year = 2024
myback.Profit_and_Loss(start_year = start_year, end_year= end_year)
