#!/usr/bin/env python3

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PIL import Image, ImageQt
import os
import threading
import time
import copy
from simpledit import image
from simpledit import im_functions

class Ui_MainWindow(object):
    def __init__(self):
        self.location = os.path.realpath(os.path.join(os.getcwd()))
        self.image = None
        self.other_image = None

    def setup_ui(self, MainWindow, app):
        if not os.path.exists(os.path.expanduser("~")+'/SimplEdit_Filters'):
            os.mkdir(os.path.expanduser("~")+'/SimplEdit_Filters')
        self.home = os.path.expanduser("~")+"/SimplEdit_Filters/"
        self.app = app
        self.lister = ''
        self.currentCustom = 45
        self.switchOrder = False
        self.save = None
        self.tha = None
        self.loading_widget = None
        self.processSwirl=False
        self.processCustom=False
        MainWindow.setWindowTitle("SimplEdit")
        MainWindow.resize(1200, 850)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setWindowIcon(QtGui.QIcon(self.location + "/images/icon.png"))

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.central_widget(MainWindow)
        self.tab_widget(MainWindow)
        self.tab_elements(MainWindow)
        self.label_widget(MainWindow)
        self.layouts(MainWindow)

    def central_widget(self, MainWindow):
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setToolTipDuration(0)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        MainWindow.setCentralWidget(self.centralwidget)

    def label_widget(self, MainWindow):
        filepath = self.location + '/images/default.png'
        pixmap = QtGui.QPixmap(filepath)
        self.labelWidget = QtWidgets.QLabel(self.frame)
        self.labelWidget.setPixmap(pixmap)
        self.labelWidget.setAlignment(QtCore.Qt.AlignCenter)

    def tab_widget(self, MainWindow):
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setMaximumSize(QtCore.QSize(3000, 75))

        self.tab_home = QtWidgets.QWidget()
        self.tab_edit = QtWidgets.QWidget()
        self.tab_color = QtWidgets.QWidget()
        self.tab_filters = QtWidgets.QWidget()
        self.tab_effects = QtWidgets.QWidget()
        self.tab_creative = QtWidgets.QWidget()
        self.tab_blending = QtWidgets.QWidget()
        self.tab_custom = QtWidgets.QWidget()

        self.tabWidget.addTab(self.tab_home, "Home")
        self.tabWidget.addTab(self.tab_edit, "Edit")
        self.tabWidget.addTab(self.tab_color, "Color")
        self.tabWidget.addTab(self.tab_effects, "Effects")
        self.tabWidget.addTab(self.tab_filters, "Filters")
        self.tabWidget.addTab(self.tab_creative, "Creative")
        self.tabWidget.addTab(self.tab_blending, "Blending")
        self.tabWidget.addTab(self.tab_custom, "Custom Effects")

        self.tabWidget.setCurrentIndex(0)

    def tab_elements(self, MainWindow):
        # Home Buttons

        self.tab_button(self, self.tab_home,
                        (0, 0, 40, 40), "Open an Image", "Open")
        self.button.clicked.connect(self.open_img)
        self.button.setIcon(QtGui.QIcon(self.location + "/images/open_file.svg"))
        self.button.setIconSize(QtCore.QSize(40, 40))

        self.tab_button(self, self.tab_home,
                        (45, 0, 40, 40), "Save a file", "Save")
        self.button.clicked.connect(self.save_file)
        self.button.setIcon(QtGui.QIcon(self.location + "/images/save_file.svg"))
        self.button.setIconSize(QtCore.QSize(40, 40))

        # Edit Buttons

        self.tab_button(self, self.tab_edit,
                        (0, 0, 40, 40), "Undo the last operation", "Undo")
        self.button.clicked.connect(self.undo)
        self.button.setIcon(QtGui.QIcon(self.location + "/images/undo.svg"))
        self.button.setIconSize(QtCore.QSize(40, 40))

        self.tab_button(self, self.tab_edit,
                        (45, 0, 40, 40), "Redo the last operation", "Redo")
        self.button.clicked.connect(self.redo)
        self.button.setIcon(QtGui.QIcon(self.location + "/images/redo.svg"))
        self.button.setIconSize(QtCore.QSize(40, 40))

        self.tab_button(self, self.tab_edit,
                        (95, 0, 40, 40), "Rotate the image Left", "Rotate")
        self.button.clicked.connect(self.rotate_left)
        self.button.setIcon(QtGui.QIcon(self.location + "/images/rotate_left.svg"))
        self.button.setIconSize(QtCore.QSize(40, 40))

        self.tab_button(self, self.tab_edit,
                        (140, 0, 40, 40), "Rotate the image Right", "Rotate")
        self.button.clicked.connect(self.rotate_right)
        self.button.setIcon(QtGui.QIcon(self.location + "/images/rotate_right.svg"))
        self.button.setIconSize(QtCore.QSize(40, 40))

        self.tab_button(self, self.tab_edit,
                        (185, 0, 40, 40), "Flip the image horizontally", "Flip")
        self.button.clicked.connect(self.flip)
        self.button.setIcon(QtGui.QIcon(self.location + "/images/flip.png"))
        self.button.setIconSize(QtCore.QSize(40, 40))

        self.tab_button(self, self.tab_edit,
                        (230, 0, 40, 40), "Crop the Image", "Crop")
        self.button.clicked.connect(self.crop)
        self.button.setIcon(QtGui.QIcon(self.location + "/images/Crop.svg"))
        self.button.setIconSize(QtCore.QSize(40, 40))

        # Color Buttons

        self.tab_button(self, self.tab_color,
                        (0, 0, 40, 40), "Brighten or darken colors", "Brightness")
        self.button.clicked.connect(self.brighten)
        self.button.setIcon(QtGui.QIcon(self.location + "/images/brightness.svg"))
        self.button.setIconSize(QtCore.QSize(40, 40))

        self.tab_button(self, self.tab_color,
                        (45, 0, 40, 40), "Change image transparency", "Transparency")
        self.button.clicked.connect(self.change_transparency)
        self.button.setIcon(QtGui.QIcon(self.location + "/images/transparency.svg"))
        self.button.setIconSize(QtCore.QSize(40, 40))

        self.tab_button(self, self.tab_color,
                        (90, 0, 40, 40), "Change image contrast", "Contrast")
        self.button.clicked.connect(self.change_contrast)
        self.button.setIcon(QtGui.QIcon(self.location + "/images/contrast.png"))
        self.button.setIconSize(QtCore.QSize(40, 40))

        self.tab_button(self, self.tab_color,
                        (135, 0, 40, 40), "Change color intensity", "Saturation")
        self.button.clicked.connect(self.change_saturation)
        self.button.setIcon(QtGui.QIcon(self.location + "/images/saturation.svg"))
        self.button.setIconSize(QtCore.QSize(40, 40))

        self.tab_button(self, self.tab_color,
                        (185, 0, 40, 40), "Add Border", "Border")
        self.button.clicked.connect(self.add_border)
        self.button.setIcon(QtGui.QIcon(self.location + "/images/border.svg"))
        self.button.setIconSize(QtCore.QSize(40, 40))

        # Effects Buttons

        self.tab_button(self, self.tab_effects,
                        (0, 0, 40, 40), "Reduce noise and detail", "Blur")
        self.button.clicked.connect(self.blur)
        self.button.setIcon(QtGui.QIcon(self.location + "/images/blur.svg"))
        self.button.setIconSize(QtCore.QSize(40, 40))

        self.tab_button(self, self.tab_effects,
                        (45, 0, 40, 40), "Enhance the image", "Enhance")
        self.button.clicked.connect(self.enhance)
        self.button.setIcon(QtGui.QIcon(self.location + "/images/enhance.svg"))
        self.button.setIconSize(QtCore.QSize(40, 40))

        self.tab_button(self, self.tab_effects,
                        (90, 0, 40, 40), "Smooth the image", "Smooth")
        self.button.clicked.connect(self.smooth)
        self.button.setIcon(QtGui.QIcon(self.location + "/images/smooth.svg"))
        self.button.setIconSize(QtCore.QSize(40, 40))

        self.tab_button(self, self.tab_effects,
                        (140, 0, 40, 40), "Pixelate the image", "Pixelate")
        self.button.clicked.connect(self.pixelate)
        self.button.setIcon(QtGui.QIcon(self.location + "/images/pixelate.svg"))
        self.button.setIconSize(QtCore.QSize(40, 40))

        self.tab_button(self, self.tab_effects,
                        (185, 0, 40, 40), "Create a swirl effect", "Swirl")
        self.button.clicked.connect(self.process_swirl)
        self.button.setIcon(QtGui.QIcon(self.location + "/images/swirl.svg"))
        self.button.setIconSize(QtCore.QSize(40, 40))

        # Filter Buttons

        self.tab_button(self, self.tab_filters,
                        (0, 0, 40, 40), "Invert all colors", "Invert")
        self.button.clicked.connect(self.invert_colors)
        self.button.setIcon(QtGui.QIcon(self.location + "/images/invert.svg"))
        self.button.setIconSize(QtCore.QSize(40, 40))

        self.tab_button(self, self.tab_filters,
                        (45, 0, 40, 40), "Convert to black and white", "Grayscale")
        self.button.clicked.connect(self.grayscale)
        self.button.setIcon(QtGui.QIcon(self.location + "/images/grayscale.svg"))
        self.button.setIconSize(QtCore.QSize(40, 40))

        self.tab_button(self, self.tab_filters,
                        (90, 0, 40, 40), "Simulate an old sepia photograph", "Sepia")
        self.button.clicked.connect(self.sepia)
        self.button.setIcon(QtGui.QIcon(self.location + "/images/sepia.svg"))
        self.button.setIconSize(QtCore.QSize(40, 40))

        self.tab_button(self, self.tab_filters,
                        (140, 0, 40, 40), "Add a light yellow tint", "Yellow Tint")
        self.button.clicked.connect(self.yellow_tint)
        self.button.setIcon(QtGui.QIcon(self.location + "/images/yellow_tint.svg"))
        self.button.setIconSize(QtCore.QSize(40, 40))

        self.tab_button(self, self.tab_filters,
                        (185, 0, 40, 40), "Add shades of maroon", "Redwood")
        self.button.clicked.connect(self.redwood)
        self.button.setIcon(QtGui.QIcon(self.location + "/images/redwood.svg"))
        self.button.setIconSize(QtCore.QSize(40, 40))

        self.tab_button(self, self.tab_filters,
                        (230, 0, 40, 40), "Add a blue and yellow tint", "Aqua")
        self.button.clicked.connect(self.aqua)
        self.button.setIcon(QtGui.QIcon(self.location + "/images/aqua.png"))
        self.button.setIconSize(QtCore.QSize(40, 40))

        self.tab_button(self, self.tab_filters,
                        (275, 0, 40, 40), "Add a green and blue tint", "Olive")
        self.button.clicked.connect(self.olive)
        self.button.setIcon(QtGui.QIcon(self.location + "/images/olive.svg"))
        self.button.setIconSize(QtCore.QSize(40, 40))

        # Creative Buttons

        self.tab_button(self, self.tab_creative, (0, 0, 40, 40), "Before and After", "Before & After")
        self.button.clicked.connect(self.before_after)
        self.button.setIcon(QtGui.QIcon(self.location + "/images/before_after.svg"))
        self.button.setIconSize(QtCore.QSize(40, 40))

        # Blending Buttons

        self.tab_button(self, self.tab_blending, (0, 0, 40, 40), "Open another image", "Open")
        self.button.clicked.connect(self.open_second_img)
        self.button.setIcon(QtGui.QIcon(self.location + "/images/open_file.svg"))
        self.button.setIconSize(QtCore.QSize(40, 40))

        # Custom Buttons

        self.scrollArea = QtWidgets.QScrollArea(self.tab_custom)
        self.sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.sizePolicy.setHorizontalStretch(0)
        self.sizePolicy.setVerticalStretch(0)
        self.sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(self.sizePolicy)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1200, 75))
        self.horizontalLayout2 = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout2.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout2.setSpacing(5)
        self.tab_button(self, self.scrollAreaWidgetContents, (0, 0, 40, 40), "Add Custom Filter", "Add Filter")
        self.button.setIcon(QtGui.QIcon(self.location + "/images/add_filter.svg"))
        self.button.clicked.connect(self.add_custom)
        self.button.setIconSize(QtCore.QSize(40, 40))
        self.button.setMaximumSize(40, 40)
        self.horizontalLayout2.addWidget(self.button, 0, QtCore.Qt.AlignLeft)
        self.tab_button(self, self.scrollAreaWidgetContents, (45, 0, 40, 40), "Remove Custom Filter", "Remove Filter")
        self.button.setIcon(QtGui.QIcon(self.location + "/images/remove.svg"))
        self.button.clicked.connect(self.remove_custom_filter)
        self.button.setIconSize(QtCore.QSize(40, 40))
        self.button.setMaximumSize(40, 40)
        self.horizontalLayout2.addWidget(self.button, 0, QtCore.Qt.AlignLeft)
        if not os.path.exists(self.home+'filter.txt'):
            f = open(self.home+'filter.txt', 'w')
            f.close()

        f = open(self.home+"filter.txt", "r")
        listo = {}
        for x in f:
            if x != '':
                y = x
                if x[len(x) - 1:len(x)] == '\n':
                    y = x[0:len(x) - 1]
                if y != 'filter' and os.path.exists(self.home+y + '.txt') and y not in listo:
                    listo[(y)] = 'hi'
                    self.currentCustom = self.currentCustom + 45
                    self.tab_button(self, self.scrollAreaWidgetContents, (self.currentCustom, 0, 40, 40), "Apply " + x,
                                    x)
                    self.button.setMaximumSize(40, 40)
                    self.button.clicked.connect(lambda checked, name=x: self.process_custom(name))
                    self.button.setIcon(QtGui.QIcon(self.location + "/images/Custom.svg"))
                    self.button.setIconSize(QtCore.QSize(40, 40))
                    self.horizontalLayout2.addWidget(self.button)
                    self.horizontalLayout2.addWidget(self.button, 0, QtCore.Qt.AlignLeft)
        f.close()
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.tabWidget.addTab(self.tab_custom, "Custom Filters")
        if (self.currentCustom + 45 >= 1174):
            self.scrollArea.setGeometry(QtCore.QRect(0, 0, 1174, 50))
        else:
            self.scrollArea.setGeometry(QtCore.QRect(0, 0, self.currentCustom + 53, 50))
        self.horizontalLayout2.setContentsMargins(1, 3, 7, 0)

        # Button Separators

        self.tab_frame(self, self.tab_home, (90, 0, 3, 61))
        self.tab_frame(self, self.tab_edit, (90, 0, 3, 61))
        self.tab_frame(self, self.tab_edit, (275, 0, 3, 61))
        self.tab_frame(self, self.tab_color, (180, 0, 3, 61))
        self.tab_frame(self, self.tab_color, (230, 0, 3, 61))
        self.tab_frame(self, self.tab_effects, (135, 0, 3, 61))
        self.tab_frame(self, self.tab_effects, (230, 0, 3, 61))
        self.tab_frame(self, self.tab_filters, (135, 0, 3, 61))
        self.tab_frame(self, self.tab_filters, (320, 0, 3, 61))
        self.tab_frame(self, self.tab_creative, (45, 0, 3, 61))
        self.tab_frame(self, self.tab_blending, (45, 0, 3, 61))
        self.tab_frame(self, self.tab_custom, (self.currentCustom + 45, 0, 1, 61))

    def tab_button(self, MainWindow, widget_parent, position, status_tip, tool_tip):
        x, y, z, k = position
        self.button = QtWidgets.QToolButton(widget_parent)
        self.button.setGeometry(QtCore.QRect(x, y + 3, z, k))
        if len(status_tip) > 0 and status_tip[len(status_tip) - 1: len(status_tip)] == '\n':
            status_tip = status_tip[0:len(status_tip) - 1]
        if len(tool_tip) > 0 and tool_tip[len(tool_tip) - 1: len(tool_tip)] == '\n':
            tool_tip = tool_tip[0:len(tool_tip) - 1]
        self.button.setStatusTip(status_tip)
        self.button.setToolTip(tool_tip)

    def tab_frame(self, MainWindow, widget_parent, position):
        x, y, z, k = position
        self.separator = QtWidgets.QFrame(widget_parent)
        self.m = self.separator
        self.separator.setGeometry(QtCore.QRect(x, y, z, k))
        self.separator.setFrameShape(QtWidgets.QFrame.VLine)
        self.separator.setFrameShadow(QtWidgets.QFrame.Sunken)

    def layouts(self, MainWindow):
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.horizontalLayout = QtWidgets.QGridLayout(self.frame)
        self.horizontalLayout.addWidget(self.labelWidget, 0, 0)
        self.gridLayout.addWidget(self.frame, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

    def open_img(self, secondImage):
        if(self.processSwirl == False and self.processCustom == False):
            if self.switchOrder:
                self.reorder_rescale()
            try:
                filename = QtWidgets.QFileDialog.getOpenFileName()
                imagePath = filename[0]
                pixmap = QtGui.QPixmap(imagePath)
                img = Image.open(imagePath).convert("RGBA")
                self.image = image.ImageObject(img, imagePath, False)
            except:
                return
            if self.tha != None:
                self.horizontalLayout.removeItem(self.tha)
                self.tha = None
            self.labelWidget.setPixmap(pixmap.scaled(QtCore.QSize(600, 600), QtCore.Qt.KeepAspectRatio))
            if self.save != None:
                for i in reversed(range(self.horizontalLayout.count())):
                    self.horizontalLayout.itemAt(i).widget().setParent(None)
                self.labelWidget.setPixmap(ImageQt.toqpixmap(self.image.get_current_image()).scaled(QtCore.QSize(600, 600),
                                                                                                    QtCore.Qt.KeepAspectRatio))
                self.horizontalLayout.addWidget(self.labelWidget, 0, 0)
                self.save = None
            else:
                for i in reversed(range(self.horizontalLayout.count() - 1)):
                    self.horizontalLayout.itemAt(i + 1).widget().setParent(None)

    def save_file(self):
        if self.image != None and (self.processSwirl==False and self.processCustom==False):
            filePath = QtWidgets.QFileDialog.getSaveFileName(None, ("Save File"),
                                                             self.location + "/images",
                                                             ("Images (*.png *.jpg)"))

            if filePath[0] == "":
                return

            img = self.image.get_current_image()
            pixmap = ImageQt.toqpixmap(img)
            file_type = filePath[0].rpartition('.')

            if (file_type[2].upper == "PNG"):
                pixmap.save(filePath[0], "PNG")
            elif (file_type[2].upper == "JPG"):
                pixmap.save(filePath[0], "JPG")
            else:
                pixmap.save((filePath[0] + '.png'), "PNG")

            self.image.save_state = True

    def remove_custom_filter(self):
        if (self.processSwirl == False and self.processCustom == False):
            if self.tha != None:
                self.horizontalLayout.removeItem(self.tha)
                self.tha = None
            for i in reversed(range(self.horizontalLayout.count() - 1)):
                self.horizontalLayout.itemAt(i + 1).widget().setParent(None)
            self.save = self.horizontalLayout.itemAt(0).widget()
            self.horizontalLayout.itemAt(0).widget().setParent(None)

            nameCustomTextBox = QtWidgets.QLineEdit('fileToRemove')
            self.horizontalLayout.addWidget(nameCustomTextBox, 4, 0, 1, 2)
            subm = QtWidgets.QPushButton('Delete Filter')
            self.horizontalLayout.addWidget(subm, 4, 2, 1, 1)
            subm.clicked.connect(lambda: self.custom_filter_removal(nameCustomTextBox.text()))

            self.textBrowser = QtWidgets.QTextBrowser()
            self.horizontalLayout.addWidget(self.textBrowser, 0, 0, 3, 3)
            _translate = QtCore.QCoreApplication.translate
            self.textBrowser.setHtml(_translate("MainWindow",
                                                "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                "p, li { white-space: pre-wrap; }\n"
                                                "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
                                                "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; color:#00007f;\">Here, you can remove any custom filter you no longer want!  Just type the name of the custom filter you want to remove and ta-da, like magic, it's gone!\n\n\n</span></p></body></html>"))

    def custom_filter_removal(self, str):
        lis = []
        ret = False
        if not os.path.exists(self.home+'filter.txt'):
            f = open(self.home+'filter.txt', 'w')
            f.close()
        f = open(self.home+"filter.txt", "r")
        for x in f:
            x = x[0:len(x) - 1]
            if x != '' and x != str:
                lis.append(x)
            elif x == str and x != 'filter':
                ret = True
                os.remove(self.home+str + '.txt')
        f.close()
        file = open(self.home+"filter.txt", "w")
        for x in lis:
            file.write(x + '\n')
        file.close()

        message = ''
        color = "#00007f"
        if ret == True:
            message = "Filter removed successfully"
            color = "#23ce31"
        else:
            message = "No such filter found"
            color = "#cb0523"

        _translate = QtCore.QCoreApplication.translate
        self.textBrowser.setHtml(_translate("MainWindow",
                                            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                            "p, li { white-space: pre-wrap; }\n"
                                            "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
                                            "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; color:#00007f;\">Here, you can remove any custom filter you no longer want!  Just type the name of the custom filter you want to remove and ta-da, like magic, it's gone!</span></p><br></br><br></br><p align = \"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; color:" + color + ";\">" + message + "</body></html>"))

        self.currentCustom = 45
        self.tab_button(self, self.scrollAreaWidgetContents, (0, 0, 40, 40), "Add Custom Filter", "Add Filter")
        self.button.clicked.connect(self.add_custom)
        self.button.setIcon(QtGui.QIcon(self.location + "/images/add_filter.svg"))
        self.button.setIconSize(QtCore.QSize(40,40))
        self.button.setMaximumSize(40, 40)
        for i in reversed(range(self.horizontalLayout2.count())):
            self.horizontalLayout2.itemAt(i).widget().setParent(None)
        self.horizontalLayout2.addWidget(self.button, 0, QtCore.Qt.AlignLeft)
        self.tab_button(self, self.scrollAreaWidgetContents, (45, 0, 40, 40), "Remove Custom Filter", "Remove Filter")
        self.button.clicked.connect(self.remove_custom_filter)
        self.button.setIconSize(QtCore.QSize(40, 40))
        self.button.setIcon(QtGui.QIcon(self.location + "/images/remove.svg"))
        self.button.setMaximumSize(40, 40)
        self.horizontalLayout2.addWidget(self.button, 0, QtCore.Qt.AlignLeft)

        f = open(self.home+"filter.txt", "r")
        listo = {}
        for x in f:
            if x != '':
                y = x
                if x[len(x) - 1:len(x)] == '\n':
                    y = x[0:len(x) - 1]
                if y != 'filter' and os.path.exists(self.home+y + '.txt') and y not in listo:
                    listo[(y)] = 'hi'
                    self.currentCustom = self.currentCustom + 45
                    self.tab_button(self, self.scrollAreaWidgetContents, (self.currentCustom, 0, 40, 40), "Apply " + x,
                                    x)
                    self.button.setMaximumSize(40, 40)
                    self.button.clicked.connect(lambda checked, name=x: self.process_custom(name))
                    self.button.setIconSize(QtCore.QSize(40, 40))
                    self.button.setIcon(QtGui.QIcon(self.location + "/images/Custom.svg"))
                    self.horizontalLayout2.addWidget(self.button)
                    self.horizontalLayout2.addWidget(self.button, 0, QtCore.Qt.AlignLeft)
        f.close()

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.tabWidget.addTab(self.tab_custom, "Custom Filters")
        if (self.currentCustom + 45 >= 1174):
            self.scrollArea.setGeometry(QtCore.QRect(0, 0, 1174, 50))
        else:
            self.scrollArea.setGeometry(QtCore.QRect(0, 0, self.currentCustom + 53, 50))
        self.horizontalLayout2.setContentsMargins(1, 3, 7, 0)
        self.lister = ''
        self.tabWidget.setCurrentIndex(7)
        self.m.setParent(None)
        self.tab_frame(self, self.tab_custom, (self.currentCustom + 45, 0, 1, 61))

        # need to check if this is in the filter.txt file and if it is, then remove it from that file, remove the txt file with name str.txt and move all the other filters down a place

    def add_custom(self):
        if (self.processSwirl == False and self.processCustom == False):
            if self.tha != None:
                self.horizontalLayout.removeItem(self.tha)
                self.tha = None
            for i in reversed(range(self.horizontalLayout.count() - 1)):
                self.horizontalLayout.itemAt(i + 1).widget().setParent(None)
            self.save = self.horizontalLayout.itemAt(0).widget()
            self.horizontalLayout.itemAt(0).widget().setParent(None)
            self.textBrowser = QtWidgets.QTextBrowser()
            self.horizontalLayout.addWidget(self.textBrowser, 0, 0, 3, 3)
            _translate = QtCore.QCoreApplication.translate
            self.textBrowser.setHtml(_translate("MainWindow",
                                                "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                "p, li { white-space: pre-wrap; }\n"
                                                "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
                                                "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; color:#00007f;\">Here, you can create your own custom filters!  Just click on the filters you want to add in the order you want them and save your filter with a name (please only include alphanumeric characters or _ in name)!  When you\'re done, the filter will apply in your toolbar so you can apply it to any image!</span></p></body></html>"))

            self.ytinty = QtWidgets.QPushButton('Yellow Tint')
            self.horizontalLayout.addWidget(self.ytinty, 8, 0)
            self.ytinty.clicked.connect(lambda: self.add_filter('YellowT'))
            self.rrrotate = QtWidgets.QPushButton('Rotate Right')
            self.horizontalLayout.addWidget(self.rrrotate, 4, 0)
            self.rrrotate.clicked.connect(lambda: self.add_filter('RotateR'))
            self.lllrotate = QtWidgets.QPushButton('Rotate Left')
            self.horizontalLayout.addWidget(self.lllrotate, 4, 1)
            self.lllrotate.clicked.connect(lambda: self.add_filter('RotateL'))
            self.rrtint = QtWidgets.QPushButton('Redwood Tint')
            self.horizontalLayout.addWidget(self.rrtint, 8, 1)
            self.rrtint.clicked.connect(lambda: self.add_filter('RedT'))
            self.ssw = QtWidgets.QPushButton('Swirl')
            self.horizontalLayout.addWidget(self.ssw, 6, 1)
            self.ssw.clicked.connect(lambda: self.add_filter('Swirl'))
            self.sinv = QtWidgets.QPushButton('Invert Colors')
            self.horizontalLayout.addWidget(self.sinv, 7, 0)
            self.sinv.clicked.connect(lambda: self.add_filter('Invert'))
            self.spix = QtWidgets.QPushButton('Pixelate')
            self.horizontalLayout.addWidget(self.spix, 6, 0)
            self.spix.clicked.connect(lambda: self.add_filter('Pixelate'))
            self.smo = QtWidgets.QPushButton('Smooth')
            self.horizontalLayout.addWidget(self.smo, 5, 2)
            self.smo.clicked.connect(lambda: self.add_filter('Smooth'))
            self.enh = QtWidgets.QPushButton('Enhance')
            self.horizontalLayout.addWidget(self.enh, 5, 1)
            self.enh.clicked.connect(lambda: self.add_filter('Enhance'))
            self.rnoi = QtWidgets.QPushButton('Blur')
            self.horizontalLayout.addWidget(self.rnoi, 5, 0)
            self.rnoi.clicked.connect(lambda: self.add_filter('ReduceNoise'))
            self.sepio = QtWidgets.QPushButton('Sepia')
            self.horizontalLayout.addWidget(self.sepio, 7, 2)
            self.sepio.clicked.connect(lambda: self.add_filter('Sepia'))
            self.sbw = QtWidgets.QPushButton('Grayscale')
            self.horizontalLayout.addWidget(self.sbw, 7, 1)
            self.sbw.clicked.connect(lambda: self.add_filter('BlackWhite'))
            self.sby = QtWidgets.QPushButton('Aqua')
            self.horizontalLayout.addWidget(self.sby, 8, 2)
            self.sby.clicked.connect(lambda: self.add_filter('BlueYellow'))
            self.sgb = QtWidgets.QPushButton('Olive')
            self.horizontalLayout.addWidget(self.sgb, 9, 0)
            self.sgb.clicked.connect(lambda: self.add_filter('GreenBlue'))
            self.bri = QtWidgets.QPushButton('Brighten (Use Slider Above Then Click)')
            self.specialSlider = QtWidgets.QSlider()
            self.specialSlider.setValue(100)
            self.specialSlider.setTickPosition(100)
            self.specialSlider.setTickInterval(10)
            self.specialSlider.setMaximum(200)
            self.specialSlider.setMinimum(0)
            self.specialSlider.setOrientation(QtCore.Qt.Horizontal)
            self.horizontalLayout.addWidget(self.specialSlider, 11, 0)
            self.specialSlider.setMaximumSize(400, 10)
            self.horizontalLayout.addWidget(self.bri, 12, 0)
            self.bri.clicked.connect(lambda: self.add_filter('Brighten' + str(self.specialSlider.value())))
            self.tha = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
            self.horizontalLayout.addItem(self.tha, 10, 0, 1, 3)

            self.bri2 = QtWidgets.QPushButton('Transparency (Use Slider Above Then Click)')
            self.specialSlider2 = QtWidgets.QSlider()
            self.specialSlider2.setValue(100)
            self.specialSlider2.setTickPosition(100)
            self.specialSlider2.setTickInterval(10)
            self.specialSlider2.setMaximum(200)
            self.specialSlider2.setMinimum(0)
            self.specialSlider2.setOrientation(QtCore.Qt.Horizontal)
            self.horizontalLayout.addWidget(self.specialSlider2, 13, 1)
            self.specialSlider2.setMaximumSize(400, 10)
            self.horizontalLayout.addWidget(self.bri2, 14, 1)
            self.bri2.clicked.connect(lambda: self.add_filter('Transparency' + str(self.specialSlider2.value())))

            self.bri3 = QtWidgets.QPushButton('Contrast (Use Slider Above Then Click)')
            self.specialSlider3 = QtWidgets.QSlider()
            self.specialSlider3.setValue(100)
            self.specialSlider3.setTickPosition(100)
            self.specialSlider3.setTickInterval(10)
            self.specialSlider3.setMaximum(200)
            self.specialSlider3.setMinimum(0)
            self.specialSlider3.setOrientation(QtCore.Qt.Horizontal)
            self.horizontalLayout.addWidget(self.specialSlider3, 13, 2)
            self.specialSlider3.setMaximumSize(400, 10)
            self.horizontalLayout.addWidget(self.bri3, 14, 2)
            self.bri3.clicked.connect(lambda: self.add_filter('Contrast' + str(self.specialSlider3.value())))

            self.bri4 = QtWidgets.QPushButton('Saturation (Use Slider Above Then Click)')
            self.specialSlider4 = QtWidgets.QSlider()
            self.specialSlider4.setValue(100)
            self.specialSlider4.setTickPosition(100)
            self.specialSlider4.setTickInterval(10)
            self.specialSlider4.setMaximum(200)
            self.specialSlider4.setMinimum(0)
            self.specialSlider4.setOrientation(QtCore.Qt.Horizontal)
            self.horizontalLayout.addWidget(self.specialSlider4, 13, 0)
            self.specialSlider4.setMaximumSize(400, 10)
            self.horizontalLayout.addWidget(self.bri4, 14, 0)
            self.bri4.clicked.connect(lambda: self.add_filter('Intensity' + str(self.specialSlider4.value())))

            self.color2 = (0, 0, 0)
            self.choosecol = QtWidgets.QPushButton('Choose Border Color')
            self.horizontalLayout.addWidget(self.choosecol, 11, 1)
            self.choosecol.clicked.connect(self.color_select)
            self.bri5 = QtWidgets.QPushButton('Create Border (Use Slider and Color Selector Above Then Click)')
            self.specialSlider5 = QtWidgets.QSlider()
            self.specialSlider5.setValue(0)
            self.specialSlider5.setTickPosition(0)
            self.specialSlider5.setTickInterval(10)
            self.specialSlider5.setMaximum(200)
            self.specialSlider5.setMinimum(0)
            self.specialSlider5.setOrientation(QtCore.Qt.Horizontal)
            self.horizontalLayout.addWidget(self.specialSlider5, 11, 2)
            self.specialSlider5.setMaximumSize(400, 10)
            self.horizontalLayout.addWidget(self.bri5, 12, 1, 1, 2)
            self.bri5.clicked.connect(
                lambda: self.add_filter('Border' + str(self.specialSlider5.value()) + str(self.color2)))

            self.bri6 = QtWidgets.QPushButton('Choose File To Blend')
            self.hi = ''
            self.bri6.clicked.connect(self.choose_file)
            self.bri7 = QtWidgets.QPushButton("Blend (Use Slider and File Selector Above Then Click)")
            self.horizontalLayout.addWidget(self.bri6, 15, 0)
            self.specialSlider6 = QtWidgets.QSlider()
            self.specialSlider6.setValue(0)
            self.specialSlider6.setTickPosition(0)
            self.specialSlider6.setTickInterval(5)
            self.specialSlider6.setMaximum(100)
            self.specialSlider6.setMinimum(0)
            self.specialSlider6.setOrientation(QtCore.Qt.Horizontal)
            self.horizontalLayout.addWidget(self.specialSlider6, 15, 1)
            self.specialSlider6.setMaximumSize(400, 10)
            self.horizontalLayout.addWidget(self.bri7, 16, 0, 1, 2)
            self.bri7.clicked.connect(
                lambda: self.add_filter('Blend' + str(self.hi) + ' ' + str(self.specialSlider6.value())))

            self.nameCustomTextBox = QtWidgets.QLineEdit('customName')
            self.sflip = QtWidgets.QPushButton('Flip')
            self.horizontalLayout.addWidget(self.sflip, 4, 2)
            self.sflip.clicked.connect(lambda: self.add_filter('Flip'))
            self.horizontalLayout.addWidget(self.nameCustomTextBox, 18, 0, 2, 2)
            self.ssubm = QtWidgets.QPushButton('Create Filter')
            self.horizontalLayout.addWidget(self.ssubm, 18, 2, 2, 1)
            self.ssubm.clicked.connect(lambda: self.submit_name(self.nameCustomTextBox.text()))

    def add_filter(self, type):
        if self.lister != '':
            self.lister += '\n'
        self.lister += type

    def choose_file(self):
        self.hi = QtWidgets.QFileDialog.getOpenFileName()[0]

    def submit_name(self, name):
        if name == "" or name == 'filter' or name == 'filter\n':
            _translate = QtCore.QCoreApplication.translate
            self.textBrowser.setHtml(_translate("MainWindow",
                                                "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                "p, li { white-space: pre-wrap; }\n"
                                                "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
                                                "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; color:#00007f;\">Here, you can create your own custom filters!  Just click on the filters you want to add in the order you want them and save your filter with a name (please only include alphanumeric characters or _ in name)!  When you\'re done, the filter will apply in your toolbar so you can apply it to any image!</span></p><br></br><br></br><p align = \"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; color:#cb0523;\">Invalid Filter Name! Please Rename Your Filter!</body></html>"))

            return
        for i in name:
            if i not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_":
                _translate = QtCore.QCoreApplication.translate
                self.textBrowser.setHtml(_translate("MainWindow",
                                                    "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                    "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                    "p, li { white-space: pre-wrap; }\n"
                                                    "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
                                                    "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; color:#00007f;\">Here, you can create your own custom filters!  Just click on the filters you want to add in the order you want them and save your filter with a name (please only include alphanumeric characters or _ in name)!  When you\'re done, the filter will apply in your toolbar so you can apply it to any image!</span></p><br></br><br></br><p align = \"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; color:#cb0523;\">Invalid Filter Name! Please Rename Your Filter!</body></html>"))

                return
        if name in ["CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
                    "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"]:
            _translate = QtCore.QCoreApplication.translate
            self.textBrowser.setHtml(_translate("MainWindow",
                                                "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                "p, li { white-space: pre-wrap; }\n"
                                                "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
                                                "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; color:#00007f;\">Here, you can create your own custom filters!  Just click on the filters you want to add in the order you want them and save your filter with a name (please only include alphanumeric characters or _ in name)!  When you\'re done, the filter will apply in your toolbar so you can apply it to any image!</span></p><br></br><br></br><p align = \"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; color:#cb0523;\">Invalid Filter Name! Please Rename Your Filter!</body></html>"))

            return
        f = open(self.home+"filter.txt", "r")
        for i in f:
            if i[len(i) - 1:len(i)] == '\n':
                i = i[0:len(i) - 1]
            if i == name:
                _translate = QtCore.QCoreApplication.translate
                self.textBrowser.setHtml(_translate("MainWindow",
                                                    "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                    "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                    "p, li { white-space: pre-wrap; }\n"
                                                    "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
                                                    "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; color:#00007f;\">Here, you can create your own custom filters!  Just click on the filters you want to add in the order you want them and save your filter with a name (please only include alphanumeric characters or _ in name)!  When you\'re done, the filter will apply in your toolbar so you can apply it to any image!</span></p><br></br><br></br><p align = \"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; color:#cb0523;\">You already have a filter by this name! You must delete it first before adding one with the same name!</body></html>"))

                return
        boo = False
        if len(self.lister) > 0:
            file = open(self.home+name + ".txt", "w")
            file.write(self.lister)
            file.close()
            if not os.path.exists(self.home+'filter.txt'):
                f = open(self.home+'filter.txt', 'w')
                f.close()
            file = open(self.home+"filter.txt", "a")
            file.write(name + '\n')
            file.close()
            self.currentCustom = 45
            self.tab_button(self, self.scrollAreaWidgetContents, (0, 2, 40, 40), "Add Custom Filter", "Add Filter")
            self.button.clicked.connect(self.add_custom)
            self.button.setIconSize(QtCore.QSize(40, 40))
            self.button.setMaximumSize(40, 40)
            self.button.setIcon(QtGui.QIcon(self.location + "/images/add_filter.svg"))
            for i in reversed(range(self.horizontalLayout2.count())):
                self.horizontalLayout2.itemAt(i).widget().setParent(None)
            self.horizontalLayout2.addWidget(self.button, 0, QtCore.Qt.AlignLeft)
            self.tab_button(self, self.scrollAreaWidgetContents, (45, 0, 40, 40), "Remove Custom Filter",
                            "Remove Filter")
            self.button.clicked.connect(self.remove_custom_filter)
            self.button.setIconSize(QtCore.QSize(40, 40))
            self.button.setIcon(QtGui.QIcon(self.location + "/images/remove.svg"))
            self.button.setMaximumSize(40, 40)
            self.horizontalLayout2.addWidget(self.button, 0, QtCore.Qt.AlignLeft)

            f = open(self.home+"filter.txt", "r")
            listo = {}
            for x in f:
                if x != '':
                    y = x
                    if x[len(x) - 1:len(x)] == '\n':
                        y = x[0:len(x) - 1]
                    if y != 'filter' and os.path.exists(self.home+y + '.txt') and y not in listo:
                        listo[(y)] = 'hi'
                        self.currentCustom = self.currentCustom + 45
                        self.tab_button(self, self.scrollAreaWidgetContents, (self.currentCustom, 0, 40, 40),
                                        "Apply " + x, x)
                        self.button.setMaximumSize(40, 40)
                        self.button.clicked.connect(lambda checked, name=x: self.process_custom(name))
                        self.button.setIconSize(QtCore.QSize(40, 40))
                        self.button.setIcon(QtGui.QIcon(self.location + "/images/Custom.svg"))
                        self.horizontalLayout2.addWidget(self.button)
                        self.horizontalLayout2.addWidget(self.button, 0, QtCore.Qt.AlignLeft)
            f.close()
        else:
            boo = True
            _translate = QtCore.QCoreApplication.translate
            self.textBrowser.setHtml(_translate("MainWindow",
                                                "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                "p, li { white-space: pre-wrap; }\n"
                                                "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
                                                "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; color:#00007f;\">Here, you can create your own custom filters!  Just click on the filters you want to add in the order you want them and save your filter with a name (please only include alphanumeric characters or _ in name)!  When you\'re done, the filter will apply in your toolbar so you can apply it to any image!</span></p><br></br><br></br><p align = \"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; color:#cb0523;\">Please select at least one operation for your filter to do!</body></html>"))

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.tabWidget.addTab(self.tab_custom, "Custom Filters")
        if (self.currentCustom + 45 >= 1174):
            self.scrollArea.setGeometry(QtCore.QRect(0, 0, 1174, 50))
        else:
            self.scrollArea.setGeometry(QtCore.QRect(0, 0, self.currentCustom + 53, 50))
        self.horizontalLayout2.setContentsMargins(1, 3, 7, 0)
        self.lister = ''

        self.m.setParent(None)
        self.tab_frame(self, self.tab_custom, (self.currentCustom + 45, 0, 1, 61))
        self.tabWidget.setCurrentIndex(7)

        _translate = QtCore.QCoreApplication.translate
        if not boo:
            self.textBrowser.setHtml(_translate("MainWindow",
                                                "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                "p, li { white-space: pre-wrap; }\n"
                                                "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
                                                "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; color:#00007f;\">Here, you can create your own custom filters!  Just click on the filters you want to add in the order you want them and save your filter with a name (please only include alphanumeric characters or _ in name)!  When you\'re done, the filter will apply in your toolbar so you can apply it to any image!</span></p><br></br><br></br><p align = \"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; color:#23ce31;\">Filter added successfully!</body></html>"))

    def cleanup_ui(self):
        if self.image != None:
            if self.tha != None:
                self.horizontalLayout.removeItem(self.tha)
                self.tha = None
            if self.switchOrder:
                self.reorder_rescale()
            if self.save != None:
                for i in reversed(range(self.horizontalLayout.count())):
                    self.horizontalLayout.itemAt(i).widget().setParent(None)
                self.labelWidget.setPixmap(
                    ImageQt.toqpixmap(self.image.get_current_image()).scaled(QtCore.QSize(600, 600),
                                                                             QtCore.Qt.KeepAspectRatio))
                self.horizontalLayout.addWidget(self.labelWidget, 0, 0)
                self.save = None
            else:
                for i in reversed(range(self.horizontalLayout.count() - 1)):
                    self.horizontalLayout.itemAt(i + 1).widget().setParent(None)
            if self.loading_widget != None:
                self.loading_widget.hide()
                self.loading_widget.destroy()

    def undo(self):
        if self.image != None and (self.processSwirl==False and self.processCustom==False):
            self.cleanup_ui()
            if (self.image.get_index()) > 0:
                self.image.decrement_index()
                img = self.image.get_current_image()
                pixmap = ImageQt.toqpixmap(img)
                self.labelWidget.setPixmap(pixmap.scaled(QtCore.QSize(600, 600), QtCore.Qt.KeepAspectRatio))

    def redo(self):
        if self.image != None and (self.processSwirl==False and self.processCustom==False):
            self.cleanup_ui()
            if (self.image.get_index() < self.image.num_images() - 1):
                self.image.increment_index()
                img = self.image.get_current_image()
                pixmap = ImageQt.toqpixmap(img)
                self.labelWidget.setPixmap(pixmap.scaled(QtCore.QSize(600, 600), QtCore.Qt.KeepAspectRatio))

    def rotate_left(self):
        if self.image != None and (self.processSwirl==False and self.processCustom==False):
            self.cleanup_ui()
            img = self.image.get_current_image()
            self.image.increment_index()
            index = self.image.get_index()
            m_img = im_functions.left_rotate(img)  # Takes in PIL image and returns modified PIL image
            self.image.add_image(index, m_img)  # add modified image to object
            pixmap = ImageQt.toqpixmap(m_img)  # converts PIL to pixmap
            self.labelWidget.setPixmap(pixmap.scaled(QtCore.QSize(600, 600), QtCore.Qt.KeepAspectRatio))

    def rotate_right(self):
        if self.image != None and (self.processSwirl==False and self.processCustom==False):
            self.cleanup_ui()
            img = self.image.get_current_image()
            self.image.increment_index()
            index = self.image.get_index()
            m_img = im_functions.right_rotate(img)
            self.image.add_image(index, m_img)
            pixmap = ImageQt.toqpixmap(m_img)
            self.labelWidget.setPixmap(pixmap.scaled(QtCore.QSize(600, 600), QtCore.Qt.KeepAspectRatio))

    def flip(self):
        if self.image != None and (self.processSwirl==False and self.processCustom==False):
            self.cleanup_ui()
            img = self.image.get_current_image()
            self.image.increment_index()
            index = self.image.get_index()
            m_img = im_functions.flip(img)
            self.image.add_image(index, m_img)
            pixmap = ImageQt.toqpixmap(m_img)
            self.labelWidget.setPixmap(pixmap.scaled(QtCore.QSize(600, 600), QtCore.Qt.KeepAspectRatio))

    def brighten(self):
        if self.image != None and (self.processSwirl==False and self.processCustom==False):
            self.cleanup_ui()
            self.horizontalLayout.itemAt(0).widget().setParent(None)
            self.horizontalLayout.addWidget(self.labelWidget, 0, 0)
            self.labelWidget.setPixmap(ImageQt.toqpixmap(self.image.get_current_image()).scaled(QtCore.QSize(600, 600),
                                                                                                QtCore.Qt.KeepAspectRatio))
            self.save = self.labelWidget

            self.slider_widget = QtWidgets.QSlider()
            self.slider_widget.setMinimum(0)
            self.slider_widget.setMaximum(200)
            self.slider_widget.setTickInterval(10)
            self.slider_widget.setSliderPosition(100)
            self.slider_widget.setValue(100)
            self.horizontalLayout.addWidget(self.slider_widget, 10, 0)
            self.slider_widget.setOrientation(QtCore.Qt.Horizontal)
            self.slider_widget.valueChanged.connect(self.update_brightness)
            self.submit_widget = QtWidgets.QPushButton('Apply')
            self.horizontalLayout.addWidget(self.submit_widget, 10, 1)
            self.submit_widget.clicked.connect(self.submit_brightness)

    def update_brightness(self):
        img = ''
        try:
            img = self.image.get_current_image()
        except:
            img = self.image.get_original_image()
        self.new_bright = im_functions.adjust_brightness(img, self.slider_widget.value() / 100)
        pixmap = ImageQt.toqpixmap(self.new_bright)
        self.labelWidget.setPixmap(pixmap.scaled(QtCore.QSize(600, 600), QtCore.Qt.KeepAspectRatio))

    def submit_brightness(self):
        if self.slider_widget.value() != 100:
            try:
                self.image.increment_index()
                index = self.image.get_index()
                self.image.add_image(index, self.new_bright)
                self.save = None
                self.cleanup_ui()

            except:
                return
        else:
            return

    def update_label(self, value):
        self.slider_value = value / 100

    def change_transparency(self):
        if self.image != None and (self.processSwirl==False and self.processCustom==False):
            self.cleanup_ui()
            self.horizontalLayout.itemAt(0).widget().setParent(None)
            self.horizontalLayout.addWidget(self.labelWidget, 0, 0)
            self.labelWidget.setPixmap(ImageQt.toqpixmap(self.image.get_current_image()).scaled(QtCore.QSize(600, 600),
                                                                                                QtCore.Qt.KeepAspectRatio))
            self.save = self.labelWidget
            self.slider_widget = QtWidgets.QSlider()
            self.slider_widget.setMinimum(0)
            self.slider_widget.setMaximum(200)
            self.slider_widget.setTickInterval(10)
            self.slider_widget.setSliderPosition(100)
            self.slider_widget.setValue(100)
            self.horizontalLayout.addWidget(self.slider_widget, 19, 0)
            self.slider_widget.setOrientation(QtCore.Qt.Horizontal)
            self.slider_widget.valueChanged.connect(self.update_transparency)
            self.submit_widget = QtWidgets.QPushButton('Apply')
            self.horizontalLayout.addWidget(self.submit_widget, 19, 1)
            self.submit_widget.clicked.connect(self.submit_transparency)

    def update_transparency(self):
        img = ''
        try:
            img = self.image.get_current_image()
        except:
            img = self.image.get_original_image()
        self.new_trans = im_functions.adjust_transparency(img, self.slider_widget.value() / 100)
        pixmap = ImageQt.toqpixmap(self.new_trans)
        self.labelWidget.setPixmap(pixmap.scaled(QtCore.QSize(600, 600), QtCore.Qt.KeepAspectRatio))

    def submit_transparency(self):
        if self.slider_widget.value() != 100:
            try:
                self.image.increment_index()
                index = self.image.get_index()
                self.image.add_image(index, self.new_trans)
                self.save = None
                self.cleanup_ui()
            except:
                return
        else:
            return

    def change_contrast(self):
        if self.image != None and (self.processSwirl==False and self.processCustom==False):
            self.cleanup_ui()
            self.horizontalLayout.itemAt(0).widget().setParent(None)
            self.horizontalLayout.addWidget(self.labelWidget, 0, 0)
            self.labelWidget.setPixmap(ImageQt.toqpixmap(self.image.get_current_image()).scaled(QtCore.QSize(600, 600),
                                                                                                QtCore.Qt.KeepAspectRatio))
            self.save = self.labelWidget
            self.slider_widget = QtWidgets.QSlider()
            self.slider_widget.setMinimum(0)
            self.slider_widget.setMaximum(200)
            self.slider_widget.setTickInterval(10)
            self.slider_widget.setSliderPosition(100)
            self.slider_widget.setValue(100)
            self.horizontalLayout.addWidget(self.slider_widget, 19, 0)
            self.slider_widget.setOrientation(QtCore.Qt.Horizontal)
            self.slider_widget.valueChanged.connect(self.update_contrast)
            self.submit_widget = QtWidgets.QPushButton('Apply')
            self.horizontalLayout.addWidget(self.submit_widget, 19, 1)
            self.submit_widget.clicked.connect(self.submit_contrast)

    def update_contrast(self):
        img = ''
        try:
            img = self.image.get_current_image()
        except:
            img = self.image.get_original_image()

        self.new_cont = im_functions.adjust_contrast(img, self.slider_widget.value() / 100)
        pixmap = ImageQt.toqpixmap(self.new_cont)
        self.labelWidget.setPixmap(pixmap.scaled(QtCore.QSize(600, 600), QtCore.Qt.KeepAspectRatio))

    def submit_contrast(self):
        if self.slider_widget.value() != 100:
            try:
                self.image.increment_index()
                index = self.image.get_index()
                self.image.add_image(index, self.new_cont)
                self.save = None
                self.cleanup_ui()
            except:
                return
        else:
            return

    def change_saturation(self):
        if self.image != None and (self.processSwirl==False and self.processCustom==False):
            self.cleanup_ui()
            self.horizontalLayout.itemAt(0).widget().setParent(None)
            self.horizontalLayout.addWidget(self.labelWidget, 0, 0)
            self.labelWidget.setPixmap(ImageQt.toqpixmap(self.image.get_current_image()).scaled(QtCore.QSize(600, 600),
                                                                                                QtCore.Qt.KeepAspectRatio))
            self.save = self.labelWidget
            self.slider_widget = QtWidgets.QSlider()
            self.slider_widget.setMinimum(0)
            self.slider_widget.setMaximum(200)
            self.slider_widget.setTickInterval(10)
            self.slider_widget.setSliderPosition(100)
            self.slider_widget.setValue(100)
            self.horizontalLayout.addWidget(self.slider_widget, 19, 0)
            self.slider_widget.setOrientation(QtCore.Qt.Horizontal)
            self.slider_widget.valueChanged.connect(self.update_saturation)
            self.submit_widget = QtWidgets.QPushButton('Apply')
            self.horizontalLayout.addWidget(self.submit_widget, 19, 1)
            self.submit_widget.clicked.connect(self.submit_saturation)

    def update_saturation(self):
        img = ''
        try:
            img = self.image.get_current_image()
        except:
            img = self.image.get_original_image()

        self.new_sat = im_functions.adjust_saturation(img, self.slider_widget.value() / 100)
        pixmap = ImageQt.toqpixmap(self.new_sat)
        self.labelWidget.setPixmap(pixmap.scaled(QtCore.QSize(600, 600), QtCore.Qt.KeepAspectRatio))

    def submit_saturation(self):
        if self.slider_widget.value() != 100:
            try:
                self.image.increment_index()
                index = self.image.get_index()
                self.image.add_image(index, self.new_sat)
                self.save = None
                self.cleanup_ui()
            except:
                return
        else:
            return

    def crop(self):
        if self.image != None and (self.processSwirl==False and self.processCustom==False):
            self.cleanup_ui()
            self.labelWidget.setPixmap(ImageQt.toqpixmap(self.image.get_current_image()).scaled(QtCore.QSize(600, 600),
                                                                                                QtCore.Qt.KeepAspectRatio))
            self.save = self.labelWidget
            self.new_cro = None
            self.horizontalLayout.itemAt(0).widget().setParent(None)
            self.horizontalLayout.addWidget(self.labelWidget, 1, 1)
            self.slider_widgetBottom = QtWidgets.QSlider()
            self.slider_widgetBottom.setMinimum(0)
            self.slider_widgetBottom.setMaximum(200)
            self.slider_widgetBottom.setTickInterval(10)
            self.slider_widgetBottom.setSliderPosition(0)
            self.slider_widgetBottom.setValue(0)
            self.horizontalLayout.addWidget(self.slider_widgetBottom, 19, 1)
            self.slider_widgetBottom.setOrientation(QtCore.Qt.Horizontal)
            self.slider_widgetBottom.valueChanged.connect(self.update_crop)
            self.submit_widgetBottom = QtWidgets.QPushButton('Submit Change')
            self.horizontalLayout.addWidget(self.submit_widgetBottom, 20, 1)
            self.submit_widgetBottom.clicked.connect(self.submit_crop)

            self.slider_widgetTop = QtWidgets.QSlider()
            self.slider_widgetTop.setMinimum(0)
            self.slider_widgetTop.setMaximum(200)
            self.slider_widgetTop.setTickInterval(10)
            self.slider_widgetTop.setSliderPosition(200)
            self.slider_widgetTop.setValue(200)
            self.horizontalLayout.addWidget(self.slider_widgetTop, 0, 1)
            self.slider_widgetTop.setOrientation(QtCore.Qt.Horizontal)
            self.slider_widgetTop.valueChanged.connect(self.update_crop)

            self.slider_widgetRight = QtWidgets.QSlider()
            self.slider_widgetRight.setMinimum(0)
            self.slider_widgetRight.setMaximum(200)
            self.slider_widgetRight.setTickInterval(10)
            self.slider_widgetRight.setSliderPosition(200)
            self.slider_widgetRight.setValue(200)
            self.horizontalLayout.addWidget(self.slider_widgetRight, 1, 0)
            self.slider_widgetRight.setOrientation(QtCore.Qt.Vertical)
            self.slider_widgetRight.valueChanged.connect(self.update_crop)

            self.slider_widgetLeft = QtWidgets.QSlider()
            self.slider_widgetLeft.setMinimum(0)
            self.slider_widgetLeft.setMaximum(200)
            self.slider_widgetLeft.setTickInterval(10)
            self.slider_widgetLeft.setSliderPosition(0)
            self.slider_widgetLeft.setValue(0)
            self.horizontalLayout.addWidget(self.slider_widgetLeft, 1, 2)
            self.slider_widgetLeft.setOrientation(QtCore.Qt.Vertical)
            self.slider_widgetLeft.valueChanged.connect(self.update_crop)

            img = ''
            try:
                img = self.image.get_current_image()
            except:
                img = self.image.get_original_image()

            w, h = img.size
            self.mostRecentWMax = w
            self.mostRecentWMin = 0
            self.mostRecentHMax = h
            self.mostRecentHMin = 0

    def update_crop(self):
        img = ''
        try:
            img = self.image.get_current_image()
        except:
            img = self.image.get_original_image()

        w, h = img.size
        w2 = round(w / 2 + self.slider_widgetTop.value() / 200 * w / 2)
        w1 = round((w / 2 * self.slider_widgetBottom.value() / 200))
        h2 = round(h / 2 + (200 - self.slider_widgetLeft.value()) / 200 * h / 2)
        h1 = round((h / 2 * (200 - self.slider_widgetRight.value()) / 200))
        if w1 != w2 or h1 != h2:
            if w1 != w2 and h1 != h2:
                self.new_cro = im_functions.crop(img, w1, h1, w2, h2)
                self.mostRecentHMax = h2
                self.mostRecentHMin = h1
                self.mostRecentWMax = w2
                self.mostRecentWMin = w1

            if w1 == w2 and h1 != h2:
                self.new_cro = im_functions.crop(img, self.mostRecentWMin, h1, self.mostRecentWMax, h2)
                self.mostRecentHMax = h2
                self.mostRecentHMin = h1

            if w1 != w2 and h1 == h2:
                self.new_cro = im_functions.crop(img, w1, self.mostRecentHMin, w2, self.mostRecentHMax)
                self.mostRecentWMax = w2
                self.mostRecentWMin = w1

            pixmap = ImageQt.toqpixmap(self.new_cro)
            self.labelWidget.setPixmap(pixmap.scaled(QtCore.QSize(600, 600), QtCore.Qt.KeepAspectRatio))

    def submit_crop(self):
        if (self.new_cro != None):
            try:
                self.image.increment_index()
                index = self.image.get_index()
                self.image.add_image(index, self.new_cro)
                self.save = None
                self.new_cro = None
            except:
                return

    def apply_color_filter(self, r_val, g_val, b_val):
        img = self.image.get_current_image()
        self.image.increment_index()
        index = self.image.get_index()
        m_img = im_functions.color_filter(img, r_val, g_val, b_val)
        self.image.add_image(index, m_img)
        pixmap = ImageQt.toqpixmap(m_img)
        self.labelWidget.setPixmap(pixmap.scaled(QtCore.QSize(600, 600), QtCore.Qt.KeepAspectRatio))

    def yellow_tint(self):
        if self.image != None and (self.processSwirl==False and self.processCustom==False):
            self.cleanup_ui()
            self.apply_color_filter(25, 25, 0)

    def redwood(self):
        if self.image != None and (self.processSwirl==False and self.processCustom==False):
            self.cleanup_ui()
            self.apply_color_filter(40, 10, 0)

    def aqua(self):
        if self.image != None and (self.processSwirl==False and self.processCustom==False):
            self.cleanup_ui()
            self.apply_color_filter(0, 25, 50)

    def olive(self):
        if self.image != None and (self.processSwirl==False and self.processCustom==False):
            self.cleanup_ui()
            self.apply_color_filter(0, 50, 25)

    def grayscale(self):
        if self.image != None and (self.processSwirl==False and self.processCustom==False):
            self.cleanup_ui()
            img = self.image.get_current_image()
            self.image.increment_index()
            index = self.image.get_index()
            m_img = im_functions.grayscale_filter(img)
            self.image.add_image(index, m_img)
            pixmap = ImageQt.toqpixmap(m_img)
            self.labelWidget.setPixmap(pixmap.scaled(QtCore.QSize(600, 600), QtCore.Qt.KeepAspectRatio))

    def sepia(self):
        if self.image != None and (self.processSwirl==False and self.processCustom==False):
            self.cleanup_ui()
            img = self.image.get_current_image()
            self.image.increment_index()
            index = self.image.get_index()
            m_img = im_functions.sepia_filter(img)
            self.image.add_image(index, m_img)
            pixmap = ImageQt.toqpixmap(m_img)
            self.labelWidget.setPixmap(pixmap.scaled(QtCore.QSize(600, 600), QtCore.Qt.KeepAspectRatio))

    def do_custom(self, name):
        img = self.image.get_current_image()
        f = open(self.home+name[0:len(name) - 1] + ".txt", "r")
        for x in f:
            if x[len(x) - 1:len(x)] == '\n':
                x = x[0:len(x) - 1]
            if x == 'RotateL':
                img = im_functions.left_rotate(img)
            elif x == 'RotateR':
                img = im_functions.right_rotate(img)
            elif x == 'YellowT':
                img = im_functions.color_filter(img, 25, 25, 0)
            elif x == 'RedT':
                img = im_functions.color_filter(img, 40, 10, 0)
            elif x == 'Swirl':
                img = im_functions.swirl_effect(img)
            elif x == 'Invert':
                img = im_functions.invert_filter(img)
            elif x == 'GreenBlue':
                img = im_functions.color_filter(img, 0, 50, 25)
            elif x == 'BlackWhite':
                img = im_functions.grayscale_filter(img)
            elif x == 'Sepia':
                img = im_functions.sepia_filter(img)
            elif x == 'ReduceNoise':
                img = im_functions.blur(img)
            elif x == 'Enhance':
                img = im_functions.edge_enhance(img)
            elif x == 'Smooth':
                img = im_functions.smooth(img)
            elif x == 'Pixelate':
                img = im_functions.pixelate(img)
            elif x == 'BlueYellow':
                img = im_functions.color_filter(img, 0, 25, 50)
            elif x == 'Flip':
                img = im_functions.flip(img)
            elif len(x) >= 8 and x[0:8] == 'Brighten':
                num = 0
                try:
                    num = int(x[8:len(x)])
                    if num > 200 or num < 0:
                        continue
                except:
                    continue
                img = im_functions.adjust_brightness(img, num / 100)

            elif len(x) >= 12 and x[0:12] == 'Transparency':
                num = 0
                try:
                    num = int(x[12:len(x)])
                    if num > 200 or num < 0:
                        continue
                except:
                    continue
                img = im_functions.adjust_transparency(img, num / 100)

            elif len(x) >= 8 and x[0:8] == 'Contrast':
                num = 0
                try:
                    num = int(x[8:len(x)])
                    if num > 200 or num < 0:
                        continue
                except:
                    continue
                img = im_functions.adjust_contrast(img, num / 100)

            elif len(x) >= 9 and x[0:9] == 'Intensity':
                num = 0
                try:
                    num = int(x[9:len(x)])
                    if num > 200 or num < 0:
                        continue
                except:
                    continue
                img = im_functions.adjust_saturation(img, num / 100)

            elif len(x) >= 5 and x[0:5] == 'Blend':
                num = 0
                try:
                    y = x[5:x.index(' ')]
                    if not y.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                        continue
                    if not os.path.exists(y):
                        continue
                    im = ''
                    try:
                        im = Image.open(y).convert('RGBA')
                    except:
                        continue
                    num = int(x[x.index(' ') + 1:len(x)])
                    img = im_functions.blend(img, im, num / 100)
                except:
                    return

            elif len(x) >= 6 and x[0:6] == 'Border':
                num = 0
                tu = ''
                tickVal = ''
                try:
                    end = x.index("(")
                    num = int(x[6:end])
                    x = x[end + 1:len(x)]
                    p1 = x[0:x.index(',')]
                    x = x[x.index(',') + 2:len(x)]
                    p2 = x[0:x.index(',')]
                    x = x[x.index(',') + 2:len(x)]
                    p3 = ''
                    try:
                        p3 = x[0:x.index(',')]
                    except:
                        p3 = x[0:x.index(')')]

                    p1 = int(p1)
                    p2 = int(p2)
                    p3 = int(p3)

                    if num > 200 or num < 0 or p1 < 0 or p1 > 255 or p2 < 0 or p2 > 255 or p3 < 0 or p3 > 255:
                        continue

                    w, h = img.size
                    minimum = min(w, h)
                    tickVal = minimum / 200

                except:
                    continue
                img = im_functions.create_border(img, tickVal * num, (p1, p2, p3))

        f.close()
        self.image.increment_index()
        index = self.image.get_index()
        self.image.add_image(index, img)  # add modified image to object
        pixmap = ImageQt.toqpixmap(img)  # converts PIL to pixmap
        self.labelWidget.setPixmap(pixmap.scaled(QtCore.QSize(600, 600), QtCore.Qt.KeepAspectRatio))
        self.horizontalLayout.itemAt(0).widget().setParent(None)
        self.labelWidget.setPixmap(pixmap.scaled(QtCore.QSize(600, 600), QtCore.Qt.KeepAspectRatio))
        self.horizontalLayout.addWidget(self.labelWidget, 0, 0)
        self.loading_widget.hide()
        self.processCustom=False

    def process_custom(self, name):
        if self.image != None and (self.processSwirl==False):
            self.cleanup_ui()
            movie = QtGui.QMovie("images/loading.gif")
            self.loading_widget = QtWidgets.QLabel(self.centralwidget)
            movie.setScaledSize(QtCore.QSize(256, 256))
            self.loading_widget.setMovie(movie)
            self.loading_widget.setAlignment(QtCore.Qt.AlignCenter)
            x = self.frame.width()
            y = self.frame.height()
            self.loading_widget.setGeometry(QtCore.QRect((x / 2) - 100, (y / 2) - 50, 256, 256))
            movie.start()
            self.app.processEvents()
            self.loading_widget.show()
            self.loading_widget.update()
            self.processCustom=True
            run = threading.Thread(target=lambda: self.do_custom(name))
            run.start()

    def process_swirl(self):
        if self.image != None and (self.processCustom==False):
            self.cleanup_ui()
            movie = QtGui.QMovie("images/loading.gif")
            self.loading_widget = QtWidgets.QLabel(self.centralwidget)
            movie.setScaledSize(QtCore.QSize(256, 256))
            self.loading_widget.setMovie(movie)
            self.loading_widget.setAlignment(QtCore.Qt.AlignCenter)
            x = self.frame.width()
            y = self.frame.height()
            self.loading_widget.setGeometry(QtCore.QRect((x / 2) - 100, (y / 2) - 50, 256, 256))
            movie.start()
            self.app.processEvents()
            self.loading_widget.show()
            self.loading_widget.update()
            self.processSwirl=True
            run = threading.Thread(target=self.swirl)
            run.start()

    def swirl(self):
        img = self.image.get_current_image()
        self.image.increment_index()
        index = self.image.get_index()
        m_img = im_functions.swirl_effect(img)
        self.image.add_image(index, m_img)
        pixmap = ImageQt.toqpixmap(m_img)
        self.horizontalLayout.itemAt(0).widget().setParent(None)
        self.labelWidget.setPixmap(pixmap.scaled(QtCore.QSize(600, 600), QtCore.Qt.KeepAspectRatio))
        self.horizontalLayout.addWidget(self.labelWidget, 0, 0)
        self.loading_widget.hide()
        self.processSwirl=False

    def invert_colors(self):
        if self.image != None and (self.processSwirl==False and self.processCustom==False):
            self.cleanup_ui()
            img = self.image.get_current_image()
            self.image.increment_index()
            index = self.image.get_index()
            m_img = im_functions.invert_filter(img)
            self.image.add_image(index, m_img)
            pixmap = ImageQt.toqpixmap(m_img)
            self.labelWidget.setPixmap(pixmap.scaled(QtCore.QSize(600, 600), QtCore.Qt.KeepAspectRatio))

    def blur(self):
        if self.image != None and (self.processSwirl==False and self.processCustom==False):
            self.cleanup_ui()
            img = self.image.get_current_image()
            self.image.increment_index()
            index = self.image.get_index()
            m_img = im_functions.blur(img)
            self.image.add_image(index, m_img)
            pixmap = ImageQt.toqpixmap(m_img)
            self.labelWidget.setPixmap(pixmap.scaled(QtCore.QSize(600, 600), QtCore.Qt.KeepAspectRatio))

    def enhance(self):
        if self.image != None and (self.processSwirl==False and self.processCustom==False):
            self.cleanup_ui()
            img = self.image.get_current_image()
            self.image.increment_index()
            index = self.image.get_index()
            m_img = im_functions.edge_enhance(img)
            self.image.add_image(index, m_img)
            pixmap = ImageQt.toqpixmap(m_img)
            self.labelWidget.setPixmap(pixmap.scaled(QtCore.QSize(600, 600), QtCore.Qt.KeepAspectRatio))

    def add_border(self):
        if self.image != None and (self.processSwirl==False and self.processCustom==False):
            if self.tha != None:
                self.horizontalLayout.removeItem(self.tha)
                self.tha = None
            if self.switchOrder:
                self.reorder_rescale()
            if self.save != None:
                for i in reversed(range(self.horizontalLayout.count())):
                    self.horizontalLayout.itemAt(i).widget().setParent(None)
                self.labelWidget.setPixmap(
                    ImageQt.toqpixmap(self.image.get_current_image()).scaled(QtCore.QSize(600, 600),
                                                                             QtCore.Qt.KeepAspectRatio))
                self.horizontalLayout.addWidget(self.labelWidget, 0, 0)
                self.save = None
            else:
                for i in reversed(range(self.horizontalLayout.count() - 1)):
                    self.horizontalLayout.itemAt(i + 1).widget().setParent(None)
            if self.loading_widget != None:
                self.loading_widget.hide()
                self.loading_widget.destroy()

            self.labelWidget.setPixmap(ImageQt.toqpixmap(self.image.get_current_image()).scaled(QtCore.QSize(600, 600),
                                                                                                QtCore.Qt.KeepAspectRatio))
            self.horizontalLayout.itemAt(0).widget().setParent(None)
            self.horizontalLayout.addWidget(self.labelWidget,0,0)
            self.save = self.labelWidget
            self.slider_widget = QtWidgets.QSlider()
            self.slider_widget.setMinimum(0)
            self.slider_widget.setMaximum(200)
            self.slider_widget.setTickInterval(10)
            self.slider_widget.setSliderPosition(0)
            self.slider_widget.setValue(0)
            self.horizontalLayout.addWidget(self.slider_widget, 19, 0)
            self.slider_widget.setOrientation(QtCore.Qt.Horizontal)
            self.slider_widget.valueChanged.connect(self.update_border)
            self.color = (0, 0, 0)
            self.button3 = QtWidgets.QPushButton('Choose Border Color')
            self.horizontalLayout.addWidget(self.button3, 14, 0)
            self.button3.clicked.connect(self.border_color)
            self.submit_widget = QtWidgets.QPushButton('Apply')
            self.horizontalLayout.addWidget(self.submit_widget, 19, 1)
            self.submit_widget.clicked.connect(self.save_add_border)

    def border_color(self):
        self.color = QtWidgets.QColorDialog.getColor().getRgb()
        img = ''
        try:
            img = self.image.get_current_image()
        except:
            img = self.image.get_original_image()
        w, h = img.size
        minimum = min(w, h)
        tickVal = minimum / 200
        if (self.slider_widget.value() > 0):
            self.new_border = im_functions.create_border(img, tickVal * self.slider_widget.value(), self.color)
            pixmap = ImageQt.toqpixmap(self.new_border)
            self.labelWidget.setPixmap(pixmap.scaled(QtCore.QSize(600, 600), QtCore.Qt.KeepAspectRatio))

    def update_border(self):
        img = ''
        try:
            img = self.image.get_current_image()
        except:
            img = self.image.get_original_image()
        w, h = img.size
        minimum = min(w, h)
        tickVal = minimum / 200
        self.new_border = im_functions.create_border(img, (tickVal * self.slider_widget.value()), self.color)
        pixmap = ImageQt.toqpixmap(self.new_border)
        self.labelWidget.setPixmap(pixmap.scaled(QtCore.QSize(600, 600), QtCore.Qt.KeepAspectRatio))

    def save_add_border(self):
        if self.slider_widget.value() != 0:
            try:
                self.image.increment_index()
                index = self.image.get_index()
                self.image.add_image(index, self.new_border)
                self.save = None
                self.cleanup_ui()
            except:
                return
        else:
            return

    def color_select(self):
        self.color2 = QtWidgets.QColorDialog.getColor().getRgb()

    def smooth(self):
        if self.image != None and (self.processSwirl==False and self.processCustom==False):
            self.cleanup_ui()
            img = self.image.get_current_image()
            self.image.increment_index()
            index = self.image.get_index()
            m_img = im_functions.smooth(img)
            self.image.add_image(index, m_img)
            pixmap = ImageQt.toqpixmap(m_img)
            self.labelWidget.setPixmap(pixmap.scaled(QtCore.QSize(600, 600), QtCore.Qt.KeepAspectRatio))

    def pixelate(self):
        if self.image != None and (self.processSwirl==False and self.processCustom==False):
            self.cleanup_ui()
            img = self.image.get_current_image()
            self.image.increment_index()
            index = self.image.get_index()
            m_img = im_functions.pixelate(img)
            self.image.add_image(index, m_img)
            pixmap = ImageQt.toqpixmap(m_img)
            self.labelWidget.setPixmap(pixmap.scaled(QtCore.QSize(600, 600), QtCore.Qt.KeepAspectRatio))

    def before_after(self):
        if self.image != None and self.switchOrder == False and (self.processSwirl==False and self.processCustom==False):
            self.cleanup_ui()
            self.labelWidget2 = QtWidgets.QLabel(self.frame)
            self.labelWidget.setPixmap(
                QtGui.QPixmap(self.labelWidget.pixmap().scaled(QtCore.QSize(600, 600), QtCore.Qt.KeepAspectRatio)))
            self.horizontalLayout.itemAt(0).widget().setParent(None)
            self.labelWidget2.setPixmap(
                QtGui.QPixmap(ImageQt.toqpixmap(self.image.get_original_image()).scaled(QtCore.QSize(600, 600),
                                                                                        QtCore.Qt.KeepAspectRatio)))
            self.horizontalLayout.addWidget(self.labelWidget2, 0, 0)
            self.horizontalLayout.addWidget(self.labelWidget, 0, 1)
            self.switchOrder = True

        elif self.image != None and self.switchOrder == True:
            self.cleanup_ui()

    def reorder_rescale(self):
        self.switchOrder = False
        self.horizontalLayout.itemAt(1).widget().setParent(None)
        self.horizontalLayout.itemAt(0).widget().setParent(None)
        image = self.image.get_current_image()
        self.labelWidget.setPixmap(
            QtGui.QPixmap(ImageQt.toqpixmap(image).scaled(QtCore.QSize(600, 600), QtCore.Qt.KeepAspectRatio)))
        self.horizontalLayout.addWidget(self.labelWidget, 0, 0)

    def blend(self):
        try:

            img = self.image.get_current_image()
            self.blImage = im_functions.blend(img, self.imagine, self.slider_widget.value() / 100)
            pixmap = ImageQt.toqpixmap(self.blImage)
            self.labelWidget.setPixmap(pixmap.scaled(QtCore.QSize(600, 600), QtCore.Qt.KeepAspectRatio))

        except:
            return

    def blend_save(self):
        if self.slider_widget.value() != 0:
            try:
                self.image.increment_index()
                index = self.image.get_index()
                self.image.add_image(index, self.blImage)
                self.save = None
                self.cleanup_ui()
            except:
                return
        else:
            return

    def open_second_img(self, secondImage):
        try:
            if self.image != None and (self.processSwirl==False and self.processCustom==False):
                if self.tha != None:
                    self.horizontalLayout.removeItem(self.tha)
                    self.tha = None
                if self.switchOrder:
                    self.reorder_rescale()
                if self.save != None:
                    for i in reversed(range(self.horizontalLayout.count())):
                        self.horizontalLayout.itemAt(i).widget().setParent(None)
                    self.labelWidget.setPixmap(
                        ImageQt.toqpixmap(self.image.get_current_image()).scaled(QtCore.QSize(600, 600),
                                                                                 QtCore.Qt.KeepAspectRatio))
                    self.horizontalLayout.addWidget(self.labelWidget, 0, 0)
                    self.save = None
                else:
                    for i in reversed(range(self.horizontalLayout.count() - 1)):
                        self.horizontalLayout.itemAt(i + 1).widget().setParent(None)
                if self.loading_widget != None:
                    self.loading_widget.hide()
                    self.loading_widget.destroy()
                self.labelWidget.setPixmap(
                    ImageQt.toqpixmap(self.image.get_current_image()).scaled(QtCore.QSize(600, 600),
                                                                             QtCore.Qt.KeepAspectRatio))
                self.horizontalLayout.itemAt(0).widget().setParent(None)
                self.horizontalLayout.addWidget(self.labelWidget, 0, 0)
                self.save = self.labelWidget
                filename = QtWidgets.QFileDialog.getOpenFileName()
                imagePath = filename[0]
                pixmap = QtGui.QPixmap(imagePath)
                self.imagine = Image.open(imagePath).convert("RGBA")
                self.labelWidget3 = QtWidgets.QLabel()
                self.labelWidget3.setPixmap(
                    QtGui.QPixmap(
                        ImageQt.toqpixmap(self.imagine).scaled(QtCore.QSize(600, 600), QtCore.Qt.KeepAspectRatio)))
                self.horizontalLayout.addWidget(self.labelWidget3, 0, 1)
                self.bu = QtWidgets.QPushButton("Apply")
                self.horizontalLayout.addWidget(self.bu, 19,2)
                self.bu.clicked.connect(self.blend_save)
                self.slider_widget = QtWidgets.QSlider()
                self.slider_widget.setMinimum(0)
                self.slider_widget.setMaximum(100)
                self.slider_widget.setTickInterval(5)
                self.slider_widget.setSliderPosition(0)
                self.slider_widget.setValue(0)
                self.horizontalLayout.addWidget(self.slider_widget, 19, 0,1,2)
                self.bu.setMaximumSize(95,40)
                self.slider_widget.setOrientation(QtCore.Qt.Horizontal)
                self.slider_widget.valueChanged.connect(self.blend)
        except:
            return

        # additional image is now held in other_image attribute
