# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from PyQt5.QtWidgets import QApplication
import sys
from window_start import WindowStart


def application():
    app = QApplication(sys.argv)
    window = WindowStart()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    application()
