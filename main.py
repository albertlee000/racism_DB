import pymongo
from bson.objectid import ObjectId
from bson.regex import Regex
import re
import pprint

# 启动客户端，连接本地MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017")

# 找到名为test的数据库，该数据库中包含5个来自YELP官网的数据json包
db = client.test

# 打开test数据库中的 yelp_academic_dataset_business 表格，该表格存有所有YLEP注册店铺的营业数据
business = db['yelp_academic_dataset_business']

# 建立用于搜索中餐馆信息的模糊查询正则表达式
pattern = re.compile('.*Chinese.*Restaurants.*|.*Restaurants.*Chinese.*')
regex = Regex.from_native(pattern)
regex.flags = re.UNICODE

# 获取一家id为'64212ff0a59bcf01998d0140'的餐馆的信息
store = business.find_one({"_id": ObjectId('64212ff0a59bcf01998d0140')})
print(store)
print(type(store))

# 获取一家中餐馆的信息
ChinaStore = business.find_one({"categories": regex})
print(ChinaStore)

# 计数所有中餐馆的数量
print(business.count_documents({"categories": regex}))


states = list(business.aggregate([
    {"$unwind": "$state"},
    {"$group": {"_id": "$state", "count": {"$sum": 1}}}
]))
pprint.pprint(states)
