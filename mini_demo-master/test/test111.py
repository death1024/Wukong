import asyncio
import logging
import random
from mini import mini_sdk as MiniSdk
from mini.apis.api_action import MoveRobot, MoveRobotDirection, MoveRobotResponse
from mini.apis.api_sound import StartPlayTTS
from mini.apis.api_observe import ObserveSpeechRecognise
from mini.apis.base_api import MiniApiResultType
from mini.dns.dns_browser import WiFiDevice
from mini.pb2.codemao_speechrecognise_pb2 import SpeechRecogniseResponse
from test_connect import test_get_device_by_name

logging.basicConfig(level=logging.INFO)

class AsyncServer:
    def __init__(self):
        self.is_running = True
        self.attention = 'unknown'
        self.relaxation = 'unknown'
        self.pressure = 'unknown'
        self.arousal = 'unknown'
        self.pleasure = 'unknown'
        self.coherence = 'unknown'
        self.hr_data = 'unknown'

    async def receive_data(self):
        while self.is_running:
            await asyncio.sleep(1)  # Simulate receiving data every second
            self.attention = random.choice(['low', 'medium', 'high'])
            self.relaxation = random.choice(['low', 'medium', 'high'])
            logging.info(f"Simulated Data Received - Attention: {self.attention}, Relaxation: {self.relaxation}")

class RobotController:
    async def control_robot(self):
        device: WiFiDevice = await test_get_device_by_name()
        if device:
            await MiniSdk.connect(device)
            await MiniSdk.enter_program()

            try:
                while self.is_running:
                    if self.attention == 'high':
                        block: MoveRobot = MoveRobot(step=10, direction=MoveRobotDirection.FORWARD)
                        resultType, response = await block.execute()
                        if resultType == MiniApiResultType.Success and response.isSuccess:
                            logging.info("Robot moved forward successfully")
                        else:
                            logging.error("Robot failed to move forward")

                    elif self.attention == 'low':
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

class SpeechHandler:
    async def handle_response(self, text):
        if text.lower() == "我们是第七小组":
            await self.say_greeting()
        elif text.lower() == "结束":
            logging.info("识别到结束命令，停止监听或执行其他操作")

    async def say_greeting(self):
        block: StartPlayTTS = StartPlayTTS(text="你好，我们是第七小组，啦里啦，啦里啦")
        response = await block.execute()
        logging.info(f'TTS播放结果: {response}')

    async def test_speech_recognise(self):
        observe: ObserveSpeechRecognise = ObserveSpeechRecognise()

        def handler(msg: SpeechRecogniseResponse):
            asyncio.create_task(self.handle_response(msg.text))

        observe.set_handler(handler)
        observe.start()
        await asyncio.sleep(0)

async def main():
    server = AsyncServer()

    receive_data_task = asyncio.create_task(server.receive_data())
    control_robot_task = asyncio.create_task(RobotController.control_robot())
    speech_recognise_task = asyncio.create_task(SpeechHandler.test_speech_recognise())

    await asyncio.gather(receive_data_task, control_robot_task, speech_recognise_task)

if __name__ == '__main__':
    asyncio.run(main())