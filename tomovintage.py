import math
import requests
from bs4 import BeautifulSoup

# 브랜드 리스트 가져오기
# https://tomovintage.com/product/list.html?
#   cate_no=61

# total
# .prdCount 

# html crawing
def get_html_from_url(url):
  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
  response = requests.get(url, headers=headers)
  html = response.text
  return html

# 상품 수량에 따른 페이지 계산
def count_pages(total_items):
    items_per_page = 200
    max_page = math.ceil(total_items / items_per_page)
    return max_page

url = 'https://tomovintage.com/product/list.html?cate_no=61&page=1'
html = get_html_from_url(url)
soup = BeautifulSoup(html, 'html.parser')
total_items = int(soup.select_one('.prdCount strong').text)
max_page = count_pages(total_items)

brand_list = []
for page in range(1, max_page+1):
  url = f'https://tomovintage.com/product/list.html?cate_no=61&page={page}'
  html = get_html_from_url(url)
  soup = BeautifulSoup(html, 'html.parser')
  for element in soup.select('.item.-box.xans-record- .name span'):
    brand_list.append(element.text)
print(len(brand_list))
brand_list = list(set(brand_list))
print(len(brand_list))
print(brand_list)

# 검색
# https://tomovintage.com/product/search.html?
#   view_type=&
#   supplier_code=&
#   category_no=61&
#   search_type=product_name&
#   keyword=RALPH+LAUREN&
#   exceptkeyword=&
#   product_price1=&
#   product_price2=&
#   order_by=
