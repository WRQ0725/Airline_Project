import pandas as pd
import requests
from pymongo import MongoClient
import tqdm

# 高德地图API密钥
GAODE_API_KEY = "896b84e88f8357a812487834d46c163f"  # 替换为你的高德地图API密钥

# MongoDB连接信息
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "airport-management"
COLLECTION_NAME = "airports"

def get_airport_coordinates(airport_name):
    """通过高德地图POI查询API获取机场的经纬度"""
    url = "https://restapi.amap.com/v3/place/text"  # POI查询API
    params = {
        "keywords": airport_name,  # 查询关键词
        "key": GAODE_API_KEY,
        "extensions": "all",  # 获取详细信息
        "types": "机场"  # 指定查询类型为机场
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["status"] == "1" and data["info"] == "OK" and data["pois"]:
            print("查询成功！")
            location = data["pois"][0]["location"]
            lon, lat = location.split(",")
            return lon, lat
    return None, None

def main():
    # 读取Excel文件
    excel_file = "携程航班数据-北京.xlsx"  # 替换为你的Excel文件路径
    df = pd.read_excel(excel_file)

    # 提取所有非重复的机场名称
    all_airports = set(df["departPortName"].tolist() + df["arrivePortName"].tolist())

    print("提取完成！")
    # 存储机场信息的列表
    airport_data = []

    # 查询机场经纬度并整理数据
    for airport in tqdm.tqdm(all_airports):
        lon, lat = get_airport_coordinates(airport)
        if lon and lat:
            airport_data.append({
                "name": airport,
                "coord": {
                    "x": lon,
                    "y": lat
                }
            })

    # 连接MongoDB
    print("连接MongoDB数据库...")
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    # 将数据存入数据库
    collection.insert_many(airport_data)

    print("机场数据已成功存入MongoDB数据库！")

if __name__ == "__main__":
    main()