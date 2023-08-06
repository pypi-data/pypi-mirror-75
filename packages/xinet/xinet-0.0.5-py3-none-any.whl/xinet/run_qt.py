from .Qt.qt5 import QtWidgets


def run(window_type, *args, **kwargs):
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = window_type(*args, **kwargs)
    window.show()
    app.exec_()
