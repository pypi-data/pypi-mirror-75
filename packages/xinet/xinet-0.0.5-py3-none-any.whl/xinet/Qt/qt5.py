try:
    # PySide2
    from PySide2 import QtGui, QtWidgets, QtCore, QtPrintSupport
    from PySide2.QtCore import Signal, Slot
except ImportError:
    # PyQt5
    from PyQt5 import QtGui, QtWidgets, QtCore, QtPrintSupport
    from PyQt5.QtCore import pyqtSignal as Signal, pyqtSlot as Slot