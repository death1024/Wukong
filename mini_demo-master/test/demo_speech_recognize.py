
import asyncio
from mini.apis.api_observe import ObserveSpeechRecognise
from mini.dns.dns_browser import WiFiDevice
from mini.apis.api_sound import StartPlayTTS
from mini.pb2.codemao_speechrecognise_pb2 import SpeechRecogniseResponse
from test_connect import test_connect, shutdown
from test_connect import test_get_device_by_name, test_start_run_program
import global_data 
import EEGmodel 
import ttsmodel
import music
from bigmodel import returnContent


#signal
initialflag=1
llm_flag = 0



async def __tts(sentence, observe: ObserveSpeechRecognise):
    """播放TTS并在完成后重新启动监听"""
    observe.stop()  # 停止语音监听
    block: StartPlayTTS = StartPlayTTS(text=sentence)
    response = await block.execute()
    print(f'tes_play_tts: {response}')
    observe.start()  # 重新启动语音监听

#运动模式
async def action_model():
    await EEGmodel.hrmodel(int(float(global_data.read_specific_data("HRData"))))



#冥想模式
async def sequential_meditation():
    nflag=0
    await ttsmodel.__tts_speak("已进入冥想模式")
    await ttsmodel.__tts_speak("深深地吸一口气，然后缓缓地呼出。再次重复，每次呼吸都让你更加接近于现实")
    await music.test_play_online_audio()

    coherancedata=EEGmodel.check_coherence_model(int(float(global_data.read_specific_data("PressureData"))))

    while coherancedata==1:
        nflag=nflag+1

        await ttsmodel.__tts_speak("继续深呼吸，吸气")
        await asyncio.sleep(2)
        await ttsmodel.__tts_speak("呼气")
        await asyncio.sleep(2)

        coherancedata=EEGmodel.check_coherence_model(int(float(global_data.read_specific_data("PressureData"))))
        if nflag==3:
            break


#脑电模式
async def sequential_eeg():
    global actflag
    global initialflag
    '''
    进入脑电模式后，执行以下函数
    flag为标志位，EEGmodel.……函数执行后则置0，时一次只执行一类动作
    '''
    global flag
    flag = 1
    await ttsmodel.__tts_speak("已进入脑电模式")
    #直说一次
    if initialflag==1:
        await ttsmodel.__tts_speak("我是悟空，现在我和你共享心情了噢")
        initialflag=0
    
    #压力值
    flag = await EEGmodel.pressuremodel(int(float(global_data.read_specific_data("PressureData"))),flag)
    #注意力
    flag = await EEGmodel.attentionmodel(int(float(global_data.read_specific_data("AttentionData"))),flag)

    await ttsmodel.__tts_speak("让我再感受一下你的心情")




async def test_speech_recognise():
    global flag_eeg_model
    global actflag
    """监听语音识别demo
    监听语音识别事件，机器人上报语音识别后的文字
    当识别到语音为"悟空"时，播报"你好， 我是悟空， 啦里啦，啦里啦"
    当识别到语音为"结束"时，停止监听
    # SpeechRecogniseResponse.text
    # SpeechRecogniseResponse.isSuccess
    # SpeechRecogniseResponse.resultCode
    """
    # 语音监听对象

    observe: ObserveSpeechRecognise = ObserveSpeechRecognise()
    # 处理器
    # SpeechRecogniseResponse.text
    # SpeechRecogniseResponse.isSuccess
    # SpeechRecogniseResponse.resultCode
    def handler(msg: SpeechRecogniseResponse):

        global flag_eeg_model
        global flag
        #打印监听到的内容
        print(f'=======handle speech recognise:{msg}')
        print("{0}".format(str(msg.text)))
        #复位标志位


        
        if str(msg.text).lower() == "脑电模式" or str(msg.text).lower() == "老电模式"or str(msg.text).lower() == "电模式"or str(msg.text).lower() == "电模"or str(msg.text).lower() == "省电模式"  or str(msg.text).lower() == "脑电模" or str(msg.text).lower() == "脑电" :
            flag=1
            asyncio.create_task(sequential_eeg())
        


        elif str(msg.text).lower() == "冥想模式" or str(msg.text).lower() == "想模式" or str(msg.text).lower() == "冥想模"  or str(msg.text).lower() == "冥想" or str(msg.text).lower() == "影响":
            asyncio.create_task(sequential_meditation())



        elif str(msg.text).lower() == "运动模式" or str(msg.text).lower() == "动模式" or str(msg.text).lower() == "运动模" or str(msg.text).lower() == "动模" :
            asyncio.create_task(action_model())


        global llm_flag
        if str(msg.text).lower() == "聊天模式" or str(msg.text).lower() =="开始聊天"  and llm_flag == 0:
            asyncio.create_task(__tts("好的，让我们来聊天吧", observe))
            llm_flag = 1
        
        if llm_flag == 1:
            if str(msg.text).lower() == "停止聊天":
                asyncio.create_task(__tts('已退出星火大模型聊天，期待下次的交流哦', observe))
                llm_flag = 0
            else:
                res = returnContent('请对以下问题生成不多于70字的简短回答:' + str(msg.text).lower())
                print(res)
                asyncio.create_task(__tts(res, observe))



        elif str(msg.text).lower() == "结束":
            # 监听到结束, 停止监听
            observe.stop()
            # 结束event_loop
            asyncio.get_running_loop().run_in_executor(None, asyncio.get_running_loop().stop)


    observe.set_handler(handler)
    # 启动
    observe.start()
    await asyncio.sleep(0)




if __name__ == '__main__':
    device: WiFiDevice = asyncio.get_event_loop().run_until_complete(test_get_device_by_name())
    if device:
        asyncio.get_event_loop().run_until_complete(test_connect(device))
        asyncio.get_event_loop().run_until_complete(test_start_run_program())
        ##进入监听
        asyncio.get_event_loop().run_until_complete(test_speech_recognise())
        asyncio.get_event_loop().run_until_complete(ttsmodel.__tts_speak("请选择模式"))
        asyncio.get_event_loop().run_forever()
        asyncio.get_event_loop().run_until_complete(shutdown())

















