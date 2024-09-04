import socket
import json
from test_connect import test_connect
from test_connect import test_start_run_program
from test_connect import shutdown
import asyncio
import logging
from mini import mini_sdk as MiniSdk
from mini.apis.api_action import GetActionList, GetActionListResponse, RobotActionType
from mini.apis.api_action import MoveRobot, MoveRobotDirection, MoveRobotResponse
from mini.apis.api_action import PlayAction, PlayActionResponse
from mini.apis.base_api import MiniApiResultType
from mini.dns.dns_browser import WiFiDevice
from test_connect import test_get_device_by_name
import mini.mini_sdk as MiniSdk
from mini.dns.dns_browser import WiFiDevice




class ServerThread:
    def __init__(self, host='0.0.0.0', port=65432):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.is_running = False

        self.attention = '未知'
        self.relaxation = '未知'
        self.pressure = '未知'
        self.arousal = '未知'
        self.pleasure = '未知'
        self.coherence = '未知'
        self.hr_data = '未知'
        self.bc_data = '未知'
        self.eeg_left = '未知'
        self.eeg_right = '未知'

    def run(self):
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            print("Server started")
            self.is_running = True
            while self.is_running:
                client_socket, _ = self.server_socket.accept()
                with client_socket:
                    buffer = ""
                    while True:
                        data = client_socket.recv(1024)
                        if not data:
                            break
                        buffer += data.decode('utf-8')
                        while '\n' in buffer:
                            message, buffer = buffer.split('\n', 1)
                            self.process_message(message)
        finally:
            self.server_socket.close()
            print("Server stopped")

    def process_message(self, message):
        try:
            label, json_data = message.split(':', 1)
            data_dict = json.loads(json_data)
            self.update_data(label, data_dict)
        except Exception as e:
            print(f"Error processing message [{message}]: {e}")

    def update_data(self, label, data):
        value = data.get('value', '未知')

        if label == "AttentionData":
            self.attention = value
            print(f"Attention Level Updated: {value}")

        elif label == "RelaxationData":
            self.relaxation = value
            print(f"Relaxation Level Updated: {value}")

        elif label == "PressureData":
            self.pressure = value
            print(f"Pressure Level Updated: {value}")

        elif label == "ArousalData":
            self.arousal = value
            print(f"Arousal Level Updated: {value}")

        elif label == "PleasureData":
            self.pleasure = value
            print(f"Pleasure Level Updated: {value}")

        elif label == "CoherenceData":
            self.coherence = value
            print(f"Coherence Level Updated: {value}")

        elif label == "HRData":
            self.hr_data = value
            print(f"Heart Rate Data: {value}")

        elif label == "BCData":
            self.bc_data = value
            print(f"BC Data: {value}")

        elif label == "EEGData(L)":
            self.eeg_left = value
            print(f"EEG Left Data: {value}")

        elif label == "EEGData(R)":
            self.eeg_right = value
            print(f"EEG Right Data: {value}")

    def stop_server(self):
        self.is_running = False

async def test_move_robot():
    """控制机器人移动demo

    控制机器人往左(LEFTWARD)移动10步，并等待执行结果

    #MoveRobotResponse.isSuccess : 是否成功　

    #MoveRobotResponse.code : 返回码

    """
    # step: 移动几步
    # direction: 方向,枚举类型
    block: MoveRobot = MoveRobot(step=8, direction=MoveRobotDirection.FORWARD)
    # response : MoveRobotResponse
    (resultType, response) = await block.execute()

    print(f'test_move_robot result:{response}')

    assert resultType == MiniApiResultType.Success, 'test_move_robot timetout'
    assert response is not None and isinstance(response, MoveRobotResponse), 'test_move_robot result unavailable'
    assert response.isSuccess, 'move_robot failed'

async def test_get_action_list():
    """获取动作列表demo

    获取机器人内置的动作列表，等待回复结果

    """
    # action_type: INNER 是指机器人内置的不可修改的动作文件, CUSTOM 是放置在sdcard/customize/action目录下可被开发者修改的动作
    block: GetActionList = GetActionList(action_type=RobotActionType.INNER)
    # response:GetActionListResponse
    (resultType, response) = await block.execute()

    print(f'test_get_action_list result:{response}')

    assert resultType == MiniApiResultType.Success, 'test_get_action_list timetout'
    assert response is not None and isinstance(response,GetActionListResponse), 'test_get_action_list result unavailable'
    assert response.isSuccess, 'get_action_list failed'

async def test_play_action():
    """执行一个动作demo

    控制机器人执行一个指定名称的本地(内置/自定义)动作，并等待执行结果回复

    动作名称可用GetActionList获取

    #PlayActionResponse.isSuccess : 是否成功

    #PlayActionResponse.resultCode : 返回码

    """
    # action_name: 动作文件名, 可以通过GetActionList获取机器人支持的动作
    block: PlayAction = PlayAction(action_name='018')
    # response: PlayActionResponse
    (resultType, response) = await block.execute()

    print(f'test_play_action result:{response}')

    assert resultType == MiniApiResultType.Success, 'test_play_action timetout'
    assert response is not None and isinstance(response, PlayActionResponse), 'test_play_action result unavailable'
    assert response.isSuccess, 'play_action failed'



async def main():
    device: WiFiDevice = await test_get_device_by_name()
    if device:
        await MiniSdk.connect(device)
        await MiniSdk.enter_program()
        await test_play_action()
        await test_move_robot()
        await test_get_action_list()
        await MiniSdk.quit_program()
        await MiniSdk.release()


    #server_thread = ServerThread()
    #try:
        #server_thread.run()
    #except KeyboardInterrupt:
        #server_thread.stop_server()

    if __name__ == '__main__':
        asyncio.run(main())
