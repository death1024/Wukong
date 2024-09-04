import asyncio
from mini import mini_sdk as MiniSdk
from mini.apis.api_action import MoveRobot, MoveRobotDirection
from mini.dns.dns_browser import WiFiDevice
from test_connect import test_get_device_by_name


async def test_move_and_tts():
    """控制机器人行走并定时播报文本的demo"""
    steps_taken = 0  # 记录步数

    # 循环执行移动和播报文本
    while True:
        # 创建移动对象
        move_block = MoveRobot(step=10, direction=MoveRobotDirection.FORWARD)
        # 执行移动指令
        success = await move_block.execute()
        if success:
            print("Robot moved 10 steps forward.")
        else:
            print("Failed to move robot.")

        steps_taken += 10  # 增加步数

        # 定时播报文本
        if steps_taken % 10 == 0:
            await tts_action()

            # 创建旋转移动对象
            rotate_block = MoveRobot(step=3, direction=MoveRobotDirection.RIGHTWARD)
            success = await rotate_block.execute()
            if success:
                print("Robot rotated 90 degrees.")
            else:
                print("Failed to rotate robot.")

        await asyncio.sleep(1)  # 等待1秒，模拟实际运行中的延迟


async def tts_action():
    """定时播报文本"""
    from mini.apis.api_sound import StartPlayTTS
    result = await StartPlayTTS(text="请跟着我走路吧").execute()
    print(f"TTS播报完成: {result}")

if __name__ == '__main__':
    asyncio.run(test_move_and_tts())