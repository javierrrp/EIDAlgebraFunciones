import sys
from PyQt6.QtWidgets import QApplication
from View.main_window import MainWindow
from Controller.controller import Controller

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    controller = Controller(view=window)
    window.show()
    sys.exit(app.exec())