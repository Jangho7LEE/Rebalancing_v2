class stock(object):
    def __init__(self,**kwargs):
        if "corp_code" in kwargs: self.corp_code  = kwargs['corp_code'] # str
        if "corp_name" in kwargs: self.corp_name  = kwargs['corp_name'] # str
        if "stock_code" in kwargs: self.stock_code  = kwargs['stock_code'] # str
        if "modify_date" in kwargs: self.modify_date  = kwargs['modify_date']  # str
        if "financestate" in kwargs: self.financestate  = kwargs['financestate'] # dic
        self.financestate = {'status': 0} # status 1: 존재한다
    def export_dic(self):
        """
        |
        | export_dic은 stock에 저장된 정보를 dictionary 형태로 반환
        |
        """
        dic = {
            "corp_code": self.corp_code,
            "corp_name": self.corp_name,
            "stock_code": self.stock_code,
            "modify_date": self.modify_date,
            "financestate": self.financestate,
        }
        return dic

    