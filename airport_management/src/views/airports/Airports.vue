<template>
	<div>
		<el-card>
			<!-- 标签列 -->
			<el-tabs tab-position="left">
				<el-tab-pane class="tab_item" label="热门机场">
					<airports-list
						:cAirportsList="hotAirportList"
						@queryNumChanged="queryNumChanged"
					></airports-list>
				</el-tab-pane>
				<el-tab-pane label="按名称查询">
					<name-query-container></name-query-container>
				</el-tab-pane>
				<el-tab-pane label="查找附近">
					<location-container></location-container>
				</el-tab-pane>
			</el-tabs>
		</el-card>
	</div>
</template>

<script>
// 引用组件
import AirportsList from "../../components/airports/AirportsList"
import MapContainer from "../../components/airports/MapContainer"
import NameQueryContainer from "../../components/airports/NameQueryContainer"
import LocationContainer from "../../components/airports/LocationContainer"

export default {
	name: "Airports",
	data() {
		return {
			hotAirportList: [],
			num: 10,
		}
	},
	methods: {
		// 获取热门机场列表
		async _getHotAirportsList() {
			const { data: result } = await this.$http.get("/api/airports/hot", {
				params: {
					num: this.num,
				},
			})
			if (result.meta.status == 1) {
				this.hotAirportList = result.data
				console.log('成功获取热门机场列表')
				console.log(this.hotAirportList)
			} else {
				this.$message({ type: "error", message: result.meta.msg })
			}
		},
		// 请求个数发生改变
		queryNumChanged(num) {
			this.num = num
			this._getHotAirportsList()
		},
	},
	created() {
		this._getHotAirportsList()
	},
	components: {
		AirportsList,
		MapContainer,
		NameQueryContainer,
		LocationContainer,
	},
}
</script>

<style lang="less" scoped>
</style>