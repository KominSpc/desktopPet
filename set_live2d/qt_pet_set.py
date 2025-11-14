import io
import threading

import live2d.v3 as live2d
import pygame

from PyQt5.Qt import QCursor
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QOpenGLWidget, QGraphicsDropShadowEffect, QWidget
from live2d.utils.lipsync import WavHandler
from live2d.v3 import StandardParams
from qfluentwidgets import TeachingTip, TeachingTipTailPosition, InfoBarIcon
import dt_config
import set_live2d.resources as resources
import os

from PyQt5.QtCore import QCoreApplication, Qt, QUrl, QTimer


class Pet(QOpenGLWidget):
    def __init__(self):
        live2d.init()
        pygame.mixer.init()
        super().__init__()
        self.setFixedSize(dt_config.WINDOW_SIZE_WIDTH, dt_config.WINDOW_SIZE_HEIGHT)
        self.wavHandler = WavHandler()  # 声音处理控件初始化
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.pet_model: live2d.LAppModel | None = None
        self.setAcceptDrops(True)
        self.lipSyncN=3

        self.audio_timer=QTimer()
        self.audio_timer.timeout.connect(self.update_audio)

    def timerEvent(self, a0):
        # x, y = QCursor.pos().x() - self.x(), QCursor.pos().y() - self.y()
        x,y=_eye_follow(QCursor.pos().x(),QCursor.pos().y())
        self.pet_model.Drag(x, y)  # 设置看向鼠标坐标

        self.update()

    def initializeGL(self):
        live2d.glewInit()
        self.pet_model = live2d.LAppModel()
        try:
            if dt_config.LIVE2D_FOLDER_PATH.strip()!="":
                self.pet_model.LoadModelJson(dt_config.LIVE2D_FOLDER_PATH)
            else:
                self.pet_model.LoadModelJson(os.path.join(resources.RESOURCES_DIRECTORY, "v3/跳蚤/跳蚤.model3.json"))# 设置原始路径，避免在酒吧里点炒菜
        except:
            self.pet_model.LoadModelJson(os.path.join(resources.RESOURCES_DIRECTORY, "v3/跳蚤/跳蚤.model3.json"))
        if dt_config.LIVE2D_PARAMETER.strip()!="" and dt_config.LIVE2D_SIZE.strip()!="":
            print(f"{dt_config.LIVE2D_PARAMETER}+{dt_config.LIVE2D_SIZE}")
            self.pet_model.SetParameterValue(dt_config.LIVE2D_PARAMETER,float(dt_config.LIVE2D_SIZE),float(dt_config.LIVE2D_SIZE))
        self.startTimer(1)

    def resizeGL(self, w, h):
        self.pet_model.Resize(w, h)

    def paintGL(self):
        live2d.clearBuffer()
        self.pet_model.Update()
        self.pet_model.Draw()

    @property
    def modelParams(self):
        return self.pet_model.GetParamIds()

    def setModelParams(self, key,value,weight):
        self.pet_model.SetParameterValue(key, value, weight)  # 水印设置

    def showTeachingTip(self,title:str,msg:str):
        try:
            print()
            TeachingTip.create(
                target=self,
                title=title,
                content=msg,
                isClosable=True,
                tailPosition=TeachingTipTailPosition.BOTTOM,
                duration=int(len(msg)/5*1500+2000),
                parent=self
            )
        except Exception as e:
            print(e)

    def start_audio_processing(self,msg,model_tts):
        try:
            save_thread = threading.Thread(target=lambda: model_tts.save_to_file(msg, r"temp/temp.wav", "temp"))
            save_thread.start()
        except Exception as e:
            print(e)
        audio_path = r"temp/temp.wav"
        # 调用timer处理同步播放和嘴部动作
        pygame.mixer.stop()
        save_thread.join()
        with open(audio_path, 'rb') as f:
            audio_data = f.read()
        audio_buffer = io.BytesIO(audio_data)
        sound = pygame.mixer.Sound(audio_buffer)
        sound.play()
        self.wavHandler.Start(audio_path)
        self.audio_timer.start(5)  # 每5毫秒更新一次
        os.unlink(audio_path)

    def update_audio(self):
        if self.wavHandler.Update():
            rms_value = self.wavHandler.GetRms() * 1.5 * self.lipSyncN
            self.pet_model.SetParameterValue(
                StandardParams.ParamMouthOpenY, rms_value
            )
        else:
            self.audio_timer.stop()

def _eye_follow(x, y):

    _prev_eye_x=0
    _prev_eye_y=0

    # 线性插值法平滑
    lerp_factor = 0.3
    _prev_eye_x = _prev_eye_x + (x - _prev_eye_x) * lerp_factor
    _prev_eye_y = _prev_eye_y + (y - _prev_eye_y) * lerp_factor

    return _prev_eye_x, _prev_eye_y


# if __name__ == '__main__':
#     QCoreApplication.setAttribute(Qt.ApplicationAttribute.AA_ShareOpenGLContexts)
#     app = QApplication(sys.argv)
#     window = Pet()
#     window.setWindowFlag(Qt.WindowStaysOnTopHint, True) # 因为播放音频的问题，需要将宠物持置顶
#     window.move(100, 100)
#     window.show()
#     window.showTeachingTip("有礼貌的回复","你好啊")
#     print(window.modelParams)
#     sys.exit(app.exec_())
