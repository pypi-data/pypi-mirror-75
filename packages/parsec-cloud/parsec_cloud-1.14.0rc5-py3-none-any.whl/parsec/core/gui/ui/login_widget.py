# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parsec/core/gui/forms/login_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LoginWidget(object):
    def setupUi(self, LoginWidget):
        LoginWidget.setObjectName("LoginWidget")
        LoginWidget.resize(513, 594)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(LoginWidget.sizePolicy().hasHeightForWidth())
        LoginWidget.setSizePolicy(sizePolicy)
        LoginWidget.setMinimumSize(QtCore.QSize(0, 0))
        LoginWidget.setAutoFillBackground(False)
        LoginWidget.setStyleSheet("#line_edit_password, #combo_username {\n"
"    border: none;\n"
"}\n"
"\n"
"#label_username, #label_password {\n"
"    color: #999999;\n"
"}\n"
"\n"
"#button_login {\n"
"    text-transform: uppercase;\n"
"}")
        self.horizontalLayout = QtWidgets.QHBoxLayout(LoginWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.widget = QtWidgets.QWidget(LoginWidget)
        self.widget.setMinimumSize(QtCore.QSize(300, 300))
        self.widget.setMaximumSize(QtCore.QSize(300, 300))
        self.widget.setObjectName("widget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(30)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setMinimumSize(QtCore.QSize(230, 40))
        self.label_3.setMaximumSize(QtCore.QSize(230, 40))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap(":/logos/images/logos/parsec.png"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.widget_login = QtWidgets.QWidget(self.widget)
        self.widget_login.setFocusPolicy(QtCore.Qt.NoFocus)
        self.widget_login.setObjectName("widget_login")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.widget_login)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(10)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setSpacing(5)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_username = QtWidgets.QLabel(self.widget_login)
        self.label_username.setObjectName("label_username")
        self.verticalLayout_4.addWidget(self.label_username)
        self.combo_username = ComboBox(self.widget_login)
        self.combo_username.setObjectName("combo_username")
        self.verticalLayout_4.addWidget(self.combo_username)
        self.verticalLayout_2.addLayout(self.verticalLayout_4)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setSpacing(5)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_password = QtWidgets.QLabel(self.widget_login)
        self.label_password.setObjectName("label_password")
        self.verticalLayout_5.addWidget(self.label_password)
        self.line_edit_password = QtWidgets.QLineEdit(self.widget_login)
        self.line_edit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.line_edit_password.setObjectName("line_edit_password")
        self.verticalLayout_5.addWidget(self.line_edit_password)
        self.verticalLayout_2.addLayout(self.verticalLayout_5)
        self.button_login = QtWidgets.QPushButton(self.widget_login)
        self.button_login.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_login.setObjectName("button_login")
        self.verticalLayout_2.addWidget(self.button_login)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem4)
        self.verticalLayout_6.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addWidget(self.widget_login)
        self.widget_no_device = QtWidgets.QWidget(self.widget)
        self.widget_no_device.setObjectName("widget_no_device")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.widget_no_device)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setSpacing(10)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_no_device = QtWidgets.QLabel(self.widget_no_device)
        self.label_no_device.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.label_no_device.setWordWrap(True)
        self.label_no_device.setObjectName("label_no_device")
        self.verticalLayout_7.addWidget(self.label_no_device)
        self.button_create_org = QtWidgets.QPushButton(self.widget_no_device)
        self.button_create_org.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.button_create_org.setObjectName("button_create_org")
        self.verticalLayout_7.addWidget(self.button_create_org)
        self.button_join_org = QtWidgets.QPushButton(self.widget_no_device)
        self.button_join_org.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.button_join_org.setObjectName("button_join_org")
        self.verticalLayout_7.addWidget(self.button_join_org)
        self.verticalLayout_3.addWidget(self.widget_no_device)
        self.verticalLayout.addWidget(self.widget)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem5)
        self.horizontalLayout.addLayout(self.verticalLayout)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem6)

        self.retranslateUi(LoginWidget)
        QtCore.QMetaObject.connectSlotsByName(LoginWidget)

    def retranslateUi(self, LoginWidget):
        _translate = QtCore.QCoreApplication.translate
        LoginWidget.setWindowTitle(_translate("LoginWidget", "Form"))
        self.label_username.setText(_translate("LoginWidget", "TEXT_LABEL_USER_NAME"))
        self.label_password.setText(_translate("LoginWidget", "TEXT_LABEL_PASSWORD"))
        self.button_login.setText(_translate("LoginWidget", "ACTION_LOG_IN"))
        self.label_no_device.setText(_translate("LoginWidget", "TEXT_LOGIN_NO_AVAILABLE_DEVICE"))
        self.button_create_org.setText(_translate("LoginWidget", "ACTION_MAIN_MENU_CREATE_ORGANIZATION"))
        self.button_join_org.setText(_translate("LoginWidget", "ACTION_MAIN_MENU_JOIN_ORGANIZATION"))
from parsec.core.gui.custom_widgets import ComboBox
from parsec.core.gui import resources_rc
