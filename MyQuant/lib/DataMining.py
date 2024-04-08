import os


def mining_finance(self):
    corp_code_in_finance = os.listdir(self.finance_path)
    for corp_code in list(self.stock_dic.keys()):
        if corp_code in corp_code_in_finance:
            corp_code_fianance_path = self.finance_path + f'/{corp_code}'
            finance_dic = self.openfile(data_path=corp_code_fianance_path)
            self.stock_dic[corp_code].financestate = set_financestate(financial_list = finance_dic['list'])
        else:
            self.stock_dic[corp_code].financestate['status'] = 0  
    self.save_stock_dic()

def mining_stocknum(self):
    corp_code_in_price = os.listdir(self.stocknum_path)
    for corp_code in list(self.stock_dic.keys()):
        if corp_code in corp_code_in_price:
            corp_code_stocknum_path = self.stocknum_path + f'/{corp_code}'
            stocknum_dic = self.openfile(data_path=corp_code_stocknum_path)
            set_stocknum(stocknum_list = stocknum_dic['list'], input_dic= self.stock_dic[corp_code].financestate)
        else: 
            self.stock_dic[corp_code].financestate['status'] = 0
    self.save_stock_dic()

def set_stocknum(stocknum_list, input_dic):
    stock_keyword =['의결권있는주식', '의결권주식', '의결권이있는주식', '의결권有', '의결권있는주식수']
    prefferd_stock_keyword = ['의결권없는주식', '무의결권주식']
    for dic in stocknum_list:
        if 'distb_stock_co' in dic and dic['se'] !='비고' and dic['distb_stock_co'] != '-':
            se = dic['se'].replace(" ","").replace("\t","").replace("\n","")
            if '보통' in se or se in stock_keyword : 
                input_dic['보통주'] = float(dic['distb_stock_co'].replace(",",""))
            elif '우선' in se or se in prefferd_stock_keyword :
                input_dic['우선주'] = float(dic['distb_stock_co'].replace(",",""))
            else:
                input_dic['status'] = 0
            

def mining_price(self):
    corp_code_in_price = os.listdir(self.price_path)
    for corp_code in list(self.stock_dic.keys()):
        if corp_code in corp_code_in_price:
            corp_code_price_path = self.price_path + f'/{corp_code}'
            price_dic = self.openfile(data_path=corp_code_price_path)
            set_price(price_dic = price_dic, input_dic= self.stock_dic[corp_code].financestate)
        else: 
            self.stock_dic[corp_code].financestate['status'] = 0
    self.save_stock_dic()

def set_price(price_dic, input_dic):
    input_dic['status'] = 1
    for price in price_dic:
        input_dic[price] = float(price_dic[price])
    
def set_financestate(financial_list):
    newDic = {'status': 1}
    bs_year = int(financial_list[0]['bsns_year'])
    for account in financial_list:
        newDic[account['account_id']] = {}
        if 'thstrm_amount' in account and len(account['thstrm_amount'])>1:
            newDic[account['account_id']][f'{bs_year}'] = float(account['thstrm_amount'].replace('.',''))
        if 'frmtrm_amount' in account and len(account['frmtrm_amount'])>1: 
            newDic[account['account_id']][f'{bs_year-1}'] = float(account['frmtrm_amount'].replace('.',''))
        if 'bfefrmtrm_amount' in account and len(account['bfefrmtrm_amount'])>1: 
            newDic[account['account_id']][f'{bs_year-2}'] = float(account['bfefrmtrm_amount'].replace('.',''))
    return newDic

def curving_finance(self):
    stocks = list(self.stock_dic.keys())
    for s in stocks:
        if self.stock_dic[s].financestate['status'] == 0:
            del self.stock_dic[s]
        else:
            self.stock_dic[s].valuestate['status'] = 1
            _set_values(self.stock_dic[s], self.bsns_year)
            if self.stock_dic[s].valuestate['status'] == 0:
                del self.stock_dic[s]
    self.save_stock_dic()


def _set_values(stock,bsns_year):
    _set_values_PBR(stock, bsns_year)
    _set_values_PER(stock, bsns_year)
    _set_values_PSR(stock, bsns_year)
    _set_values_EE(stock, bsns_year)
    _set_values_PCR(stock, bsns_year)
    _set_values_DIV(stock, bsns_year)


def _get_market_cap(stock):
    '''
    기업 시가 총액을 계산: 주가*보통주(유통주식수) + 우선주 주가*우선주(유통주식수)
    '''
    if '우선주' in stock.financestate and 'preffered_stockprice' in stock.financestate:
        return stock.financestate['보통주'] * stock.financestate['stockprice'] + stock.financestate['우선주']*stock.financestate['preffered_stockprice']
    elif '우선주' in stock.financestate:
         return (stock.financestate['보통주'] + stock.financestate['우선주']) * stock.financestate['stockprice'] 
    else:
        return stock.financestate['보통주'] * stock.financestate['stockprice']

