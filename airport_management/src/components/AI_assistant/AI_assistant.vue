<template>
  <div id="talkbox_wrapper_min" ref="tb_normal">
    <div id="talkbox_max" class="b_hide" ref="tb_max">
      <div class="talkbox_header">
        <svg t="1747986010003" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"
          p-id="2887" width="32" height="32">
          <path
            d="M213.333333 588.16c15.914667-5.824 31.04-11.456 46.293334-16.746667 1.493333-0.533333 3.968 0.554667 5.589333 1.557334 17.024 10.538667 33.92 21.269333 50.986667 31.786666 1.6 1.002667 4.288 1.578667 5.973333 0.96 34.666667-12.416 69.248-25.045333 103.829333-37.632 0.576-0.213333 1.109333-0.576 2.112-1.130666l-133.12-205.141334c1.578667-0.682667 2.816-1.28 4.074667-1.749333 16.384-5.994667 32.832-11.861333 49.130667-18.048 3.498667-1.322667 5.76-0.704 8.576 1.536 70.272 55.850667 140.650667 111.573333 210.88 167.466667 3.626667 2.88 6.4 3.242667 10.688 1.664 55.893333-20.501333 111.850667-40.853333 167.808-61.141334 26.048-9.450667 51.797333 5.888 55.914666 33.130667 2.816 18.624-8.682667 37.077333-27.605333 44.010667-44.053333 16.085333-88.106667 32.106667-132.181333 48.149333L334.613333 688.853333c-22.144 8.085333-39.04 2.048-53.162666-16.938666-12.906667-17.344-27.2-33.664-40.874667-50.410667L213.333333 588.16z"
            fill="#3D3D3D" p-id="2888"></path>
        </svg>
        <div id="tb_header_text" class="tb_header_text">
          珞航小智
        </div>
        <i class="iconfont closeIcon" @click="panelSwitch">&#xeaf2;</i>
      </div>
      <div id="default_talk">
        <span id="talk" class="talk" ref="talk">
          <div id="privacy_text_top">由xxx队提供的中国民航大语言模型已唤醒，可以随时开始聊天啦</div>
          <div style="padding: 0 0 5px 0; display: flex; justify-content: center;">
            <el-radio-group v-model="radio" size="small">
              <el-radio-button label="文字模式"></el-radio-button>
              <el-radio-button label="图表模式"></el-radio-button>
              <el-radio-button label="图文报表模式"></el-radio-button>
            </el-radio-group>
          </div>
          <div class="talk_panel">
            <div v-for="(message, index) in messages" :key="index"
              :class="message.isUser ? 'user-message' : 'robot-message'">
              <img class="avatar" :src="message.isUser ? '../../../imgs/user.png' : '../../../imgs/robot.png'"
                :alt="message.isUser ? 'User Avatar' : 'Robot Avatar'" :style="{ order: message.isUser ? 2 : 1 }" />
              <p :style="{ order: message.isUser ? 1 : 2 }">
                <template v-if="message.isUser">
                  {{ message.text }}
                </template>
                <template v-else>
                  <div v-html="markdown(message.text)"></div>
                  <template v-if="message.isImage">
                    <div style="display: flex;justify-content: center">
                      <el-image :src="message.thumbnail" :preview-src-list="message.masterImg">
                      </el-image>
                    </div>
                  </template>

                  <template v-else-if="message.isReport">
                    <div
                      style="margin-top:10px;display: flex;flex-direction:column;justify-content: center;cursor: pointer;">
                      <img @click="PreviewFile(message.docxFile)" src="@/assets/images/word文档.png">
                      <el-button type="text" @click="PreviewFile(message.docxFile)">报表预览</el-button>
                    </div>
                  </template>

                </template>
              </p>
            </div>
          </div>
        </span>
        <div id="privacy_text_bottom" ref="loadParent">
          <div id="privacy_text_bottom_text" ref="loadChild">本服务由xxx队运营</div>
        </div>
        <div id="voice">
          <div class="voice-input-button-wrapper" style="display: flex; justify-content: center;">
            <voice-input-button v-model="voiceResult" @record="showResult" @record-start="recordStart"
              @record-stop="recordStop" @record-blank="recordNoResult" @record-failed="recordFailed"
              @record-ready="recordReady" @record-complete="recordComplete" interactiveMode="touch">
              <template slot="no-speak">没听清您说的什么</template>
            </voice-input-button>
          </div>
          <el-input placeholder="来说点什么吧" v-model="voiceResult" @keyup.enter.native="sendMessage">
            <el-button slot="append" @click="sendMessage"><i class="iconfont">&#xe646;</i></el-button>
          </el-input>
        </div>
      </div>
    </div>
    <!-- AI缩小模式 -->
    <div id="talkbox_min" class="Draggable_container talkbox_min" :style="{ top: `${top}px`, right: `${right}px` }"
      ref="tb_min">
      <div class="zoom-ai" @click="toggleZoom">
        <!-- 根据 isZoomed 的值动态切换 SVG 图标 -->
        <svg v-if="!isZoomed" class="icon_zoom" width="64px" height="64.00px" viewBox="0 0 1024 1024" version="1.1"
          xmlns="http://www.w3.org/2000/svg">
          <path
            d="M480 544V853.333333h-64v-200.106666l-222.72 222.72-45.226667-45.226667 222.72-222.72H170.666667v-64h309.333333z m350.72-395.946667l45.226667 45.226667-222.72 222.72H853.333333v64h-309.333333V170.666667h64v200.106666l222.72-222.72z">
          </path>
        </svg>
        <svg v-else class="icon_zoom" width="64px" height="64.00px" viewBox="0 0 1024 1024" version="1.1"
          xmlns="http://www.w3.org/2000/svg">
          <path
            d="M425.386667 553.386667l45.226666 45.226666-201.386666 201.386667h178.773333v64H160V576h64v178.688l201.386667-201.301333z m438.613333-393.386667v288h-64V269.226667l-201.386667 201.386666-45.226666-45.226666 201.301333-201.386667H576v-64h288z">
          </path>
        </svg>
      </div>
      <div class="pet-content" v-show="!isZoomed" @click="panelSwitch">
        <img src="../../assets/images/chatRobot.gif" alt="Pet" class="gif" />
      </div>
      <div class="pet-name" v-show="!isZoomed">珞航小智</div>
    </div>
  </div>
