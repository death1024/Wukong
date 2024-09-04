import asyncio
import logging
from mini import mini_sdk as MiniSdk
from mini.apis.api_action import MoveRobot, MoveRobotDirection
from mini.apis.api_sound import StartPlayTTS
from mini.apis.api_observe import ObserveSpeechRecognise
from mini.apis.base_api import MiniApiResultType
from mini.dns.dns_browser import WiFiDevice
from mini.pb2.codemao_speechrecognise_pb2 import SpeechRecogniseResponse
from global_data import data
from server_module import Server
from test_connect import test_connect, shutdown
from test_connect import test_get_device_by_name, test_start_run_program
from mini.apis.api_observe import ObserveSpeechRecognise
from mini.apis.api_sound import StartPlayTTS
from mini.dns.dns_browser import WiFiDevice
from mini.pb2.codemao_speechrecognise_pb2 import SpeechRecogniseResponse

logging.basicConfig(level=logging.INFO)
MiniSdk.set_robot_type(MiniSdk.RobotType.MINI)

class SpeechHandler: 
    async def say_greeting(self):
        block: StartPlayTTS = StartPlayTTS(text="你好，我们是第七小组，啦里啦，啦里啦")
        response = await block.execute()
        logging.info(f'TTS播放结果: {response}')


    async def handle_response(self, text):
        if text.lower() == "我们是第七小组":
            await self.say_greeting()
        elif text.lower() == "结束":
            logging.info("识别到结束命令，停止监听或执行其他操作")

    async def test_speech_recognise(self):
        observe: ObserveSpeechRecognise = ObserveSpeechRecognise()

        def handler(msg: SpeechRecogniseResponse):
            print(f'=======handle speech recognise:{msg}')
            print("{0}".format(str(msg.text)))
            asyncio.create_task(self.handle_response(msg.text))

        observe.set_handler(handler)
        observe.start()
        await asyncio.sleep(0)



class RobotController:
    async def test_get_device_by_name(self):
        """根据机器人序列号后缀搜索设备"""
        result: WiFiDevice = await MiniSdk.get_device_by_name("030007KFK18091800089", 10)
        print(f"test_get_device_by_name result:{result}")
        return result

    async def control_robot(self, data):
        device: WiFiDevice = await self.test_get_device_by_name()
        if device:
            await MiniSdk.connect(device)
            await MiniSdk.enter_program()
            try:
                while True:
                    await asyncio.sleep(5)
                    if data["AttentionData"] == 'high':
                        block: MoveRobot = MoveRobot(step=4, direction=MoveRobotDirection.FORWARD)
                        resultType, response = await block.execute()
                        if resultType == MiniApiResultType.Success and response.isSuccess:
                            logging.info("Robot moved forward successfully")
                        else:
                            logging.error("Robot failed to move forward")

                    elif data["AttentionData"] == 'low':
                        block: MoveRobot = MoveRobot(step=10, direction=MoveRobotDirection.BACKWARD)
                        resultType, response = await block.execute()
                        if resultType == MiniApiResultType.Success and response.isSuccess:
                            logging.info("Robot moved backward successfully")
                        else:
                            logging.error("Robot failed to move backward")

                    await asyncio.sleep(1)  # Check every second
            except asyncio.CancelledError:
                logging.info("Robot control task cancelled")
            finally:
                await MiniSdk.quit_program()
                await MiniSdk.release()

async def main():
    speech_handler = SpeechHandler()
    robot_controller = RobotController()
    server = Server()
    server_task = asyncio.create_task(server.run())
    control_robot_task = asyncio.create_task(robot_controller.control_robot(data))
    speech_recognise_task = asyncio.create_task(speech_handler.test_speech_recognise())

    await asyncio.gather(server_task, control_robot_task, speech_recognise_task)

if __name__ == '__main__':
    asyncio.run(main())
