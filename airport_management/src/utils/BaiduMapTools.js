import axios from "axios";

export default {
	// 用户token
	_token: "DS4dGbczubyhkID8XEScXMuanchuBAhH",
	// 获取当前定位
	getLoacation() {
		return axios.get("baidu/location/ip", {
			params: {
				ak: this._token,
				coor: "bd09ll"
			}
		});
	},
	// 获取最近的两个机场
	async getNearestAirports(point) {
		const { data: result } = await axios.get("/api/airports/all");
		let list = [];
		if (result.meta.status == 1) {
			list = result.data.map(item => {
				return {
					name: item.name,
					originX: point.x,
					originY: point.y,
					x: item.coord.x,
					y: item.coord.y,
					distance: Math.pow(parseFloat(point.x) - parseFloat(item.coord.x), 2) + Math.pow(parseFloat(point.y) - parseFloat(item.coord.y), 2)
				};
			});
			list = list
				.sort((obj1, obj2) => {
					let { distance: distance1 } = obj1;
					let { distance: distance2 } = obj2;
					if (distance1 < distance2) return -1;
					else if (distance1 > distance2) return 1;
					else return 0;
				})
				.slice(0, 2);
			return list;
		} else {
			return null;
		}
	},
	// 获取路线信息
	async getRouteInfo(list) {
		let resList = [];
		for (let item of list) {
			let { name, x, y, originX, originY } = item;
			try {
				let response = await axios.get("/baidu/direction/v2/driving", {
					params: {
						ak: this._token,
						origin: `${originY},${originX}`,
						destination: `${y},${x}`
					}
				});

				// 检查接口返回的状态码
				if (response.status !== 200) {
					console.error(`请求失败，状态码：${response.status}`);
					continue; // 跳过当前项
				}

				let info = response.data;

				// 检查返回数据的结构
				if (!info || !info.result || !info.result.routes || info.result.routes.length === 0) {
					console.error(`数据结构不符合预期，返回数据：${JSON.stringify(info)}`);
					continue; // 跳过当前项
				}

				// 将结果添加到返回列表中
				resList.push({
					name,
					route: info.result.routes[0]
				});
			} catch (error) {
				console.error(`请求失败，错误信息：${error.message}`);
				// 可以选择跳过当前项或者记录错误信息
			}
		}
		console.log("路线信息", resList);
		return resList;
	},
	// 地点检索
	async locationSearch(name) {
		const { data: result } = await axios.get("/baidu/place/v2/search", {
			params: {
				query: name,
				region: "全国",
				ak: this._token,
				output: "json"
			}
		});
		if (result.results.length > 0) {
			const res = result.results[0];
			return {
				name: res.name,
				x: res.location.lng,
				y: res.location.lat
			};
		} else {
			return null;
		}
	},
	// 根据侧重要求选择路径
	chooseRoute(fromList, toList, preference) {
		let resList = [];
		switch (preference) {
			case 0: // 低廉
				if (fromList[0].route.distance < fromList[1].route.distance) {
					resList[0] = fromList[0].name;
				} else {
					resList[0] = fromList[1].name;
				}
				if (toList[0].route.distance < toList[1].route.distance) {
					resList[1] = toList[0].name;
				} else {
					resList[1] = toList[1].name;
				}
				break;
			case 1: // 均衡
				if (fromList[0].route.distance * 0.5 + fromList[0].route.duration * 0.5 < fromList[1].route.distance * 0.5 + fromList[1].route.duration * 0.5) {
					resList[0] = fromList[0].name;
				} else {
					resList[0] = fromList[1].name;
				}
				if (toList[0].route.distance * 0.5 + toList[0].route.duration * 0.5 < toList[1].route.distance * 0.5 + toList[1].route.duration * 0.5) {
					resList[1] = toList[0].name;
				} else {
					resList[1] = toList[1].name;
				}
				break;
			case 2: // 快速
				if (fromList[0].route.duration < fromList[1].route.duration) {
					resList[0] = fromList[0].name;
				} else {
					resList[0] = fromList[1].name;
				}
				if (toList[0].route.duration < toList[1].route.duration) {
					resList[1] = toList[0].name;
				} else {
					resList[1] = toList[1].name;
				}
				break;
		}
		return resList;
	}
};
