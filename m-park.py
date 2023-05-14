import requests
import time

## requests GET으로 가져온 데이터 JSON으로 변환
def get_data(url):
  response = requests.get(url)
  data = response.json()
  return data

## JSON 데이터에서 새로운 데이터 리스트 뽑기
def transform_data(data, level_key, key_mapping=None):
  ori_brand_data = data['data'][level_key]
  brand_list = []
  for brand_data in ori_brand_data:
    new_dict = {}
    for mapping in key_mapping:
      new_dict[mapping['new_key']] = brand_data[mapping['origin_key']]
    brand_list.append(new_dict)
  return brand_list

## url 만들기
def make_url(country, maker, model, model_detail, type):
  
  url_template = ''
  if type == 'list' :
    url_template = 'https://api.m-park.co.kr/home/api/v1/wb/main/carcodetotal/get?menuType=search&country={}&maker={}&model={}&modelDetail={}'
  else :
    url_template = 'https://api.m-park.co.kr/home/api/v1/wb/searchmycar/carlistinfo/get?country={}&maker={}&model={}&modelDetail={}'
    
  url = url_template.format(country, maker, model, model_detail)
  return url



def crawling_fun():
  count = 0
  country = 1
  url = make_url(country, maker='', model='', model_detail='', type='list')
  data = get_data(url)
  level_key='level1'
  key_mapping = [
    {'origin_key': 'carCode', 'new_key': 'brand_id'},
    {'origin_key': 'carName', 'new_key': 'brand_name'},
    {'origin_key': 'cnt', 'new_key': 'count'},
  ]
  brand_list = transform_data(data, level_key, key_mapping=key_mapping)
  print('brand_list',len(brand_list))
  for brand in brand_list:
    url = make_url(country, maker=brand['brand_id'], model='', model_detail='', type='list')
    data = get_data(url)
    level_key='level2'
    key_mapping = [
      {'origin_key': 'carCode', 'new_key': 'model_id'},
      {'origin_key': 'carName', 'new_key': 'model_name'},
      {'origin_key': 'cnt', 'new_key': 'count'},
    ]
    model_list = transform_data(data, level_key, key_mapping=key_mapping)
    print('model_list',len(model_list))
    for model in model_list:
      url = make_url(country, maker=brand['brand_id'], model=model['model_id'], model_detail='', type='list')
      data = get_data(url)
      level_key='level3'
      key_mapping = [
        {'origin_key': 'carCode', 'new_key': 'rating_id'},
        {'origin_key': 'carName', 'new_key': 'rating_name'},
        {'origin_key': 'cnt', 'new_key': 'count'},
        {'origin_key': 'codeNameYear', 'new_key': 'rating_year'},
      ]
      rating_list = transform_data(data, level_key, key_mapping=key_mapping)
      print('rating_list',len(rating_list))
      for rating in rating_list:
        url = make_url(country, maker=brand['brand_id'], model=model['model_id'], model_detail=rating['rating_id'], type='')
        data = get_data(url)
        for car in data['data']:
          print(brand['brand_name'], model['model_name'], rating['rating_name'], car['carName'])
          count = count + 1
  print('총',count,'개의 상품이 있습니다')


start_time = time.perf_counter()
crawling_fun()
end_time = time.perf_counter()
print("Execution time: {:.5f} seconds".format(end_time - start_time))



# 제조국, 제조사, 모델, 등급,

# m-park
# https://www.m-park.co.kr/buy/search

### 국산차 리스트 종류
# https://api.m-park.co.kr/home/api/v1/wb/main/carcodetotal/get?menuType=search&country=1 국산차
# https://api.m-park.co.kr/home/api/v1/wb/main/carcodetotal/get?menuType=search&country=1&maker=5 현대차
# https://api.m-park.co.kr/home/api/v1/wb/main/carcodetotal/get?menuType=search&country=1&maker=5&model=129 포터
### 수입차 리스트 종류
# https://api.m-park.co.kr/home/api/v1/wb/main/carcodetotal/get?menuType=search&country=2 수입차
# https://api.m-park.co.kr/home/api/v1/wb/main/carcodetotal/get?menuType=search&country=2&maker=68 벤츠
# https://api.m-park.co.kr/home/api/v1/wb/main/carcodetotal/get?menuType=search&country=2&maker=68&model=145 AMG GT
# https://api.m-park.co.kr/home/api/v1/wb/main/carcodetotal/get?menuType=search&country=2&maker=68&model=147&modelDetail=1102

### 차량 디테일 정보 받아오기
# https://api.m-park.co.kr/home/api/v1/wb/searchmycar/carlistinfo/get?country=2&maker=68&model=147&modelDetail=1102 
# country : 국산차, 수입차
# maker : 현대차, 기아차, 포르쉐, 벤츠
# model : 포터, 그랜저, 소나타, B클래스
# modelDetail : (15 ~ 현재), B클래스(2세대), B클래스(1세대)

# https://api.m-park.co.kr/home/api/v1/wb/searchmycar/carlistinfo/get?
#   maker=5&
#   model=112&
#   modelDetail=2854


# https://api.m-park.co.kr/home/api/v1/wb/main/carcodetotal/get?
#   menuType=search&
#   maker=5&
#   model=112&
#   modelDetail=1571

# maker=5 제조사
# model=112 모델 그룹명
# modelDetail=1571 모델명


### html 분석해서 내부 데이터 빼와야함
# https://www.m-park.co.kr/buy/detail/3031502314