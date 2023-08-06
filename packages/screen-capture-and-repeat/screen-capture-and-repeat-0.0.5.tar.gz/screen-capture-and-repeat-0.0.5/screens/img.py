import sys
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication, QLabel # type: ignore
from PyQt5.QtGui import QIcon, QPixmap # type: ignore

from typing import *

class ShowImage(QWidget): # type: ignore
 
    def __init__(self, file_name: str, width: int, height: int) -> None:
        super().__init__()
        self.file_name = file_name
        self.width = width
        self.height = height
        self.click_x = -1
        self.click_y = -1
        self.initUI()
 
    def initUI(self) -> None:
        self.setGeometry(0, 0, self.width, self.height)
        self.setWindowTitle('Message box')

        label = QLabel(self)
        pixmap = QPixmap(self.file_name)
        label.setPixmap(pixmap)
        self.resize(pixmap.width(),pixmap.height())

        self.show()

    def mousePressEvent(self, e: Any) -> None:
        self.click_x = e.x()
        self.click_y = e.y()
        print(f"x: {self.click_x},  y: {self.click_y}")
        self.close()

def show_image(file_name: str, width: int, height: int) -> Tuple[int, int]:
    app = QApplication(sys.argv)
    ex = ShowImage(file_name, width, height)
    app.exec_()
    return (ex.click_x, ex.click_y)