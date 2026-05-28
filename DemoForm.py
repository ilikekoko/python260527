# DemoForm.py

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt6 import uic

# 디자인 파일을 로딩
form_class = uic.loadUiType("DemoForm.ui")[0]

#폼클래스를 정의
class DemoForm(QDialog, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.label.setText("이렇게 화면에 출력")

#진입점 체크
if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = DemoForm()
    demo.show()
    sys.exit(app.exec())
        

