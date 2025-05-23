import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import ElementUI from 'element-ui';
// 引用样式
import "./assets/less/style.less";
import "./assets/less/loading.less";
import "./assets/icon/iconfont.css";
import './assets/fonts/iconfont.css'
// 引用element-ui
import "./plugins/element.js";
import voiceInputButton from 'voice-input-button2'
// 引用axios
import axios from "axios";
// 配置基础url
// axios.defaults.baseURL = "http://localhost:3000/api/airmana";

// 配置发送前拦截并添加token
axios.interceptors.request.use(config => {
	config.headers.Authorization = window.sessionStorage.getItem("token");
	return config;
});
// 将axios工具添加至axios原型链中
Vue.prototype.$http = axios;

Vue.config.productionTip = false;

new Vue({
	router,
	render: h => h(App)
}).$mount("#app");

Vue.use(voiceInputButton, {
	appId: 'd22bb119', // 您申请的语音听写服务应用的ID
	apiKey: '03dc4164811c96df36e089c23e197b48', // 您开通的语音听写服务的 apiKey
	apiSecret: 'NjE2ZGE1ZmZhNGYxZWJlYTM5YTExOTg1', // 您开通的语音听写服务的 apiSecret
	color: "#ffffff", // 按钮图标的颜色
	tipPosition: 'top', // 提示条位置
	vad_eos: 1500
	// 其他配置项, 参见下方 [Attributes / 属性] 部分
});

Vue.use(ElementUI)