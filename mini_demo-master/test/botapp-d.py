import asyncio
import websockets
import json
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

class AsyncServer:
    def __init__(self, host='0.0.0.0', port=65432):
        self.host = host
        self.port = port
        self.is_running = True
        self.n=0
        self.attention = '未知'
        self.relaxation = '未知'
        self.pressure = '未知'
        self.arousal = '未知'
        self.pleasure = '未知'
        self.coherence = '未知'
        self.hr_data = '未知'


    async def server(self, websocket, path):
        print("A client just connected")
        try:
            while self.is_running:
                message = await websocket.recv(1024)
                await self.process_message(message)
        except websockets.ConnectionClosed:
            print("Connection with client closed")
        except Exception as e:
            print("Error in connection: ", str(e))

    async def process_message(self, message):
        try:
            label, json_data = message.split(':', 1)
            data_dict = json.loads(json_data)
            self.update_data(label, data_dict)
        except Exception as e:
            print(f"Error processing message [{message}]: {e}")

    async def update_data(self, label, data):
        value = data.get('value', '未知')
        self.n+=1
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

    async def run(self):
        start_server = websockets.serve(self.server, self.host, self.port)
        asyncio.get_event_loop().run_until_complete(start_server)
        print(f"Server started on {self.host}:{self.port}")
        try:
            asyncio.get_event_loop().run_forever()
        except KeyboardInterrupt:
            print("Server stopped manually")
        finally:
            self.stop_server()


    async def stop_server(self):
        self.is_running = False
        print("Server stopping...")


async def test_move_robot():
    block: MoveRobot = MoveRobot(step=2, direction=MoveRobotDirection.FORWARD)
    (resultType, response) = await block.execute()
    print(f'test_move_robot result:{response}')
    assert resultType == MiniApiResultType.Success, 'test_move_robot timetout'  
    assert response is not None and isinstance(response, MoveRobotResponse), 'test_move_robot result unavailable'
    assert response.isSuccess, 'move_robot failed'



async def main():
    device: WiFiDevice = await test_get_device_by_name()
    server = AsyncServer()
    server.run()


if __name__ == '__main__':
    asyncio.run(main())
