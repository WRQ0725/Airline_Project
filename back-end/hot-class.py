from pymongo import MongoClient

# 连接到 MongoDB 数据库
def connect_to_db(uri, db_name):
    client = MongoClient(uri)
    db = client[db_name]
    return db

# 统计 startAirport 和 endAirport 字段值的出现次数
def count_airport_occurrences(airlines_collection):
    pipeline = [
        {"$project": {
            "airports": {
                "$concatArrays": [
                    ["$startAirport"],  # 将 startAirport 转换为数组
                    ["$endAirport"]    # 将 endAirport 转换为数组
                ]
            }
        }},
        {"$unwind": "$airports"},
        {"$group": {"_id": "$airports", "count": {"$sum": 1}}}
    ]
    result = list(airlines_collection.aggregate(pipeline))
    return {item["_id"]: item["count"] for item in result}

# 根据出现次数对机场进行排序并分配序号
def rank_airports_by_occurrences(airport_counts, all_airports):
    # 初始化所有机场的 hot 值为 0
    hot_levels = {airport: 0 for airport in all_airports}
    
    # 对机场按出现次数升序排序
    sorted_airports = sorted(airport_counts.items(), key=lambda x: x[1], reverse=False)
    
    # 为每个机场分配序号
    for index, (airport, count) in enumerate(sorted_airports, start=1):
        hot_levels[airport] = index  # 序号从1开始
    return hot_levels

# 更新 airports 集合，添加 hot 字段
def update_airports_collection(airports_collection, hot_levels):
    for airport_name, hot_level in hot_levels.items():
        airports_collection.update_one(
            {"name": airport_name},
            {"$set": {"hot": hot_level}},
            upsert=True  # 如果机场不存在，则插入新文档
        )

# 主函数
def main():
    # 数据库连接信息
    uri = "mongodb://localhost:27017"  # 替换为你的 MongoDB URI
    db_name = "airport-management"

    # 连接到数据库
    db = connect_to_db(uri, db_name)

    # 获取 airlines 和 airports 集合
    airlines_collection = db["airlines"]
    airports_collection = db["airports"]

    # 获取所有机场的名称
    all_airports = [airport["name"] for airport in airports_collection.find({}, {"name": 1, "_id": 0})]

    # 统计机场出现次数
    airport_counts = count_airport_occurrences(airlines_collection)

    # 根据出现次数对机场进行排序并分配序号
    hot_levels = rank_airports_by_occurrences(airport_counts, all_airports)

    # 更新 airports 集合
    update_airports_collection(airports_collection, hot_levels)

    print("机场分级完成！")

if __name__ == "__main__":
    main()