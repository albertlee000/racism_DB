import pymongo
from bson.objectid import ObjectId
from bson.regex import Regex
import re
import pprint

# 启动客户端，连接本地MongoDB
client = pymongo.MongoClient(host='127.0.0.1',
                             port=27017,
                             username='root',
                             password='123456')

# 找到名为test的数据库，该数据库中包含5个来自YELP官网的数据json包
db = client.racismDB

# 打开test数据库中的 yelp_academic_dataset_business 表格，该表格存有所有YLEP注册店铺的营业数据, 打开yelp_academic_dataset_review表格其中含有所有review的文字信息
ybusiness = db['yelp_business']
yreview = db['yelp_review']
ycheckin = db['yelp_checkin']
ytip = db['yelp_tip']
yuser = db['yelp_user']
yphoto = db['yelp_photo']

# ethnic餐馆正则列表
ethnic = '.*Thai.*|.*Chinese.*|.*Vietnamese.*|.*Mexican.*|.*Indian.*|.*Pakistani.*|.*Mediterranean.*|.*Caribbean.*|' \
         '.*Filipino.*|.*Latin American.*|.*Japanese.*|.*Colombian.*|.*Cuban.*|.*Korean.*|.*Halal.*|.*African.*|' \
         '.*Senegalese.*|.*Middle Eastern.*|.*Moroccan.*|.*Cambodian.*|.*Asian Fusion.*|.*Brazilian.*|.*Puerto Rican.*|' \
         '.*Argentine.*|.*Israeli.*|.*Turkish.*|.*Pan Asian.*|.*Taiwanese.*|.*Sri Lankan.*|.*Mongolian.*|.*Cantonese.*|' \
         '.*Indonesian.*|.*Singaporean.*|.*Persian.*|.*Iranian.*|.*Shanghainese.*|.*Bangladeshi.*|.*Arabic.*|.*Russian.*|' \
         '.*Laotian.*|.*Afghan.*|.*Nepalese.*|.*Himalayan.*|.*Lebanese.*|.*Szechuan.*|.*Ukrainian.*'
#restaurant正则
restaurant_reg = re.compile('.*Restaurants.*')
#ethnic restaurant正则
ethnic_restaurant_reg = re.compile("(.*((?=%s)(?=(.*restaurants.*))).*)"%ethnic, re.I)

# china_reg = re.compile('.*Chinese.*Restaurants.*|.*Restaurants.*Chinese.*|.*food.*Chinese.*|.*chinese.*food.*')
# # 日本餐馆
# japan_reg = re.compile('.*japan.*Restaurants.*|.*Restaurants.*japan.*|.*food.*japan.*|.*japan.*food.*')
# # 韩国餐馆
# korea_reg = re.compile('.*korea.*Restaurants.*|.*Restaurants.*korea.*'
#                        '|.*food.*korea.*|.*korea.*food.*')
# # 亚洲餐馆
# asia_reg = re.compile('.*asia.*Restaurants.*|.*Restaurants.*asia.*'
#                        '|.*food.*asia.*|.*asia.*food.*')
# # 泰国餐馆
# thai_reg = re.compile('.*thai.*Restaurants.*|.*Restaurants.*thai.*'
#                        '|.*food.*thai.*|.*thai.*food.*')
# # 找出有ethnic tag的餐馆
# ethnic_reg = re.compile('.*ethnic.*Restaurants.*|.*Restaurants.*ethnic.*|'
#                         '.*food.*ethnic.*|.*ethnic.*food.')
restaurant_regex = Regex.from_native(restaurant_reg)
ethnic_regex = Regex.from_native(ethnic_restaurant_reg)

# 获取一家id为'64212ff0a59bcf01998d0140'的餐馆的信息
# store = ybusiness.find_one({"_id": ObjectId('642a9b0ae989b830b4296ca7')})
# print("a certain store: ", store)

# 获取一家中餐馆的信息
# ChinaStore = ybusiness.find_one({"categories": regex})
# print("a chinese store: ", ChinaStore)
# chinese_example_id = ChinaStore['business_id']
# 获取上文选中的中餐馆的评论信息
# chinese_example_review = yreview.find_one({"business_id": chinese_example_id})
# print('\n' + "stars:", str(chinese_example_review['stars']), '\n' +
#       "review text is:", chinese_example_review['text'], '\n' +
#       "review date is:",  chinese_example_review['date'] + '\n')

# 计数所有中餐馆的数量
Num_restaurant = ybusiness.count_documents({"categories": restaurant_regex})
Num_ethnic = ybusiness.count_documents({"categories": ethnic_regex})

print('Total number of Restaurants:', Num_restaurant)
print('Total number of Ethnic restaurants:', Num_ethnic)
print('Total number of Western food restaurants:', Num_restaurant-Num_ethnic)
# 获取所有注册在YELP的店铺在不同州的分布
# states = list(ybusiness.aggregate([
#     {"$unwind": "$state"},
#     {"$group": {"_id": "$state", "count": {"$sum": 1}}}
# ]))
# pprint.pprint(states)

#
