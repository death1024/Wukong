from mini.pb2.codemao_speechrecognise_pb2 import SpeechRecogniseResponse
from global_data import flag
import ttsmodel
import asyncio
from mini.apis.api_action import MoveRobot, MoveRobotDirection, MoveRobotResponse
from mini.apis.api_action import PlayAction, PlayActionResponse
from dance import StartBehavior
from mini.apis import errors
from mini.apis.api_behavior import StartBehavior, ControlBehaviorResponse, StopBehavior
from mini.apis.api_expression import ControlMouthLamp, ControlMouthResponse
from mini.apis.api_expression import PlayExpression, PlayExpressionResponse
from mini.apis.api_expression import SetMouthLamp, SetMouthLampResponse, MouthLampColor, MouthLampMode
from Action import PlayAction
import random
from mini.apis.api_action import MoveRobot, MoveRobotDirection


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
            await ttsmodel.__tts_speak("请跟我走路吧")

            # 创建旋转移动对象
            rotate_block = MoveRobot(step=3, direction=MoveRobotDirection.RIGHTWARD)
            success = await rotate_block.execute()
            if success:
                print("Robot rotated 90 degrees.")
            else:
                print("Failed to rotate robot.")
        await asyncio.sleep(1)  # 等待1秒，模拟实际运行中的延迟







async def pressuremodel(pressuredata,flag):

    m=random.randint(1, 5)
    if flag==1 and m==1 and pressuredata>=30:
        await ttsmodel.__tts_speak("您现在很难过，让我给你跳个舞蹈吧")
        #走路
        block: MoveRobot = MoveRobot(step=8, direction=MoveRobotDirection.FORWARD)
        await block.execute()
        #跳舞
        block: StartBehavior = StartBehavior(name="dance_0004")
        # response ControlBehaviorResponse
        await block.execute()
        await ttsmodel.__tts_speak("舞蹈结束")
        return 0
        
    if flag==1 and m==2 and pressuredata>=30:
        await ttsmodel.__tts_speak("拍拍，看样子小主人不太高兴呀，抱抱你")
        #走路random_short2
        block = PlayAction(action_name="random_short2")
        await block.execute()
        #跳舞
        await ttsmodel.__tts_speak("我来给你跳个舞")
        block: StartBehavior = StartBehavior(name="dance_0008")
        # response ControlBehaviorResponse
        await block.execute()
        return 0

    if flag==1 and m==3 and pressuredata>=30:
        await ttsmodel.__tts_speak("高兴点儿")
        block: PlayExpression = PlayExpression(express_name="codemao19")
        await block.execute()
        await ttsmodel.__tts_speak("我来给你讲个笑话吧")
        await ttsmodel.__tts_speak("为什么所有的警察都喜欢玩扑克？因为他们在逮捕坏人的时候，总是会说：“摊牌时间到了！")
        await ttsmodel.__tts_speak("哈哈哈")
        # response ControlBehaviorResponse
        return 0
    
    if flag==1 and m==4 and pressuredata>=30:
        await ttsmodel.__tts_speak("别沮丧啊小主人，看我给你表演个才艺")
        block: PlayExpression = PlayExpression(express_name="codemao16")
        await block.execute()
        #金鸡独立
        block: PlayAction = PlayAction(action_name="016")
        await block.execute()
        return 0

        
    if flag==1 and m==5 and pressuredata>=30:
        await ttsmodel.__tts_speak("拉里拉，我感觉你的压力有点大，现在是悟空表演时间")
        block: PlayExpression = PlayExpression(express_name="emo_027")
        await block.execute()
        #金鸡独立
        block: StartBehavior = StartBehavior(name="dance_0003")
        await block.execute()
        return 0
    return 1





async def attentionmodel(attentiondata,flag):
    m=random.randint(1, 2)
    if  flag==1 and attentiondata>=60 and m==1:
        await ttsmodel.__tts_speak("你好专注啊，我们来学习会吧，跟我念")
        # 重新初始化 PlayAction 和 PlayExpression 对象
        block1 = PlayAction(action_name="action_014")
        block2 = PlayExpression(express_name="codemao11")
        
        await asyncio.gather(
            block1.execute(),
            block2.execute(),
            ttsmodel.__tts_speak("爸 爸的爸 爸叫什么？ 爸爸的爸爸叫爷爷。爸爸的妈妈叫什么？")
        )
        await ttsmodel.__tts_speak("怎么样。你学会了吗？")
        return 0
    

    if  flag==1 and attentiondata>=60 and m==2:
        await ttsmodel.__tts_speak("你好专注啊，我们来学学英语吧")
        #瑜伽
        block1 = PlayAction(action_name="024")
        #斗志
        block2 = PlayExpression(express_name="codemao11")
        
        await asyncio.gather(
            block1.execute(),
            block2.execute(),
            ttsmodel.__tts_speak("Apple 苹果；banana 香蕉；pear 梨；watermelon 西瓜；grape 葡萄；peach 桃子；orange 橘子")
        )
        await ttsmodel.__tts_speak("怎么样，你学会了吗？")
        return 0
    

    if  flag==1 and attentiondata<60:
        await ttsmodel.__tts_speak("打起精神来")
        #斗志
        #只因你太美 baby 只因你太美 baby
        block = PlayExpression(express_name="codemao16")
        await block.execute()

        await ttsmodel.__tts_speak("只因你太美，baby 只因你太美 baby，只因你实在是太美 baby ，只因你太美 baby，迎面走来的你让我如此蠢蠢欲动，这种感觉我从未有，Cause I got a crush on you who you，你是我的我是你的谁，再多一眼看一眼就会爆炸，再近一点靠近点快被融化")
        await ttsmodel.__tts_speak("怎么样，有精神了吗")
        return 0
    
    return 1




async def hrmodel(hrdata):
    m=random.randint(1, 2)
    if m==1:
        if hrdata>=95:
            await ttsmodel.__tts_speak("你运动累了吧，换我试试")
            # 俯卧撑
            block1: PlayAction = PlayAction(action_name="012")
            await block1.execute()
            #眨眼并说话
            block2: PlayExpression = PlayExpression(express_name="codemao10")
            await asyncio.gather(block2.execute(),ttsmodel.__tts_speak("我做了几个俯卧撑，厉害吧"))
            block3: PlayAction = PlayAction(action_name="009")
            await block3.execute()
        if hrdata<=80:
            await ttsmodel.__tts_speak("和我来活动一下吧")
            await test_move_and_tts()

    if m==2:
        if hrdata>=95:
            await ttsmodel.__tts_speak("休息，休息一下")
            #太极
            block: StartBehavior = StartBehavior(name="014")
            await block.execute()

        if hrdata<=80:
            #深蹲
            await ttsmodel.__tts_speak("和我来活动一下吧")
            for _ in range(0 ,5):
                block: PlayAction = PlayAction(action_name="031")
                await block.execute()
                block: PlayAction = PlayAction(action_name="009")
                await block.execute()





async def check_coherence_model (coherencedata):
    if coherencedata >= 60:
        await ttsmodel.__tts_speak("你冥想的效果很好")
        await ttsmodel.__tts_speak("现在轻轻地动动你的手指和脚趾，慢慢地在你的脚踝和手腕上打转。当你准备好时，可以开始轻轻地伸展你的身体。")
        return 0
    return 1
    
