# https://vintagefarm.co.kr/product/list.html?cate_no=112
import math
import requests
from bs4 import BeautifulSoup
import urllib
import time
import json
import threading
from queue import Queue
'''
1. 브랜드 페이지 접속하여 등록된 상품 총 수량을 파악하고 max-page를 계산한다.
2. 모든 페이지를 돌면서 모든 상품의 브랜드 명 만 가져온 후 set을 이용하여 brand_list를 만든다.
3. 각 브랜드로 조회 후 등록된 상품 총 수량을 파악하고 max-page를 계산한다.
4. 모든 페이지를 돌면서 모든 상품의 데이터를 가져온한 후 json을 만든다.

1) 브랜드 페이지 접속하여 등록된 상품 총 수량을 파악하고 max-page를 계산한다.
2) max-page를 이용하여 모든 페이지 number를 Queue에 넣는다.
3) 쓰레드 갯수를 선언하고 선언된 쓰레드를 이용하여 Queue에 일을 실행한다.
4) 각 쓰레드가 실행해서 return 한 값들을 item_list에 담는다.


A. 만들어야할 공통 함수 
  a. 페이지 접속 후 총 수량 파악 후 max-page계산
      return max-page
  b. 특정 페이지에 나오는 상품의 데이터를 크롤링 하기
      return item-data

가져올 데이터
'href_url' : 
'img_url' :
'name' : 
'brand' : 
'price' :
'discount_price' :
'size' : 

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
    data = int(soup.select_one(class_name).text)  
  if(data_type == 'item_list'):
    data = soup.select(class_name)
  return data

# 검색어가 입력된 url 만들기
def set_url(url, values):
  data = urllib.parse.urlencode(values)
  new_url = url + '?' + data
  return new_url

# 키워드로 item에서 특정 태그 찾고 값 출력하기
def find_element(item, tag, keyword, select_one):
  for element in item.find_all(tag):
    if keyword in element.text:
      return element.select_one(select_one).text.strip()

# 상품 데이터 받아오기
def get_product_data(item):
  data = {
    'brand' : find_element(item, "li", "브랜드", "li > span"),
    'name' : item.select_one(".description .name a span:nth-child(2)").text.strip(),
    'price' : find_element(item, "li", "판매가", "li > span"),
    'discount_price' : find_element(item, "li", "할인판매가", "li > span"),
    'size' : find_element(item, "li", "실측사이즈 cm", "li > span"),
    'img_url' : 'https:' + item.select_one(".thumbnail > a > img")['data-src'],
    'href_url' : 'https://vintagefarm.co.kr/' + item.select_one(".thumbnail a")['href'],
  }
  return data

def check_sortout(item):
  img = item.select_one('.PrdItem .icon .promotion img')
  if img and img['alt'] == '품절':
    return True
  else:
    return False
  
def get_item_list(url, max_page):
  item_list = []
  sortout = False
  # 1. 전체 페이지 수 확인하고 반복을 돌린다.
  # 2. 각 페이지에서 아이템 태그를 가져온다.
  # 3. 각 태그를 반복을 돌면서 품절인지 확인하다.
  # 4. 만약 품절이면 그 순간 반복문을 종료한다.
  # 5. 만약 품절이 아니면 아이템에 대한 데이터를 item_list에 담는다.

  
  for i in range(1, max_page+1):
    if(sortout): return
    new_url = set_url(url,{'cate_no':112, 'page': i})
    html = get_html(new_url)
    soup = BeautifulSoup(html, 'html.parser')
    print(new_url)
    class_name = '.PrdItem'
    items = soup.select(class_name)
    for item in items:
      # 품절인지 확인
      sortout = check_sortout(item)
      if(sortout):
        return item_list
      
      data = get_product_data(item)
      
      item_list.append(data)
      
def get_item_list_thread(item_list):
  while True:
    data = url_queue.get()
    if data is None:
      break
    
    new_url = set_url(data['url'],{'cate_no':112, 'page': data['page']})
    html = get_html(new_url)
    soup = BeautifulSoup(html, 'html.parser')
    print(new_url)
    class_name = '.PrdItem'
    items = soup.select(class_name)
    url_queue.task_done()
    for item in items:
      # 품절인지 확인
      sortout = check_sortout(item)
      if(sortout == False):
        data = get_product_data(item)
        item_list.append(data)
      

def start_clawling(url, search_url, name, count):
  new_url = set_url(url,{'cate_no':112})
  html = get_html(new_url)
  total = get_data(html, 'total', '#ListTotalCount strong')
  max_page = get_max_page(total, count)  
  item_list = get_item_list(url, max_page)
  return item_list

def start_clawling_thread(url, search_url, name, count):
  
  new_url = set_url(url,{'cate_no':112})
  html = get_html(new_url)
  total = get_data(html, 'total', '#ListTotalCount strong')
  max_page = get_max_page(total, count)
  item_list = []
  for i in range(1, max_page+1):
    print(i)
    url_queue.put({'page':i, 'url':url})
  # 스레드를 생성하고 실행합니다.
  threads = []
  for _ in range(num_threads):
    thread = threading.Thread(target=get_item_list_thread,args=(item_list,))
    thread.start()
    threads.append(thread)
  # 모든 작업이 완료될 때까지 대기합니다.
  url_queue.join()
  # None을 큐에 추가하여 스레드를 종료합니다.
  for _ in range(num_threads):
    url_queue.put(None)
  # 모든 스레드가 작업을 마칠 때까지 대기합니다.
  for thread in threads:
    thread.join()
  return item_list
url_queue = Queue()  # 크롤링할 URL을 저장할 큐를 생성합니다.
num_threads = 1  # 동시에 실행할 스레드 개수를 지정합니다.

  
start_time = time.perf_counter()    
# data = start_clawling(
#   'https://vintagefarm.co.kr/product/list.html',
#   'https://vintagefarm.co.kr/product/search.html?banner_action=&keyword=adidas&page=2',
#   'vintagefarm',
#   120
# )
data = start_clawling_thread(
  'https://vintagefarm.co.kr/product/list.html',
  'https://vintagefarm.co.kr/product/search.html?banner_action=&keyword=adidas&page=2',
  'vintagefarm',
  120
)
end_time = time.perf_counter()
print("Execution time: {:.5f} seconds".format(end_time - start_time))
# 데이터 확인용 json 파일 만들기
with open('brand_data.json', 'w', encoding='utf-8') as f:
  json.dump(data, f, ensure_ascii=False, indent=4)

