# 程序-架构-制作:komin
## Bug反馈：https://github.com/KominSpc/desktopPet

import os
import sys
import tempfile
import time

import pyperclip
import pyttsx3
from PyQt5.QtWidgets import QApplication, QWidget, QMenu, QHBoxLayout, QMessageBox, QMainWindow
from PyQt5.QtCore import Qt, QPoint, pyqtSignal, QThread, pyqtSlot
from PyQt5.QtGui import QCursor
from pydub import AudioSegment
from pyttsx3 import Engine
from qfluentwidgets import RoundMenu, Action, MenuAnimationType, FluentIcon

import keyboard

import dt_config
# from set_live2d.qt_main_panel import Window # 全是bug!不要用！！！
from set_live2d.qt_setting_config.qt_main_panel_qt5 import SettingsWindow
from set_live2d.chat_window import ChatWindow
from llm_api.llm_api import LLMModel
from set_live2d.qt_pet_set import Pet
import llm_api.api_config as api_config
import dt_asr.asr as asr


os.environ['QT_QPA_PLATFORM_PLUGIN_PATH']=r".venv/Lib/site-packages/PyQt5/Qt5/plugins/platforms"
class DesktopPet(QWidget):
    settings_clicked = pyqtSignal()
    info_clicked = pyqtSignal()
    exit_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.chat_window = ChatWindow()
        self.pet=Pet()

        # 鼠标拖动相关变量
        self.is_dragging = False
        self.drag_position = QPoint()
        self.llm_model = LLMModel() #单纯对话框处理
        self.rb_controller=SettingsWindow() # 初始化右键菜单
        # 初始化UI
        self.init_ui()
        # 允许复制时启动时清空剪切板
        if dt_config.READ_PAPER_CLIP:
            pyperclip.copy("")
        try:
            # 初始化声音线程
            self.tts_model_thread=TTSThread()
            self.talk_thread=CommunicateWithLLMThread()
            self.tts_model_thread.start()
            self.talk_thread.start()
            self.talk_thread.callback.connect(self.__onTalkThread)
            self.talk_thread.callback_recognized.connect(self.__onRecognized)
            self.tts_model_thread.callback.connect(self.__get_tts_model)

            # 线程异常捕获
            self.talk_thread.callback_error.connect(self.__showErrorMsg)
        except Exception as e:
            print(e)

    def init_ui(self):
        self.setFixedSize(dt_config.WINDOW_SIZE_WIDTH, dt_config.WINDOW_SIZE_HEIGHT)

        # 创建布局
        layout = QHBoxLayout(self)
        layout.addWidget(self.pet)
        layout.setContentsMargins(0, 0, 0, 0)

    def contextMenuEvent(self, event):
        menu = RoundMenu(parent=self)
        # 创建菜单项
        settings_action = Action(FluentIcon.SETTING, '控制面板')
        info_action = Action(FluentIcon.INFO, '详细信息')
        chat_action = Action(FluentIcon.CHAT, '聊天窗口')
        exit_action = Action(FluentIcon.CLOSE, '退出')


        # 连接信号
        settings_action.triggered.connect(self.on_settings_clicked)
        info_action.triggered.connect(self.on_info_clicked)
        chat_action.triggered.connect(self.on_chat_clicked)
        exit_action.triggered.connect(self.on_exit_clicked)

        # 添加菜单项
        menu.addAction(settings_action)
        menu.addAction(info_action)
        menu.addAction(chat_action)
        menu.addSeparator()
        menu.addAction(exit_action)

        # 显示菜单
        menu.exec_(QCursor.pos(),True,MenuAnimationType.FADE_IN_PULL_UP)

    def on_settings_clicked(self):
        print("设置菜单被点击")
        self.rb_controller.load_settings()
        self.rb_controller.show()

    def on_info_clicked(self):
        self.info_clicked.emit()
        print("详细信息菜单被点击")
        self.__showMessageBox()


    def on_chat_clicked(self):
        print("聊天窗口被点击")
        self.chat_window.show()

    def on_exit_clicked(self):
        self.exit_clicked.emit()
        print("退出菜单被点击")
        self.tts_model.stop()
        app.quit()
        sys.exit(0)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_dragging = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
            self.setCursor(Qt.ClosedHandCursor)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.is_dragging:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_dragging = False
            self.setCursor(Qt.ArrowCursor)
            event.accept()

    def __onRecognized(self,msg:str):
        self.chat_window.add_message(msg,True)
        self.chat_window.ban_send() # 录音时禁用窗口发送

    @pyqtSlot(str)
    def __onTalkThread(self,msg:str):
        self.chat_window.add_message(msg,False)
        if dt_config.OPEN_TTS:
            self.pet.start_audio_processing(msg,self.tts_model)
        self.pet.showTeachingTip(dt_config.LIVE2D_NAME,msg)
        self.chat_window.activate_send()  # 输入结束后启用

    def __audio_segment_to_temp_wav(self,audio_segment):
        # 创建临时文件
        temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        temp_path = temp_file.name
        temp_file.close()
        # 导出为WAV文件
        audio_segment.export(temp_path, format='wav')
        return temp_path

    @pyqtSlot(Engine)
    def __get_tts_model(self,engine:Engine):
        self.tts_model=engine
        self.tts_model.runAndWait()

    def __showErrorMsg(self,error:str):
        QMessageBox.critical(self,"出错啦",error)

    def __showMessageBox(self):
        QMessageBox.information(self, "这是一个天才提示框", "当前版本为beta0.0.2，Bug反馈请在本人的github项目上进行反馈：https://github.com/KominSpc/desktopPet！")


