import requests
from bs4 import BeautifulSoup
import json
import math
import time

def get_html_from_url(url):
  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
  response = requests.get(url, headers=headers)
  html = response.text
  return html

def get_brand_data():
  html = get_html_from_url('https://m.vinzip.kr/brandlist/list.html')
  soup = BeautifulSoup(html, 'html.parser')

  elements = soup.select('.df-dataRows.xans-record- .box')

  brand_list = []
  for element in elements:
    html = str(element)
    soup = BeautifulSoup(html, 'html.parser')

    brandimg_src = soup.select_one('.brandimg img')['src']
    img_src = brandimg_src

    df_boarddata_text = soup.select_one('.df-boarddata').text.strip()

    df_boarddata_text = df_boarddata_text.replace('brandName1', 'brand_name_ko')
    df_boarddata_text = df_boarddata_text.replace('brandName2', 'brand_name_en')
    df_boarddata_text = df_boarddata_text.replace('brandUrl', 'brand_url')
    df_boarddata_text = df_boarddata_text.replace('brand_urlTarget', 'brand_img_url')

    origin_data =  json.loads(df_boarddata_text)
    origin_data['brand_img_url'] = img_src
    brand_list.append(origin_data)

  brand_data = []
  
  for i in range(len(brand_list)):
    brand_name = brand_list[i]['brand_name_ko'];
    html = get_html_from_url(f'https://m.vinzip.kr/product/search.html?banner_action=&keyword={brand_name}')
    soup = BeautifulSoup(html, 'html.parser')

    total_items = int(soup.select_one('#titleArea h2 .count').text)
    items_per_page = 24
    max_page = math.ceil(total_items / items_per_page)

    item_data = []
    for page in range(1, max_page+1):
      html = get_html_from_url(f'https://m.vinzip.kr/product/search.html?banner_action=&keyword={brand_name}&page={page}')
      soup = BeautifulSoup(html, 'html.parser')
      item_htmls = soup.select('.df-prl-item.xans-record-')

      for item_html in item_htmls:
        html = str(item_html)
        soup = BeautifulSoup(html, 'html.parser')
        price = soup.select_one('.df-prl-data-price').text.strip()
        name = soup.select_one('.df-prl-name').text.strip()
        size = soup.select_one('.custom_option1 > span').text.strip()
        img = soup.select_one('.df-prl-thumb-link img')['src']
        status = soup.select_one('.df-prl-icon img')
        if status:
            status = status['alt']

        item_data.append({"price": price, "name": name, "size": size, "img": size, "status": status})
    brand_data.append({
      "brand_name" : brand_name,
      "brand_data" : item_data
    })


  return brand_data



start_time = time.perf_counter()
brand_data = get_brand_data()
# 데이터 확인용 json 파일 만들기
end_time = time.perf_counter()

with open('brand_data.json', 'w', encoding='utf-8') as f:
  json.dump(brand_data, f, ensure_ascii=False, indent=4)
print("Execution time: {:.5f} seconds".format(end_time - start_time))
