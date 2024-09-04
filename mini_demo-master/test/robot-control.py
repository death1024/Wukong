# robot_control.py
import RobotApi
import time
from chatEach import chatEach
from global_data import data
from threading import Thread
from Queue import Queue, Empty

def connect_robot():
    RobotApi.ubtRobotInitialize()
    ret = RobotApi.ubtRobotConnect("SDK", "1", "127.0.0.1")
    if ret != 0:
        print "Cannot connect to robot SDK"
        exit(1)

def disconnect_robot():
    RobotApi.ubtStartRobotAction("reset", 1)
    RobotApi.ubtRobotDisconnect("SDK", "1", "127.0.0.1")
    RobotApi.ubtRobotDeinitialize()

def mode_selection_loop(command_queue):
    while True:
        try:
            command = command_queue.get(timeout=10)  # Check every 10 seconds if there's a command
            if command == "focus":
                focus_mode()
            elif command == "fun":
                fun_mode()
        except Empty:
            RobotApi.ubtVoiceTTS(0, "请选择模式")
            if RobotApi.ubtDetectVoiceMsg("进入模式选择", 20) == 0:
                mode_select(command_queue)

def mode_select(command_queue):
    RobotApi.ubtVoiceTTS(0, "模式选择：1. 专注模式 2. 对话模式 3. 退出模式选择")
    if RobotApi.ubtDetectVoiceMsg("进入专注模式", 20) == 0:
        command_queue.put("focus")
    elif RobotApi.ubtDetectVoiceMsg("进入对话模式", 20) == 0:
        command_queue.put("fun")

def focus_mode():
    attention_level = float(data['attention'])
    RobotApi.ubtVoiceTTS(0, "专注模式启动")
    if attention_level < 40:
        RobotApi.ubtSetRobotLED("button", "red", "blink")
        RobotApi.ubtVoiceTTS(0, "前面需要打起精神")
        time.sleep(3)
    elif attention_level > 60:
        RobotApi.ubtVoiceTTS(0, "你很专注")
        time.sleep(3)

def fun_mode():
    RobotApi.ubtVoiceTTS(0, "开始交流吧")
    time.sleep(1)
    response = chatEach("who are you")
    RobotApi.ubtVoiceTTS(0, response)
