
from mini.apis.api_sound import StartPlayTTS



async def __tts_speak(text: str):
    block: StartPlayTTS = StartPlayTTS(text=text)
    response = await block.execute()
    print(f'tes_play_tts: {response}')


