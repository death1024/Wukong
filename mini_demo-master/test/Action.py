#!/usr/bin/env python3
import enum

from mini.apis.base_api import BaseApi, DEFAULT_TIMEOUT
from mini.apis.cmdid import _PCProgramCmdId
from mini.pb2.codemao_getactionlist_pb2 import GetActionListRequest, GetActionListResponse
from mini.pb2.codemao_moverobot_pb2 import MoveRobotRequest, MoveRobotResponse
from mini.pb2.codemao_playaction_pb2 import PlayActionRequest, PlayActionResponse
from mini.pb2.codemao_playcustomaction_pb2 import PlayCustomActionRequest, PlayCustomActionResponse
from mini.pb2.codemao_stopaction_pb2 import StopActionRequest, StopActionResponse
from mini.pb2.codemao_stopcustomaction_pb2 import StopCustomActionRequest, StopCustomActionResponse
from mini.pb2.pccodemao_message_pb2 import Message

class PlayAction(BaseApi):
    """执行内置动作api

    机器人执行一个指定名称的内置动作
    动作名称可用GetActionList获取

    Args:
        is_serial (bool): 是否等待回复，默认True
        action_name (str): 动作名称，不能为none或空字符串

    #PlayActionResponse.isSuccess : 是否成功

    #PlayActionResponse.resultCode : 返回码

    """

    def __init__(self, is_serial: bool = True, action_name: str = None):
        """执行动作api初始化
        """
        assert isinstance(action_name, str) and action_name is not None and len(
            action_name), 'PlayAction actionName should be available'
        self.__is_serial = is_serial
        self.__action_name = action_name
    async def execute(self):
        """发送执行动作指令

        Returns:
            PlayActionResponse
        """
        timeout = 0
        if self.__is_serial:
            timeout = DEFAULT_TIMEOUT
        request = PlayActionRequest()
        request.actionName = self.__action_name

        cmd_id = _PCProgramCmdId.PLAY_ACTION_REQUEST.value
        return await self.send(cmd_id, request, timeout)


    def _parse_msg(self, message):
        """解析回复指令

        Args:
            message (Message):待解析的Message对象

        Returns:
            PlayActionResponse
        """
        if isinstance(message, Message):
            data = message.bodyData
            response = PlayActionResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class StopAllAction(BaseApi):
    """停止所有动作api

    停止所有正在执行的动作, 停止指定的自定义动作, 如果动作是一个不可打断的动作, StopCustomActionResponse.resultCode = 403

    Args
        is_serial (bool): 是否等待回复，默认True

    """

    def __init__(self, is_serial: bool = True):
        self.__is_serial = is_serial
    async def execute(self):
        """
        发送停止所有动作指令

        Returns:
            StopActionResponse
        """
        timeout = 0
        if self.__is_serial:
            timeout = DEFAULT_TIMEOUT

        request = StopActionRequest()

        cmd_id = _PCProgramCmdId.STOP_ACTION_REQUEST.value
        return await self.send(cmd_id, request, timeout)


    def _parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            StopActionResponse

            #StopCustomActionResponse.isSuccess : 是否成功

            #StopCustomActionResponse.resultCode : 返回码

        """
        if isinstance(message, Message):
            data = message.bodyData
            response = StopActionResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


@enum.unique
class MoveRobotDirection(enum.Enum):
    """机器人移动方向

    FORWARD :  向前

    BACKWARD : 向后

    LEFTWARD : 向左

    RIGHTWARD : 向右
    """
    FORWARD = 3  # 向前
    BACKWARD = 4  # 向后
    LEFTWARD = 1  # 向左
    RIGHTWARD = 2  # 向右


class MoveRobot(BaseApi):
    """控制机器人移动api

    控制机器人往某个方向(MoveRobotDirection)移动n步

    Args:
        is_serial (bool): 是否等待回复，默认True
        direction (MoveRobotDirection): 机器人移动方向，默认FORWARD，向前移动
        step (int): 步数，默认1步

    #MoveRobotResponse.isSuccess : 是否成功　

    #MoveRobotResponse.code : 返回码

    """

    def __init__(self, is_serial: bool = True, direction: MoveRobotDirection = MoveRobotDirection.FORWARD,
                 step: int = 1):
        assert isinstance(direction, MoveRobotDirection), 'MoveRobot : direction should be MoveRobotDirection instance'
        assert isinstance(step, int) and step > 0, 'MoveRobot : step should be Positive'
        self.__is_serial = is_serial
        self.__direction = direction.value
        self.__step = step
    async def execute(self):
        """发送机器人移动指令

        Returns:
            MoveRobotResponse
        """
        timeout = 0
        if self.__is_serial:
            timeout = DEFAULT_TIMEOUT

        request = MoveRobotRequest()
        request.direction = self.__direction
        request.step = self.__step

        cmd_id = _PCProgramCmdId.MOVE_ROBOT_REQUEST.value
        return await self.send(cmd_id, request, timeout)


    def _parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            MoveRobotResponse
        """
        if isinstance(message, Message):
            data = message.bodyData
            response = MoveRobotResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


