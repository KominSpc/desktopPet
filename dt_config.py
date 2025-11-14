# 此文件内存放各种设置和路径
import json
import os
from pygame.pypm import Initialize

TTS_MODEL_PATH="tts_call.bat"
ASR_MODEL_PATH="models/vosk-model-cn-0.22"
# PROMPT_AUDIO_PATH="../../audio_refer/test.wav"
# PROMPT_AUDIO_TEXT="今天是个阳光明媚的日子"
PROMPT_LANGUAGE="zh"
PREDICTION_LANGUAGE="zh"
TEMP_FILE="temp/"
DESKTOP_PATH=os.path.join(os.path.expanduser("~"), "Desktop")

CONTEXT_PATH="llm_api/context.json"
CHARACTER_DESIGN_PATH= "llm_api/character_design.txt"
PROMPT_PATH= "llm_api/prompt.komin"


# live2d相关设置
LIVE2D_FOLDER_PATH = ""
LIVE2D_PARAMETER = ""
LIVE2D_SIZE = ""
LIVE2D_NAME = ""
# llm相关设置
LLM_API_KEY = ""
LLM_API_URL = ""
LLM_VISION_API_KEY = ""
LLM_VISON_API_URL=""
# 基本页面配置
WINDOW_SIZE = "小"
WINDOW_SIZE_WIDTH = 200
WINDOW_SIZE_HEIGHT = 200
OPEN_TTS=True
VOICE_SHORTCUT = "tab"
READ_PAPER_CLIP=True
OPEN_VISION_MODEL=True



class InitSettings:
    def __init__(self):
        with open("settings.json","r",encoding='utf-8') as f:
            self.settings=json.loads(f.read())
            self.refresh()

    def refresh(self):
        global_vars=globals()
        try:
            # Live2D模型设置
            global_vars['LIVE2D_FOLDER_PATH'] = self.settings['live2d_model_settings']['live2d_folder_settings'][
                'folder_path']
            global_vars['LIVE2D_PARAMETER'] = self.settings['live2d_model_settings']['live2d_parameter_settings'][
                'parameter']
            global_vars['LIVE2D_SIZE'] = self.settings['live2d_model_settings']['live2d_parameter_settings']['size']
            global_vars['LIVE2D_NAME'] = self.settings['live2d_model_settings']['live2d_name_settings']['name']

            # LLM模型设置
            global_vars['LLM_API_KEY'] = self.settings['llm_model_settings']['apikey_settings']['api_key']
            global_vars['LLM_API_URL'] = self.settings['llm_model_settings']['apiurl_settings']['api_url']
            global_vars['LLM_VISION_API_KEY'] = self.settings['llm_model_settings']['apikey_vision_settings']['apikey_vision']
            global_vars['LLM_VISON_API_URL'] = self.settings['llm_model_settings']['apiurl_vision_settings']['apiurl_vision']

            # 操作设置
            global_vars['WINDOW_SIZE'] = self.settings['operation_settings']['window_size']
            global_vars['WINDOW_SIZE_WIDTH'] = self.settings['operation_settings']['window_size_width']
            global_vars['WINDOW_SIZE_HEIGHT'] = self.settings['operation_settings']['window_size_height']
            global_vars['OPEN_TTS'] = self.settings['operation_settings']['voice_input_enabled']
            global_vars['VOICE_SHORTCUT'] = self.settings['operation_settings']['voice_shortcut']
            global_vars['READ_PAPER_CLIP'] = self.settings['operation_settings']['clipboard_hint_enabled']
            global_vars['OPEN_VISION_MODEL'] = self.settings['operation_settings']['screen_shot_enabled']
        except Exception as e:
            print(e)

# 根据setting.json载入设置
InitSettings()

if __name__=="__main__":
    settings=InitSettings()
    settings.refresh()
    print(OPEN_TTS)

