from MyDart.lib.utils import check_required_parameter
from MyDart.lib.utils import check_required_parameters

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