from vosk import Model, KaldiRecognizer
import pyaudio
import json
import dt_config

def asr_init():
    audio_model = Model(dt_config.ASR_MODEL_PATH)
    # 接收麦克风
    microphone_obj = pyaudio.PyAudio()
    # 接收语音
    microphone_input = microphone_obj.open(
        format=pyaudio.paInt16,
        # 声道
        channels=1,
        # 采样率
        rate=16000,
        # 获取数据方法
        input=True,
        # 每次读取数据块大小
        frames_per_buffer=4000
    )
    # 语音识别器
    recognizer = KaldiRecognizer(audio_model, 16000) # 前置项的初始化比较花时间，后续将下半部分改为按键录音
    return recognizer,microphone_input

def asr_vosk(recognizer:KaldiRecognizer,microphone_input:pyaudio):
    rt_msg=""
    print("开始识别")
    while True:
        data = microphone_input.read(4096)
        if recognizer.AcceptWaveform(data):
            json_result = recognizer.Result()
            result = json.loads(json_result)['text'].replace(" ", '')
            rt_msg = result
            return rt_msg # 直接进行llm发送

def main():
    print(asr_vosk())

if __name__ == '__main__':
    main()