def _check_account(stock, paramlist,bsns_year):
    check = 1
    for account in paramlist:
        if account not in stock.financestate: check = 0
        elif bsns_year not in stock.financestate[account]: check = 0
        
    return check

def _set_values_PBR(stock,bsns_year):
    '''
    PBR = 주가 / 주당 순자산 = 시가총액 / 순자산 
    순자산 = 자산총계 (ifrs-full_Assets) - 부채총계 (ifrs-full_Liabilities)
    '''
    required_account_list = ['ifrs-full_Assets',
                             'ifrs-full_Liabilities',
                             ]
    if _check_account(stock,required_account_list,bsns_year):
        PBR  = _get_market_cap(stock) / (stock.financestate['ifrs-full_Assets'][bsns_year] - stock.financestate['ifrs-full_Liabilities'][bsns_year])
        stock.valuestate['PBR'] = {'value' : PBR}
    else: stock.valuestate['status'] = 0
    

def _set_values_PER(stock,bsns_year):
    '''
    PER = 주가 / 주당 순이익 = 시가총액 / 순이익 (ifrs-full_ProfitLoss)
    '''
    required_account_list = ['ifrs-full_ProfitLoss',
                             ]
    if _check_account(stock,required_account_list,bsns_year):
        PER  = _get_market_cap(stock) / (stock.financestate['ifrs-full_ProfitLoss'][bsns_year])
        stock.valuestate['PER'] = {'value' : PER}
    else: stock.valuestate['status'] = 0

def _set_values_PSR(stock,bsns_year):
    '''
    PSR = 주가 / 주당 매출액 = 시가총액 / 매출액 (ifrs-full_Revenue)
    '''
    required_account_list = ['ifrs-full_Revenue',
                             ]
    if _check_account(stock,required_account_list,bsns_year):
        PSR  = _get_market_cap(stock) / (stock.financestate['ifrs-full_Revenue'][bsns_year])
        stock.valuestate['PSR'] = {'value' : PSR}
    else: stock.valuestate['status'] = 0
    

def _set_values_EE(stock,bsns_year):
    '''
    EV/EBITDA 
    기업 인수비용 EV = 시가총액 + 부채총계 (ifrs-full_Liabilities)- 현금및현금성자산 (ifrs-full_CashAndCashEquivalents)
    EBITDA = 법인세비용차감전순이익 (ifrs-full_ProfitLossBeforeTax) + 감가상각비 
    우선은 EBITDA를 법인세비용차감전순이익 (ifrs-full_ProfitLossBeforeTax) 으로 대체한다
    '''
    required_account_list = ['ifrs-full_Liabilities',
                             'ifrs-full_CashAndCashEquivalents',
                             'ifrs-full_ProfitLossBeforeTax',
                             ]
    if _check_account(stock,required_account_list,bsns_year):
        EV = _get_market_cap(stock) + stock.financestate['ifrs-full_Liabilities'][bsns_year] - stock.financestate['ifrs-full_CashAndCashEquivalents'][bsns_year]
        EBITDA =  stock.financestate['ifrs-full_ProfitLossBeforeTax'][bsns_year]
        stock.valuestate['EE'] = {'value' : EV/EBITDA}
    else: stock.valuestate['status'] = 0

def _set_values_PCR(stock,bsns_year):
    '''
    PCR = 주가 / 주당 영업 현금흐름 = 시가총액 / 영업활동현금흐름 (ifrs-full_CashFlowsFromUsedInOperatingActivities)
    '''
    required_account_list = ['ifrs-full_CashFlowsFromUsedInOperatingActivities',
                             ]
    if _check_account(stock,required_account_list,bsns_year):
        PCR  = _get_market_cap(stock) / (stock.financestate['ifrs-full_CashFlowsFromUsedInOperatingActivities'][bsns_year])
        stock.valuestate['PCR'] = {'value' : PCR}
    else: stock.valuestate['status'] = 0

def _set_values_DIV(stock,bsns_year):
    '''
    배당수익률 = 주당 배당금 / 주가 = 배당금 (ifrs-full_DividendsPaidClassifiedAsFinancingActivities) / 시가총액
    '''
    required_account_list = ['ifrs-full_DividendsPaidClassifiedAsFinancingActivities',
                             ]
    if _check_account(stock,required_account_list,bsns_year):
        DIV  = (stock.financestate['ifrs-full_DividendsPaidClassifiedAsFinancingActivities'][bsns_year]) / _get_market_cap(stock) 
        stock.valuestate['DIV'] = {'value' : DIV}
    else:
        stock.valuestate['DIV'] = {'value' : 0}
    

