# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parsec/core/gui/forms/workspace_sharing_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WorkspaceSharingWidget(object):
    def setupUi(self, WorkspaceSharingWidget):
        WorkspaceSharingWidget.setObjectName("WorkspaceSharingWidget")
        WorkspaceSharingWidget.resize(474, 468)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(WorkspaceSharingWidget.sizePolicy().hasHeightForWidth())
        WorkspaceSharingWidget.setSizePolicy(sizePolicy)
        WorkspaceSharingWidget.setStyleSheet("#WorkspaceSharingWidget {\n"
"    background-color: #F4F4F4;\n"
"}\n"
"\n"
"#scroll_content, #widget_users {\n"
"    background-color: #FFFFFF;\n"
"    border-radius: 8px;\n"
"}\n"
"\n"
"#button_share, #button_apply {\n"
"    text-transform: uppercase;\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(WorkspaceSharingWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_add = QtWidgets.QWidget(WorkspaceSharingWidget)
        self.widget_add.setObjectName("widget_add")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widget_add)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.line_edit_share = QtWidgets.QLineEdit(self.widget_add)
        self.line_edit_share.setMinimumSize(QtCore.QSize(0, 32))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.line_edit_share.setFont(font)
        self.line_edit_share.setText("")
        self.line_edit_share.setObjectName("line_edit_share")
        self.horizontalLayout_6.addWidget(self.line_edit_share)
        self.combo_role = ComboBox(self.widget_add)
        self.combo_role.setEnabled(True)
        self.combo_role.setMinimumSize(QtCore.QSize(150, 32))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.combo_role.setFont(font)
        self.combo_role.setToolTip("")
        self.combo_role.setObjectName("combo_role")
        self.horizontalLayout_6.addWidget(self.combo_role)
        self.verticalLayout_4.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 5, -1, 5)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.button_share = QtWidgets.QPushButton(self.widget_add)
        self.button_share.setEnabled(False)
        self.button_share.setMinimumSize(QtCore.QSize(0, 32))
        font = QtGui.QFont()
        self.button_share.setFont(font)
        self.button_share.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_share.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.button_share.setIconSize(QtCore.QSize(16, 16))
        self.button_share.setObjectName("button_share")
        self.horizontalLayout_2.addWidget(self.button_share)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addWidget(self.widget_add)
        self.widget_users = QtWidgets.QWidget(WorkspaceSharingWidget)
        self.widget_users.setMinimumSize(QtCore.QSize(400, 250))
        self.widget_users.setObjectName("widget_users")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.widget_users)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.scrollArea = QtWidgets.QScrollArea(self.widget_users)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setFrameShadow(QtWidgets.QFrame.Plain)
        self.scrollArea.setLineWidth(0)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scroll_content = QtWidgets.QWidget()
        self.scroll_content.setGeometry(QtCore.QRect(0, 0, 474, 267))
        self.scroll_content.setObjectName("scroll_content")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.scroll_content)
        self.verticalLayout_3.setContentsMargins(20, 10, 0, 10)
        self.verticalLayout_3.setSpacing(5)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.scrollArea.setWidget(self.scroll_content)
        self.verticalLayout_5.addWidget(self.scrollArea)
        self.verticalLayout.addWidget(self.widget_users)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.check_show_revoked = QtWidgets.QCheckBox(WorkspaceSharingWidget)
        self.check_show_revoked.setObjectName("check_show_revoked")
        self.horizontalLayout_4.addWidget(self.check_show_revoked)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem3)
        self.button_apply = QtWidgets.QPushButton(WorkspaceSharingWidget)
        self.button_apply.setEnabled(False)
        self.button_apply.setMinimumSize(QtCore.QSize(0, 32))
        font = QtGui.QFont()
        self.button_apply.setFont(font)
        self.button_apply.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_apply.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.button_apply.setIconSize(QtCore.QSize(16, 16))
        self.button_apply.setObjectName("button_apply")
        self.horizontalLayout_5.addWidget(self.button_apply)
        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.retranslateUi(WorkspaceSharingWidget)
        QtCore.QMetaObject.connectSlotsByName(WorkspaceSharingWidget)

    def retranslateUi(self, WorkspaceSharingWidget):
        _translate = QtCore.QCoreApplication.translate
        self.line_edit_share.setPlaceholderText(_translate("WorkspaceSharingWidget", "TEXT_WORKSPACE_SHARING_USER_SEARCH_PLACEHOLDER"))
        self.button_share.setText(_translate("WorkspaceSharingWidget", "ACTION_WORKSPACE_SHARING_SHARE"))
        self.check_show_revoked.setText(_translate("WorkspaceSharingWidget", "TEXT_WORKSPACE_SHARING_CHECK_SHOW_REVOKED_USER"))
        self.button_apply.setText(_translate("WorkspaceSharingWidget", "ACTION_WORKSPACE_SHARING_UPDATE_ROLES"))
from parsec.core.gui.custom_widgets import ComboBox
