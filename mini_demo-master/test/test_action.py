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


# ����, ִ��һ�������ļ�
async def test_play_action():
    """ִ��һ������demo

    ���ƻ�����ִ��һ��ָ�����Ƶı���(����/�Զ���)���������ȴ�ִ�н���ظￄ1�7

    �������ƿ���GetActionList��ȡ

    #PlayActionResponse.isSuccess : �Ƿ�ɹￄ1�7

    #PlayActionResponse.resultCode : ������

    """
    # action_name: �����ļ���, ����ͨ��GetActionList��ȡ������֧�ֵĶ���
    block: PlayAction = PlayAction(action_name='018')
    # response: PlayActionResponse
    (resultType, response) = await block.execute()

    print(f'test_play_action result:{response}')

    assert resultType == MiniApiResultType.Success, 'test_play_action timetout'
    assert response is not None and isinstance(response, PlayActionResponse), 'test_play_action result unavailable'
    assert response.isSuccess, 'play_action failed'


# ����, ���ƻ�����,��ǰ/��/��/�� �ƶ�
async def test_move_robot():
    """���ƻ������ƶ�demo

    ���ƻ���������(LEFTWARD)�ƶ�10�������ȴ�ִ�н�ￄ1�7

    #MoveRobotResponse.isSuccess : �Ƿ�ɹ��ￄ1�7

    #MoveRobotResponse.code : ������

    """
    # step: �ƶ�����
    # direction: ����,ö������
    block: MoveRobot = MoveRobot(step=8, direction=MoveRobotDirection.FORWARD)
    # response : MoveRobotResponse
    (resultType, response) = await block.execute()

    print(f'test_move_robot result:{response}')

    assert resultType == MiniApiResultType.Success, 'test_move_robot timetout'
    assert response is not None and isinstance(response, MoveRobotResponse), 'test_move_robot result unavailable'
    assert response.isSuccess, 'move_robot failed'


# ����, ��ȡ֧�ֵĶ����ļ��б�
async def test_get_action_list():
    """��ȡ�����б�demo

    ��ȡ���������õĶ����б����ȴ��ظ���ￄ1�7

    """
    # action_type: INNER ��ָ���������õĲ����޸ĵĶ����ļ�, CUSTOM �Ƿ�����sdcard/customize/actionĿ¼�¿ɱ��������޸ĵĶ���
    block: GetActionList = GetActionList(action_type=RobotActionType.INNER)
    # response:GetActionListResponse
    (resultType, response) = await block.execute()

    print(f'test_get_action_list result:{response}')

    assert resultType == MiniApiResultType.Success, 'test_get_action_list timetout'
    assert response is not None and isinstance(response,GetActionListResponse), 'test_get_action_list result unavailable'
    assert response.isSuccess, 'get_action_list failed'


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


if __name__ == '__main__':
    asyncio.run(main())
