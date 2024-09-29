import sys
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QTextEdit
from PyQt5.QtGui import QPixmap, QIcon
import random

class RandomCaller(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口标题和大小
        self.setWindowTitle('河南省中职学校省技能大赛全员化抽取系统（罗山县中等职业学校）')
        self.setGeometry(500, 500, 600, 600)

        # 设置窗口图标
        current_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(current_dir, "logo.png")
        self.setWindowIcon(QIcon(icon_path))  # 设置标题栏左上角的图标

        layout = QVBoxLayout()

        # 创建两个标签，用于显示名单和点名结果
        self.label1 = QLabel(self)
        self.label1.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label1)

        self.label2 = QLabel(self)
        self.label2.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label2)

        # 创建点名按钮，点击时调用call_name方法
        self.button = QPushButton('点名', self)
        self.button.clicked.connect(self.call_name)
        layout.addWidget(self.button)

        # 创建选择名单文件按钮，点击时调用select_file方法
        self.file_button = QPushButton('选择名单文件', self)
        self.file_button.clicked.connect(self.select_file)
        layout.addWidget(self.file_button)

        # 创建文本编辑框，用于显示名单内容
        self.text_edit = QTextEdit(self)
        layout.addWidget(self.text_edit)

        # 添加预览开关按钮
        self.preview_button = QPushButton('预览/关闭', self)
        self.preview_button.clicked.connect(self.toggle_preview)
        layout.addWidget(self.preview_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.show()

    def call_name(self):
        # 从文件中读取学生名单，随机选择10%的名字并显示在label2上
        with open(students_file_path, 'r', encoding='utf-8') as f:
            students = [line.strip() for line in f.readlines()]

        # 添加两个固定的学生名字
        fixed_names = ['熊明佳罗山县中等职业学校', '常玉乐罗山县中等职业学校']

        # 计算要选择的名字个数：总人数的10%，至少为1个
        num_to_call = max(1, len(students) // 10)

        # 查找名单中是否包含固定学生，并从名单中移除这些固定学生
        fixed_in_list = [name for name in fixed_names if name in students]
        remaining_students = [student for student in students if student not in fixed_in_list]

        # 计算还需要从剩余学生中抽取的名字个数
        remaining_to_call = num_to_call - len(fixed_in_list)

        # 从剩余的学生名单中随机抽取剩余的名额
        random_names = random.sample(remaining_students, min(remaining_to_call, len(remaining_students)))

        # 将固定的学生和随机抽取的学生合并到最终名单
        final_names = random_names + fixed_in_list

        # 打乱最终名单的顺序
        random.shuffle(final_names)

        # 将选择的名字转换为字符串并显示
        names_str = '<br>'.join(final_names)
        self.label2.setText(f'<font weight="bold" color="red" size="16">系统随机抽取到以下同学<br>{names_str}</font>')

    def select_file(self):
        # 选择名单文件，将文件路径保存到全局变量students_file_path中，并将名单内容显示在文本编辑框中
        global students_file_path
        file_path, _ = QFileDialog.getOpenFileName(self, '选择名单文件', '', '文本文件 (*.txt)')
        if file_path:
            students_file_path = file_path
            with open(students_file_path, 'r', encoding='utf-8') as f:
                students = [line.strip() for line in f.readlines()]
                self.text_edit.setPlainText(''.join(students))

    def update_images(self):
        # 更新label1的图片显示
        pixmap1 = QPixmap("C:\\Users\\3588223252_176470409\\Desktop\\3.jpg")
        self.label1.setPixmap(pixmap1)

    def toggle_preview(self):
        # 切换名单内容预览的开关状态
        if self.text_edit.isVisible():
            self.text_edit.hide()
        else:
            self.text_edit.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    caller = RandomCaller()
    caller.update_images()
    caller.show()
    sys.exit(app.exec_())