@enum.unique
class RobotActionType(enum.Enum):
    """
    机器人动作类型

    INNER(内置)：机器人内置的不可修改的动作文件

    CUSTOM(自定义): 放置在sdcard/customize/actions目录下可被开发者修改的动作文件

    """
    INNER = 0  # 内置
    CUSTOM = 1  # 自定义


class GetActionList(BaseApi):
    """获取机器人动作列表api

    获取存储在机器人本地(内置/自定义)的动作文件列表

    Args:
        is_serial (bool): 是否等待回复，默认True
        action_type (RobotActionType): 动作类型，默认为INNER，内置动作

    #GetActionListResponse.actionList ([str]) : 动作列表，str数组

    #GetActionListResponse.isSuccess : 是否成功

    #GetActionListResponse.resultCode : 返回码

    """

    def __init__(self, is_serial: bool = True, action_type: RobotActionType = RobotActionType.INNER):
        assert isinstance(action_type, RobotActionType), 'GetActionList : action_type should be RobotActionType ' \
                                                         'instance '
        self.__is_serial = is_serial
        self.__action_type = action_type.value
    async def execute(self):
        """发送获取机器人动作列表指令

        Returns:
            GetActionListResponse
        """
        timeout = 0
        if self.__is_serial:
            timeout = DEFAULT_TIMEOUT

        request = GetActionListRequest()
        request.actionType = self.__action_type

        cmd_id = _PCProgramCmdId.GET_ACTION_LIST.value

        return await self.send(cmd_id, request, timeout)


    def _parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            GetActionListResponse
        """
        if isinstance(message, Message):
            data = message.bodyData
            response = GetActionListResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class PlayCustomAction(BaseApi):
    """执行自定义动作api

    让机器人执行一个指定名称的自定义动作
    动作名称可用GetActionList获取

    Args:
        is_serial (bool): 是否等待回复，默认True
        action_name (str): 自定义动作名称，不可为空或者None

    #PlayCustomActionResponse.isSuccess : 是否成功

    #PlayCustomActionResponse.resultCode : 返回码
    """

    def __init__(self, is_serial: bool = True, action_name: str = None):

        assert isinstance(action_name, str) and len(action_name) > 0, 'PlayCustomAction : actionName should be ' \
                                                                      'available '
        self.__is_serial = is_serial
        self.__action_name = action_name
    async def execute(self):
        """发送执行自定义动作指令

        Returns:
            PlayCustomActionResponse
        """
        timeout = 0
        if self.__is_serial:
            timeout = DEFAULT_TIMEOUT

        request = PlayCustomActionRequest()
        request.actionName = self.__action_name

        cmd_id = _PCProgramCmdId.PLAY_CUSTOM_ACTION_REQUEST.value
        return await self.send(cmd_id, request, timeout)


    def _parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            PlayCustomActionResponse
        """

        if isinstance(message, Message):
            data = message.bodyData
            response = PlayCustomActionResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class StopCustomAction(BaseApi):
    """停止自定义动作api

    停止指定的自定义动作, 如果动作是一个不可打断的动作, StopCustomActionResponse.resultCode = 403

    Args:
        is_serial (bool): 是否等待回复，默认True
        action_name (str): 自定义动作名称，不可为空或None

    #StopCustomActionResponse.isSuccess : 是否成功

    #StopCustomActionResponse.resultCode : 返回码

    """

    def __init__(self, is_serial: bool = True, action_name: str = None):
        assert isinstance(action_name, str) and len(action_name) > 0, 'StopCustomAction actionName should be available'
        self.__is_serial = is_serial
        self.__action_name = action_name
    async def execute(self):
        """执行停止自定义动作指令

        Returns:
            StopCustomActionResponse
        """
        timeout = 0
        if self.__is_serial:
            timeout = DEFAULT_TIMEOUT

        request = StopCustomActionRequest()
        request.actionName = self.__action_name

        cmd_id = _PCProgramCmdId.STOP_CUSTOM_ACTION_REQUEST.value
        return await self.send(cmd_id, request, timeout)


    def _parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            StopCustomActionResponse
        """

        if isinstance(message, Message):
            data = message.bodyData
            response = StopCustomActionResponse()
            response.ParseFromString(data)
            return response
        else:
            return None