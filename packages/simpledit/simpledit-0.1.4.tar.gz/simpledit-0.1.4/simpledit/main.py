from PyQt5 import QtWidgets
import sys
import os
import gui

def RunApp():
    app = QtWidgets.QApplication(sys.argv)
    __location__ = os.path.realpath(os.path.join(os.getcwd()))
    qss_file = open(__location__ + '/styling/style.qss').read()
    app.setStyleSheet(qss_file)

    MainWindow = QtWidgets.QMainWindow()
    ui = gui.Ui_MainWindow()
    ui.setup_ui(MainWindow, app)
    MainWindow.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    RunApp()