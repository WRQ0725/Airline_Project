<template>
	<div id="login_container">
		<label>
			<div class="card" :class="{ convered: !isSignin }">
				<div class="login_box" id="signin">
					<!-- 遮罩 -->
					<div class="login_blur"></div>
					<div class="Title">
						<span>"天 枢 智 策"</span>
						<br />
						<span>智 能 民 航 系 统
						</span>
					</div>
					<div class="login_content">
						<div class="login_title">
							<span>欢迎登录</span>
						</div>
						<LoginForm :c-is-login="isSignin"></LoginForm>
						<el-button icon="el-icon-right" size="mini" round plain class="switch_btn"
							@click="switchFunc">注册</el-button>
					</div>
				</div>
				<div class="login_box" id="signup">
					<!-- 遮罩 -->
					<div class="login_blur"></div>
					<div class="Title">
						<span>"天 枢 智 策"</span>
						<br />
						<span>智 能 民 航 系 统
						</span>
					</div>
					<div class="login_content">
						<div class="login_title">
							<span>注册用户</span>
						</div>
						<LoginForm :c-is-login="isSignin"></LoginForm>
						<el-button icon="el-icon-right" size="mini" round plain class="switch_btn"
							@click="switchFunc">登录</el-button>
					</div>
				</div>
			</div>
		</label>
	</div>
</template>

<script>
import LoginForm from "../components/login/LoginForm"

export default {
	name: "Login",
	data() {
		return {
			isSignin: true,
		}
	},
	methods: {
		switchFunc() {
			this.isSignin = !this.isSignin
			if (this.isSignin) document.title = "登录"
			else document.title = "注册"
		},
	},
	components: {
		LoginForm,
	},
}
</script>

<style lang="less" scoped>
#login_container {
	width: 100%;
	height: 100%;
	background: url("../assets/images/login_back.png") no-repeat fixed;
	background-position: center;
	background-size: cover;
	position: relative;
}

label {
	width: 60%;
	height: 70%;
	position: relative;
	top: 50%;
	left: 50%;
	display: block;
	z-index: 10;
	transform: translate(-50%, -50%);
	perspective: 1000px;
}

.card {
	width: 100%;
	height: 100%;
	transform-style: preserve-3d;
	z-index: 20;

	&.convered {
		#signin {
			transform: rotateX(180deg);
		}

		#signup {
			transform: rotateX(360deg);
		}
	}
}

.login_box {
	width: 100%;
	height: 100%;
	border-radius: 10px;
	box-shadow: 0 0 3px 0 rgba(60, 64, 67, 0.2),
		0 0 15px 4px rgba(60, 64, 67, 0.15);
	overflow: hidden;
	backface-visibility: hidden;
	transition: all 600ms;
	position: absolute;

	&#signin {
		.login_blur {
			background-size: 100%;
			background: url("../assets/images/L.jpg");
		}
		.login_content {
			background: rgba(220, 218, 73, 0.15);
		}
		.login_title {
			color: @signinColor;
			span {
				&::after {
					background: linear-gradient(to right, transparent, @signinColor);
				}
				&::before {
					background: linear-gradient(to left, transparent, @signinColor);
				}
			}
		}
	}

	&#signup {
		transform: rotateX(180deg);

		.login_blur {
			background: url("../assets/images/bur.jpg");
			background-size: 100%;
		}
		.login_content {
			background: rgba(45, 92, 128, 0.15);
		}
		.login_title {
			color: @signupColor;
			span {
				&::after {
					background: linear-gradient(to right, transparent, @signupColor);
				}
				&::before {
					background: linear-gradient(to left, transparent, @signupColor);
				}
			}
		}
	}

	.login_blur {
		background-position: center;
		filter: blur(10px);
		position: absolute;
		width: 100%;
		height: 100%;
		top: 0;
		left: 0;
	}

	.login_content {
		position: absolute;
		right: 0;
		height: 100%;
		width: 40%;
		display: flex;
		align-items: center;
		flex-direction: column;

		.login_title {
			margin: 30px 0px 25px 0;
			font-weight: 600;
			font-size: 24px;

			span {
				position: relative;
				padding: 0 10px;
				&::after {
					content: "";
					position: absolute;
					left: 0;
					top: 50%;
					transform: translate(-100%, -50%);
					width: 70%;
					height: 2px;
				}

				&::before {
					content: "";
					position: absolute;
					right: 0;
					top: 50%;
					transform: translate(100%, -50%);
					width: 70%;
					height: 2px;
				}
			}
		}
	}
}
.switch_btn {
	margin-top: 15px;
	margin-right: 20px;
	margin-left: auto;
}
.Title{
	position: absolute;
		left: 0;
		height: 100%;
		width: 60%;
		display: flex;
		align-items: center;
		/* 垂直居中 */
		justify-content: center;
		/* 水平居中 */
		flex-direction: column;
		font-size: 3em;
		font-weight: 800;
		color: #fefefe;
		text-shadow: 0px 1px 0px #c0c0c0, 0px 2px 0px #b0b0b0,
			0px 3px 0px #a0a0a0, 0px 4px 0px #909090,
			0px 5px 10px rgba(0, 0, 0, 0.9);
		user-select: none;
}
</style>