from mini.apis import errors
from mini.apis.api_sound import ChangeRobotVolume, ChangeRobotVolumeResponse
from mini.apis.api_sound import FetchAudioList, GetAudioListResponse, AudioSearchType
from mini.apis.api_sound import PlayAudio, PlayAudioResponse, AudioStorageType
# from mini.apis.api_sound import PlayOnlineMusic, MusicResponse
from mini.apis.api_sound import StartPlayTTS, StopPlayTTS, ControlTTSResponse
from mini.apis.api_sound import StopAllAudio, StopAudioResponse
from mini.apis.base_api import MiniApiResultType
from mini.dns.dns_browser import WiFiDevice
from test_connect import test_connect, shutdown
from test_connect import test_get_device_by_name, test_start_run_program
import asyncio



async def test_play_online_audio():
    """娴嬭瘯鎾斁鍦ㄧ嚎闊虫晥

    浣挎満鍣ㄤ汉鎾斁涓€娈靛湪绾块煶鏁堬紝渚嬪"http://hao.haolingsheng.com/ring/000/995/52513bb6a4546b8822c89034afb8bacb.mp3"

    鏀寔鏍煎紡鏈塵p3,amr,wav 绛�

    骞剁瓑寰呯粨鏋�

    #PlayAudioResponse.isSuccess : 鏄惁鎴愬姛

    #PlayAudioResponse.resultCode : 杩斿洖鐮�

    """
    # 鎾斁闊虫晥, url琛ㄧず瑕佹挱鏀剧殑闊虫晥鍒楄〃
    block: PlayAudio = PlayAudio(
        url="http://music.163.com/song/media/outer/url?id=2051335753.mp3",
        storage_type=AudioStorageType.NET_PUBLIC)
    # response鏄釜PlayAudioResponse
    (resultType, response) = await block.execute()

    print(f'test_play_online_audio result: {response}')
    print('resultCode = {0}, error = {1}'.format(response.resultCode, errors.get_speech_error_str(response.resultCode)))

    assert resultType == MiniApiResultType.Success, 'test_play_online_audio timetout'
    assert response is not None and isinstance(response, PlayAudioResponse), 'test_play_online_audio result unavailable'
    assert response.isSuccess, 'test_play_online_audio failed'



if __name__ == "__main__":
    device: WiFiDevice = asyncio.get_event_loop().run_until_complete(test_get_device_by_name())
    if device:
        asyncio.get_event_loop().run_until_complete(test_connect(device))
        asyncio.get_event_loop().run_until_complete(test_start_run_program())
        asyncio.get_event_loop().run_until_complete(test_play_online_audio())