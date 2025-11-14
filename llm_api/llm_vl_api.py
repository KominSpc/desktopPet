import openai
import dt_config
import base64
import os
from PIL import ImageGrab

class VisionLLM:
    def __init__(self):
        self.model=openai.OpenAI(
            api_key=dt_config.LLM_VISION_API_KEY,
            base_url=dt_config.LLM_VISON_API_URL
        )
    def send_msg(self):
        self.__screenShot()
        img_base64=self.__screenShot()
        prompt=""
        with open("llm_api/vision_prompt.komin","r",encoding="utf-8") as c:
            prompt = c.read()
        res=self.model.chat.completions.create(
            model="qwen-vl-plus",
            messages=[
                {"role":"user",
                 "content":[
                     {"type":"image_url",
                      "image_url":f"data:image/png;base64,{img_base64}"
                      },
                     {"type":"text","text":prompt}
                 ],
                }
            ]
        )
        return res.choices[0].message.content

    def __screenShot(self):
        temp_path:str="temp/region_screenshot.png"
        # bbox = (100, 100, 500, 500)
        #region_screenshot = ImageGrab.grab(bbox=bbox) # 要限制截屏区域修改此处代码就ok了
        region_screenshot = ImageGrab.grab()
        region_screenshot.save(temp_path)
        with open(temp_path, "rb") as img:
            pic_base64 = base64.b64encode(img.read())
        os.remove(temp_path)
        return pic_base64.decode("utf-8")


if __name__ == "__main__":
    img = VisionLLM()
    print(img.send_msg().replace("\n",""))
