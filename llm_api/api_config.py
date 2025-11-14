import json
import dt_config
from pymsgbox import prompt

API_KEY=dt_config.LLM_API_KEY
API_URL=dt_config.LLM_API_URL

MSG=[]



# 储存上下文信息
def collect_msg(user:json,system:json):
    global MSG
    with open(dt_config.CONTEXT_PATH,"r",encoding="utf-8") as msg:
        MSG=json.loads(msg.read())
    MSG.append(user)
    MSG.append(system)
    with open(dt_config.CONTEXT_PATH,'w',encoding="utf-8") as file:
        json.dump(MSG,file,ensure_ascii=False,indent=2)
        pass

# 返回上下文信息
def rt_msg():
    prompt=""
    with open(dt_config.PROMPT_PATH, "r", encoding="utf-8") as p: #读取二进制文件
        with open(dt_config.CHARACTER_DESIGN_PATH,"r",encoding="utf-8") as c:
            prompt = p.read()+c.read()
    with open(dt_config.CONTEXT_PATH,"r",encoding="utf-8") as msg:
        his_msg=json.loads(msg.read())
        his_msg[0]["content"]=prompt
    return his_msg

# 清理上下文内容
def clear_msg():
    init_msg=[]
    init_msg.append({"role":"system","content":""})
    with open(dt_config.CONTEXT_PATH,"w",encoding="utf-8") as f:
        json.dump(init_msg,f,ensure_ascii=False,indent=2)

def rt_talk_msg():
    with open(dt_config.CONTEXT_PATH,"r",encoding="utf-8") as p:
        MSG = json.loads(p.read())
    return MSG
