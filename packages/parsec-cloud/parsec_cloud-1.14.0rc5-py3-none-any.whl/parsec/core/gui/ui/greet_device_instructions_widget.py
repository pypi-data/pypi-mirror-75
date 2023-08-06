# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parsec/core/gui/forms/greet_device_instructions_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GreetDeviceInstructionsWidget(object):
    def setupUi(self, GreetDeviceInstructionsWidget):
        GreetDeviceInstructionsWidget.setObjectName("GreetDeviceInstructionsWidget")
        GreetDeviceInstructionsWidget.resize(400, 227)
        self.verticalLayout = QtWidgets.QVBoxLayout(GreetDeviceInstructionsWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_instructions = QtWidgets.QLabel(GreetDeviceInstructionsWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_instructions.sizePolicy().hasHeightForWidth())
        self.label_instructions.setSizePolicy(sizePolicy)
        self.label_instructions.setWordWrap(True)
        self.label_instructions.setObjectName("label_instructions")
        self.verticalLayout.addWidget(self.label_instructions)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.button_copy_addr = QtWidgets.QPushButton(GreetDeviceInstructionsWidget)
        self.button_copy_addr.setObjectName("button_copy_addr")
        self.horizontalLayout_2.addWidget(self.button_copy_addr)
        self.button_send_email = QtWidgets.QPushButton(GreetDeviceInstructionsWidget)
        self.button_send_email.setObjectName("button_send_email")
        self.horizontalLayout_2.addWidget(self.button_send_email)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.button_start = QtWidgets.QPushButton(GreetDeviceInstructionsWidget)
        self.button_start.setObjectName("button_start")
        self.horizontalLayout.addWidget(self.button_start)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(GreetDeviceInstructionsWidget)
        QtCore.QMetaObject.connectSlotsByName(GreetDeviceInstructionsWidget)

    def retranslateUi(self, GreetDeviceInstructionsWidget):
        _translate = QtCore.QCoreApplication.translate
        GreetDeviceInstructionsWidget.setWindowTitle(_translate("GreetDeviceInstructionsWidget", "Form"))
        self.label_instructions.setText(_translate("GreetDeviceInstructionsWidget", "TEXT_GREET_DEVICE_INSTRUCTIONS"))
        self.button_copy_addr.setText(_translate("GreetDeviceInstructionsWidget", "ACTION_COPY_ADDR"))
        self.button_send_email.setText(_translate("GreetDeviceInstructionsWidget", "ACTION_SEND_EMAIL"))
        self.button_start.setText(_translate("GreetDeviceInstructionsWidget", "ACTION_START"))
