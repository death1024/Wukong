import asyncio
import websockets
import json
import sqlite3

def setup_database():
    conn = sqlite3.connect('app_data.db')
    c = conn.cursor()
    # 创建只有一个条目的表，每个标签仅存储最新值
    c.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            label TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    conn.commit()
    conn.close()

class Server:
    def __init__(self, host='0.0.0.0', port=65432):
        self.host = host
        self.port = port
        self.is_running = True
        setup_database()  # 初始化数据库

    async def run(self):
        async with websockets.serve(self.handle_client, self.host, self.port):
            print(f"Server started on {self.host}:{self.port}")
            await asyncio.Future()  # 运行直到被取消

    async def handle_client(self, websocket, path):
        try:
            while self.is_running:
                message = await websocket.recv()
                if message:
                    await self.process_message(message)
        except websockets.exceptions.ConnectionClosed:
            print("Client has disconnected")
        except Exception as e:
            print(f"Error handling a client: {e}")

    async def process_message(self, message):
        try:
            label, json_data = message.split(':', 1)
            data_dict = json.loads(json_data)
            await self.update_data(label, data_dict)
        except Exception as e:
            print(f"Error processing message: {e}")

    async def update_data(self, label, data_dict):
        value = data_dict.get('value', 'unknown')
        conn = sqlite3.connect('app_data.db')
        c = conn.cursor()
        # 更新或插入数据，确保每个标签只有一个条目
        c.execute('REPLACE INTO sensor_data (label, value) VALUES (?, ?)', (label, value))
        conn.commit()
        conn.close()
        print(f"Updated {label}: {value}")

if __name__ == "__main__":
    server = Server()
    asyncio.run(server.run())