</template>


<script>

import MarkdownIt from 'markdown-it';

export default {
  data() {
    return {
      top: window.innerHeight - 150, // 初始位置：距离底部的偏移量
      right: 20, // 初始位置：距离右侧的偏移量
      isDragging: false, // 是否正在拖动
      offsetX: 0, // 鼠标点击时的偏移量
      offsetY: 0,
      isZoomed: false, // 控制缩放状态

      //GPT相关配置
      // 语音以及输入 people
      voiceResult: '',
      voiceResultTemp: '',
      // chatgpt
      generatedText: '',
      // 总对话
      messages: [{
        text: '请问有什么能够帮助您的?',
        isUser: false,
        isImage: false,
        isReport: false,
        docxFile: null,
        thumbnail: '',
        masterImg: [
          '',
        ]
      }],
      isImage: false,
      isReport: false,
      docxFile: null,
      htmlData: '',
      // 面板状态
      isMax: false,
      // test: '## 我是'
      thumbnail: `http://localhost:7070/wpfgpt/api/images/20.png`,
      masterImg: [
        `http://localhost:7070/wpfgpt/api/images/20.png`,
      ],
      radio: '文字模式'
    };
  },
  components:{
  },
  methods: {
    startDrag(event) {
      this.isDragging = true;
      this.offsetX = event.clientX - this.right;
      this.offsetY = event.clientY - this.top;
      document.addEventListener("mousemove", this.onDragging);
      document.addEventListener("mouseup", this.stopDrag);
    },
    onDragging(event) {
      if (this.isDragging) {
        this.right = event.clientX - this.offsetX;
        this.top = event.clientY - this.offsetY;
      }
    },
    stopDrag() {
      this.isDragging = false;
      document.removeEventListener("mousemove", this.onDragging);
      document.removeEventListener("mouseup", this.stopDrag);
    },
    toggleZoom() {
      this.isZoomed = !this.isZoomed; // 切换缩放状态
    },

    //下面是AI智能体相关的函数
    PreviewFile(docxFile) {//点击预览事件的时候拿到当前对应的一个文件属性
      this.panelSwitch();
      this.$emit('custom-event', { docxFile: docxFile });
    },

    markdown(text) {
      const md = new MarkdownIt()
      const result = md.render(text)
      return result
    },

    // 科大讯飞
    recordReady() {
      console.info('按钮就绪!')
    },
    recordStart() {
      console.info('录音开始')
    },
    showResult(text) {
      console.info('收到识别结果：', text)
    },
    recordStop() {
      console.info('录音结束')
    },
    recordNoResult() {
      console.info('没有录到什么，请重试')
    },
    recordComplete(text) {
      console.info('识别完成! 最终结果：', text)
    },
    recordFailed(error) {
      console.info('识别失败，错误栈：', error)
    },
    // chatgpt
    async generateText() {
      // 前端版本
      // this.generatedText = await ChatGPT.generateText(this.voiceResult);
      // 发送对话信息给gpt接口
      // Java版本
      //根据用户输入构建请求
      if (this.radio =='智能推荐模式'){
        var processParams = {
          "question": this.voiceResultTemp,
          "fileName": this.$store.state.global.uploadedFileName,
        }

        await this.request.post("/wpfgpt/postChat2", processParams).then((res) => {
          if (res.code === "200") {
            this.isImage = res.image
            this.isReport = res.report
            this.thumbnail = "http://" + serverIp + ":7070/wpfgpt/api/images/" + (res.time) + ".png"
            this.masterImg = ["http://" + serverIp + ":7070/wpfgpt/api/images/" + (res.time) + ".png"]
            this.docxFile = "http://" + serverIp + ":7070/wpfgpt/docx/" + processParams.fileName.replace(".csv", "") + "_" + (res.time) + ".docx";
            console.log(res.msg)
            this.generatedText = res.msg;
          } else {
            document.getElementById('loading').textContent = '抱歉，服务器异常，请重试';
          }
        });
      }
      else if (this.radio=='智能调度模式'){
      }
      else {
        
      }
      },
    // 对话信息
    async sendMessage() {
      // 将用户发送的信息添加到对话数组中
      this.messages.push({
        text: this.voiceResult,
        isUser: true, // 表示该条信息是用户发送的
        isImage: this.isImage,
        isReport: this.isReport,
        thumbnail: this.thumbnail,
        masterImg: this.masterImg,
        docxFile: this.docxFile,
      });


      this.voiceResultTemp = this.voiceResult;
      // 清空用户输入框
      this.voiceResult = '';

      //  判断异常与否
      if (document.getElementById('loading')) {
        document.getElementById('loading').remove()
      }
      // 创建新的元素
      const loadingP = document.createElement('p');
      loadingP.id = 'loading';

      // 设置元素内容和样式
      loadingP.textContent = '请稍候...';
      loadingP.setAttribute('style', 'width: 100%;height: 14px;text-align: center;line-height: 14px;padding: 8px 0;color: #000000;font-size: 12px;letter-spacing: 0;margin:0')

      // 将元素插入页面
      this.$refs.loadParent.insertBefore(loadingP, this.$refs.loadChild);
      this.$refs.loadChild.style.display = 'none'

      await this.generateText()

      // 恢复原状
      document.getElementById('loading').remove();
      this.$refs.loadChild.style.display = 'block'
      // 模拟机器人回答信息（这里使用了setTimeout来模拟异步）
      // setTimeout(() => {
      //   // this.generatedText = '这是机器人的回答'; // 替换成真实的机器人回答信息

      //   // 将机器人回答的信息添加到对话数组中
      //   this.messages.push({
      //     text: this.generatedText,
      //     isUser: false, // 表示该条信息是机器人回答的
      //   });
      // }, 0);
      this.messages.push({
        text: this.generatedText,
        isUser: false, // 表示该条信息是机器人回答的
        isImage: this.isImage,
        isReport: this.isReport,
        thumbnail: this.thumbnail,
        masterImg: this.masterImg,
        docxFile: this.docxFile,
      });

      setTimeout(() => {
        //  滚动至最下方
        this.$refs.talk.scrollTop = this.$refs.talk.scrollHeight;
        console.log(this.$refs.talk.scrollTop)
      }, 500)
    },
    // 切换GPT面版
    panelSwitch() {
      if (!this.isMax) {
        this.$refs.tb_normal.classList.add('talkbox_wrapper_max', 'animated', 'fadeInRight')
        this.$refs.tb_max.classList.remove('b_hide')
        this.$refs.tb_min.classList.add('b_hide')
        this.isMax = true
      } else {
        this.$refs.tb_normal.classList.remove('talkbox_wrapper_max', 'fadeInRight')
        this.$refs.tb_max.classList.add('b_hide')
        this.$refs.tb_min.classList.remove('b_hide')
        this.isMax = false
      }
    },
    mouseLeaveSwitch() {
      this.$refs.minImg.addEventListener('mouseleave', () => {
        this.$refs.minImg.style.backgroundImage = "url('../../../imgs/th_sleep.jpg')";
      });
    }
  },
  mounted() {
    this.mouseLeaveSwitch()
  }
};
</script>

