const { Airports } = require("../utils/db");

// 从数据库获取热门机场
exports.findHot = num => {
	// 确保 num 是一个有效的数字
	const parsedNum = parseInt(num);
	if (isNaN(parsedNum) || parsedNum <= 0) {
		throw new Error("Invalid input: num must be a positive integer");
	}

	// 查询 hot 字段最大的 num 条数据
	return Airports.find({})
		.sort({ hot: -1 }) // 按 hot 字段升序排序
		.limit(parsedNum); // 限制返回的条数
  };
// 从数据库获取所有机场列表
exports.findAll = () => {
	return Airports.find();
};

// 从数据库获取机场列表(关键词正则，页码，每页数据量)
exports.findList = (queryInfoReg, queryPage, querySize) => {
	return Airports.find({ name: { $regex: queryInfoReg } }) // 查询包含关键字
		.sort({ first: 1 }) // 按拼音排序
		.skip((parseInt(queryPage) - 1) * parseInt(querySize)) // 跳过前n-1页
		.limit(parseInt(querySize)); // 获取m个
};

// 查询数据的数据量
exports.findCount = queryInfoReg => {
	return Airports.count({ name: { $regex: queryInfoReg } });
};

// 从数据库，根据name获取坐标值
exports.findByName = name => {
	return Airports.findOne({ name });
};
