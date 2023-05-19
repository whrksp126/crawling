import requests
from bs4 import BeautifulSoup
import json
import math
import time
import asyncio
import aiohttp
import threading
from queue import Queue
# html crawing
def get_html_from_url(url):
  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
  response = requests.get(url, headers=headers)
  html = response.text
  return html

# 모든 브랜드 리스트 가져오기
def get_brand_data():
    url = 'https://m.vinzip.kr/brandlist/list.html'
    html = get_html_from_url(url)
    soup = BeautifulSoup(html, 'html.parser')

    brand_list = []
    for element in soup.select('.df-dataRows.xans-record- .box'):
        brandimg_src = element.select_one('.brandimg img')['src']
        img_src = brandimg_src

        df_boarddata_text = element.select_one('.df-boarddata').text.strip()
        df_boarddata_text = df_boarddata_text.replace('brandName1', 'brand_name_ko') \
                                           .replace('brandName2', 'brand_name_en') \
                                           .replace('brandUrl', 'brand_url') \
                                           .replace('brand_urlTarget', 'brand_img_url')

        origin_data = json.loads(df_boarddata_text)
        origin_data['brand_img_url'] = img_src
        brand_list.append(origin_data)
    return brand_list

# 상품 수량에 따른 페이지 계산
def count_pages(total_items):
    items_per_page = 24
    max_page = math.ceil(total_items / items_per_page)
    return max_page

# 브랜드에 등록된 상품 수량 확인
def get_brand_products_quantity(brand_list):
    
    # for brand in brand_list:
    for i in range(50):
        brand_name = brand_list[i]['brand_name_ko']
        url = f'https://m.vinzip.kr/product/search.html?banner_action=&keyword={brand_name}'
        html = get_html_from_url(url)
        soup = BeautifulSoup(html, 'html.parser')
        total_items = int(soup.select_one('#titleArea h2 .count').text)
        
        
        max_page = count_pages(total_items)
        html = get_page_html(max_page, brand_name)
        item_data = get_products_data(html)
        
        
# 브랜드 페이지별 HTML 빼오기
def get_page_html(max_page, brand_name):
    for page in range(1, max_page+1):
        url = f'https://m.vinzip.kr/product/search.html?banner_action=&keyword={brand_name}&page={page}'
        html = get_html_from_url(url)
        return html
        
# 페이지에서 상품 정보 빼오기
def get_products_data(html):
        item_data = []
        soup = BeautifulSoup(html, 'html.parser')
        item_htmls = soup.select('.df-prl-item.xans-record-')

        for item_html in item_htmls:
            price = item_html.select_one('.df-prl-data-price').text.strip()
            name = item_html.select_one('.df-prl-name').text.strip()
            size = item_html.select_one('.custom_option1 > span').text.strip()
            img = item_html.select_one('.df-prl-thumb-link img')['src']
            status = item_html.select_one('.df-prl-icon img')
            if status:
                status = status['alt']

            item_data.append({"price": price, "name": name, "size": size, "img": img, "status": status})
        return item_data
    # brand_data.append({"brand_name": brand_name, "brand_data": item_data})
    # return brand_data




brand_data=[];
def crawler():
    while True:
        data = url_queue.get()
        if data is None:
            break
        
        html = get_html_from_url(data['url'])
        # print(data['brand_name'],data['url'])
        soup = BeautifulSoup(html, 'html.parser')
        total_items = int(soup.select_one('#titleArea h2 .count').text)
        if total_items != 0:
            max_page = count_pages(total_items)
            html = get_page_html(max_page, data['brand_name'])
            item_data = get_products_data(html)
            brand_data.append({"brand_name": data['brand_name'], "brand_data": item_data})

        url_queue.task_done()


start_time = time.perf_counter()        
url_queue = Queue()  # 크롤링할 URL을 저장할 큐를 생성합니다.
num_threads = 16  # 동시에 실행할 스레드 개수를 지정합니다.

brand_list = get_brand_data()


# URL 큐에 URL을 추가합니다.
# for i in range(5):
#     brand_name = brand_list[i]['brand_name_ko']

for brand in brand_list:
    brand_name = brand['brand_name_ko']
    url = f'https://m.vinzip.kr/product/search.html?banner_action=&keyword={brand_name}'
    url_queue.put({'url':url , 'brand_name': brand_name})


# 스레드를 생성하고 실행합니다.
threads = []
for _ in range(num_threads):
    thread = threading.Thread(target=crawler)
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
end_time = time.perf_counter()
print("Execution time: {:.5f} seconds".format(end_time - start_time))

# 데이터 확인용 json 파일 만들기
with open('brand_data.json', 'w', encoding='utf-8') as f:
  json.dump(brand_data, f, ensure_ascii=False, indent=4)