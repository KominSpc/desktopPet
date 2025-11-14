import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy, QOpenGLWidget
from PyQt5.QtCore import Qt, QTimer, QSize, QThread, pyqtSignal
from PyQt5.QtGui import QFontMetrics, QSurfaceFormat
from qfluentwidgets import (PrimaryPushButton, PushButton, TextEdit,
                            ScrollArea, SimpleCardWidget, isDarkTheme,CardWidget)
from llm_api.llm_api import LLMModel
import llm_api.api_config as api_config
class ChatBubble(CardWidget):

    def __init__(self, message, is_me=True, parent=None):
        super().__init__(parent)

        self.message = message
        self.is_me = is_me
        self.setup_ui()
        self.adjust_size()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        self.message_label = QLabel(self.message)
        self.message_label.setWordWrap(True)
        self.message_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.message_label.setMaximumWidth(500)  # 限制最大宽度
        self.message_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        font = self.message_label.font()
        font.setPointSize(11)
        font.setFamily("Microsoft YaHei")
        self.message_label.setFont(font)
        # 设置样式
        if self.is_me:
            self.message_label.setStyleSheet("""
                    QLabel {
                        color: white;
                        background-color: #FFB6C1;
                        padding: 8px 12px;
                        border-radius: 12px;
                    }
                """)
            layout.addStretch()
            layout.addWidget(self.message_label)
            layout.setAlignment(self.message_label, Qt.AlignRight)
        else:
            self.message_label.setStyleSheet("""
                    QLabel {
                        color: %s;
                        background-color: %s;
                        padding: 8px 12px;
                        border-radius: 12px;
                    }
                """ % ("black" if not isDarkTheme() else "white",
                       "#F0F0F0" if not isDarkTheme() else "#2D2D2D"))
            layout.addWidget(self.message_label)
            layout.addStretch()
            layout.setAlignment(self.message_label, Qt.AlignLeft)

    def adjust_size(self):
        font_metrics = QFontMetrics(self.message_label.font())

        # 计算文本所需的宽度和高度
        text_rect = font_metrics.boundingRect(
            0, 0, 500, 1000,  # 最大宽度400，高度限制1000
            Qt.TextWordWrap | Qt.AlignRight,
            self.message
        )

        # 加上内边距
        width = min(text_rect.width() + 40, 540)  # 最大440px
        height = text_rect.height() + 20

        # 设置气泡固定大小
        self.message_label.setFixedSize(width, height)
        self.setFixedSize(750, height + 20)  # 加上布局边距


class ChatWindow(QWidget):

    could_taking=True # 消息发送开关
    def __init__(self):
        super().__init__()
        self.llm_model = LLMModel()
        self.setup_ui()

    def setup_ui(self):
        print("刷新")
        self.setWindowTitle('聊天界面')

        self.setFixedSize(800,600)

        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # 聊天显示区域
        self.setup_chat_display(main_layout)

        # 输入区域
        self.setup_input_area(main_layout)

    def setup_chat_display(self, layout):

        self.scroll_area = ScrollArea()
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
            ScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background-color: transparent;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #C0C0C0;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #A0A0A0;
            }
        """)

        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setSpacing(8)
        self.chat_layout.setContentsMargins(10, 10, 10, 10)
        self.chat_layout.addStretch()

        self.scroll_area.setWidget(self.chat_container)
        layout.addWidget(self.scroll_area, 1)

    def setup_input_area(self, layout):
        # 输入框
        self.input_text = TextEdit()
        self.input_text.setPlaceholderText("输入消息...")
        self.input_text.setFixedHeight(120)
        self.input_text.setStyleSheet("""
            TextEdit {
                border: none;
                background-color: %s;
                border-radius: 8px;
                font-size: 14px;
                padding: 12px;
            }
        """ % ("#FFFFFF" if not isDarkTheme() else "#2D2D2D"))

        layout.addWidget(self.input_text)

        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        # 语音按钮
        # self.voice_btn = PushButton('语音')
        # self.voice_btn.setFixedSize(80, 35)

        # 取消按钮
        self.cancel_btn = PushButton('清空')
        self.cancel_btn.setFixedSize(80, 35)

        # 发送按钮
        self.send_btn = PrimaryPushButton('发送')
        self.send_btn.setFixedSize(80, 35)

        # button_layout.addWidget(self.voice_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_btn)
        button_layout.addWidget(self.send_btn)

        layout.addLayout(button_layout)

        # 连接信号
        self.send_btn.clicked.connect(self.send_message)
        self.cancel_btn.clicked.connect(self.clear_input)

    def add_message(self, message, is_me=True):
        bubble = ChatBubble(message, is_me)
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, bubble)
        # 滚动到底部 及时更新+计时器实现scrollbar最大值被正确读取（为了解决逆天BUG）
        bubble.show()
        bubble.update()
        bubble.updateGeometry()
        # 强制布局重新计算
        self.chat_layout.activate()
        self.scroll_area.widget().updateGeometry()
        QTimer.singleShot(50, self.scroll_to_bottom)

    def scroll_to_bottom(self):
        scrollbar = self.scroll_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def send_message(self):
        print(self.scroll_area.verticalScrollBar().maximum())
        message = self.input_text.toPlainText().strip()
        self.add_message(message, True)
        self.ban_send()
        if message:
            try:
                self.send_thread = SendThread(self.llm_model, message)
                self.send_thread.callback.connect(self.__sendMsgCallback)
                self.send_thread.finished.connect(self.__finishSendMsg)
                print("a")
                self.send_thread.start()
                self.input_text.clear()

            except Exception as e:
                print(e)

    def keyPressEvent(self, event):
        print(event.key())
        if event.key() == Qt.Key_Return and self.could_taking:
            self.send_message()

    def __sendMsgCallback(self,msg:str):
        self.add_message(msg,False)
        # 发送结束恢复可发送状态
        self.activate_send()

    def __finishSendMsg(self):
        # 停止对话线程，避免调用时线程回收
        print("开始结束线程")
        self.send_thread.quit()

    def ban_send(self):
        self.could_taking=False
        self.send_btn.setEnabled(False)

    def activate_send(self):
        self.could_taking=True
        self.send_btn.setEnabled(True)

    def clear_input(self):
        self.input_text.clear()

# 发送线程
class SendThread(QThread):
    callback=pyqtSignal(str)
    callback_finished=pyqtSignal()
    def __init__(self,llm_model,message):
        super().__init__()
        self.llm_model = llm_model
        self.message = message

    def run(self):
        res=self.llm_model.sendMsg(self.message)
        self.callback.emit(res[1])
        #self.callback_finished.emit() #结束线程返回消息
        return None

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 设置应用样式
    window = ChatWindow()
    window.show()

    sys.exit(app.exec_())
