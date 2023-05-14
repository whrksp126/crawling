import requests
url = 'https://www.kbchachacha.com/public/search/list.empty?page=1&sort=sellAmt&makerCode=101&classCode=1109&carCode=3079&_pageSize=4&pageSize=5'
response = requests.get(url)
html = response.text
# print(html)
## KB차차차
# https://www.kbchachacha.com/

### html 분석해서 내부 데이터 빼와야함
# https://www.kbchachacha.com/public/search/list.empty?
#   page=1&
#   sort=sellAmt&
#   makerCode=101&
#   classCode=1109&
#   carCode=3079&
#   _pageSize=4&
#   pageSize=5

# https://www.kbchachacha.com/public/search/list.empty?
#   page=1&
#   sort=sellAmt&
#   makerCode=101&
#   classCode=1109&
#   carCode=3317&
#   _pageSize=4&
#   pageSize=5

# https://www.kbchachacha.com/public/search/list.empty?
#   page=1&
#   sort=sellAmt&
#   makerCode=107&
#   classCode=1904&
#   carCode=2865&
#   _pageSize=4&
#   pageSize=5




# https://www.kbchachacha.com/public/car/detail.kbc?carSeq=24310181
