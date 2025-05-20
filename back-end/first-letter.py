from pymongo import MongoClient
from pypinyin import lazy_pinyin

# 连接到 MongoDB 数据库
def connect_to_db(uri, db_name):
    client = MongoClient(uri)
    db = client[db_name]
    return db

# 获取字符串的第一个字的拼音首字母
def get_first_letter(text):
    if not text:
        return ""
    # 提取第一个字的拼音首字母
    first_letter = lazy_pinyin(text[0])[0][0].upper()
    return first_letter

# 更新 airports 集合，添加 first 字段
def update_airports_collection(airports_collection):
    # 查询所有机场文档
    airports = list(airports_collection.find({}))
    
    # 遍历每个文档，添加 first 字段
    for airport in airports:
        name = airport.get("name", "")
        first_letter = get_first_letter(name)
        airports_collection.update_one(
            {"_id": airport["_id"]},
            {"$set": {"first": first_letter}}
        )
        print(f"Updated {name} with first letter {first_letter}")

# 主函数
def main():
    # 数据库连接信息
    uri = "mongodb://localhost:27017"  # 替换为你的 MongoDB URI
    db_name = "airport-management"    # 替换为你的数据库名称

    # 连接到数据库
    db = connect_to_db(uri, db_name)

    # 获取 airports 集合
    airports_collection = db["airports"]

    # 更新 airports 集合
    update_airports_collection(airports_collection)

    print("所有机场文档已更新！")

if __name__ == "__main__":
    main()