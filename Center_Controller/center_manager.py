from . import controller
import io
import os
import subprocess
import requests
import dt_config
import tempfile
from pydub import AudioSegment
from pydub.playback import play
import pyttsx3

def wecchat_send(program:str):
    judge=eval(program)
    if(judge):
        return "执行完成"
    else:
        return "执行失败"

# 以下为tts本地部署的版本，由于体积过大不满足参赛要求所以改用小模型
# def init_tts():
#     subprocess.run("tts_stop.bat")
#     try:
#         path=dt_config.TTS_MODEL_PATH
#         path=os.path.abspath(path) # 项目总目录
#         code=subprocess.Popen(
#             [path],
#             cwd=os.path.dirname(path),
#         )
#         print(code)
#     except:
#         print("未找到模型启动路径")
#         pass
#
# def tts_audio_play(text:str,refer_wav_path:str,prompt_text:str,prompt_language:str,text_language:str):
#     """
#     发送并播放语音（默认参数）
#     :param text:需要进行TTS处理的文本
#     :param refer_wav_path:参考语音
#     :param prompt_text:参考语音文本
#     :param prompt_language:参考语音文本的语种
#     :param text_language:TTS处理后语音的语种
#     :return:
#     """
#     if (text,refer_wav_path,prompt_text,prompt_language,text_language) is not None:
#         data={
#             "refer_wav_path": refer_wav_path,
#             "prompt_text": prompt_text,
#             "prompt_language":prompt_language,
#             "text": text,
#             "text_language": text_language,
#             "top_k": 4,
#             "top_p": 0.6,
#             "temperature": 1,
#             "speed": 1
#         }
#
#     else:
#         print("关键参数不全")
#         return None
#     print(data)
#     res=requests.post("http://localhost:9880",json=data)
#     temp_path=dt_config.TEMP_FILE
#     if res.status_code==200:
#         audio_data = io.BytesIO(res.content)
#         audio = AudioSegment.from_file(audio_data, format="wav")
#         return audio
#     else:
#         print("返回数据异常")
#     return None
#
# def tts_audio_play_high(text:str,refer_wav_path:str,prompt_text:str,prompt_language:str,text_language:str,
#                    top_k:int,top_p:float,temperature:float,speed:int):
#     """
#     发送并播放语音（高级参数）
#     :param speed: 语速
#     :param temperature: 感情温度
#     :param top_k: k值
#     :param top_p: p值
#     :param text:需要进行TTS处理的文本
#     :param refer_wav_path:参考语音
#     :param prompt_text:参考语音文本
#     :param prompt_language:参考语音文本的语种
#     :param text_language:TTS处理后语音的语种
#     :return:
#     """
#     if (text,refer_wav_path,prompt_text,prompt_language,text_language) is not None:
#         data={
#             "refer_wav_path": refer_wav_path,
#             "prompt_text": prompt_text,
#             "prompt_language":prompt_language,
#             "text": text,
#             "text_language": text_language,
#             "top_k": top_k,
#             "top_p": top_p,
#             "temperature": temperature,
#             "speed": speed
#         }
#         print(data)
#     else:
#         print("关键参数不全")
#         return None
#     return requests.post("http://localhost:9880",data=data)

def mini_tts_audio_init():
    engine = pyttsx3.init()

    engine.say("我谢谢你")
    engine.runAndWait()
    return engine

if __name__ == '__main__':
    mini_tts_audio_init()
