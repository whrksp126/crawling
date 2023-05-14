import requests
url = 'https://www.kbchachacha.com/public/search/list.empty?page=1&sort=sellAmt&makerCode=101&classCode=1109&carCode=3079&_pageSize=4&pageSize=5'
response = requests.get(url)
html = response.text
print(html)

import requests

url = 'https://api.kcar.com/bc/search/list/drct'

params = {
    'limit': 26,
    'orderBy': "time_deal_yn:desc|time_deal_end_dt:asc|hotdeal_stnc:asc|sort_ordr:asc",
    'orderFlag': True,
    'pageno': 1,
    'wr_eq_sell_dcd': "ALL",
    'wr_in_multi_columns': "cntr_rgn_cd|cntr_cd",
    'wr_in_multi_mnuftr_modelGrp_model': "001,019,176",
}

response = requests.post(url, json=params)

print(response.json())  # 서버에서 반환하는 JSON 형식의 응답을 출력합니다

## Kcar
# https://www.kcar.com/


# Post 요청
# https://api.kcar.com/bc/search/list/drct
# { 
#   'limit': 26,
#   'orderBy': "time_deal_yn:desc|time_deal_end_dt:asc|hotdeal_stnc:asc|sort_ordr:asc",
#   'orderFlag': true,
#   'pageno': 1,
#   'wr_eq_sell_dcd': "ALL",
#   'wr_in_multi_columns': "cntr_rgn_cd|cntr_cd",
#   'wr_in_multi_mnuftr_modelGrp_model': "001,019,176",
# }




# {
#   'useNm':'영업용',
#   'reqStsCd':'30',
#   'hotdealStnc':'',
#   'rentPriceAvc':'',
#   'themeExhbtYn':'N',
#   'buyFlag':'Y',
#   'mnuftrNm':'현대',
#   'cntrRgnNm':'경북',
#   'dcPrc':'',
#   'trnsmsnCd':'001',
#   'instAmt':'32',
#   'extrColorNm':'쥐색',
#   'prcGrpCd':'002',
#   'outaprncNm':'',
#   'optnCd':'001|005|014|017|020|022|023|024|026|027|030|031|032|033|034|036|037|055|056|057|058|068|072|083|086|088|091|092|097|205',
#   'acdtHistCd':'300',
#   'grdNm':'LPG 1.6 (일반인판매용)',
#   'fuelCd':'003',
#   'timeDealYn':'N',
#   'carctgrNm':'준중형차',
#   'selerSafeMbpno':'0504-3187-0362',
#   'prc':'1910',
#   'selerSafeTno':'0504-1370-3568',
#   'carctgrCd':'003',
#   'milg':'9494',
#   'trnsmsnNm':'오토',
#   'leseType':'3',
#   'keywordNm':'사회초년생첫차',
#   'keywordNo':'2',
#   'selerMpno':'010-9925-5429',
#   'mfgDt':'202103',
#   'carWhlNm':'현대 아반떼 (CN7) LPG 1.6 (일반인판매용) 스마트',
#   'dcFlag':'N',
#   'extrColorCd':'COLOR0220',
#   'simcDesc':'1인소유★보험이력無★앰비언트라이트★순정내비★엔진오일 신품',
#   'cntrRgnCd':'DEGUE',
#   'pasngrCnt':'5',
#   'hotmarkNm':'제조사AS;보험이력없음',
#   'csgmtYn':'N',
#   'mnuftrCd':'001',
#   'fuelNm':'LPG',
#   'grdDtlCd':'002',
#   'onlnSellAplyYn':'N',
#   'selerNm':'김영남',
#   'rentAmtN4':'',
#   'resvYn':'N',
#   'rentType':'',
#   'acdtHistCnts':'무사고',
#   'modelCd':'176',
#   'msizeImgPath':'https://img.kcar.com/carpicture/carpicture10/pic6080/kcarM_60802500_045.jpg',
#   'sellEmpId':'3667',
#   'carType':'KOR',
#   'timeDealEndDt':'',
#   'hotmarkCd':'26;30',
#   'prepareReqCnt':'',
#   'modelGrpCd':'019',
#   'grdDtlNm':'스마트',
#   'onlnSellAplyStrtDt':'',
#   'regType':'SELL',
#   'cntrCd':'162',
#   'leseCondYn':'N',
#   'ssizeImgPath':'https://img.kcar.com/carpicture/carpicture10/pic6080/kcar_60802500_043.jpg',
#   'lsizeImgPath':'https://img.kcar.com/carpicture/carpicture10/pic6080/kcarM_60802500_001.jpg',
#   'udtkngExcalAmt':'0',
#   'sortOrdr':'8264',
#   'cno':'226저7855',
#   'gmCertYn':'',
#   'modelNm':'아반떼 (CN7)',
#   'engdispmnt':'1591',
#   'useCd':'U02',
#   'view3dFg':'2D',
#   'optnNm':'ABS|내비게이션|가죽시트|알루미늄 휠|에어백 : 사이드|열선시트 : 운전석|오토 에어컨|전동접이사이드미러|에어백 : 운전석|에어백 : 조수석|룸미러 : ECM|스티어링 휠 리모컨|감지센서 : 후방|TPMS : 타이어공기압감지|통풍시트 : 운전석|차체자세 제어장치|에어백 : 커튼|스마트키|카메라 : 후방|크루즈컨트롤|USB 단자|차량 메뉴얼|오토 라이트|블루투스|열선시트 : 조수석|LDWS:차선이탈경보시스템|자동긴급제동|하이패스',
#   'rentRegYn':'N',
#   'prdcnYr':'2021',
#   'prcGrpNm':'1천만원대',
#   'carCd':'EC60802500',
#   'outaprncCd':'',
#   'mnuftrType':'MAKE_TYPE010',
#   'sellDcd':'GNRL',
#   'prepareBuyRegDt':'',
#   'grdCd':'002',
#   'cntrNm':'포항직영점',
#   'modelGrpNm':'아 반떼'
# },


# 중고 차량 개별 상세 페이지  'carCd':'EC60802500', 
# https://www.kcar.com/bc/detail/carInfoDtl?i_sCarCd=EC60826417

### 차량 별 세부 데이터 POST
# https://api.kcar.com/bc/inst-calc
# {carCd: "EC60826417"}