# 创建发送和语音识别线程
class CommunicateWithLLMThread(QThread):
    callback = pyqtSignal(str)
    callback_recognized = pyqtSignal(str)
    callback_error = pyqtSignal(str)

    def __init__(self):
        super(CommunicateWithLLMThread, self).__init__()
        self.recognizer, self.microphone_input = asr.asr_init()
        self.model = LLMModel()
        self._is_running = True  # 添加运行控制标志
        api_config.clear_msg()

    def run(self):
        while self._is_running:
            try:
                time.sleep(0.05)  # 50ms的间隔

                if keyboard.is_pressed(dt_config.VOICE_SHORTCUT):
                    # 添加去抖动，防止重复触发
                    time.sleep(0.2)

                    try:
                        recognize_text = asr.asr_vosk(self.recognizer, self.microphone_input)
                    except Exception as e:
                        self.callback_error.emit(f"ASR模型错误: {str(e)}")
                        continue

                    self.callback_recognized.emit(recognize_text)

                    try:
                        call_back_msg = self.model.sendMsg(recognize_text)
                    except Exception as e:
                        self.callback_error.emit(f"LLM API错误: {str(e)}")
                        continue

                    recall_msg = call_back_msg[1]
                    if recall_msg is None:
                        continue

                    recall_msg = recall_msg.replace("\"", '\'')
                    self.callback.emit(recall_msg)
                    pyperclip.copy("")

            except Exception as e:
                print(f"线程运行异常: {e}")
                time.sleep(0.1)

    def stop(self):
        self._is_running = False

# class TTSThread(QThread):
#     # callback=pyqtSignal(bool)
#     def __init__(self, parent=None):
#         super(TTSThread, self).__init__(parent)
#     def run(self):
#         self.tts_model = cm.init_tts()

class TTSThread(QThread):
    callback=pyqtSignal(Engine)
    def __init__(self, parent=None):
        super(TTSThread, self).__init__(parent)
    def run(self):
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.9)
        self.callback.emit(engine)



if __name__ == "__main__":
    QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)


    app = QApplication(sys.argv)

    # 创建DesktopPet实例
    pet = DesktopPet()
    pet.move(300, 10)
    # 连接信号
    pet.show()
    # pet.start_audio_processing("../audio_refer/test.wav") # 这两步需要等待模型加载结束
    sys.exit(app.exec_())
