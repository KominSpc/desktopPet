import pyautogui
import time
import subprocess
import pygetwindow as gw
import glob
import os
import pyperclip
import webbrowser
import matplotlib.pyplot as plt
import numpy as np
import re
from typing import List, Dict, Any, Optional, Union
import requests
os.environ['PYPANDOC_PANDOC']=r".venv/Lib/pandocloc/pandoc.exe"
import pypandoc
import dt_config


# 手动开微信（doge）
def send_wechat_message(contact_name, message):
    try:
        open_desktop_app("微信")
        time.sleep(1)  # 等待微信启动

        # 等待微信窗口激活
        wechat_window = None
        max_wait = 10
        for i in range(max_wait):
            try:
                wechat_window = gw.getWindowsWithTitle('微信')[0]
                if wechat_window:
                    wechat_window.activate()
                    break
            except IndexError:
                time.sleep(0.5)

        if not wechat_window:
            print("未能找到微信窗口")
            return False

        _repoint_wechat_window()
        time.sleep(0.2)

        # 使用Ctrl+F搜索联系人
        pyautogui.hotkey('ctrl', 'f')
        time.sleep(0.2)

        # 输入联系人名称
        pyperclip.copy(contact_name)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.2)

        # 按回车选择第一个搜索结果
        pyautogui.press('enter')
        time.sleep(0.2)

        # 输入消息
        pyperclip.copy(message)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.2)

        # 发送消息
        pyautogui.press('enter')

        print(f"消息已发送给 {contact_name}")
        return True

    except Exception as e:
        print(f"发送消息时出错: {e}")
        return False
def _repoint_wechat_window():
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(0.1)

    # 输入联系人名称
    pyperclip.copy("文件传输助手")
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.2)
    pyautogui.press('enter')
# 打开网页
def open_web(url: str):
    webbrowser.open_new_tab(url)
# 读取桌面应用数据
def get_desktop_app_name():
    desktop_path = r"C:\Users\Public\Desktop"
    app_name = glob.glob(os.path.join(desktop_path, "*.lnk"))
    app_list=[]
    for app in app_name:
        app_list.append(os.path.basename(app))
    return app_list
# 打开桌面应用
def open_desktop_app(app_name):
    desktop_path = r"C:\Users\Public\Desktop"
    shortcut_path = os.path.join(desktop_path, f"{app_name}.lnk")

    if os.path.exists(shortcut_path):
        try:
            subprocess.Popen(shortcut_path, shell=True)
            print(f"成功打开: {app_name}")
        except Exception as e:
            print(f"打开应用时出错: {e}")
    else:
        print(f"未找到桌面应用: {app_name}")
# 创建doc文档文件
def create_doc(md_content:str,file_name:str):
    doc_path = dt_config.DESKTOP_PATH
    doc_path = os.path.join(doc_path, f"{file_name}.doc")
    try:
        output = pypandoc.convert_text(md_content, 'docx', format='md', outputfile=doc_path)
        print(f"文档已生成: {doc_path}")
        return True
    except Exception as e:
        print(f"转换失败: {str(e)}")
        return False
# 科研图绘制（因为自己要用所以还是加上吧）
def plot_chart(code:str):
    is_eps: bool=False
    title="组合图"
    try:
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    except:
        print("检查一下你的中文设置哦")
    save_path=dt_config.DESKTOP_PATH
    if is_eps:
        save_path = os.path.join(save_path, f"{title}.eps")
    else:
        save_path = os.path.join(save_path, f"{title}.png")
    compiled_code = compile(code, '<string>', 'exec')
    exec(compiled_code)
    plt.savefig(save_path, dpi=300,bbox_inches='tight')
    plt.close()


# TODO后续功能扩展.....先挖个坑

# if __name__ == "__main__":
#