<style lang="less">
.Draggable_container {
  position: fixed;
  z-index: 10000;
  cursor: pointer;
  padding: 15px;
  background-color: #fff;
  border: 1px solid #ccc;
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.pet-content {
  text-align: center;
  border-radius: 5px;
}

.pet-content img {
  width: 100px;
  height: 80px;
  border-radius: 50%;
}

.pet-name {
  font-size: 14px;
  color: #333;
  margin-top: 10px;
  text-align: center;
}

.zoom-ai {
  cursor: pointer;
  position: absolute;
  top: 5px;
  right: 5px;
  display: flex;
  /* 使用 flex 布局 */
  justify-content: center;
  /* 水平居中 */
  align-items: center;
  /* 垂直居中 */
  padding: 0px;
  margin-bottom: 30px;
}

.icon_zoom {
  width: 20px;
  height: 20px;
  fill: #333;
}

.gif {

  user-select: none;

}

//AI窗口的样式
// 大于800px
@media only screen and (min-width: 800px) {
  #voice {
    margin: 0 auto;
    width: 100%;
    height: 30px;
    display: flex;
    justify-content: space-around;
    align-items: center;
    margin-bottom: 10px;

    .voice-input-button-wrapper {
      width: 30px;
      height: 30px;
      background-color: #77ACEF;
      border-radius: 50%;
    }

    .el-input {
      width: 90%;

      .el-input__inner,
      .el-button {
        height: 30px;
      }

      .el-button:hover {
        font-weight: 900;
        font-size: larger;
      }
    }
  }

  .b_hide {
    display: none;
  }

  // 缩略图
  .el-image-viewer__wrapper {
    z-index: 999999999999 !important;
  }

  #talkbox_wrapper_min {
    position: fixed;
    cursor: pointer;
    top: 85%;
    right: 5px;
    background-color: transparent;
    z-index: 99999999999;

  }

  .talkbox_wrapper_max {
    cursor: default !important;
    width: 50%;
    top: 20% !important;
    right: 25% !important;
    // transform: translateX(50%) !important;
    background-color: white !important;
    border-radius: 6px;
    border: 1px #B8D4FF solid;

    #talkbox_max {
      // width: 50%;
      height: 500px;

      .talkbox_header {
        height: 40px;
        line-height: 40px;
        border-radius: 6px 6px 0 0;
        border-bottom: 1px #F1F1F1 solid;
        background: white;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 10px;

        .closeIcon {
          cursor: pointer;
        }
      }

      #default_talk {
        border-radius: 0 0 6px 6px;

        #talk {
          display: block;
          overflow-x: hidden;
          overflow-y: auto;
          height: 395px;
          width: 100%;

          #privacy_text_top {
            text-align: center;
            font-size: 14px;
            letter-spacing: .8px;
            color: #c0c0c0;
            overflow: hidden;
            padding: 10px 0 5px 0;
            vertical-align: middle;
          }

          .talk_panel {
            display: flex;
            flex-direction: column;

            .user-message,
            .robot-message {
              display: flex;
              align-items: start;
              margin-bottom: 10px;
            }

            .user-message {
              justify-content: flex-end;
              margin-left: 5px;
              margin-right: 5px;

              p {
                margin-right: 5px;
                font-size: 14px;
                text-align: right;
              }
            }

            .robot-message {
              margin-left: 5px;
              margin-right: 5px;
              // width: 290px;

              p {
                margin-left: 5px;
                font-size: 14px;
                text-align: left;

                .el-image {
                  width: 250px;
                  height: 250px;
                }

                div {
                  // width: 290px;

                  p {
                    margin: 0;
                  }

                  pre {
                    code {
                      display: inline-block;
                      width: 100% !important;
                      white-space: pre-wrap;
                      background-color: rgba(251, 251, 251, 0.8);
                      color: #409EFF;
                      font-weight: 800;
                      border: 1px solid #F1F1F1;
                      padding: 5px;

                      #text {
                        // width: 280px !important;
                      }
                    }
                  }
                }
              }
            }
          }
        }

        #privacy_text_bottom {
          height: 30px;
          width: 100%;

          #privacy_text_bottom_text {
            width: 100%;
            height: 14px;
            text-align: center;
            line-height: 14px;
            padding: 8px 0;
            color: #c8c8c8;
            font-size: 14px;
            letter-spacing: 0;
          }
        }
      }
    }
  }
}

