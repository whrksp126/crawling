import requests
url = 'http://api.encar.com/search/car/list/premium?count=true&q=(And.Hidden.N._.(C.CarType.N._.(C.Manufacturer.벤츠._.(C.ModelGroup.A-클래스._.Model.A-클래스+W177.))))&sr=|PriceAsc|100|50'
response = requests.get(url)
html = response.text
# print(html)
### 엔카
# http://www.encar.com/index.do

### 낮은 가격순 가져오기 
### (C.Manufacturer.벤츠._.(C.ModelGroup.A-클래스._.Model.A-클래스+W177.) 제조사, 모델 그룹, 모델 명
### |PriceAsc|100|50 낮은 가격순|100번째 부터|50개 가져오기
# http://api.encar.com/search/car/list/premium?count=true&q=(And.Hidden.N._.(C.CarType.N._.(C.Manufacturer.벤츠._.(C.ModelGroup.A-클래스._.Model.A-클래스+W177.))))&sr=|PriceAsc|100|50
# http://api.encar.com/search/car/list/premium?
#   count=true&
#   q=(And.Hidden.N._.(C.CarType.N._.(C.Manufacturer.벤츠._.(C.ModelGroup.A-클래스._.Model.A-클래스+W177.))))&
#   sr=|PriceAsc|100|50

# {
#   "Id":"34777615",
#   "Separation":["B"],
#   "Trust":["HomeService"],
#   "Condition":["Inspection","Record"],
#   "Photo":"/carpicture07/pic3477/34772434_",
#   "Photos":[
#     {
#       "type":"001",
#       "location":"/carpicture07/pic3477/34772434_001.jpg",
#       "updatedDate":"2023-04-06T05:48:01Z",
#       "ordering":1.0
#     },{
#     "type":"003",
#     "location":"/carpicture07/pic3477/34772434_003.jpg",
#     "updatedDate":"2023-04-06T05:48:01Z",
#     "ordering":3.0
#     },{
#     "type":"004",
#     "location":"/carpicture07/pic3477/34772434_004.jpg",
#     "updatedDate":"2023-04-06T05:48:01Z",
#     "ordering":4.0
#     },{
#     "type":"007",
#     "location":"/carpicture07/pic3477/34772434_007.jpg",
#     "updatedDate":"2023-04-06T05:48:01Z",
#     "ordering":7.0
#     }
#   ],
#   "Manufacturer":"벤츠",
#   "Model":"A-클래스 W177",
#   "Badge":"A200d 세단",
#   "Transmission":"오토",
#   "FuelType":"디젤",
#   "Year":202108.0,
#   "FormYear":"2021",
#   "Mileage":12292.0,
#   "ServiceCopyCar":"DUPLICATION",
#   "Price":3199.0,
#   "OfficeCityState":"경기",
#   "ModifiedDate":"2023-05-08 21:46:07.000 +09"
# }


### 중고차량 개별 상세 페이지 링크 carid 만 변경 함
# http://www.encar.com/dc/dc_cardetailview.do?pageid=fc_carsearch&listAdvType=&carid=34647705&view_type=&adv_attribute=&wtClick_forList=&advClickPosition=&tempht_arg=
# http://www.encar.com/dc/dc_cardetailview.do?
#   pageid=fc_carsearch&
#   listAdvType=&
#   carid=34647705&
#   view_type=&
#   adv_attribute=&
#   wtClick_forList=&
#   advClickPosition=&
#   tempht_arg=

