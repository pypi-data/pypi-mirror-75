from PyQt5 import QtWidgets
import sys
import os
from simpledit import gui

def RunApp():
    app = QtWidgets.QApplication(sys.argv)
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    qss_file = open(dname + '/styling/style.qss').read()
    app.setStyleSheet(qss_file)

    MainWindow = QtWidgets.QMainWindow()
    ui = gui.Ui_MainWindow()
    ui.setup_ui(MainWindow, app)
    MainWindow.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    RunApp()