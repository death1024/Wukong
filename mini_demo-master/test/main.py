# main.py
from server_module import Server
from robot_control import connect_robot, disconnect_robot, mode_selection_loop
from getNews import getNews
from getWeather import getWeather
import threading
from Queue import Queue

def main():
    command_queue = Queue()
    connect_robot()
    time.sleep(1)
    RobotApi.ubtVoiceTTS(0,getNews())
    time.sleep(1)
    RobotApi.ubtVoiceTTS(0,getWeather())
    server = Server()
    server_thread = threading.Thread(target=server.run)
    server_thread.start()

    mode_selection_thread = threading.Thread(target=mode_selection_loop, args=(command_queue,))
    mode_selection_thread.start()

    try:
        while True:
            command = raw_input("Enter 'exit' to quit: ")
            if command == "exit":
                server.is_running = False
                break
    finally:
        disconnect_robot()
        server_thread.join()
        mode_selection_thread.join()

if __name__ == '__main__':
    main()