// 小于800px
@media only screen and (max-width: 800px) {
  #voice {
    margin: 0 auto;
    width: 324px;
    height: 30px;
    display: flex;
    justify-content: space-around;
    align-items: center;
    margin-bottom: 10px;

    .voice-input-button-wrapper {
      width: 30px;
      height: 30px;
      background-color: #77ACEF;
      border-radius: 50%;
    }

    .el-input {
      width: 85%;

      .el-input__inner,
      .el-button {
        height: 30px;
      }

      .el-button:hover {
        font-weight: 900;
        font-size: larger;
      }
    }
  }

  .b_hide {
    display: none;
  }

  #talkbox_wrapper_min {
    position: fixed;
    cursor: pointer;
    top: 85%;
    right: 5px;
    background-color: transparent;
    z-index: 99999999999;

  }

  .talkbox_wrapper_max {
    cursor: default !important;
    top: 25% !important;
    right: 25px !important;
    background-color: white !important;
    border-radius: 6px;
    border: 1px #B8D4FF solid;

    #talkbox_max {
      width: 348px;
      //width: 700px;
      height: 400px;
      //height: 500px;

      .talkbox_header {
        height: 40px;
        line-height: 40px;
        border-radius: 6px 6px 0 0;
        border-bottom: 1px #F1F1F1 solid;
        background: white;
        display: flex;
        justify-content: space-around;
        align-items: center;

        .closeIcon {
          cursor: pointer;
        }
      }

      #default_talk {
        border-radius: 0 0 6px 6px;

        #talk {
          display: block;
          overflow-x: hidden;
          overflow-y: auto;
          height: 290px;
          width: 348px;

          #privacy_text_top {
            text-align: center;
            font-size: 10px;
            letter-spacing: .3px;
            color: #c0c0c0;
            overflow: hidden;
            padding: 10px 0 5px 0;
            vertical-align: middle;
          }

          .talk_panel {
            display: flex;
            flex-direction: column;

            .user-message,
            .robot-message {
              display: flex;
              align-items: start;
              margin-bottom: 10px;
            }

            .user-message {
              justify-content: flex-end;
              margin-left: 5px;
              margin-right: 5px;

              p {
                margin-right: 5px;
                font-size: 12px;
                text-align: right;
              }
            }

            .robot-message {
              margin-left: 5px;
              margin-right: 5px;
              width: 290px;

              p {
                margin-left: 5px;
                font-size: 12px;
                text-align: left;

                .el-image {
                  width: 100px;
                  height: 100px;
                }

                div {
                  width: 290px;

                  p {
                    margin: 0;
                  }

                  pre {
                    code {
                      display: inline-block;
                      width: 280px !important;
                      white-space: pre-wrap;
                      background-color: rgba(251, 251, 251, 0.8);
                      color: #409EFF;
                      font-weight: 800;
                      border: 1px solid #F1F1F1;
                      padding: 5px;

                      #text {
                        width: 280px !important;
                      }
                    }
                  }
                }
              }
            }
          }
        }

        #privacy_text_bottom {
          height: 30px;
          width: 348px;

          #privacy_text_bottom_text {
            width: 348px;
            height: 14px;
            text-align: center;
            line-height: 14px;
            padding: 8px 0;
            color: #c8c8c8;
            font-size: 10px;
            letter-spacing: 0;
          }
        }
      }
    }
  }
}
</style>