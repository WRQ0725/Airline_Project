from pymongo import MongoClient
import json

# 连接到 MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['airport-management']
collection = db['airports']

# 读取集合中的所有数据
documents = collection.find()

# 初始化 GeoJSON 数据结构
geojson = {
    "type": "FeatureCollection",
    "features": []
}

# 遍历集合中的每个文档，转换为 GeoJSON 点数据
for doc in documents:
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [float(doc['coord']['x']), float(doc['coord']['y'])]  # GeoJSON 使用 [经度, 纬度]
        },
        "properties": {
            "name": doc['name'],
            "id": str(doc['_id'])  # 将 ObjectId 转换为字符串
        }
    }
    geojson['features'].append(feature)

# 将 GeoJSON 数据写入文件
with open('0.geojson', 'w', encoding='utf-8') as f:
    json.dump(geojson, f, ensure_ascii=False, indent=4)

print("GeoJSON 数据已成功导出到 output.geojson 文件。")