import sys
import json
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QGroupBox, QLabel, QLineEdit, QComboBox, QRadioButton,
                             QPushButton, QButtonGroup, QFileDialog, QMessageBox, QFrame,QScrollArea)
from PyQt5.QtCore import Qt, QSettings, QRegExp
from PyQt5.QtGui import QFont, QPalette, QColor, QDoubleValidator, QRegExpValidator
import glob

class SettingsWindow(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.settings_file = "settings.json"
        self.initUI()
        self.load_settings()
        self.setObjectName("setting".replace(' ', '-'))

    def initUI(self):
        self.setWindowTitle('设置窗口')
        self.setFixedSize(800, 600)
        # 设置圆角样式
        self.setStyleSheet("* {font-family: 黑体;}}")
        # 设置浅色主题
        self.set_light_theme()

        # 创建中央部件

        # 主布局
        main_layout = QVBoxLayout(self)
        self.scroll_area = QScrollArea(self)

        self.setting_container = QWidget()
        self.setting_container.resize(800,900)

        sc_layout = QVBoxLayout(self.setting_container)
        sc_layout.setSpacing(30)
        sc_layout.setContentsMargins(30, 30, 30, 30)
        # 创建各个设置分组
        self.create_live2d_group(sc_layout)
        self.create_llm_group(sc_layout)
        self.create_operation_group(sc_layout)

        self.scroll_area.setWidget(self.setting_container)
        main_layout.addWidget(self.scroll_area)


        # 按钮区域
        self.create_button_area(main_layout)

    def set_light_theme(self):
        # 设置浅色调色板
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(248, 250, 252))
        palette.setColor(QPalette.WindowText, QColor(33, 37, 41))
        palette.setColor(QPalette.Base, QColor(255, 255, 255))
        palette.setColor(QPalette.AlternateBase, QColor(243, 245, 247))
        palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
        palette.setColor(QPalette.ToolTipText, QColor(33, 37, 41))
        palette.setColor(QPalette.Text, QColor(33, 37, 41))
        palette.setColor(QPalette.Button, QColor(108, 117, 125))
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(0, 123, 255))
        palette.setColor(QPalette.Highlight, QColor(0, 123, 255))
        palette.setColor(QPalette.HighlightedText, Qt.white)
        self.setPalette(palette)

        # 设置字体
        font = QFont("Microsoft YaHei", 9)
        self.setFont(font)

    def create_live2d_group(self, parent_layout):
        # Live2D模型设置主分组
        live2d_group = QGroupBox("Live2D模型设置")
        live2d_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 15px;
                border: 2px solid #dee2e6;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
            }
        """)

        live2d_layout = QVBoxLayout(live2d_group)

        # Live2D文件夹设置子分组
        folder_group = QGroupBox("Live2D文件夹设置")
        folder_group.setStyleSheet("""
            QGroupBox {
                font-weight: normal;
                border: 1px solid #e9ecef;
                border-radius: 6px;
                margin-top: 5px;
            }
        """)
        folder_layout = QHBoxLayout(folder_group)

        self.folder_path = QLineEdit()
        self.folder_path.setPlaceholderText("选择Live2D模型文件夹，文件夹内部需要包含对应的.model3.json文件")
        folder_browse_btn = QPushButton("浏览")
        folder_browse_btn.clicked.connect(self.browse_folder)

        folder_layout.addWidget(self.folder_path)
        folder_layout.addWidget(folder_browse_btn)

        # Live2D参数设置子分组
        param_group = QGroupBox("Live2D参数设置（开发中）")
        param_group.setStyleSheet("""
            QGroupBox {
                font-weight: normal;
                border: 1px solid #e9ecef;
                border-radius: 6px;
                margin-top: 5px;
            }
        """)
        param_layout = QVBoxLayout(param_group)

        # 参数输入框
        param1_layout = QHBoxLayout()
        param1_layout.addWidget(QLabel("参数名称设置(参数名一般为Param开头的):"))
        self.param_input = QLineEdit()
        self.param_input.setPlaceholderText("请输入Live2D参数...")
        param1_layout.addWidget(self.param_input)

        # 大小输入框
        #param2_layout = QHBoxLayout()
        param1_layout.addWidget(QLabel("参数大小(0-1):"))
        self.size_input = QLineEdit()
        reg_exp = QRegExp("^(0(\\.\\d{1,2})?|1(\\.0{1,2})?)$")
        validator = QRegExpValidator(reg_exp)
        self.size_input.setValidator(validator)
        self.size_input.setPlaceholderText("请输入参数大小（一般为0-1）...")
        param1_layout.addWidget(self.size_input)

        param_layout.addLayout(param1_layout)
        #param_layout.addLayout(param2_layout)

        name_group = QGroupBox("称谓设置")
        name_group.setStyleSheet("""
            QGroupBox {
                font-weight: normal;
                border: 1px solid #e9ecef;
                border-radius: 6px;
                margin-top: 5px;
            }
        """)
        name_layout = QVBoxLayout(name_group)

        # 参数输入框
        name1_layout = QHBoxLayout()
        name1_layout.addWidget(QLabel("称呼"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("请输入桌面宠物的名称")
        name1_layout.addWidget(self.name_input)
        name_layout.addLayout(name1_layout)

        # 添加到主布局
        live2d_layout.addWidget(folder_group)
        live2d_layout.addWidget(param_group)
        live2d_layout.addWidget(name_group)
        parent_layout.addWidget(live2d_group)

    def create_llm_group(self, parent_layout):
        # LLM模型设置主分组
        llm_group = QGroupBox("LLM模型设置")
        llm_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 15px;
                border: 2px solid #dee2e6;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
            }
        """)

        llm_layout = QVBoxLayout(llm_group)

        # API Key设置
        api_llm_group = QGroupBox("LLM API设置")
        api_llm_group.setStyleSheet("""
            QGroupBox {
                font-weight: normal;
                border: 1px solid #e9ecef;
                border-radius: 6px;
                margin-top: 5px;
            }
        """)
        api_llm_layout = QHBoxLayout(api_llm_group)
        api_llm_layout.addWidget(QLabel("API Key:"))
        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText("请输入API Key...")
        api_llm_layout.addWidget(self.api_key_input)

        # API URL设置
        api_llm_layout.addWidget(QLabel("API Url:"))
        self.api_url_input = QLineEdit()
        self.api_url_input.setPlaceholderText("请输入API URL...")
        api_llm_layout.addWidget(self.api_url_input)

        # API vision设置
        api_vision_llm_group = QGroupBox("多模态LLM API设置")
        api_vision_llm_group.setStyleSheet("""
            QGroupBox {
                font-weight: normal;
                border: 1px solid #e9ecef;
                border-radius: 6px;
                margin-top: 5px;
            }
        """)

        # API vision KEY
        api_vision_llm_layout = QHBoxLayout(api_vision_llm_group)
        api_vision_llm_layout.addWidget(QLabel("API Key:"))
        self.api_vision_key_input = QLineEdit()
        self.api_vision_key_input.setPlaceholderText("请输入多模态API Key...")
        api_vision_llm_layout.addWidget(self.api_vision_key_input)
        # API vision URL设置
        api_vision_llm_layout.addWidget(QLabel("API Url:"))
        self.api_vision_url_input = QLineEdit()
        self.api_vision_url_input.setPlaceholderText("请输入多模态API Url...")
        api_vision_llm_layout.addWidget(self.api_vision_url_input)

        llm_layout.addWidget(api_llm_group)
        llm_layout.addWidget(api_vision_llm_group)
        parent_layout.addWidget(llm_group)

    def create_operation_group(self, parent_layout):
        # 操作设置主分组
        operation_group = QGroupBox("操作设置")
        operation_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 15px;
                border: 2px solid #dee2e6;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
            }
        """)

        operation_layout = QVBoxLayout(operation_group)

        # 窗口大小设置
        window_size_layout = QHBoxLayout()
        window_size_layout.addWidget(QLabel("窗口大小:"))
        self.window_size_combo = QComboBox()
        self.window_size_combo.addItems(["小", "中", "大", "我要来点特别的"])
        self.window_size_combo.currentTextChanged.connect(self.__changeFrameSize)

        window_size_layout.addWidget(self.window_size_combo)
        window_size_layout.addStretch()

        # 语音输入设置
        voice_layout = QHBoxLayout()
        voice_layout.addWidget(QLabel("语音输入:"))

        self.voice_yes = QRadioButton("开启")
        self.voice_no = QRadioButton("关闭")
        self.voice_group = QButtonGroup()
        self.voice_group.addButton(self.voice_yes)
        self.voice_group.addButton(self.voice_no)

        voice_layout.addWidget(self.voice_yes)
        voice_layout.addWidget(self.voice_no)
        voice_layout.addStretch()

        # 语音输入快捷键
        shortcut_layout = QHBoxLayout()
        shortcut_layout.addWidget(QLabel("语音快捷键:"))
        self.shortcut_combo = QComboBox()
        self.shortcut_combo.addItems(["tab", "shift", "alt", "f1","fn"])

        shortcut_layout.addWidget(self.shortcut_combo)
        shortcut_layout.addStretch()

        # 粘贴板提示设置
        clipboard_layout = QHBoxLayout()
        clipboard_layout.addWidget(QLabel("利用粘贴板进行提示（提问前复制内容）:"))

        self.clipboard_yes = QRadioButton("启用")
        self.clipboard_no = QRadioButton("禁用")
        self.clipboard_group = QButtonGroup()
        self.clipboard_group.addButton(self.clipboard_yes)
        self.clipboard_group.addButton(self.clipboard_no)

        clipboard_layout.addWidget(self.clipboard_yes)
        clipboard_layout.addWidget(self.clipboard_no)
        clipboard_layout.addStretch()

        # 开启设置
        vision_layout = QHBoxLayout()
        vision_layout.addWidget(QLabel("是否开启模型视觉（回答速度可能会变慢）:"))

        self.vision_yes = QRadioButton("开启")
        self.vision_no = QRadioButton("关闭")
        self.vision_group = QButtonGroup()
        self.vision_group.addButton(self.vision_yes)
        self.vision_group.addButton(self.vision_no)

        vision_layout.addWidget(self.vision_yes)
        vision_layout.addWidget(self.vision_no)
        vision_layout.addStretch()

        operation_layout.addLayout(window_size_layout)
        operation_layout.addLayout(voice_layout)
        operation_layout.addLayout(shortcut_layout)
        operation_layout.addLayout(clipboard_layout)
        operation_layout.addLayout(vision_layout)
        parent_layout.addWidget(operation_group)

    def __changeFrameSize(self):
        if self.window_size_combo.currentText() == "小":
            self.pet_width=200
            self.pet_height=200
        if self.window_size_combo.currentText() == "中" :
            self.pet_width=300
            self.pet_height=400
        if self.window_size_combo.currentText() == "大" :
            self.pet_width=500
            self.pet_height=600
        if self.window_size_combo.currentText() == "我要来点特别的" :
            self.pet_width=1500
            self.pet_height=1500

    def create_button_area(self, parent_layout):
        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.save_btn = QPushButton("保存设置")
        # self.load_btn = QPushButton("加载设置")
        self.reset_btn = QPushButton("重置")

        # 设置按钮样式
        button_style = """
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
            QPushButton:pressed {
                background-color: #545b62;
            }
        """

        self.save_btn.setStyleSheet(button_style)
        # self.load_btn.setStyleSheet(button_style)
        self.reset_btn.setStyleSheet(button_style)

        self.save_btn.clicked.connect(self.save_settings)
        # self.load_btn.clicked.connect(self.load_settings)
        self.reset_btn.clicked.connect(self.reset_settings)

        button_layout.addWidget(self.reset_btn)
        # button_layout.addWidget(self.load_btn)
        button_layout.addWidget(self.save_btn)

        parent_layout.addLayout(button_layout)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "选择Live2D模型文件夹")
        if folder:
            # 检查文件夹中是否包含特定后缀的文件
            valid_extensions = {'.json', '.model3.json', '.moc', '.moc3'}
            has_valid_files = any(
                any(fname.endswith(ext) for ext in valid_extensions)
                for fname in os.listdir(folder)
            )
            if has_valid_files:
                path_list=self.__find_model3_json_files_recursive(folder)
                print(path_list[0])
                try:
                    self.folder_path.setText(str(path_list[0]).replace("\\", "/"))
                except Exception as e:
                    print(e)
            else:
                QMessageBox.warning(
                    self,
                    "无效的文件夹",
                    "选择的文件夹中不包含Live2D模型文件（文件夹内应该包含: .json, .model3.json, .moc, .moc3）"
                )
                self.folder_path.setText("")

    def __find_model3_json_files_recursive(self,folder_path):
        if not os.path.exists(folder_path):
            return []

        # 使用 glob 递归搜索
        pattern = os.path.join(folder_path, "**", "*.model3.json")
        model_files = glob.glob(pattern, recursive=True)

        return model_files

    def save_settings(self):
        print(self.folder_path.text())
        try:
            settings = {
            "live2d_model_settings": {
                "live2d_folder_settings": {
                    "folder_path": self.folder_path.text()
                },
                "live2d_parameter_settings": {
                    "parameter": self.param_input.text(),
                    "size": self.size_input.text()
                },
                "live2d_name_settings": {
                    "name": self.name_input.text()
                }
            },
            "llm_model_settings": {
                "apikey_settings": {
                    "api_key": self.api_key_input.text()
                },
                "apiurl_settings": {
                    "api_url": self.api_url_input.text()
                },
                "apikey_vision_settings": {
                    "apikey_vision": self.api_vision_key_input.text(),
                },
                "apiurl_vision_settings": {
                    "apiurl_vision": self.api_vision_url_input.text(),
                }
            },
            "operation_settings": {
                "window_size": self.window_size_combo.currentText(),
                "window_size_width": self.pet_width,
                "window_size_height":self.pet_height,
                "voice_input_enabled": self.voice_yes.isChecked(),
                "voice_shortcut": self.shortcut_combo.currentText(),
                "clipboard_hint_enabled": self.clipboard_yes.isChecked(),
                "screen_shot_enabled": self.vision_yes.isChecked()
            }
        }
        except Exception as e:
            print(e)
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=4)
            QMessageBox.information(self, "成功", "已成功保存_(:з )∠)_\n记得重新启动喔")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存设置失败: {str(e)}")

    def load_settings(self):
        if not os.path.exists(self.settings_file):
            return
        try:
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                settings = json.load(f)

            # Live2D设置
            live2d_folder = settings["live2d_model_settings"]["live2d_folder_settings"]["folder_path"]
            self.folder_path.setText(live2d_folder)

            live2d_params = settings["live2d_model_settings"]["live2d_parameter_settings"]
            self.param_input.setText(live2d_params["parameter"])
            self.size_input.setText(live2d_params["size"])

            live2d_name = settings["live2d_model_settings"]["live2d_name_settings"]
            self.name_input.setText(live2d_name["name"])

            # LLM设置
            llm_api_key = settings["llm_model_settings"]["apikey_settings"]["api_key"]
            self.api_key_input.setText(llm_api_key)

            llm_api_url = settings["llm_model_settings"]["apiurl_settings"]["api_url"]
            self.api_url_input.setText(llm_api_url)

            llm_vision_api_key = settings["llm_model_settings"]["apikey_vision_settings"]["apikey_vision"]
            self.api_vision_key_input.setText(llm_vision_api_key)

            llm_vision_api_url = settings["llm_model_settings"]["apiurl_vision_settings"]["apiurl_vision"]
            self.api_vision_url_input.setText(llm_vision_api_url)

            # 操作设置
            op_settings = settings["operation_settings"]
            self.window_size_combo.setCurrentText(op_settings["window_size"])

            # 防止加载出错，所以在启动前先进行预加载
            try:
                self.pet_width = settings["operation_settings"]["window_size_width"]
                self.pet_height = settings["operation_settings"]["window_size_height"]
            except:
                self.pet_width = 200
                self.pet_height = 200
            print(f"{settings["operation_settings"]["window_size_width"]}+{settings["operation_settings"]["window_size_height"]}")
            if op_settings["voice_input_enabled"]:
                self.voice_yes.setChecked(True)
            else:
                self.voice_no.setChecked(True)

            self.shortcut_combo.setCurrentText(op_settings["voice_shortcut"])

            if op_settings["clipboard_hint_enabled"]:
                self.clipboard_yes.setChecked(True)
            else:
                self.clipboard_no.setChecked(True)

            if op_settings["screen_shot_enabled"]:
                self.vision_yes.setChecked(True)
            else:
                self.vision_no.setChecked(True)

        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载设置失败: {str(e)}")

    def reset_settings(self):
        reply = QMessageBox.question(self, "确认重置", "确定要重置所有设置为默认值吗？",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.folder_path.clear()
            self.param_input.clear()
            self.size_input.clear()

            self.api_key_input.clear()
            self.api_url_input.clear()
            self.api_vision_url_input.clear()
            self.api_vision_key_input.clear()

            self.window_size_combo.setCurrentIndex(0)
            self.voice_yes.setChecked(True)
            self.shortcut_combo.setCurrentIndex(0)
            self.clipboard_yes.setChecked(True)
            self.vison_yes.setChecked(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SettingsWindow()
    window.load_settings()
    window.show()
    sys.exit(app.exec_())
