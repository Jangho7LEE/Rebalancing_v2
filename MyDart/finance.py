from MyDart.lib.utils import check_required_parameter
from MyDart.lib.utils import check_required_parameters
import os
def get_corp_finance(self,corp_code_list, reset = 0):
    '''
    get_corp_finance는 list에 존재하는 기업의 재무재표를 가져와 stock_dic에 저장한다.
    input: 
        reset: 0) data/finance에 있는 기업은 가져오지 않는다
               1) 모든 기업의 재무재표를가져온다
    '''
    if reset == 0:
        saved_corp_code_list = os.listdir(self.base_path + "/finance")
        target_list = [s for s in corp_code_list if s not in saved_corp_code_list]
        self.save_corp_finance(target_list)
    elif reset == 1:
        self.save_corp_finance(corp_code_list)
    else:
        raise KeyError('Invalid input param: check reset!')
    pass

def save_corp_finance(self,corp_code_list):
    '''
    save_corp_finance는 주어진 list에 해당하는 corp code를 가지는 기업의 재무정보를
    base_path/finance에 저장한다.
    '''
    for code in corp_code_list:
        data = self.corp_finance(corp_code=code, bsns_year=self.bsns_year, reprt_code="11011")
        if data['status'] == "000":
            self._save_file(path = f"/finance/{code}",data= data)

def corp_code(self):
    """
    |
    | DART에 등록되어있는 공시대상회사의 고유번호,회사명,종목코드, 최근변경일자를 파일로 제공합니다.
    |
    """
    url_path = "/api/corpCode.xml"
    return self.content_request("GET", url_path)

def corp_finance(self,corp_code, bsns_year, reprt_code):
    """
    |
    | 상장법인(유가증권, 코스닥) 및 주요 비상장법인(사업보고서 제출대상 & IFRS 적용)이 
    | 제출한 정기보고서 내에 XBRL재무제표의 주요계정과목(재무상태표, 손익계산서)을 제공합니다. 
    | (대상법인 복수조회 복수조회 가능)
    |  https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS003&apiId=2019017
    |
    """
    check_required_parameters([[corp_code,"corp_code"],[bsns_year,"bsns_year"],[reprt_code,"reprt_code"]])
    params = {"corp_code": corp_code,
              "bsns_year": bsns_year,
              "reprt_code":reprt_code  
              }
    url_path = "/api/fnlttMultiAcnt.json"
    return self.limit_request("GET", url_path, payload = params)