import asyncio
from mini.apis.api_observe import ObserveSpeechRecognise
from mini.apis.api_sound import StartPlayTTS
from mini.dns.dns_browser import WiFiDevice
from mini.pb2.codemao_speechrecognise_pb2 import SpeechRecogniseResponse
from test_connect import test_connect, shutdown
from test_connect import test_get_device_by_name, test_start_run_program

async def __tts():
    block: StartPlayTTS = StartPlayTTS(text="��֪�������ǵ���С�飬 ������գ��һ���ʮ����Ŷ")
    response = await block.execute()
    print(f'tes_play_tts: {response}')


# ���Լ�������ʶ��
async def test_speech_recognise():
    """��������ʶ��demo

    ��������ʶ���¼����������ϱ�����ʶ��������

    ��ʶ������Ϊ"���"ʱ������"��ã� ������գ� ��������������"

    ��ʶ������Ϊ"����"ʱ��ֹͣ����

    # SpeechRecogniseResponse.text

    # SpeechRecogniseResponse.isSuccess

    # SpeechRecogniseResponse.resultCode

    """
    # ������������
    observe: ObserveSpeechRecognise = ObserveSpeechRecognise()

    # ������
    # SpeechRecogniseResponse.text
    # SpeechRecogniseResponse.isSuccess
    # SpeechRecogniseResponse.resultCode
    def handler(msg: SpeechRecogniseResponse):
        print(f'=======handle speech recognise:{msg}')
        print("{0}".format(str(msg.text)))

        # if str(msg.text)[-1].isalpha() is False:
        #     if str(msg.text)[:-1].lower() == "Hello":
        #         asyncio.create_task(__tts())

        if str(msg.text).lower() == "�����ǵ���С��":
            # ������"���", tts����к�
            asyncio.create_task(__tts())

        elif str(msg.text).lower() == "����":
            # ����������, ֹͣ����
            observe.stop()
            # ����event_loop
            asyncio.get_running_loop().run_in_executor(None, asyncio.get_running_loop().stop)

    observe.set_handler(handler)
    # ����
    observe.start()
    await asyncio.sleep(0)


if __name__ == '__main__':
    device: WiFiDevice = asyncio.get_event_loop().run_until_complete(test_get_device_by_name())
    if device:
        asyncio.get_event_loop().run_until_complete(test_connect(device))
        asyncio.get_event_loop().run_until_complete(test_start_run_program())
        asyncio.get_event_loop().run_until_complete(test_speech_recognise())
        # �������¼���������,������event_loop.run_forver()
        asyncio.get_event_loop().run_forever()
        asyncio.get_event_loop().run_until_complete(shutdown())
