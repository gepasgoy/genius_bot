from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit


class CustomButton(QPushButton):
    def __init__(self):
        super().__init__()
        css = '''
        
        color: #464d55;
        font-weight: 600;
        
        '''
        self.setStyleSheet(css)

class CustomLineEdit(QLineEdit):
    def __init__(self):
        super().__init__()
        css = '''
        color: #464d55;
        font-weight: 600;
        
        '''
        self.setStyleSheet(css)