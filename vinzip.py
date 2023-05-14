import requests
url = 'https://m.vinzip.kr/brandlist/list.html?cate_no=228'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

response = requests.get(url, headers=headers)
html = response.text
print(html)