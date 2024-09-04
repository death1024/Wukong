import asyncio
import mini.mini_sdk as MiniSdk

from mini.apis.api_observe import ObserveSpeechRecognise
from mini.apis.api_sound import StartPlayTTS
from mini.dns.dns_browser import WiFiDevice
from mini.pb2.codemao_speechrecognise_pb2 import SpeechRecogniseResponse
from mini.apis.api_setup import StartRunProgram

MiniSdk.set_robot_type(MiniSdk.RobotType.MINI)

async def test_get_device_by_name():
    """根据机器人序列号后缀搜索设备

    搜索指定序列号(在机器人屁股后面)的机器人, 可以只输入序列号尾部字符即可,长度任意, 建议5个字符以上可以准确匹配, 10秒超时


    Returns:
        WiFiDevice: 包含机器人名称,ip,port等信息

    """
    result: WiFiDevice = await MiniSdk.get_device_by_name("00089", 10)
    print(f"test_get_device_by_name result:{result}")
    return result

async def test_start_run_program():
    await StartRunProgram().execute()
    await asyncio.sleep(6)


# 断开连接并释放资源
async def shutdown():
    """断开连接并释放资源

    断开当前连接的设备，并释放资源

    """
    await MiniSdk.quit_program()
    await MiniSdk.release()

# MiniSdk.connect 返回值为bool, 这里忽略返回值
async def test_connect(dev: WiFiDevice) -> bool:
    """连接设备

    连接指定的设备

    Args:
        dev (WiFiDevice): 指定的设备对象 WiFiDevice

    Returns:
        bool: 是否连接成功

    """
    return await MiniSdk.connect(dev)

async def __tts():
    block: StartPlayTTS = StartPlayTTS(text="我知道你们是第七小组")
    response = await block.execute()
    print(f'tes_play_tts: {response}')


# 测试监听语音识别
async def test_speech_recognise():
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
    def handler(msg: SpeechRecogniseResponse): # type: ignore
        print(f'=======handle speech recognise:{msg}')
        print("{0}".format(str(msg.text)))

        # if str(msg.text)[-1].isalpha() is False:
        #     if str(msg.text)[:-1].lower() == "Hello":
        #         asyncio.create_task(__tts())

        if str(msg.text).lower() == "我们是第七小组":
            # 监听到"悟空", tts打个招呼
            asyncio.create_task(__tts())

        elif str(msg.text).lower() == "结束":
            # 监听到结束, 停止监听
            observe.stop()
            # 结束event_loop
            asyncio.get_running_loop().run_in_executor(None, asyncio.get_running_loop().stop)

    observe.set_handler(handler)
    # 启动
    observe.start()
    await asyncio.sleep(0)

def main():
    device: WiFiDevice = asyncio.get_event_loop().run_until_complete(test_get_device_by_name())
    if device:
        asyncio.get_event_loop().run_until_complete(test_connect(device))
        asyncio.get_event_loop().run_until_complete(test_start_run_program())
        asyncio.get_event_loop().run_until_complete(test_speech_recognise())
        # 定义了事件监听对象,必须让event_loop.run_forver()
        asyncio.get_event_loop().run_forever()
        asyncio.get_event_loop().run_until_complete(shutdown())

if __name__ == '__main__':
    main()
