# https://vintagefarm.co.kr/product/list.html?cate_no=112
import math
import requests
from bs4 import BeautifulSoup
import urllib
'''
1. 브랜드 페이지 접속하여 등록된 상품 총 수량을 파악하고 max-page를 계산한다.
2. 모든 페이지를 돌면서 모든 상품의 브랜드 명 만 가져온 후 set을 이용하여 brand_list를 만든다.
3. 각 브랜드로 조회 후 등록된 상품 총 수량을 파악하고 max-page를 계산한다.
4. 모든 페이지를 돌면서 모든 상품의 데이터를 가져온한 후 json을 만든다.

A. 만들어야할 공통 함수 
  a. 페이지 접속 후 총 수량 파악 후 max-page계산
      return max-page
  b. 특정 페이지에 나오는 상품의 데이터를 크롤링 하기
      return item-data
'''

# 입력 값에 대한 최대 페이지 수 계산
def get_max_page(total, count):
  # total = 등록된 총 아이템 수
  # count = 한 페이지당 보여지는 아이템 수
  max_page = math.ceil(total / count)
  return max_page

# 입력 url에 대한 html 가져오기
def get_html(url):
  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
  response = requests.get(url, headers=headers)
  html = response.text
  return html

# 입력 html에서 특정 값 받아오기
def get_data(html, data_type, class_name):
  soup = BeautifulSoup(html, 'html.parser')
  if(data_type == 'total'):
    print(class_name)
    data = int(soup.select_one(class_name).text)  
  if(data_type == 'brand_list'):
    data = soup.select(class_name)
    print(data)
    return data

# 검색어가 입력된 url 만들기
def set_url(url, values):
  data = urllib.parse.urlencode(values)
  new_url = url + '?' + data
  return new_url

def get_brand_list(url, max_page):
  brand_list = []
  for i in range(1, max_page+1):
    url = set_url(url,{'page': i})
    html = get_html(url)
    class_name = '.PrdItem .description .xans-product-listitem > li:nth-child(1) > span'
    brand_name = get_data(html, 'brand_list', class_name)
    brand_list.append(brand_name)
    print(brand_name)
    brand_list = list(set(brand_list))

  return brand_list

def start_clawling(url, search_url, name, count):
  html = get_html(url)
  total = get_data(html, 'total', '#ListTotalCount strong')
  print(total)
  max_page = get_max_page(total, count)
  print(max_page)
  brand_list = get_brand_list(url, max_page)
  print(brand_list, len(brand_list))
  # set_url(search_url,{'keyword': 'adidas','page': 2})
  

  
  
start_clawling(
  'https://vintagefarm.co.kr/product/list.html?cate_no=112',
  'https://vintagefarm.co.kr/product/search.html?banner_action=&keyword=adidas&page=2',
  'vintagefarm',
  120
)