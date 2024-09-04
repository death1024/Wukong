#!/usr/bin/env python3

import enum

from mini.apis.base_api import BaseApi, DEFAULT_TIMEOUT
from mini.apis.cmdid import _PCProgramCmdId
from mini.pb2.codemao_controlbehavior_pb2 import ControlBehaviorRequest, ControlBehaviorResponse
from mini.pb2.pccodemao_message_pb2 import Message


@enum.unique
class _RobotBehaviorControlType(enum.Enum):
    """
    表现力控制类型

    START(开始) : 开始舞蹈

    STOP(停止) : 停止舞蹈
    """
    START = 1  # 开始
    STOP = 0  # 停止


class StartBehavior(BaseApi):
    """开始舞蹈api

     控制机器人开始舞蹈

    Args:
        is_serial (bool): 是否等待回复，默认True
        name (str): 表现力名称，不可为空或None

    #ControlBehaviorResponse.isSuccess : 是否成功

    #ControlBehaviorResponse.resultCode : 返回码
    """

    def __init__(self, is_serial: bool = True, name: str = None):
        assert isinstance(name, str) and len(name), 'StartBehavior : name should be available'
        self.__is_serial = is_serial
        self.__name = name
        self.__event_type = _RobotBehaviorControlType.START.value

    async def execute(self):
        """
        执行开始舞蹈指令

        Returns:
            ControlBehaviorResponse
        """
        timeout = 0
        if self.__is_serial:
            timeout = DEFAULT_TIMEOUT

        request = ControlBehaviorRequest()
        request.name = self.__name
        request.eventType = self.__event_type

        cmd_id = _PCProgramCmdId.CONTROL_BEHAVIOR_REQUEST.value

        return await self.send(cmd_id, request, timeout)


    def _parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            ControlBehaviorResponse
        """
        if isinstance(message, Message):
            data = message.bodyData
            response = ControlBehaviorResponse()
            response.ParseFromString(data)
            return response
        else:
            return None



class StopBehavior(BaseApi):
    """停止舞蹈api

     控制机器人停止舞蹈

    Args:
        is_serial (bool): 是否等待回复，默认True

    #ControlBehaviorResponse.isSuccess : 是否成功

    #ControlBehaviorResponse.resultCode : 返回码
    """

    def __init__(self, is_serial: bool = True):
        self.__is_serial = is_serial
        self.__event_type = _RobotBehaviorControlType.START.value

    async def execute(self):
        """
        执行停止舞蹈指令

        Returns:
            ControlBehaviorResponse
        """
        timeout = 0
        if self.__is_serial:
            timeout = DEFAULT_TIMEOUT

        request = ControlBehaviorRequest()
        request.eventType = self.__event_type

        cmd_id = _PCProgramCmdId.CONTROL_BEHAVIOR_REQUEST.value

        return await self.send(cmd_id, request, timeout)


    def _parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            ControlBehaviorResponse
        """
        if isinstance(message, Message):
            data = message.bodyData
            response = ControlBehaviorResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


# class _ControlBehavior(BaseApi):
#     """控制表现力api
#
#      控制机器人开始/停止舞蹈
#
#     Args:
#         is_serial (bool): 是否等待回复，默认True
#         name (str): 表现力名称，不可为空或None
#         control_type (RobotBehaviorControlType): 控制类型，默认START，表示开始执行
#
#     #ControlBehaviorResponse.isSuccess : 是否成功
#
#     #ControlBehaviorResponse.resultCode : 返回码
#     """
#
#     def __init__(self, is_serial: bool = True, name: str = None,
#                  control_type: RobotBehaviorControlType = RobotBehaviorControlType.START):
#         assert name is not None and len(name), 'ControlBehavior name should be available'
#         self.__isSerial = is_serial
#         self.__name = name
#         self.__eventType = control_type.value
#
#     async def execute(self):
#         """
#         执行表现力控制指令
#
#         Returns:
#             ControlBehaviorResponse
#         """
#         timeout = 0
#         if self.__isSerial:
#             timeout = DEFAULT_TIMEOUT
#
#         request = ControlBehaviorRequest()
#         request.name = self.__name
#         request.eventType = self.__eventType
#
#         cmd_id = _PCProgramCmdId.CONTROL_BEHAVIOR_REQUEST.value
#
#         return await self.send(cmd_id, request, timeout)
#
#     def _parse_msg(self, message):
#         """
#
#         Args:
#             message (Message):待解析的Message对象
#
#         Returns:
#             ControlBehaviorResponse
#         """
#         if isinstance(message, Message):
#             data = message.bodyData
#             response = ControlBehaviorResponse()
#             response.ParseFromString(data)
#             return response
#         else:
#             return None