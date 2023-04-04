import pymongo
from bson.objectid import ObjectId
from bson.regex import Regex
import re
import pprint

# 启动客户端，连接本地MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017")

# 找到名为test的数据库，该数据库中包含5个来自YELP官网的数据json包
db = client.test

# 打开test数据库中的 yelp_academic_dataset_business 表格，该表格存有所有YLEP注册店铺的营业数据, 打开yelp_academic_dataset_review表格其中含有所有review的文字信息
business = db['yelp_academic_dataset_business']
review = db['yelp_academic_dataset_review']

# 建立用于搜索中餐馆信息的模糊查询正则表达式
china_reg = re.compile('.*Chinese.*Restaurants.*|.*Restaurants.*Chinese.*'
                       '|.*food.*Chinese.*|.*chinese.*food.*', re.I)
# 日本餐馆
japan_reg = re.compile('.*japan.*Restaurants.*|.*Restaurants.*japan.*'
                       '|.*food.*japan.*|.*japan.*food.*', re.I)
# 韩国餐馆
korea_reg = re.compile('.*korea.*Restaurants.*|.*Restaurants.*korea.*'
                       '|.*food.*korea.*|.*korea.*food.*', re.I)
# 亚洲餐馆
asia_reg = re.compile('.*asia.*Restaurants.*|.*Restaurants.*asia.*'
                       '|.*food.*asia.*|.*asia.*food.*', re.I)
# 泰国餐馆
thai_reg = re.compile('.*thai.*Restaurants.*|.*Restaurants.*thai.*'
                       '|.*food.*thai.*|.*thai.*food.*', re.I)
regex = Regex.from_native(china_reg)
regex.flags = re.UNICODE

# 获取一家id为'64212ff0a59bcf01998d0140'的餐馆的信息
store = business.find_one({"_id": ObjectId('64212ff0a59bcf01998d0140')})
print(store)

# 获取一家中餐馆的信息
ChinaStore = business.find_one({"categories": regex})
print(ChinaStore)
chinese_example_id = ChinaStore['business_id']
# 获取上文选中的中餐馆的评论信息
chinese_example_review = review.find_one({"business_id": chinese_example_id})
print('\n' + "stars:", str(chinese_example_review['stars']), '\n' +
      "review text is:", chinese_example_review['text'], '\n' +
      "review date is:",  chinese_example_review['date'] + '\n')

# 计数所有中餐馆的数量
print(business.count_documents({"categories": regex}))

# 获取所有注册在YELP的店铺在不同州的分布
states = list(business.aggregate([
    {"$unwind": "$state"},
    {"$group": {"_id": "$state", "count": {"$sum": 1}}}
]))
pprint.pprint(states)

#
