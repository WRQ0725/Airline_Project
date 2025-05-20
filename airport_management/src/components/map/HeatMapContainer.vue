<template>
	<div>
		<el-row v-loading="loading">
			<div id="heatmap-container"></div>
		</el-row>
		<div id="chart-container"></div>
	</div>
</template>

<script>
import { loadModules } from "esri-loader"
import echarts from "echarts"

import JsonToLayer from "../../utils/JsonToLayer"

const token = '7fe35faf9e6d4a2cee3eb08a3cb7fdb3'
const VEC_C = "http://{s}.tianditu.com/vec_c/wmts?layer=vec&style=default&tilematrixset=c&Service=WMTS&Request=GetTile&Version=1.0.0&Format=tiles&TileMatrix={z}&TileCol={x}&TileRow={y}&tk="
export default {
	name: "HeatMapContainer",
	data() {
		return {
			map: {},
			myChart: {},
			features: [],
			radasList: [],
			maxNum: 0,
			loading: false,
			heatmapLayer: null,
		}
	},
	methods: {
		// 初始化Leaflet地图
		loadMap() {
			if(!this.map) {
				return false;
			}
			// 加载天地图服务图层
			// 创建地图实例
			this.map = L.map('heatmap-container', {
				minZoom: 2,
				maxZoom: 17,
				center: [34.33213, 109.00945],
				zoomSnap: 0.1,
				zoom: 2,
				zoomControl: false,
				attributionControl: false,
				crs: L.CRS.EPSG4326,
			});

			// 添加tianditu底图

			L.tileLayer(VEC_C + token, {
				zoomOffset: 1,
				subdomains: ["t0", "t1", "t2", "t3", "t4", "t5", "t6", "t7"],
				opacity: 0.8,
			}).addTo(this.map);

		},
		// 数据改变更新热力图
		updateHeatMap() {
			if (this.features.length === 0) {
				return false;
			}

			this.loading = true;

			// 如果已经存在热力图层，则移除
			if (this.heatmapLayer) {
				this.map.removeLayer(this.heatmapLayer);
			}

			// 准备热力图数据
			const heatmapData = this.features.map(feature => [
				feature.geometry.y,
				feature.geometry.x,
				feature.value || 0.2 // 如果没有 value，则默认为 1
			]);

			// 创建热力图层
			this.heatmapLayer = L.heatLayer(heatmapData, {
				radius: 12, // 热力图的模糊半径
				blur: 15, // 热力图的模糊程度
				maxZoom: 1, // 热力图在最大缩放级别时的显示效果
				gradient: {
					0.4: 'rgba(0, 255, 150, 0)',
					0.6: 'rgb(250, 250, 0)',
					0.8: 'rgb(250, 150, 0)',
					1.0: 'rgb(255, 50, 0)'
				}
			});

			// 将热力图层添加到地图上
			this.heatmapLayer.addTo(this.map);

			this.loading = false;
			this.$emit('heatmapLoaded');
		},
		// 生成雷达图
		drawChart() {
			const option = {
				title: {
					text: "高通勤频率机场",
					left:'4%',
					textStyle: {
						fontSize: 15, // 设置标题字体大小
						fontWeight:5,
					}
				},
				legend: {
					data: ["通勤频率"],
					top: "6%",
					right: "5%",
				},
				tooltip: {
					trigger: "item",
				},
				radar: {
					// shape: 'circle',
					radius: "50%",
					indicator: this.radasList.map((item) => {
						return {
							name: item.name,
							max: this.maxNum,
						}
					}),
				},
				series: [
					{
						name: "预算 vs 开销（Budget vs spending）",
						type: "radar",
						data: [
							{
								value: this.radasList.map((item) => item.num),
								name: "通勤频率",
							},
						],
					},
				],
			}
			this.myChart.setOption(option)
		},
		// 统计数据
		_statistic(arr) {
			// 统计对象 {"机场名": 个数}
			let radasObj = {}
			// 统计数组 ["机场名", ...]
			let radasArr = []
			// 最大值 初始为0
			let maxNum = 0
			// 对象化
			arr.forEach((item) => {
				let { name } = item
				if (radasObj[name]) {
					radasObj[name]++
					if (radasObj[name] > maxNum) maxNum = radasObj[name]
				} else {
					radasObj[name] = 1
					if (radasObj[name] > maxNum) maxNum = radasObj[name]
				}
			})
			// 数组去重
			for (let item of arr) {
				radasArr.push(item.name)
			}
			const radasSet = new Set(radasArr)
			radasArr = Array.from(radasSet)
			// 数组添加num属性
			radasArr = radasArr.map((item) => {
				return {
					name: item,
					num: radasObj[item],
				}
			})
			// 数组按num排序+取前6个
			radasArr = radasArr
				.sort((obj1, obj2) => {
					let { num: num1 } = obj1
					let { num: num2 } = obj2
					if (num1 < num2) return 1
					else if (num1 > num2) return -1
					else return 0
				})
				.slice(0, 6)
			this.radasList = radasArr
			this.maxNum = maxNum
		},
	},
	mounted() {
		const myChart = echarts.init(document.getElementById("chart-container"))
		this.myChart = myChart
		this.loadMap()
		if (this.cfeatures.length !== 0) {
			this.features = JsonToLayer.jsonToFeatureSet(this.cfeatures)
			console.log(this.features)
			this.updateHeatMap()
		}
		this._statistic(this.cfeatures)
		this.drawChart()
	},
	watch: {
		cfeatures(val) {
			this.features = JsonToLayer.jsonToFeatureSet(val)
			this.updateHeatMap()
			this._statistic(this.cfeatures)
			this.drawChart()
		},
	},
	props: {
		cfeatures: {
			type: Array,
			default: [],
			required: true,
		},
	},
}
</script>

<style lang="less" scoped>
.el-row {
	height: 100%;
	width: 100%;
}
#heatmap-container {
	height: 100%;
	width: 100%;
}
#chart-container {
	margin-top: 100px;
	height: 300px;
	width: 100%;
}
</style>