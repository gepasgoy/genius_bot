from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout
from custom import CustomButton, CustomLineEdit
from sys import argv

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        central_widget = QWidget()
        central_layout = QVBoxLayout()
        hlayout = QHBoxLayout()
        central_layout.addLayout(hlayout)
        self.line_edit = CustomLineEdit()
        hlayout.addWidget(self.line_edit)
        self.setCentralWidget(central_widget)
        self.button = CustomButton()
        central_widget.setLayout(central_layout)
        hlayout.addWidget(self.button)



if __name__ == "__main__":
    app = QApplication(argv)
    MW = MainWindow()
    MW.show()
    app.exec()

