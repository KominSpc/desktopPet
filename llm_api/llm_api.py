from openai import OpenAI
import datetime
import llm_api.api_config as api_config
# import api_config
import re
import Center_Controller.center_manager as cm
import Center_Controller.controller as cn
import dt_config
import pyautogui
import pyperclip
from llm_api.llm_vl_api import VisionLLM


class LLMModel:
    def __init__(self):
        self.client = OpenAI(
            api_key=api_config.API_KEY,
            base_url=api_config.API_URL)
        if dt_config.OPEN_VISION_MODEL and (dt_config.LLM_VISION_API_KEY.strip()!="" and dt_config.LLM_VISON_API_URL.strip()!=""):
            self.vision_model=VisionLLM()

    # 请求消息
    def sendMsg(self, msg: str):
        his_msg=api_config.rt_msg()
        user_send_date="---用户发送具体日期:\n"+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_paste_question = "  ---用户询问信息内容:\n"
        user_screenshot_content="---用户询问时的桌面信息:\n"
        user_desktop_app_content="---用户当前桌面快捷方式:\n"+str(cn.get_desktop_app_name())
        if dt_config.READ_PAPER_CLIP: # 读取剪切板内容
            str_=pyperclip.paste()
            user_paste_question=user_paste_question+str_
            print(user_paste_question)
        if dt_config.OPEN_VISION_MODEL and (dt_config.LLM_VISION_API_KEY.strip()!="" and dt_config.LLM_VISON_API_URL.strip()!=""):
            user_screenshot_content=user_screenshot_content+self.vision_model.send_msg()
        messages=[hist for hist in his_msg]
        messages.append({"role": "user", "content": msg+user_send_date
                                                    +user_paste_question
                                                    +user_screenshot_content+user_desktop_app_content
                         })

        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            stream=False,
        )
        result=response.choices[0].message.content
        json_user={
            "role":"user",
            "content": msg+user_send_date
        }
        json_sys = {
            "role": "system",
            "content": result+"---答复具体日期:"+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        prog=match_program(result)
        recall_list=[]
        print(result)
        print(match_program(result))
        recall_list.append(match_emotion(result))
        recall_list.append(match_msg(result))
        recall_list.append(match_program(result))
        print(match_msg(result))
        if prog:
            cm.wecchat_send(prog)
        api_config.collect_msg(json_user, json_sys)
        return recall_list

def match_program(text):
    try:
        return re.findall(r'\$([^$]*)\$', text)[0]
    except Exception as e:
        print(e)
        return None

def match_msg(text):
    try:
        return re.findall(r'\^([^^]*?)(?:\^|$)', text)[0]
    except:
        return None
def match_emotion(text):
    try:
        return re.findall(r'<(.*?)>', text)[0]
    except:
        return None

