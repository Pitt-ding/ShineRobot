#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Version : PyCharm
# @Time    : 2022/12/30 18:16
# @Author  : Pitt.Ding
# @File    : ShineRobot_main.py
# @Description :

import sys
import time
import ctypes
import re
import struct
from PyQt5 import QtCore
from ShineRobot import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QAction
from PyQt5.Qt import QStandardItemModel, QCursor, Qt, QThread, pyqtSignal
from PyQt5.QtGui import QTextCursor
from shine_robot_socket_communication import SocketServer, SocketServerCloseClient, SocketClient, SocketCommunicate
from functools import partial
from Pyqt_Quaternion_Euler import QuaternionEuler


class SocketWidgetStruct:
    def __int__(self):
        self.send_fun = None
        self.receive_fun = None
        self.log_fun = None
        # self.send_continue = None
        # self.send_interval = None

        self.lineEdit_IP = None
        self.lineEdit_Port = None
        self.pushButton_CreateConnection = None
        self.pushButton_CloseConnection = None
        self.checkBox_SendStringMode = None
        self.lineEdit_StrSendSeparator = None
        self.checkBox_SendRawbytesMode = None

        self.checkBox_Send_Int = None
        self.spinBox_Send_Int = None
        self.lineEdit_Send_Int = None
        self.checkBox_Send_Float = None
        self.spinBox_Send_Float = None
        self.lineEdit_Send_Float = None
        self.checkBox_Send_Str = None
        self.spinBox_Send_Str = None
        self.lineEdit_Send_Str = None

        self.lineEdit_SendFullType = None
        self.lineEdit_SendFormatStr = None

        self.checkBox_ReceiveStrMode = None
        self.lineEdit_StrReceiveSeparator = None
        self.checkBox_ReceiveRawbytesMode = None

        self.checkBox_Receive_Int = None
        self.spinBox_Receive_Int = None
        self.lineEdit_Receive_Int = None
        self.checkBox_Receive_Float = None
        self.spinBox_Receive_Float = None
        self.lineEdit_Receive_Float = None
        self.checkBox_Receive_Str = None
        self.spinBox_Receive_Str = None
        self.spinBox_ReceiveRawLength = None
        self.lineEdit_Receive_Str = None

        self.lineEdit_ReceiveFullType = None
        self.lineEdit_ReceiveFormatStr = None
        self.pushButton_Send = None
        self.checkBox_SendContinue = None
        self.lineEdit_SendInterval = None
        self.pushButton_Receive = None
        self.checkBox_RecvContinue = None
        self.lineEdit_RecvInterval = None
        self.pushButton_ClearCache = None


class MyMainWindow(QMainWindow, Ui_MainWindow):
    # Signal should define in class not in instance
    signal_socket_server_create_connection = pyqtSignal(tuple)
    signal_socket_client_create_connection = pyqtSignal(tuple)
    signal_socket_server_not_accepted_close = pyqtSignal(tuple)
    signal_server_send = pyqtSignal(bytes)
    # signal that send interval check valid in order to update send parameters
    signal_client_send = pyqtSignal(bytes)

    # widget style sheet
    str_lineedit_style_invalid = "QLineEdit{background-color: rgb(253, 183, 184)}"
    str_lineedit_style_enable = "QLineEdit{background-color: rgb(255, 255, 255)}"
    str_lineedit_style_disable = "QLineEdit{background-color: rgb(200, 200, 200)};"
    str_spinbox_style_enable = "QSpinBox{background-color: rgb(255, 255, 255)}"
    str_spinbox_style_invalid = "QSpinBox{background-color: rgb(253, 183, 184)}"
    str_spinbox_style_disable = "QSpinBox{background-color: rgb(200, 200, 200)}"

    def __init__(self) -> None:
        super(MyMainWindow, self).__init__()

        self.setupUi(self)
        self.right_click_menu = QMenu()
        self.quaternion_euler_ins = QuaternionEuler()
        # socket server
        # self.b_close_not_accepted_server = False
        self.socket_server = SocketServer()

        # socket server close client used to close blocking socket server
        self.socket_server_client = SocketServerCloseClient()
        # socket client
        self.socket_client = SocketClient()
        # socket communication thread
        self.Thread_socket_server = QThread()
        self.thread_close_socket_server = QThread()
        self.thread_socket_client = QThread()

        self.socket_server.moveToThread(self.Thread_socket_server)
        self.socket_server_client.moveToThread(self.thread_close_socket_server)
        self.socket_client.moveToThread(self.thread_socket_client)
        self.Thread_socket_server.start()
        self.thread_close_socket_server.start()
        self.thread_socket_client.start()
        # append icon to taskbar in Windows system
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")

        # server widgets
        self.server_widgets_status = SocketWidgetStruct()
        # self.server_widgets_status.send_fun = self.socket_server.socket_send_bytes
        # self.server_widgets_status.receive_fun = self.socket_server.socket_receive_bytes
        self.server_widgets_status.lineEdit_IP = self.lineEdit_SevIP
        self.server_widgets_status.lineEdit_Port = self.lineEdit_SerPort
        self.server_widgets_status.pushButton_CreateConnection = self.pushButton_SerCreateConn
        self.server_widgets_status.pushButton_CloseConnection = self.pushButton_SerCloseConn
        self.server_widgets_status.log_fun = self.record_socket_communication_result

        self.server_widgets_status.checkBox_SendStringMode = self.checkBox_ServerSendString
        self.server_widgets_status.lineEdit_StrSendSeparator = self.lineEdit_ServerSendSeparator
        self.server_widgets_status.checkBox_SendRawbytesMode = self.checkBox_ServerSendRawbytes

        self.server_widgets_status.checkBox_Send_Int = self.checkBox_SerSendInt
        self.server_widgets_status.spinBox_Send_Int = self.spinBox_SerSendInt_Seq
        self.server_widgets_status.lineEdit_Send_Int = self.lineEdit_SerSendInt_Value
        self.server_widgets_status.checkBox_Send_Float = self.checkBox_SerSendFloat
        self.server_widgets_status.spinBox_Send_Float = self.spinBox_SerSendFloat_Seq
        self.server_widgets_status.lineEdit_Send_Float = self.lineEdit_SerSendFloat_Value
        self.server_widgets_status.checkBox_Send_Str = self.checkBox_SerSendStr
        self.server_widgets_status.spinBox_Send_Str = self.spinBox_SerSendStr_Seq
        self.server_widgets_status.lineEdit_Send_Str = self.lineEdit_SerSendstr_Value

        self.server_widgets_status.lineEdit_SendFullType = self.lineEdit_SerSendFullType
        self.server_widgets_status.lineEdit_SendFormatStr = self.lineEdit_SerSendFormatStr

        self.server_widgets_status.checkBox_ReceiveStrMode = self.checkBox_ServerReceiveString
        self.server_widgets_status.lineEdit_StrReceiveSeparator = self.lineEdit_ServerReceiveSeparator
        self.server_widgets_status.checkBox_ReceiveRawbytesMode = self.checkBox_ServerReceiveRawbytes

        self.server_widgets_status.checkBox_Receive_Int = self.checkBox_SerRecvInt
        self.server_widgets_status.spinBox_Receive_Int = self.spinBox_SerRecvInt_Seq
        self.server_widgets_status.lineEdit_Receive_Int = self.lineEdit_SerRecvInt_Value
        self.server_widgets_status.checkBox_Receive_Float = self.checkBox_SerRecvFloat
        self.server_widgets_status.spinBox_Receive_Float = self.spinBox_SerRecvFloat_Seq
        self.server_widgets_status.lineEdit_Receive_Float = self.lineEdit_SerRecvFloat_Value
        self.server_widgets_status.checkBox_Receive_Str = self.checkBox_SerRecvStr
        self.server_widgets_status.spinBox_Receive_Str = self.spinBox_SerRecvStr_Seq
        self.server_widgets_status.lineEdit_Receive_Str = self.lineEdit_SerRecvStr_Value
        self.server_widgets_status.lineEdit_ReceiveFullType = self.lineEdit_SerRecvFullType
        self.server_widgets_status.lineEdit_ReceiveFormatStr = self.lineEdit_SerRecvFormatStr

        self.server_widgets_status.pushButton_Send = self.pushButton_SerSend
        self.server_widgets_status.send_continue = self.socket_server.b_continue_send
        self.server_widgets_status.send_interval = self.socket_server.str_send_interval
        self.server_widgets_status.checkBox_SendContinue = self.checkBox_SerContinueSend
        self.server_widgets_status.lineEdit_SendInterval = self.lineEdit_SerSendInterval
        self.server_widgets_status.pushButton_Receive = self.pushButton_SerRecv
        self.server_widgets_status.spinBox_ReceiveRawLength = self.spinBox_SerRecvRawLength
        self.server_widgets_status.checkBox_RecvContinue = self.checkBox_SerContinueRecv
        self.server_widgets_status.lineEdit_RecvInterval = self.lineEdit_SerRecvInterval
        self.server_widgets_status.pushButton_ClearCache = self.pushButton_SerClearCache

        # client widgets
        self.client_widgets_status = SocketWidgetStruct()
        # self.client_widgets_status.send_fun = self.socket_client.socket_send_bytes
        # self.client_widgets_status.receive_fun = self.socket_client.socket_receive_bytes
        self.client_widgets_status.lineEdit_IP = self.lineEdit_ClntIP
        self.client_widgets_status.lineEdit_Port = self.lineEdit_ClntPort
        self.client_widgets_status.pushButton_CreateConnection = self.pushButton_ClntCreatConn
        self.client_widgets_status.pushButton_CloseConnection = self.pushButton_ClntCloseConn
        self.client_widgets_status.log_fun = self.record_socket_communication_result

        self.client_widgets_status.checkBox_SendStringMode = self.checkBox_ClientSendString
        self.client_widgets_status.lineEdit_StrSendSeparator = self.lineEdit_ClientSendSeparator
        self.client_widgets_status.checkBox_SendRawbytesMode = self.checkBox_ClientSendRawbytes

        self.client_widgets_status.checkBox_Send_Int = self.checkBox_ClntSendInt
        self.client_widgets_status.spinBox_Send_Int = self.spinBox_ClntSendInt_Seq
        self.client_widgets_status.lineEdit_Send_Int = self.lineEdit_ClntSendInt_Value
        self.client_widgets_status.checkBox_Send_Float = self.checkBox_ClntSendFloat
        self.client_widgets_status.spinBox_Send_Float = self.spinBox_ClntSendFloat_Seq
        self.client_widgets_status.lineEdit_Send_Float = self.lineEdit_ClntSendFloat_Value
        self.client_widgets_status.checkBox_Send_Str = self.checkBox_ClntSendStr
        self.client_widgets_status.spinBox_Send_Str = self.spinBox_ClntSendStr_Seq
        self.client_widgets_status.lineEdit_Send_Str = self.lineEdit_ClntSendStr_Value

        self.client_widgets_status.lineEdit_SendFullType = self.lineEdit_ClntSendFullType
        self.client_widgets_status.lineEdit_SendFormatStr = self.lineEdit_ClntSendFormatStr

        self.client_widgets_status.checkBox_ReceiveStrMode = self.checkBox_ClientReceiveString
        self.client_widgets_status.lineEdit_StrReceiveSeparator = self.lineEdit_ClientReceiveSeparator
        self.client_widgets_status.checkBox_ReceiveRawbytesMode = self.checkBox_ClientReceiveRawbytes
        self.client_widgets_status.checkBox_Receive_Int = self.checkBox_ClntRecvInt
        self.client_widgets_status.spinBox_Receive_Int = self.spinBox_ClntRecvInt_Seq
        self.client_widgets_status.lineEdit_Receive_Int = self.lineEdit_ClntRecvInt_Value
        self.client_widgets_status.checkBox_Receive_Float = self.checkBox_ClntRecvFloat
        self.client_widgets_status.spinBox_Receive_Float = self.spinBox_ClntRecvFloat_Seq
        self.client_widgets_status.lineEdit_Receive_Float = self.lineEdit_ClntRecvFloat_Value
        self.client_widgets_status.checkBox_Receive_Str = self.checkBox_ClntRecvStr
        self.client_widgets_status.spinBox_Receive_Str = self.spinBox_ClntRecvStr_Seq
        self.client_widgets_status.lineEdit_Receive_Str = self.lineEdit_ClntRecvStr_Value
        self.client_widgets_status.lineEdit_ReceiveFullType = self.lineEdit_ClntRecvFullType
        self.client_widgets_status.lineEdit_ReceiveFormatStr = self.lineEdit_ClntRecvFormatStr
        self.client_widgets_status.pushButton_Send = self.pushButton_ClntSend
        self.client_widgets_status.checkBox_SendContinue = self.checkBox_ClntContinueSend
        self.client_widgets_status.lineEdit_SendInterval = self.lineEdit_ClntSendInterval
        self.client_widgets_status.pushButton_Receive = self.pushButton_ClntRecv
        self.client_widgets_status.spinBox_ReceiveRawLength = self.spinBox_ClntRecvRawLength
        self.client_widgets_status.checkBox_RecvContinue = self.checkBox_ClntContinueRecv
        self.client_widgets_status.lineEdit_RecvInterval = self.lineEdit_ClntRecvInterval
        self.client_widgets_status.pushButton_ClearCache = self.pushButton_ClntClearCache

        self.pushButton_quaternion_euler.clicked.connect(self.quaternion_euler_ins.quaternion_to_euler)
        self.pushButton_euler_quaternion.clicked.connect(self.quaternion_euler_ins.euler_to_quaternion)
        self.pushButton_quaternion_clearinput.clicked.connect(self.quaternion_euler_ins.clear_quaternion_input)
        self.pushButton_euler_clearinput.clicked.connect(self.quaternion_euler_ins.clear_euler_input)
        self.pushButton_quaternion_copy.clicked.connect(self.quaternion_euler_ins.copy_quaternion_result)
        self.pushButton_euler_copy.clicked.connect(self.quaternion_euler_ins.copy_euler_result)
        self.textEdit_result_record.customContextMenuRequested.connect(self.qtextedit_custom_context_menu)

        # socket server send and receive event
        self.signal_server_send.connect(self.socket_server.socket_send)
        self.signal_socket_server_create_connection.connect(self.socket_server.create_socket_server)
        self.pushButton_SerCreateConn.clicked.connect(lambda: self.pushButton_SerCloseConn.setEnabled(True))
        self.pushButton_SerCreateConn.clicked.connect(lambda: self.pushButton_SerCreateConn.setDisabled(True))
        self.pushButton_SerCreateConn.clicked.connect(self.server_create_connect)
        self.pushButton_SerCloseConn.clicked.connect(self.close_socket_server)
        self.pushButton_SerSend.clicked.connect(partial(self.socket_send, self.signal_server_send,  self.server_widgets_status))
        self.pushButton_SerRecv.clicked.connect(self.socket_server.socket_receive)
        self.pushButton_SerClearCache.clicked.connect(self.socket_server.socket_clear_cache)

        self.socket_server.signal_socket_server_accepted.connect(partial(self.ui_update_socket_server_communicate_enable, widgets_status=self.server_widgets_status, _socket=self.socket_server))
        self.socket_server.signal_record_result.connect(self.record_socket_communication_result)
        self.socket_server.signal_socket_server_closed.connect(self.pushButton_SerCreateConn.setEnabled)
        self.socket_server.signal_socket_server_closed.connect(self.pushButton_SerCloseConn.setDisabled)
        self.socket_server.signal_socket_receive_bytes.connect(partial(self.socket_receive, widgets_status=self.server_widgets_status))
        self.socket_server.signal_socket_sending.connect(partial(self.ui_update_pushbutton_sending, widgets_status=self.server_widgets_status))
        self.socket_server.signal_socket_receiving.connect(partial(self.ui_update_pushbutton_recving, widgets_status=self.server_widgets_status))

        self.socket_server_client.signal_record_result.connect(self.record_socket_communication_result)
        self.socket_server_client.signal_socket_server_client_closed.connect(self.socket_server.close_socket_server)
        self.signal_socket_server_not_accepted_close.connect(self.socket_server_client.connect_to_server)

        self.signal_client_send.connect(self.socket_client.socket_send)
        self.signal_socket_client_create_connection.connect(self.socket_client.create_socket_client)
        self.pushButton_ClntCreatConn.clicked.connect(self.client_create_connect)
        self.pushButton_ClntCloseConn.clicked.connect(self.socket_client.close_socket_client)
        self.pushButton_ClntSend.clicked.connect(lambda: self.socket_send(self.signal_client_send, self.client_widgets_status))
        self.pushButton_ClntRecv.clicked.connect(self.socket_client.socket_receive)
        self.pushButton_ClntClearCache.clicked.connect(self.socket_client.socket_clear_cache)
        self.socket_client.signal_socket_client_connected.connect(self.pushButton_ClntCloseConn.setEnabled)
        self.socket_client.signal_socket_client_connected.connect(partial(self.ui_update_socket_server_communicate_enable, widgets_status=self.client_widgets_status, _socket=self.socket_client))
        self.socket_client.signal_record_result.connect(self.record_socket_communication_result)
        self.socket_client.signal_socket_receive_bytes.connect(partial(self.socket_receive, widgets_status=self.client_widgets_status))
        self.socket_client.signal_socket_sending.connect(partial(self.ui_update_pushbutton_sending, widgets_status=self.client_widgets_status))
        self.socket_client.signal_socket_receiving.connect(partial(self.ui_update_pushbutton_recving, widgets_status=self.client_widgets_status))

        self.checkBox_ServerSendString.clicked.connect(lambda: self.ui_update_checkbox_send_string_checked(self.server_widgets_status, self.socket_server))
        self.checkBox_ServerSendRawbytes.clicked.connect(lambda: self.ui_update_checkbox_send_rawbytes_checked(self.server_widgets_status, self.socket_server))
        self.checkBox_ServerReceiveString.clicked.connect(lambda: self.ui_update_checkbox_send_string_checked(self.server_widgets_status, self.socket_server))
        self.checkBox_ServerReceiveRawbytes.clicked.connect(lambda: self.ui_update_checkbox_send_rawbytes_checked(self.server_widgets_status, self.socket_server))
        self.checkBox_ClientSendString.clicked.connect(lambda: self.ui_update_checkbox_send_string_checked(self.client_widgets_status, self.socket_client))
        self.checkBox_ClientSendRawbytes.clicked.connect(lambda: self.ui_update_checkbox_send_rawbytes_checked(self.client_widgets_status, self.socket_client))
        self.checkBox_ClientReceiveString.clicked.connect(lambda: self.ui_update_checkbox_send_string_checked(self.client_widgets_status, self.socket_client))
        self.checkBox_ClientReceiveRawbytes.clicked.connect(lambda: self.ui_update_checkbox_send_rawbytes_checked(self.client_widgets_status, self.socket_client))
        # initial for checkbox sequence and values
        self.checkBox_SerSendInt.clicked.connect(lambda: self.ui_update_checkbox_toggle_init(self.server_widgets_status, self.socket_server))
        self.checkBox_SerSendFloat.clicked.connect(lambda: self.ui_update_checkbox_toggle_init(self.server_widgets_status, self.socket_server))
        self.checkBox_SerSendStr.clicked.connect(lambda: self.ui_update_checkbox_toggle_init(self.server_widgets_status, self.socket_server))
        self.checkBox_SerContinueSend.clicked.connect(lambda: self.ui_update_checkbox_toggle_init(self.server_widgets_status, self.socket_server))
        self.checkBox_SerRecvInt.clicked.connect(lambda: self.ui_update_checkbox_toggle_init(self.server_widgets_status, self.socket_server))
        self.checkBox_SerRecvFloat.clicked.connect(lambda: self.ui_update_checkbox_toggle_init(self.server_widgets_status, self.socket_server))
        self.checkBox_SerRecvStr.clicked.connect(lambda: self.ui_update_checkbox_toggle_init(self.server_widgets_status, self.socket_server))
        self.checkBox_SerContinueRecv.clicked.connect(lambda: self.ui_update_checkbox_toggle_init(self.server_widgets_status, self.socket_server))

        self.checkBox_ClntSendInt.clicked.connect(lambda: self.ui_update_checkbox_toggle_init(self.client_widgets_status, self.socket_client))
        self.checkBox_ClntSendFloat.clicked.connect(lambda: self.ui_update_checkbox_toggle_init(self.client_widgets_status, self.socket_client))
        self.checkBox_ClntSendStr.clicked.connect(lambda: self.ui_update_checkbox_toggle_init(self.client_widgets_status, self.socket_client))
        self.checkBox_ClntContinueSend.clicked.connect(lambda: self.ui_update_checkbox_toggle_init(self.client_widgets_status, self.socket_client))
        self.checkBox_ClntRecvInt.clicked.connect(lambda: self.ui_update_checkbox_toggle_init(self.client_widgets_status, self.socket_client))
        self.checkBox_ClntRecvFloat.clicked.connect(lambda: self.ui_update_checkbox_toggle_init(self.client_widgets_status, self.socket_client))
        self.checkBox_ClntRecvStr.clicked.connect(lambda: self.ui_update_checkbox_toggle_init(self.client_widgets_status, self.socket_client))
        self.checkBox_ClntContinueRecv.clicked.connect(lambda: self.ui_update_checkbox_toggle_init(self.client_widgets_status, self.socket_client))

        # check line edit widgets values
        self.lineEdit_SerSendInt_Value.textChanged.connect(lambda: self.ui_update_send_value_check(self.server_widgets_status, self.socket_server))
        self.lineEdit_SerSendFloat_Value.textChanged.connect(lambda: self.ui_update_send_value_check(self.server_widgets_status, self.socket_server))
        self.lineEdit_SerSendstr_Value.textChanged.connect(lambda: self.ui_update_send_value_check(self.server_widgets_status, self.socket_server))
        self.lineEdit_ServerSendSeparator.textChanged.connect(lambda: self.ui_update_send_value_check(self.server_widgets_status, self.socket_server))
        self.lineEdit_ServerReceiveSeparator.textChanged.connect(lambda: self.ui_update_send_value_check(self.server_widgets_status, self.socket_server))
        self.lineEdit_SerRecvInt_Value.textChanged.connect(lambda: self.ui_update_send_value_check(self.server_widgets_status, self.socket_server))
        self.lineEdit_SerRecvFloat_Value.textChanged.connect(lambda: self.ui_update_send_value_check(self.server_widgets_status, self.socket_server))
        self.lineEdit_SerRecvStr_Value.textChanged.connect(lambda: self.ui_update_send_value_check(self.server_widgets_status, self.socket_server))
        self.lineEdit_ServerReceiveSeparator.textChanged.connect(lambda: self.ui_update_send_value_check(self.server_widgets_status, self.socket_server))

        self.lineEdit_SevIP.textChanged.connect(lambda: self.ui_update_check_ip_port(self.server_widgets_status))
        self.lineEdit_SerPort.textChanged.connect(lambda: self.ui_update_check_ip_port(self.server_widgets_status))

        self.lineEdit_ClntSendInt_Value.textChanged.connect(lambda: self.ui_update_send_value_check(self.client_widgets_status, self.socket_client))
        self.lineEdit_ClntSendFloat_Value.textChanged.connect(lambda: self.ui_update_send_value_check(self.client_widgets_status, self.socket_client))
        self.lineEdit_ClntSendStr_Value.textChanged.connect(lambda: self.ui_update_send_value_check(self.client_widgets_status, self.socket_client))
        self.lineEdit_ClientSendSeparator.textChanged.connect(lambda: self.ui_update_send_value_check(self.client_widgets_status, self.socket_client))
        self.lineEdit_ClientReceiveSeparator.textChanged.connect(lambda: self.ui_update_send_value_check(self.client_widgets_status, self.socket_client))
        self.lineEdit_ClntRecvInt_Value.textChanged.connect(lambda: self.ui_update_send_value_check(self.client_widgets_status, self.socket_client))
        self.lineEdit_ClntRecvFloat_Value.textChanged.connect(lambda: self.ui_update_send_value_check(self.client_widgets_status, self.socket_client))
        self.lineEdit_ClntRecvStr_Value.textChanged.connect(lambda: self.ui_update_send_value_check(self.client_widgets_status, self.socket_client))

        self.lineEdit_ClntIP.textChanged.connect(lambda: self.ui_update_check_ip_port(self.client_widgets_status))
        self.lineEdit_ClntPort.textChanged.connect(lambda: self.ui_update_check_ip_port(self.client_widgets_status))
        # check spin box widgets sequences
        self.spinBox_SerSendInt_Seq.textChanged.connect(lambda: self.ui_update_send_value_check(self.server_widgets_status, self.socket_server))
        self.spinBox_SerSendFloat_Seq.textChanged.connect(lambda: self.ui_update_send_value_check(self.server_widgets_status, self.socket_server))
        self.spinBox_SerSendStr_Seq.textChanged.connect(lambda: self.ui_update_send_value_check(self.server_widgets_status, self.socket_server))
        self.spinBox_SerRecvInt_Seq.textChanged.connect(lambda: self.ui_update_rec_value_check(self.server_widgets_status, self.socket_server))
        self.spinBox_SerRecvFloat_Seq.textChanged.connect(lambda: self.ui_update_rec_value_check(self.server_widgets_status, self.socket_server))
        self.spinBox_SerRecvStr_Seq.textChanged.connect(lambda: self.ui_update_rec_value_check(self.server_widgets_status, self.socket_server))

        self.spinBox_ClntSendInt_Seq.textChanged.connect(lambda: self.ui_update_send_value_check(self.client_widgets_status, self.socket_client))
        self.spinBox_ClntSendFloat_Seq.textChanged.connect(lambda: self.ui_update_send_value_check(self.client_widgets_status, self.socket_client))
        self.spinBox_ClntSendStr_Seq.textChanged.connect(lambda: self.ui_update_send_value_check(self.client_widgets_status, self.socket_client))
        self.spinBox_ClntRecvInt_Seq.textChanged.connect(lambda: self.ui_update_rec_value_check(self.client_widgets_status, self.socket_client))
        self.spinBox_ClntRecvFloat_Seq.textChanged.connect(lambda: self.ui_update_rec_value_check(self.client_widgets_status, self.socket_client))
        self.spinBox_ClntRecvStr_Seq.textChanged.connect(lambda: self.ui_update_rec_value_check(self.client_widgets_status, self.socket_client))

        # socket server send and receive full type mode, auto uncheck the single mode check box
        self.lineEdit_SerSendFullType.textChanged.connect(lambda: self.ui_update_server_full_type_mode(self.server_widgets_status, self.socket_server))
        self.lineEdit_SerSendFormatStr.textChanged.connect(lambda: self.ui_update_server_full_type_mode(self.server_widgets_status, self.socket_server))
        self.lineEdit_SerRecvFormatStr.textChanged.connect(lambda: self.ui_update_server_full_type_mode(self.server_widgets_status, self.socket_server))
        self.lineEdit_SerSendInterval.textChanged.connect(lambda: self.ui_update_send_value_check(self.server_widgets_status, self.socket_server))
        self.lineEdit_SerRecvInterval.textChanged.connect(lambda: self.ui_update_rec_value_check(self.server_widgets_status, self.socket_server))

        self.lineEdit_ClntSendFullType.textChanged.connect(lambda: self.ui_update_server_full_type_mode(self.client_widgets_status, self.socket_client))
        self.lineEdit_ClntSendFormatStr.textChanged.connect(lambda: self.ui_update_server_full_type_mode(self.client_widgets_status, self.socket_client))
        self.lineEdit_ClntRecvFormatStr.textChanged.connect(lambda: self.ui_update_server_full_type_mode(self.client_widgets_status, self.socket_client))
        self.lineEdit_ClntSendInterval.textChanged.connect(lambda: self.ui_update_send_value_check(self.client_widgets_status, self.socket_client))
        self.lineEdit_ClntRecvInterval.textChanged.connect(lambda: self.ui_update_rec_value_check(self.client_widgets_status, self.socket_client))
        self.init_quaternion()

    # ------------------------------------------------------------------------------------------------------------------
    # -----------------------quaternion and euler convert function------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    def init_quaternion(self):
        self.quaternion_euler_ins.lineedit_q1 = self.lineEdit_quaternion_q1
        self.quaternion_euler_ins.lineedit_q2 = self.lineEdit_quaternion_q2
        self.quaternion_euler_ins.lineedit_q3 = self.lineEdit_quaternion_q3
        self.quaternion_euler_ins.lineedit_q4 = self.lineEdit_quaternion_q4
        self.quaternion_euler_ins.lineedit_rotx = self.lineEdit_euler_rotx
        self.quaternion_euler_ins.lineedit_roty = self.lineEdit_euler_roty
        self.quaternion_euler_ins.lineedit_rotz = self.lineEdit_euler_rotz
        self.quaternion_euler_ins.lineedit_quaternion_euler = self.lineEdit_quaternion_result
        self.quaternion_euler_ins.lineedit_euler_quaternion = self.lineEdit_euler_result
        self.quaternion_euler_ins.textedit_log = self.textEdit_result_record
        # self.quaternion_euler_ins.log_fun = self.record_convert_result

    def qtextedit_custom_context_menu(self, pos):
        """
        customer the textedit right menu function, no delete,cut,paste function
        :param pos: the cursor position
        :return:none
        """
        _menu = QMenu(self)
        # _action = _menu.addAction('Cut')
        # _action.setShortcut('Ctrl+X')
        # _action.triggered.connect(self.textEdit_result_record.cut)
        # _action = _menu.addAction('Copy')
        _action = QAction('Copy', self.textEdit_result_record)
        _action.setShortcut('Ctrl+C')
        _action.triggered.connect(self.textEdit_result_record.copy)
        # _action = _menu.addAction('Paste')
        # _action.setShortcut('Ctrl+V')
        # _action.triggered.connect(self.textEdit_result_record.paste)
        # _action = _menu.addAction('Delete')
        # _action.triggered.connect(self.textEdit_result_record.clear)
        # _action = _menu.addAction('SelectAll')
        _action2 = QAction('SelectAll', self.textEdit_result_record)
        _action2.setShortcut('Ctrl+A')
        _action2.triggered.connect(self.textEdit_result_record.selectAll)
        _menu.addAction(_action)
        _menu.addAction(_action2)
        _menu.popup(QCursor.pos())

    # ------------------------------------------------------------------------------------------------------------------
    # ----------------------socket communication -----------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    def server_create_connect(self):
        print("Server ip {}, Server port {}".format(self.lineEdit_SevIP.text(), self.lineEdit_SerPort.text()))
        self.signal_socket_server_create_connection.emit((self.lineEdit_SevIP.text(), self.lineEdit_SerPort.text()))

    def client_create_connect(self):
        print("Server ip {}, Server port {}".format(self.lineEdit_ClntIP.text(), self.lineEdit_ClntPort.text()))
        self.signal_socket_client_create_connection.emit((self.lineEdit_ClntIP.text(), self.lineEdit_ClntPort.text()))

    def close_socket_server(self):
        """
        close the socket server socket
        :return: none
        """
        try:
            if self.socket_server.socket_server_accept_client is None:
                self.signal_socket_server_not_accepted_close.emit((self.lineEdit_SevIP.text(), self.lineEdit_SerPort.text()))
                self.socket_server.b_close_not_accepted_server = True
            else:
                self.socket_server.close_socket_server()
        except OSError as e:
            self.record_socket_communication_result(str(e))
            self.record_socket_communication_result("OSError happened when close the socket server connection,"
                                                    " please check!")

    def record_socket_communication_result(self, str_record: str):
        """
        write record and date to textedit
        :param str_record: string that need to write
        :return: none
        """
        _str_time = time.strftime('%Y-%m-%d: %H:%M:%S ', time.localtime())
        self.textEdit_Log.append(_str_time + str_record)
        self.textEdit_Log.moveCursor(QTextCursor.End)

    # ------------------------------------------------------------------------------------------------------------------
    # -----------------------------------uiUpdate-----------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def socket_send(_signal_send: pyqtSignal, widgets_status: SocketWidgetStruct) -> None:
        """
        Base send widgets status quote send string function,use name tuple as input args,suit for both server and client
        """
        _send_fun = _signal_send.emit
        # _send_fun_continue = widgets_status.checkBox_SendContinue.isChecked()
        # _send_fun_interval = widgets_status.lineEdit_SendInterval.text()
        _int_checked = widgets_status.checkBox_Send_Int.isChecked()
        _int_seq = widgets_status.spinBox_Send_Int.text()
        _int_text = widgets_status.lineEdit_Send_Int.text()
        _float_checked = widgets_status.checkBox_Send_Float.isChecked()
        _float_seq = widgets_status.spinBox_Send_Float.text()
        _float_text = widgets_status.lineEdit_Send_Float.text()
        _str_checked = widgets_status.checkBox_Send_Str.isChecked()
        _str_seq = widgets_status.spinBox_Send_Str.text()
        _str_text = widgets_status.lineEdit_Send_Str.text()
        _full_type_str_text = widgets_status.lineEdit_SendFullType.text()
        _full_type_format_str_text = widgets_status.lineEdit_SendFormatStr.text()
        _send_str_Separator_text = widgets_status.lineEdit_StrSendSeparator.text()
        _log_fun = widgets_status.log_fun
        try:

            if widgets_status.checkBox_SendStringMode.isChecked():
                # send string
                if _int_checked + _float_checked + _str_checked == 1:
                    if _int_checked:
                        _send_fun(_int_text.encode())
                    elif _float_checked:
                        _send_fun(_float_text.encode())
                    else:
                        _send_fun(_str_text.encode())

                elif _int_checked + _float_checked + _str_checked == 2:
                    if not _int_checked:
                        if int(_float_seq) > int(_str_seq):
                            _send_fun((_float_text + _send_str_Separator_text + _str_text).encode())
                        else:
                            _send_fun((_str_text + _send_str_Separator_text + _float_text).encode())
                    elif not _float_checked:
                        if int(_int_seq) > int(_str_seq):
                            _send_fun((_int_text + _send_str_Separator_text + _str_text).encode())
                        else:
                            _send_fun((_str_text + _send_str_Separator_text + _int_text).encode())
                    else:
                        if int(_int_seq) > int(_float_seq):
                            _send_fun((_int_text + _send_str_Separator_text + _float_text).encode())
                        else:
                            _send_fun((_float_text + _send_str_Separator_text + _int_text).encode())

                elif _int_checked + _float_checked + _str_checked == 3:
                    # 生成字列表，并对列表按键值做排序
                    m_sequence_list = [[int(_int_seq), _int_text],
                                       [int(_float_seq), _float_text],
                                       [int(_str_seq), _str_text]]
                    m_sequence_list.sort(key=lambda x: x[0], reverse=True)
                    _send_fun((str(m_sequence_list[0][1]) + _send_str_Separator_text + str(m_sequence_list[1][1])
                              + _send_str_Separator_text + str(m_sequence_list[2][1])).encode())
                else:
                    _send_fun(_full_type_str_text.encode())
            else:
                # Send rawbytes
                if _int_checked + _float_checked + _str_checked == 1:
                    if _int_checked:
                        _send_fun(struct.pack("<h", int(_int_text)))
                    elif _float_checked:
                        _send_fun(struct.pack("<f", float(_float_text)))
                    else:
                        _send_fun(struct.pack("<f", str(_str_text)))

                elif _int_checked + _float_checked + _str_checked == 2:
                    if not _int_checked:
                        if int(_float_seq) > int(_str_seq):
                            _send_fun(
                                struct.pack("<f{}s".format(len(_str_text)), float(_float_text), _str_text.encode()))
                        else:
                            _send_fun(
                                struct.pack("<{}sf".format(len(_str_text)), _str_text.encode(), float(_float_text)))
                    elif not _float_checked:
                        if int(_int_seq) > int(_str_seq):
                            _send_fun(
                                struct.pack("<h{}s".format(len(_str_text)), int(_int_text), _str_text.encode()))
                        else:
                            _send_fun(
                                struct.pack("<{}sh".format(len(_str_text)), _str_text.encode(), int(_int_text)))
                    else:
                        if int(_int_seq) > int(_float_seq):
                            _send_fun(struct.pack("<hf", int(_int_text), float(_float_text)))
                        else:
                            _send_fun(struct.pack("<fh", float(_float_text), int(_int_text)))

                elif _int_checked + _float_checked + _str_checked == 3:
                    m_sequence_list = [
                        [int(_int_seq), int(_int_text), "h"],
                        [int(_float_seq), float(_float_text), "f"],
                        [int(_str_seq), _str_text.encode(), "{}s".format(len(_str_text))]]

                    m_sequence_list.sort(key=lambda x: x[0], reverse=True)
                    _send_fun(
                        struct.pack("<" + m_sequence_list[0][2] + m_sequence_list[1][2] + m_sequence_list[2][2],
                                    m_sequence_list[0][1], m_sequence_list[1][1], m_sequence_list[2][1]))
                else:
                    list_re = re.findall(r"(h|f|\d+s)", _full_type_format_str_text)
                    list_value = _full_type_str_text.split(_send_str_Separator_text)
                    list_byte = bytes()
                    for int_index in range(len(list_re)):
                        if list_re[int_index] == "h":
                            list_byte += (struct.pack("<" + list_re[int_index], int(list_value[int_index])))
                        elif list_re[int_index] == "f":
                            list_byte += (struct.pack("<" + list_re[int_index], float(list_value[int_index])))
                        elif "s" in list_re[int_index]:
                            list_byte += (struct.pack("<" + list_re[int_index], list_value[int_index].encode()))
                    _send_fun(list_byte)
            # time.sleep(float(widgets_status.lineEdit_SendInterval.text()))

        except ConnectionAbortedError:
            return
        except struct.error as e:
            _log_fun("Send error: " + str(e))

    @staticmethod
    def socket_receive(_recv_str: bytes, widgets_status: SocketWidgetStruct) -> None:
        """
        Base send widgets status quote receive string function,use name tuple as input args,suit for both server and client
        """
        # _recv_fun = self.socket_receive_bytes
        _int_checked = widgets_status.checkBox_Receive_Int.isChecked()
        _int_seq = widgets_status.spinBox_Receive_Int.text()
        _int_text_lineedit = widgets_status.lineEdit_Receive_Int
        _float_checked = widgets_status.checkBox_Receive_Float.isChecked()
        _float_seq = widgets_status.spinBox_Receive_Float.text()
        _float_text_lineedit = widgets_status.lineEdit_Receive_Float
        _str_checked = widgets_status.checkBox_Receive_Str.isChecked()
        _str_seq = widgets_status.spinBox_Receive_Str.text()
        _str_text_lineedit = widgets_status.lineEdit_Receive_Str
        _full_type_str_text_lineedit = widgets_status.lineEdit_ReceiveFullType
        _full_type_format_str_text = widgets_status.lineEdit_ReceiveFormatStr.text()
        _recv_str_Separator_text = widgets_status.lineEdit_StrReceiveSeparator.text()
        _log_fun = widgets_status.log_fun

        try:

            if widgets_status.checkBox_ReceiveStrMode.isChecked():
                if _int_checked + _float_checked + _str_checked == 0:
                    try:
                        _full_type_str_text_lineedit.setText(_recv_str.decode())
                    except AttributeError as e:
                        print(e)
                        _full_type_str_text_lineedit.clear()
                if _int_checked + _float_checked + _str_checked == 1:
                    if _int_checked:
                        try:
                            _int_text_lineedit.clear()
                            m_int = int(_recv_str.decode())
                            _int_text_lineedit.setText(str(m_int))
                        except ValueError:
                            _int_text_lineedit.clear()
                            _log_fun("Can't parse receive string bytes as type setting,please check")
                            return

                    elif _float_checked:
                        try:
                            _float_text_lineedit.clear()
                            m_float = float(_recv_str.decode())
                            _float_text_lineedit.setText(str(m_float))
                        except ValueError:
                            _float_text_lineedit.clear()
                            _log_fun("Can't parse receive string bytes as type setting,please check")
                            return
                    else:
                        try:
                            _str_text_lineedit.clear()
                            m_str = _recv_str.decode()
                            _str_text_lineedit.setText(m_str)
                        except ValueError:
                            _str_text_lineedit.clear()
                            _log_fun("Can't parse receive string bytes as type setting,please check")
                            return

                elif _int_checked + _float_checked + _str_checked == 2:
                    if not _int_checked:
                        if int(_float_seq) > int(_str_seq):
                            try:
                                _float_text_lineedit.clear()
                                _str_text_lineedit.clear()
                                _float_str, _string = _recv_str.decode().split(_recv_str_Separator_text)
                                _float_text_lineedit.setText(_float_str)
                                _str_text_lineedit.setText(_string)
                            except ValueError:
                                _float_text_lineedit.clear()
                                _str_text_lineedit.clear()
                                _log_fun("Can't parse receive string bytes as type setting,please check")
                                return
                        else:
                            try:
                                _float_text_lineedit.clear()
                                _str_text_lineedit.clear()
                                _string, _float_str = _recv_str.decode().split(_recv_str_Separator_text)
                                _float_text_lineedit.setText(_float_str)
                                _str_text_lineedit.setText(_string)
                            except ValueError:
                                _float_text_lineedit.clear()
                                _str_text_lineedit.clear()
                                _log_fun("Can't parse receive string bytes as type setting,please check")
                                return
                    elif not _float_checked:
                        if int(_int_seq) > int(_str_seq):
                            try:
                                _int_text_lineedit.clear()
                                _str_text_lineedit.clear()
                                _int_str, _string = _recv_str.decode().split(_recv_str_Separator_text)
                                _int_text_lineedit.setText(_int_str)
                                _str_text_lineedit.setText(_string)
                            except ValueError:
                                _int_text_lineedit.clear()
                                _str_text_lineedit.clear()
                                _log_fun("Can't parse receive string bytes as type setting,please check")
                                return
                        else:
                            try:
                                _int_text_lineedit.clear()
                                _str_text_lineedit.clear()
                                _string, _int_str = _recv_str.decode().split(_recv_str_Separator_text)
                                _int_text_lineedit.setText(_int_str)
                                _str_text_lineedit.setText(_string)
                            except ValueError:
                                _int_text_lineedit.clear()
                                _str_text_lineedit.clear()
                                _log_fun("Can't parse receive string bytes as type setting,please check")
                                return
                    else:
                        if int(_int_seq) > int(_float_seq):
                            try:
                                _int_text_lineedit.clear()
                                _float_text_lineedit.clear()
                                _int_str, _float_str = _recv_str.decode().split(_recv_str_Separator_text)
                                _int_text_lineedit.setText(_int_str)
                                _float_text_lineedit.setText(_float_str)
                            except ValueError:
                                _int_text_lineedit.clear()
                                _float_text_lineedit.clear()
                                _log_fun("Can't parse receive string bytes as type setting,please check")
                                return
                        else:
                            try:
                                _int_text_lineedit.clear()
                                _float_text_lineedit.clear()
                                _float_str, _int_str = _recv_str.decode().split(_recv_str_Separator_text)
                                _int_text_lineedit.setText(_int_str)
                                _float_text_lineedit.setText(_float_str)
                            except ValueError:
                                _int_text_lineedit.clear()
                                _float_text_lineedit.clear()
                                _log_fun("Can't parse receive string bytes as type setting,please check")
                                return

                elif _int_checked + _float_checked + _str_checked == 3:
                    try:
                        _int_text_lineedit.clear()
                        _float_text_lineedit.clear()
                        _str_text_lineedit.clear()
                        # sort receive sequence value as sequence settlement
                        list_type = sorted([[_int_seq, None], [_float_seq, None], [_str_seq, None]],
                                           key=lambda x: int(x[0]), reverse=True)
                        list_type[0][1], list_type[1][1], list_type[2][1] = _recv_str.decode().split(
                            _recv_str_Separator_text)
                        _int_text_lineedit.setText([x[1] for x in list_type if x[0] == _int_seq][0])
                        _float_text_lineedit.setText([x[1] for x in list_type if x[0] == _float_seq][0])
                        _str_text_lineedit.setText([x[1] for x in list_type if x[0] == _str_seq][0])
                    except ValueError:
                        _int_text_lineedit.clear()
                        _float_text_lineedit.clear()
                        _str_text_lineedit.clear()
                        _log_fun("Can't parse receive string bytes as type setting,please check")
            else:
                _server_receive_rawbytes_length = int(widgets_status.spinBox_ReceiveRawLength.text())
                if _int_checked + _float_checked + _str_checked == 0:
                    try:
                        _full_type_str_text_lineedit.clear()
                        # print("parse full type rawbytes")
                        _tuple = struct.unpack(_full_type_format_str_text, _recv_str)
                        _full_type_str_text_lineedit.setText(str(_tuple))
                    except (struct.error, ValueError):
                        _full_type_str_text_lineedit.clear()
                        _log_fun("Can't parse receive rawbytes as type setting,please check")

                if _int_checked + _float_checked + _str_checked == 1:
                    if _int_checked:
                        try:
                            _int_text_lineedit.clear()
                            _int, = struct.unpack('<h', _recv_str)
                            _int_text_lineedit.setText(str(_int))
                        except (struct.error, ValueError):
                            _int_text_lineedit.clear()
                            _log_fun("Can't parse receive rawbytes as type setting,please check")

                    elif _float_checked:
                        try:
                            _float_text_lineedit.clear()
                            _float, = struct.unpack('<f', _recv_str)
                            _float_text_lineedit.setText(str(_float))
                        except (struct.error, ValueError):
                            _float_text_lineedit.clear()
                            _log_fun("Can't parse receive rawbytes as type setting,please check")

                    else:
                        try:
                            _str_text_lineedit.clear()
                            _string, = struct.unpack('<{}s'.format(_server_receive_rawbytes_length), _recv_str)
                            _str_text_lineedit.setText(str(_string.decode()))
                        except (struct.error, ValueError):
                            _str_text_lineedit.clear()
                            _log_fun("Can't parse receive rawbytes as type setting,please check")

                elif _int_checked + _float_checked + _str_checked == 2:
                    if not _int_checked:
                        if int(_float_seq) > int(_str_seq):
                            try:
                                _float_text_lineedit.clear()
                                _str_text_lineedit.clear()
                                _float, _str = struct.unpack('<f{}s'.format(_server_receive_rawbytes_length),
                                                             _recv_str)
                                _float_text_lineedit.setText(str(_float))
                                _str_text_lineedit.setText(str(_str.decode()))
                            except (struct.error, ValueError):
                                _float_text_lineedit.clear()
                                _str_text_lineedit.clear()
                                _log_fun("Can't parse receive rawbytes as type setting,please check")

                        else:
                            try:
                                _float_text_lineedit.clear()
                                _str_text_lineedit.clear()
                                _str, _float = struct.unpack('<{}sf'.format(_server_receive_rawbytes_length),
                                                             _recv_str)
                                _float_text_lineedit.setText(str(_float))
                                _str_text_lineedit.setText(str(_str.decode()))
                            except (struct.error, ValueError):
                                _float_text_lineedit.clear()
                                _str_text_lineedit.clear()
                                _log_fun("Can't parse receive rawbytes as type setting,please check")

                    elif not _float_checked:
                        if int(_int_seq) > int(_str_seq):
                            try:
                                _int_text_lineedit.clear()
                                _str_text_lineedit.clear()
                                _int, _str = struct.unpack('<h{}s'.format(_server_receive_rawbytes_length),
                                                           _recv_str)
                                _int_text_lineedit.setText(str(_int))
                                _str_text_lineedit.setText(str(_str.decode()))
                            except (struct.error, ValueError):
                                _int_text_lineedit.clear()
                                _str_text_lineedit.clear()
                                _log_fun("Can't parse receive rawbytes as type setting,please check")
                        else:
                            try:
                                _int_text_lineedit.clear()
                                _str_text_lineedit.clear()
                                _str, _int, = struct.unpack('<{}sh'.format(_server_receive_rawbytes_length),
                                                            _recv_str)
                                _int_text_lineedit.setText(str(_int))
                                _str_text_lineedit.setText(str(_str.decode()))
                            except (struct.error, ValueError):
                                _int_text_lineedit.clear()
                                _str_text_lineedit.clear()
                                _log_fun("Can't parse receive rawbytes as type setting,please check")
                    else:
                        if int(_int_seq) > int(_float_seq):
                            try:
                                _int_text_lineedit.clear()
                                _float_text_lineedit.clear()
                                _int, _float = struct.unpack('<hf', _recv_str)
                                _int_text_lineedit.setText(str(_int))
                                _float_text_lineedit.setText(str(_float))
                            except (struct.error, ValueError):
                                _int_text_lineedit.clear()
                                _float_text_lineedit.clear()
                                _log_fun("Can't parse receive rawbytes as type setting,please check")
                        else:
                            try:
                                _int_text_lineedit.clear()
                                _float_text_lineedit.clear()
                                _float, _int = struct.unpack('<fh', _recv_str)
                                _int_text_lineedit.setText(str(_int))
                                _float_text_lineedit.setText(str(_float))
                            except (struct.error, ValueError):
                                _int_text_lineedit.clear()
                                _float_text_lineedit.clear()
                                _log_fun("Can't parse receive rawbytes as type setting,please check")
                elif _int_checked + _float_checked + _str_checked == 3:
                    try:
                        _int_text_lineedit.clear()
                        _float_text_lineedit.clear()
                        _str_text_lineedit.clear()
                        # append sort logic
                        list_type = sorted(
                            [[_int_seq, None, "h"], [_float_seq, None, "f"], [_str_seq, None, "{}s"]],
                            key=lambda x: int(x[0]),
                            reverse=True)
                        _unpack_format_str = "<" + list_type[0][2] + list_type[1][2] + list_type[2][2]
                        list_type[0][1], list_type[1][1], list_type[2][1] = list(
                            struct.unpack(_unpack_format_str.format(_server_receive_rawbytes_length), _recv_str))

                        _int_text_lineedit.setText([str(x[1]) for x in list_type if x[0] == _int_seq][0])
                        _float_text_lineedit.setText([str(x[1]) for x in list_type if x[0] == _float_seq][0])
                        _str_text_lineedit.setText([str(x[1].decode()) for x in list_type if x[0] == _str_seq][0])
                    except (struct.error, ValueError):
                        _int_text_lineedit.clear()
                        _float_text_lineedit.clear()
                        _str_text_lineedit.clear()
                        _log_fun("Can't parse receive rawbytes as type setting,please check")

            # time.sleep(float(widgets_status.lineEdit_RecvInterval.text()))
            # if not widgets_status.checkBox_RecvContinue.isChecked():
            #     break
        # 检查调用Socket receive方法是否接收数据超时，如果是则发布信息并return
        except OSError as e:
            _log_fun(str(e))
            _log_fun("Doesn't receive any data, please check")
            return

    @staticmethod
    def ui_update_pushbutton_sending(_b_sending: bool, widgets_status: SocketWidgetStruct) -> None:
        if _b_sending:
            widgets_status.pushButton_Send.setText("发送中...")
            widgets_status.pushButton_Send.setEnabled(False)
            widgets_status.pushButton_Receive.setEnabled(False)
            widgets_status.pushButton_ClearCache.setEnabled(False)
            if widgets_status.checkBox_SendContinue.isChecked():
                widgets_status.checkBox_SendContinue.setStyleSheet("QCheckBox{background-color: rgb(119, 190, 255)}")
            else:
                widgets_status.checkBox_SendContinue.setStyleSheet("QCheckBox{background-color: rgb(255, 255, 255)}")
        else:
            widgets_status.pushButton_Send.setText("发送")
            widgets_status.pushButton_Receive.setEnabled(True)
            widgets_status.pushButton_ClearCache.setEnabled(True)
            widgets_status.checkBox_SendContinue.setStyleSheet("QCheckBox{background-color: rgb(255, 255, 255)}")
            if widgets_status.checkBox_SendStringMode.isEnabled() or widgets_status.checkBox_SendRawbytesMode.isEnabled():
                widgets_status.pushButton_Send.setEnabled(True)

    @staticmethod
    def ui_update_pushbutton_recving(_b_receiving: bool, widgets_status: SocketWidgetStruct) -> None:
        if _b_receiving:
            widgets_status.pushButton_Receive.setText("接收中...")
            widgets_status.pushButton_ClearCache.setEnabled(False)
            widgets_status.pushButton_Receive.setEnabled(False)
            widgets_status.pushButton_Send.setEnabled(False)
            if widgets_status.checkBox_RecvContinue.isChecked():
                widgets_status.checkBox_RecvContinue.setStyleSheet("QCheckBox{background-color: rgb(119, 190, 255)}")
            else:
                widgets_status.checkBox_RecvContinue.setStyleSheet("QCheckBox{background-color: rgb(255, 255, 255)}")
        else:
            widgets_status.pushButton_Send.setEnabled(True)
            widgets_status.pushButton_Receive.setText("接收")
            widgets_status.checkBox_RecvContinue.setStyleSheet("QCheckBox{background-color: rgb(255, 255, 255)}")
            if widgets_status.checkBox_SendStringMode.isEnabled() or widgets_status.checkBox_SendRawbytesMode.isEnabled():
                widgets_status.pushButton_ClearCache.setEnabled(True)
                widgets_status.pushButton_Receive.setEnabled(True)

    @staticmethod
    def ui_update_socket_server_communicate_enable(b_accepted: bool, widgets_status: SocketWidgetStruct, _socket: SocketCommunicate) -> None:
        """
        enable send and receive widgets after socket server accept connection
        :param b_accepted:
        :param widgets_status:
        :param _socket:
        :return:
        """

        if b_accepted and not _socket.b_close_not_accepted_server:
            _socket.b_close_not_accepted_server = False
            # send widgets
            widgets_status.checkBox_SendStringMode.setEnabled(True)
            # widgets_status.lineEdit_StrSendSeparator.setEnabled(True)
            widgets_status.checkBox_SendRawbytesMode.setEnabled(True)
            widgets_status.checkBox_Send_Int.setEnabled(True)
            widgets_status.checkBox_Send_Str.setEnabled(True)
            widgets_status.checkBox_Send_Float.setEnabled(True)
            widgets_status.checkBox_SendContinue.setEnabled(True)
            widgets_status.lineEdit_SendFullType.setEnabled(True)
            widgets_status.lineEdit_SendFullType.setFocusPolicy(Qt.StrongFocus)
            widgets_status.lineEdit_SendFormatStr.setEnabled(True)
            widgets_status.lineEdit_SendFormatStr.setFocusPolicy(Qt.StrongFocus)

            # receive widgets
            widgets_status.checkBox_ReceiveStrMode.setEnabled(True)
            widgets_status.checkBox_ReceiveRawbytesMode.setEnabled(True)
            widgets_status.checkBox_RecvContinue.setEnabled(True)
            widgets_status.checkBox_Receive_Int.setEnabled(True)
            widgets_status.checkBox_Receive_Str.setEnabled(True)
            widgets_status.checkBox_Receive_Float.setEnabled(True)
            widgets_status.lineEdit_ReceiveFullType.setEnabled(True)
            widgets_status.lineEdit_ReceiveFullType.setFocusPolicy(Qt.StrongFocus)
            widgets_status.lineEdit_ReceiveFormatStr.setEnabled(True)
            widgets_status.lineEdit_ReceiveFormatStr.setFocusPolicy(Qt.StrongFocus)

        else:
            # send widgets
            widgets_status.checkBox_SendStringMode.setChecked(True)
            widgets_status.checkBox_SendStringMode.setEnabled(False)
            widgets_status.checkBox_SendRawbytesMode.setChecked(False)
            widgets_status.checkBox_SendRawbytesMode.setEnabled(False)
            widgets_status.checkBox_Send_Int.setChecked(False)
            widgets_status.checkBox_Send_Int.setEnabled(False)
            widgets_status.checkBox_Send_Float.setChecked(False)
            widgets_status.checkBox_Send_Float.setEnabled(False)
            widgets_status.checkBox_Send_Str.setChecked(False)
            widgets_status.checkBox_Send_Str.setEnabled(False)
            widgets_status.checkBox_SendContinue.setChecked(False)
            widgets_status.checkBox_SendContinue.setEnabled(False)
            widgets_status.lineEdit_SendFullType.setEnabled(False)
            widgets_status.lineEdit_SendFormatStr.setEnabled(False)
            # receive widgets
            widgets_status.checkBox_ReceiveStrMode.setChecked(True)
            widgets_status.checkBox_ReceiveStrMode.setEnabled(False)
            widgets_status.lineEdit_StrReceiveSeparator.setEnabled(False)
            widgets_status.checkBox_ReceiveRawbytesMode.setChecked(False)
            widgets_status.checkBox_ReceiveRawbytesMode.setEnabled(False)
            widgets_status.checkBox_Receive_Int.setChecked(False)
            widgets_status.checkBox_Receive_Int.setEnabled(False)
            widgets_status.checkBox_Receive_Float.setChecked(False)
            widgets_status.checkBox_Receive_Float.setEnabled(False)
            widgets_status.checkBox_Receive_Str.setChecked(False)
            widgets_status.checkBox_Receive_Str.setEnabled(False)
            widgets_status.checkBox_RecvContinue.setChecked(False)
            widgets_status.checkBox_RecvContinue.setEnabled(False)
            widgets_status.lineEdit_ReceiveFormatStr.setEnabled(False)
            widgets_status.lineEdit_ReceiveFullType.setFocusPolicy(Qt.NoFocus)
            widgets_status.lineEdit_ReceiveFullType.setEnabled(False)

        MyMainWindow.ui_update_checkbox_send_string_checked(widgets_status, _socket)

    @staticmethod
    def ui_update_checkbox_send_string_checked(widgets_status: SocketWidgetStruct, _socket: SocketCommunicate) -> None:
        """

        :param widgets_status:
        :param _socket:
        :return:
        """

        # server string checkbox checked
        if widgets_status.checkBox_SendStringMode.isChecked() and widgets_status.checkBox_SendStringMode.isEnabled():
            widgets_status.checkBox_SendRawbytesMode.setChecked(False)
        elif widgets_status.checkBox_SendStringMode.isEnabled():
            widgets_status.checkBox_SendRawbytesMode.setChecked(True)

        if widgets_status.checkBox_ReceiveStrMode.isChecked() and widgets_status.checkBox_ReceiveStrMode.isEnabled():
            widgets_status.checkBox_ReceiveRawbytesMode.setChecked(False)
        elif widgets_status.checkBox_ReceiveStrMode.isEnabled():
            widgets_status.checkBox_ReceiveRawbytesMode.setChecked(True)

        MyMainWindow.ui_update_checkbox_toggle_init(widgets_status, _socket)

    @staticmethod
    def ui_update_checkbox_send_rawbytes_checked(widgets_status: SocketWidgetStruct, _socket: SocketCommunicate):
        """

        :return:
        """
        # server rawbytes checkbox checked
        if widgets_status.checkBox_SendRawbytesMode.isChecked() and widgets_status.checkBox_SendRawbytesMode.isEnabled():
            widgets_status.checkBox_SendStringMode.setChecked(False)

        elif widgets_status.checkBox_SendRawbytesMode.isEnabled():
            widgets_status.checkBox_SendStringMode.setChecked(True)

        if widgets_status.checkBox_ReceiveRawbytesMode.isChecked() and widgets_status.checkBox_ReceiveRawbytesMode.isEnabled():
            widgets_status.checkBox_ReceiveStrMode.setChecked(False)

        elif widgets_status.checkBox_ReceiveRawbytesMode.isEnabled():
            widgets_status.checkBox_ReceiveStrMode.setChecked(True)

        MyMainWindow.ui_update_checkbox_toggle_init(widgets_status, _socket)

    @staticmethod
    def ui_update_server_full_type_mode(widgets_status: SocketWidgetStruct, _socket: SocketCommunicate):
        """
        clear send single mode sequence and values if full type mode string are changed
        :return:
        """
        # judge if the serSendFullType are clear by single mode, this would avoid the checkbox setCheck automatically!
        if widgets_status.lineEdit_SendFullType.text() != "" \
                or widgets_status.lineEdit_SendFormatStr.text() != "":
            widgets_status.checkBox_Send_Int.setChecked(False)
            widgets_status.checkBox_Send_Float.setChecked(False)
            widgets_status.checkBox_Send_Str.setChecked(False)

        if widgets_status.lineEdit_ReceiveFullType.text() != "" \
                or widgets_status.lineEdit_ReceiveFormatStr.text() != "":
            widgets_status.checkBox_Receive_Int.setChecked(False)
            widgets_status.checkBox_Receive_Float.setChecked(False)
            widgets_status.checkBox_Receive_Str.setChecked(False)

        MyMainWindow.ui_update_checkbox_toggle_init(widgets_status, _socket)

    @staticmethod
    def ui_update_checkbox_toggle_init(widgets_status: SocketWidgetStruct, _socket: SocketCommunicate):
        """

        :return:
        """
        # send widgets logic
        if widgets_status.checkBox_Send_Int.isChecked() and widgets_status.checkBox_Send_Int.isEnabled():
            widgets_status.spinBox_Send_Int.setEnabled(True)
            widgets_status.lineEdit_Send_Int.setEnabled(True)
        else:
            widgets_status.spinBox_Send_Int.setValue(0)
            widgets_status.spinBox_Send_Int.setEnabled(False)
            widgets_status.lineEdit_Send_Int.clear()
            widgets_status.lineEdit_Send_Int.setEnabled(False)
            widgets_status.spinBox_Send_Int.setStyleSheet(MyMainWindow.str_spinbox_style_disable)
            widgets_status.lineEdit_Send_Int.setStyleSheet(MyMainWindow.str_lineedit_style_disable)

        if widgets_status.checkBox_Send_Float.isChecked() and widgets_status.checkBox_Send_Float.isEnabled():
            widgets_status.spinBox_Send_Float.setEnabled(True)
            widgets_status.lineEdit_Send_Float.setEnabled(True)
        else:
            widgets_status.spinBox_Send_Float.setValue(0)
            widgets_status.spinBox_Send_Float.setEnabled(False)
            widgets_status.lineEdit_Send_Float.clear()
            widgets_status.lineEdit_Send_Float.setEnabled(False)
            widgets_status.spinBox_Send_Float.setStyleSheet(MyMainWindow.str_spinbox_style_disable)
            widgets_status.lineEdit_Send_Float.setStyleSheet(MyMainWindow.str_lineedit_style_disable)

        if widgets_status.checkBox_Send_Str.isChecked() and widgets_status.checkBox_Send_Str.isEnabled():
            widgets_status.spinBox_Send_Str.setEnabled(True)
            widgets_status.lineEdit_Send_Str.setEnabled(True)
        else:
            widgets_status.spinBox_Send_Str.setValue(0)
            widgets_status.spinBox_Send_Str.setEnabled(False)
            widgets_status.lineEdit_Send_Str.clear()
            widgets_status.lineEdit_Send_Str.setEnabled(False)
            widgets_status.spinBox_Send_Str.setStyleSheet(MyMainWindow.str_lineedit_style_disable)
            widgets_status.lineEdit_Send_Str.setStyleSheet(MyMainWindow.str_lineedit_style_disable)

        if widgets_status.checkBox_SendContinue.isChecked() and widgets_status.checkBox_SendContinue.isEnabled():
            widgets_status.lineEdit_SendInterval.setEnabled(True)
        else:
            widgets_status.lineEdit_SendInterval.setText("0.5")
            widgets_status.lineEdit_SendInterval.setStyleSheet(MyMainWindow.str_lineedit_style_disable)
            widgets_status.lineEdit_SendInterval.setEnabled(False)
            _socket.b_continue_send = widgets_status.checkBox_SendContinue.isChecked()
            _socket.str_send_interval = widgets_status.lineEdit_SendInterval.text()

        if widgets_status.checkBox_Send_Int.isChecked() + widgets_status.checkBox_Send_Float.isChecked() + widgets_status.checkBox_Send_Str.isChecked() == 0 \
                and widgets_status.checkBox_Send_Int.isEnabled() + widgets_status.checkBox_Send_Float.isEnabled() + widgets_status.checkBox_Send_Str.isEnabled() > 0:
            widgets_status.lineEdit_SendFullType.setEnabled(True)
            if widgets_status.checkBox_SendStringMode.isChecked():
                widgets_status.lineEdit_SendFormatStr.setText("<hf5s")
                widgets_status.lineEdit_SendFormatStr.setEnabled(False)
                widgets_status.lineEdit_StrSendSeparator.setText(",")
                widgets_status.lineEdit_StrSendSeparator.setStyleSheet(MyMainWindow.str_lineedit_style_disable)
                widgets_status.lineEdit_StrSendSeparator.setEnabled(False)
            else:
                widgets_status.lineEdit_StrSendSeparator.setEnabled(True)
                widgets_status.lineEdit_SendFormatStr.setEnabled(True)
        else:
            widgets_status.lineEdit_SendFullType.clear()
            widgets_status.lineEdit_SendFullType.setEnabled(False)
            widgets_status.lineEdit_SendFormatStr.setText("<hf5s")
            widgets_status.lineEdit_SendFormatStr.setEnabled(False)
            if widgets_status.checkBox_SendStringMode.isChecked() and widgets_status.checkBox_SendStringMode.isEnabled():
                widgets_status.lineEdit_StrSendSeparator.setEnabled(True)
            else:
                widgets_status.lineEdit_StrSendSeparator.setText(",")
                widgets_status.lineEdit_StrSendSeparator.setStyleSheet(MyMainWindow.str_lineedit_style_disable)
                widgets_status.lineEdit_StrSendSeparator.setEnabled(False)

        # receive checkbox logic
        if widgets_status.checkBox_Receive_Int.isChecked() and widgets_status.checkBox_Receive_Int.isEnabled():
            widgets_status.spinBox_Receive_Int.setEnabled(True)
            widgets_status.lineEdit_Receive_Int.setEnabled(True)
            widgets_status.lineEdit_Receive_Int.setStyleSheet(MyMainWindow.str_lineedit_style_enable)
        else:
            widgets_status.spinBox_Receive_Int.setValue(0)
            widgets_status.spinBox_Receive_Int.setEnabled(False)
            widgets_status.lineEdit_Receive_Int.clear()
            widgets_status.lineEdit_Receive_Int.setEnabled(False)
            widgets_status.spinBox_Receive_Int.setStyleSheet(MyMainWindow.str_spinbox_style_disable)
            widgets_status.lineEdit_Receive_Int.setStyleSheet(MyMainWindow.str_lineedit_style_disable)

        if widgets_status.checkBox_Receive_Float.isChecked() and widgets_status.checkBox_Receive_Float.isEnabled():
            widgets_status.spinBox_Receive_Float.setEnabled(True)
            widgets_status.lineEdit_Receive_Float.setEnabled(True)
            widgets_status.lineEdit_Receive_Float.setStyleSheet(MyMainWindow.str_lineedit_style_enable)
        else:
            widgets_status.spinBox_Receive_Float.setValue(0)
            widgets_status.spinBox_Receive_Float.setEnabled(False)
            widgets_status.lineEdit_Receive_Float.clear()
            widgets_status.lineEdit_Receive_Float.setEnabled(False)
            widgets_status.spinBox_Receive_Float.setStyleSheet(MyMainWindow.str_spinbox_style_disable)
            widgets_status.lineEdit_Receive_Float.setStyleSheet(MyMainWindow.str_lineedit_style_disable)

        if widgets_status.checkBox_Receive_Str.isChecked() and widgets_status.checkBox_Receive_Str.isEnabled():
            widgets_status.spinBox_Receive_Str.setEnabled(True)
            widgets_status.lineEdit_Receive_Str.setEnabled(True)
            widgets_status.lineEdit_Receive_Str.setStyleSheet(MyMainWindow.str_lineedit_style_enable)
            if widgets_status.checkBox_ReceiveStrMode.isEnabled() and widgets_status.checkBox_ReceiveStrMode.isChecked():
                widgets_status.spinBox_ReceiveRawLength.setValue(5)
                widgets_status.spinBox_ReceiveRawLength.setEnabled(False)
            else:
                widgets_status.spinBox_ReceiveRawLength.setEnabled(True)
        else:
            widgets_status.spinBox_Receive_Str.setValue(0)
            widgets_status.spinBox_Receive_Str.setEnabled(False)
            widgets_status.spinBox_ReceiveRawLength.setValue(5)
            widgets_status.spinBox_ReceiveRawLength.setEnabled(False)
            widgets_status.lineEdit_Receive_Str.clear()
            widgets_status.lineEdit_Receive_Str.setEnabled(False)
            widgets_status.spinBox_Receive_Str.setStyleSheet(MyMainWindow.str_spinbox_style_disable)
            widgets_status.lineEdit_Receive_Str.setStyleSheet(MyMainWindow.str_lineedit_style_disable)

        if widgets_status.checkBox_RecvContinue.isChecked() and widgets_status.checkBox_RecvContinue.isEnabled():
            widgets_status.lineEdit_RecvInterval.setEnabled(True)
        else:
            widgets_status.lineEdit_RecvInterval.setText("0.5")
            widgets_status.lineEdit_RecvInterval.setStyleSheet(MyMainWindow.str_lineedit_style_disable)
            widgets_status.lineEdit_RecvInterval.setEnabled(False)
            _socket.b_continue_recv = widgets_status.checkBox_RecvContinue.isChecked()
            _socket.str_recv_interval = widgets_status.lineEdit_RecvInterval.text()

        if widgets_status.checkBox_Receive_Int.isChecked() + widgets_status.checkBox_Receive_Float.isChecked() + widgets_status.checkBox_Receive_Str.isChecked() == 0 \
                and widgets_status.checkBox_Receive_Int.isEnabled() + widgets_status.checkBox_Receive_Float.isEnabled() + widgets_status.checkBox_Receive_Str.isEnabled() > 0:
            print(widgets_status.checkBox_Receive_Int.isEnabled() + widgets_status.checkBox_Receive_Float.isEnabled() + widgets_status.checkBox_Receive_Str.isEnabled())
            widgets_status.lineEdit_StrReceiveSeparator.setText(",")
            widgets_status.lineEdit_StrReceiveSeparator.setStyleSheet(MyMainWindow.str_lineedit_style_disable)
            widgets_status.lineEdit_StrReceiveSeparator.setEnabled(False)
            if widgets_status.checkBox_ReceiveStrMode.isChecked():
                widgets_status.lineEdit_ReceiveFullType.setEnabled(True)
                widgets_status.lineEdit_ReceiveFormatStr.setText("<hf5s")
                widgets_status.lineEdit_ReceiveFormatStr.setEnabled(False)
            else:
                widgets_status.lineEdit_ReceiveFullType.setEnabled(True)
                widgets_status.lineEdit_ReceiveFormatStr.setEnabled(True)
        else:
            widgets_status.lineEdit_ReceiveFullType.setEnabled(False)
            widgets_status.lineEdit_ReceiveFullType.clear()
            widgets_status.lineEdit_ReceiveFormatStr.setText("<hf5s")
            widgets_status.lineEdit_ReceiveFormatStr.setEnabled(False)
            if widgets_status.checkBox_ReceiveStrMode.isChecked() and widgets_status.checkBox_ReceiveStrMode.isEnabled():
                widgets_status.lineEdit_StrReceiveSeparator.setEnabled(True)
            else:
                widgets_status.lineEdit_StrReceiveSeparator.setText(",")
                widgets_status.lineEdit_StrReceiveSeparator.setStyleSheet(MyMainWindow.str_lineedit_style_disable)
                widgets_status.lineEdit_StrReceiveSeparator.setEnabled(False)

        MyMainWindow.ui_update_send_value_check(widgets_status, _socket)
        MyMainWindow.ui_update_rec_value_check(widgets_status, _socket)

    @staticmethod
    def ui_update_send_value_check(widgets_status: SocketWidgetStruct, _socket: SocketCommunicate):

        b_lineedit_check_valid = 0
        b_lineedit_check_valid_contrast = 0
        b_spinbox_check_valid = False
        b_lineedit_send_seperator_check_valid = False
        b_lineedit_send_interval_check_valid = False

        if widgets_status.checkBox_SendStringMode.isEnabled() or widgets_status.checkBox_SendRawbytesMode.isEnabled():
            if widgets_status.checkBox_Send_Int.isChecked():
                b_lineedit_check_valid_contrast += 1
                ins_re_match = re.match(r"^\d+$", widgets_status.lineEdit_Send_Int.text())
                if ins_re_match is not None:
                    widgets_status.lineEdit_Send_Int.setStyleSheet(MyMainWindow.str_lineedit_style_enable)
                    b_lineedit_check_valid += 1
                else:
                    widgets_status.lineEdit_Send_Int.setStyleSheet(MyMainWindow.str_lineedit_style_invalid)
                    # b_lineedit_check_valid = False
            if widgets_status.checkBox_Send_Float.isChecked():
                b_lineedit_check_valid_contrast += 1
                ins_re_match = re.match(r"^\d+\.\d+$", widgets_status.lineEdit_Send_Float.text())
                if ins_re_match is not None:
                    widgets_status.lineEdit_Send_Float.setStyleSheet(MyMainWindow.str_lineedit_style_enable)
                    b_lineedit_check_valid += 1
                else:
                    widgets_status.lineEdit_Send_Float.setStyleSheet(MyMainWindow.str_lineedit_style_invalid)
                    # b_lineedit_check_valid = False

            if widgets_status.checkBox_Send_Str.isChecked():
                b_lineedit_check_valid_contrast += 1
                ins_re_match = re.match(r"^\S+$", widgets_status.lineEdit_Send_Str.text())
                if ins_re_match is not None:
                    widgets_status.lineEdit_Send_Str.setStyleSheet(MyMainWindow.str_lineedit_style_enable)
                    b_lineedit_check_valid += 1
                else:
                    widgets_status.lineEdit_Send_Str.setStyleSheet(MyMainWindow.str_lineedit_style_invalid)
                    # b_lineedit_check_valid = False
                # Server send sequence check
            if widgets_status.checkBox_Send_Int.isChecked() + widgets_status.checkBox_Send_Float.isChecked() + widgets_status.checkBox_Send_Str.isChecked() == 0:
                if widgets_status.checkBox_SendStringMode.isChecked():
                    b_lineedit_check_valid_contrast += 1
                    if widgets_status.lineEdit_SendFullType.text() != "":
                        b_lineedit_check_valid += 1
                        b_spinbox_check_valid = True
                else:
                    b_lineedit_check_valid_contrast += 1
                    if widgets_status.lineEdit_SendFullType.text() != "" and widgets_status.lineEdit_SendFormatStr.text() != "":
                        b_lineedit_check_valid += 1
                        b_spinbox_check_valid = True

            elif widgets_status.checkBox_Send_Int.isChecked() + widgets_status.checkBox_Send_Float.isChecked() + widgets_status.checkBox_Send_Str.isChecked() == 1:
                if widgets_status.checkBox_Send_Int.isChecked():
                    widgets_status.spinBox_Send_Int.setStyleSheet(MyMainWindow.str_spinbox_style_enable)
                elif widgets_status.checkBox_Send_Float.isChecked():
                    widgets_status.spinBox_Send_Float.setStyleSheet(MyMainWindow.str_spinbox_style_enable)
                else:
                    widgets_status.spinBox_Send_Str.setStyleSheet(MyMainWindow.str_spinbox_style_enable)
                b_spinbox_check_valid = True
            elif widgets_status.checkBox_Send_Int.isChecked() + widgets_status.checkBox_Send_Float.isChecked() + widgets_status.checkBox_Send_Str.isChecked() == 2:
                if not widgets_status.checkBox_Send_Int.isChecked():
                    if widgets_status.spinBox_Send_Float.text() == widgets_status.spinBox_Send_Str.text():
                        widgets_status.spinBox_Send_Float.setStyleSheet(MyMainWindow.str_spinbox_style_invalid)
                        widgets_status.spinBox_Send_Str.setStyleSheet(MyMainWindow.str_spinbox_style_invalid)
                        b_spinbox_check_valid = False
                    else:
                        widgets_status.spinBox_Send_Float.setStyleSheet(MyMainWindow.str_spinbox_style_enable)
                        widgets_status.spinBox_Send_Str.setStyleSheet(MyMainWindow.str_spinbox_style_enable)
                        b_spinbox_check_valid = True

                elif not widgets_status.checkBox_Send_Float.isChecked():
                    if widgets_status.spinBox_Send_Int.text() == widgets_status.spinBox_Send_Str.text():
                        widgets_status.spinBox_Send_Int.setStyleSheet(MyMainWindow.str_spinbox_style_invalid)
                        widgets_status.spinBox_Send_Str.setStyleSheet(MyMainWindow.str_spinbox_style_invalid)
                        b_spinbox_check_valid = False
                    else:
                        widgets_status.spinBox_Send_Int.setStyleSheet(MyMainWindow.str_spinbox_style_enable)
                        widgets_status.spinBox_Send_Str.setStyleSheet(MyMainWindow.str_spinbox_style_enable)
                        b_spinbox_check_valid = True
                else:
                    if widgets_status.spinBox_Send_Int.text() == widgets_status.spinBox_Send_Float.text():
                        widgets_status.spinBox_Send_Float.setStyleSheet(MyMainWindow.str_spinbox_style_invalid)
                        widgets_status.spinBox_Send_Int.setStyleSheet(MyMainWindow.str_spinbox_style_invalid)
                        b_spinbox_check_valid = False
                    else:
                        widgets_status.spinBox_Send_Float.setStyleSheet(MyMainWindow.str_spinbox_style_enable)
                        widgets_status.spinBox_Send_Int.setStyleSheet(MyMainWindow.str_spinbox_style_enable)
                        b_spinbox_check_valid = True

            elif widgets_status.checkBox_Send_Int.isChecked() + widgets_status.checkBox_Send_Float.isChecked() + widgets_status.checkBox_Send_Str.isChecked() == 3:
                if widgets_status.spinBox_Send_Int.text() == widgets_status.spinBox_Send_Float.text():
                    b_spinbox_check_valid = False
                    widgets_status.spinBox_Send_Int.setStyleSheet(MyMainWindow.str_spinbox_style_invalid)
                    widgets_status.spinBox_Send_Float.setStyleSheet(MyMainWindow.str_spinbox_style_invalid)
                    if widgets_status.spinBox_Send_Int.text() == widgets_status.spinBox_Send_Str.text():
                        widgets_status.spinBox_Send_Int.setStyleSheet(MyMainWindow.str_spinbox_style_invalid)
                        widgets_status.spinBox_Send_Str.setStyleSheet(MyMainWindow.str_spinbox_style_invalid)
                    else:
                        widgets_status.spinBox_Send_Str.setStyleSheet(MyMainWindow.str_spinbox_style_enable)
                elif widgets_status.spinBox_Send_Int.text() == widgets_status.spinBox_Send_Str.text():
                    b_spinbox_check_valid = False
                    widgets_status.spinBox_Send_Float.setStyleSheet(MyMainWindow.str_spinbox_style_enable)
                    widgets_status.spinBox_Send_Int.setStyleSheet(MyMainWindow.str_spinbox_style_invalid)
                    widgets_status.spinBox_Send_Str.setStyleSheet(MyMainWindow.str_spinbox_style_invalid)
                    if widgets_status.spinBox_Send_Float.text() == widgets_status.spinBox_Send_Str.text():
                        widgets_status.spinBox_Send_Float.setStyleSheet(MyMainWindow.str_spinbox_style_invalid)
                        widgets_status.spinBox_Send_Str.setStyleSheet(MyMainWindow.str_spinbox_style_invalid)
                    else:
                        widgets_status.spinBox_Send_Float.setStyleSheet(MyMainWindow.str_spinbox_style_enable)
                elif widgets_status.spinBox_Send_Int.text() != widgets_status.spinBox_Send_Str.text():
                    widgets_status.spinBox_Send_Int.setStyleSheet(MyMainWindow.str_spinbox_style_enable)
                    if widgets_status.spinBox_Send_Float.text() == widgets_status.spinBox_Send_Str.text():
                        b_spinbox_check_valid = False
                        widgets_status.spinBox_Send_Float.setStyleSheet(MyMainWindow.str_spinbox_style_invalid)
                        widgets_status.spinBox_Send_Str.setStyleSheet(MyMainWindow.str_spinbox_style_invalid)
                    else:
                        b_spinbox_check_valid =True
                        widgets_status.spinBox_Send_Float.setStyleSheet(MyMainWindow.str_spinbox_style_enable)
                        widgets_status.spinBox_Send_Str.setStyleSheet(MyMainWindow.str_spinbox_style_enable)

            if widgets_status.lineEdit_StrSendSeparator.isEnabled():
                ins_re_match = re.match(r"[^A-Za-z\d.]", widgets_status.lineEdit_StrSendSeparator.text())
                if ins_re_match is not None:
                    widgets_status.lineEdit_StrSendSeparator.setStyleSheet(MyMainWindow.str_lineedit_style_enable)
                    b_lineedit_send_seperator_check_valid = True
                else:
                    widgets_status.lineEdit_StrSendSeparator.setStyleSheet(MyMainWindow.str_lineedit_style_invalid)
                    b_lineedit_send_seperator_check_valid = False

            else:
                b_lineedit_send_seperator_check_valid = True

            if widgets_status.lineEdit_SendInterval.isEnabled() and widgets_status.lineEdit_SendInterval.text() != "":
                try:
                    float(widgets_status.lineEdit_SendInterval.text())
                    widgets_status.lineEdit_SendInterval.setStyleSheet(MyMainWindow.str_lineedit_style_enable)
                    _socket.str_send_interval = widgets_status.lineEdit_SendInterval.text()
                    b_lineedit_send_interval_check_valid = True
                except ValueError:
                    widgets_status.lineEdit_SendInterval.setStyleSheet(MyMainWindow.str_lineedit_style_invalid)
                    b_lineedit_send_interval_check_valid = False
                    _socket.str_send_interval = widgets_status.lineEdit_SendInterval.text()
            else:
                b_lineedit_send_interval_check_valid = True

        if b_spinbox_check_valid and b_lineedit_check_valid == b_lineedit_check_valid_contrast and b_lineedit_send_interval_check_valid and b_lineedit_send_seperator_check_valid:
            _socket.b_continue_send = widgets_status.checkBox_SendContinue.isChecked()
            if not _socket.b_continue_send:
                widgets_status.pushButton_Send.setEnabled(True)
        else:
            widgets_status.pushButton_Send.setEnabled(False)
            _socket.b_continue_send = False

    @staticmethod
    def ui_update_rec_value_check(widgets_status: SocketWidgetStruct, _socket: SocketCommunicate):
        """

        """
        b_spinbox_check_valid = False
        b_lineedit_seperator_recv_check_valid = False
        b_lineedit_recv_interval_check_valid = False

        if widgets_status.checkBox_ReceiveStrMode.isEnabled() or widgets_status.checkBox_ReceiveRawbytesMode.isEnabled():
            if widgets_status.checkBox_Receive_Int.isChecked() + widgets_status.checkBox_Receive_Float.isChecked() + widgets_status.checkBox_Receive_Str.isChecked() == 0:
                if widgets_status.checkBox_ReceiveStrMode.isChecked():
                    b_spinbox_check_valid = True
                else:
                    if widgets_status.lineEdit_ReceiveFormatStr.text() != "":
                        b_spinbox_check_valid = True
                    else:
                        b_spinbox_check_valid = False
            elif widgets_status.checkBox_Receive_Int.isChecked() + widgets_status.checkBox_Receive_Float.isChecked() + widgets_status.checkBox_Receive_Str.isChecked() == 1:
                if widgets_status.checkBox_Receive_Int.isChecked():
                    widgets_status.spinBox_Receive_Int.setStyleSheet(MyMainWindow.str_spinbox_style_enable)
                elif widgets_status.checkBox_Receive_Float.isChecked():
                    widgets_status.spinBox_Receive_Float.setStyleSheet(MyMainWindow.str_spinbox_style_enable)
                else:
                    widgets_status.spinBox_Receive_Str.setStyleSheet(MyMainWindow.str_spinbox_style_enable)
                b_spinbox_check_valid = True
            elif widgets_status.checkBox_Receive_Int.isChecked() + widgets_status.checkBox_Receive_Float.isChecked() + widgets_status.checkBox_Receive_Str.isChecked() == 2:
                if not widgets_status.checkBox_Receive_Int.isChecked():
                    if widgets_status.spinBox_Receive_Float.text() == widgets_status.spinBox_Receive_Str.text():
                        widgets_status.spinBox_Receive_Float.setStyleSheet(MyMainWindow.str_spinbox_style_invalid)
                        widgets_status.spinBox_Receive_Str.setStyleSheet(MyMainWindow.str_spinbox_style_invalid)
                        b_spinbox_check_valid = False
                    else:
                        widgets_status.spinBox_Receive_Float.setStyleSheet(MyMainWindow.str_spinbox_style_enable)
                        widgets_status.spinBox_Receive_Str.setStyleSheet(MyMainWindow.str_spinbox_style_enable)
                        b_spinbox_check_valid = True

                elif not widgets_status.checkBox_Receive_Float.isChecked():
                    if widgets_status.spinBox_Receive_Int.text() == widgets_status.spinBox_Receive_Str.text():
                        widgets_status.spinBox_Receive_Int.setStyleSheet(MyMainWindow.str_spinbox_style_invalid)
                        widgets_status.spinBox_Receive_Str.setStyleSheet(MyMainWindow.str_spinbox_style_invalid)
                        b_spinbox_check_valid = False
                    else:
                        widgets_status.spinBox_Receive_Int.setStyleSheet(MyMainWindow.str_spinbox_style_enable)
                        widgets_status.spinBox_Receive_Str.setStyleSheet(MyMainWindow.str_spinbox_style_enable)
                        b_spinbox_check_valid = True
                else:
                    if widgets_status.spinBox_Receive_Int.text() == widgets_status.spinBox_Receive_Float.text():
                        widgets_status.spinBox_Receive_Float.setStyleSheet(MyMainWindow.str_spinbox_style_invalid)
                        widgets_status.spinBox_Receive_Int.setStyleSheet(MyMainWindow.str_spinbox_style_invalid)
                        b_spinbox_check_valid = False
                    else:
                        widgets_status.spinBox_Receive_Float.setStyleSheet(MyMainWindow.str_spinbox_style_enable)
                        widgets_status.spinBox_Receive_Int.setStyleSheet(MyMainWindow.str_spinbox_style_enable)
                        b_spinbox_check_valid = True

            elif widgets_status.checkBox_Receive_Int.isChecked() + widgets_status.checkBox_Receive_Float.isChecked() + widgets_status.checkBox_Receive_Str.isChecked() == 3:
                if widgets_status.spinBox_Receive_Int.text() == widgets_status.spinBox_Receive_Float.text():
                    b_spinbox_check_valid = False
                    widgets_status.spinBox_Receive_Int.setStyleSheet(MyMainWindow.str_spinbox_style_invalid)
                    widgets_status.spinBox_Receive_Float.setStyleSheet(MyMainWindow.str_spinbox_style_invalid)
                    if widgets_status.spinBox_Receive_Int.text() == widgets_status.spinBox_Receive_Str.text():
                        widgets_status.spinBox_Receive_Int.setStyleSheet(MyMainWindow.str_spinbox_style_invalid)
                        widgets_status.spinBox_Receive_Str.setStyleSheet(MyMainWindow.str_spinbox_style_invalid)
                    else:
                        widgets_status.spinBox_Receive_Str.setStyleSheet(MyMainWindow.str_spinbox_style_enable)
                elif widgets_status.spinBox_Receive_Int.text() == widgets_status.spinBox_Receive_Str.text():
                    b_spinbox_check_valid = False
                    widgets_status.spinBox_Receive_Float.setStyleSheet(MyMainWindow.str_spinbox_style_enable)
                    widgets_status.spinBox_Receive_Int.setStyleSheet(MyMainWindow.str_spinbox_style_invalid)
                    widgets_status.spinBox_Receive_Str.setStyleSheet(MyMainWindow.str_spinbox_style_invalid)
                    if widgets_status.spinBox_Receive_Float.text() == widgets_status.spinBox_Receive_Str.text():
                        widgets_status.spinBox_Receive_Float.setStyleSheet(MyMainWindow.str_spinbox_style_invalid)
                        widgets_status.spinBox_Receive_Str.setStyleSheet(MyMainWindow.str_spinbox_style_invalid)
                    else:
                        widgets_status.spinBox_Receive_Float.setStyleSheet(MyMainWindow.str_spinbox_style_enable)
                elif widgets_status.spinBox_Receive_Int.text() != widgets_status.spinBox_Receive_Str.text():
                    widgets_status.spinBox_Receive_Int.setStyleSheet(MyMainWindow.str_spinbox_style_enable)
                    if widgets_status.spinBox_Receive_Float.text() == widgets_status.spinBox_Receive_Str.text():
                        b_spinbox_check_valid = False
                        widgets_status.spinBox_Receive_Float.setStyleSheet(MyMainWindow.str_spinbox_style_invalid)
                        widgets_status.spinBox_Receive_Str.setStyleSheet(MyMainWindow.str_spinbox_style_invalid)
                    else:
                        b_spinbox_check_valid = True
                        widgets_status.spinBox_Receive_Float.setStyleSheet(MyMainWindow.str_spinbox_style_enable)
                        widgets_status.spinBox_Receive_Str.setStyleSheet(MyMainWindow.str_spinbox_style_enable)

            if widgets_status.lineEdit_StrReceiveSeparator.isEnabled():
                ins_re_match = re.match(r"[^A-Za-z\d.]", widgets_status.lineEdit_StrReceiveSeparator.text())
                if ins_re_match is not None:
                    widgets_status.lineEdit_StrReceiveSeparator.setStyleSheet(MyMainWindow.str_lineedit_style_enable)
                    b_lineedit_seperator_recv_check_valid = True
                else:
                    widgets_status.lineEdit_StrReceiveSeparator.setStyleSheet(MyMainWindow.str_lineedit_style_invalid)
                    b_lineedit_seperator_recv_check_valid = False
            else:
                b_lineedit_seperator_recv_check_valid = True

            if widgets_status.lineEdit_RecvInterval.isEnabled() and widgets_status.lineEdit_RecvInterval.text() != "":
                try:
                    float(widgets_status.lineEdit_RecvInterval.text())
                    widgets_status.lineEdit_RecvInterval.setStyleSheet(MyMainWindow.str_lineedit_style_enable)
                    b_lineedit_recv_interval_check_valid = True
                    _socket.b_continue_recv = widgets_status.checkBox_RecvContinue.isChecked()
                    _socket.str_recv_interval = widgets_status.lineEdit_RecvInterval.text()
                except ValueError:
                    widgets_status.lineEdit_RecvInterval.setStyleSheet(MyMainWindow.str_lineedit_style_invalid)
                    b_lineedit_recv_interval_check_valid = False
            else:
                b_lineedit_recv_interval_check_valid = True
                _socket.b_continue_recv = False
                _socket.str_recv_interval = widgets_status.lineEdit_RecvInterval.text()

            if widgets_status.lineEdit_Receive_Int.isEnabled() and widgets_status.lineEdit_Receive_Int.text() != "":
                try:
                    int(widgets_status.lineEdit_Receive_Int.text())
                    widgets_status.lineEdit_Receive_Int.setStyleSheet(MyMainWindow.str_lineedit_style_enable)
                except ValueError:
                    widgets_status.lineEdit_Receive_Int.setStyleSheet(MyMainWindow.str_lineedit_style_invalid)
                    _socket.b_continue_recv = False

            if widgets_status.lineEdit_Receive_Float.isEnabled() and widgets_status.lineEdit_Receive_Float.text() != "":
                try:
                    float(widgets_status.lineEdit_Receive_Float.text())
                    widgets_status.lineEdit_Receive_Float.setStyleSheet(MyMainWindow.str_lineedit_style_enable)
                except ValueError:
                    widgets_status.lineEdit_Receive_Float.setStyleSheet(MyMainWindow.str_lineedit_style_invalid)
                    _socket.b_continue_recv = False

            if widgets_status.lineEdit_Receive_Str.isEnabled() and widgets_status.lineEdit_Receive_Str.text() != "":
                try:
                    str(widgets_status.lineEdit_Receive_Str.text())
                    widgets_status.lineEdit_Receive_Str.setStyleSheet(MyMainWindow.str_lineedit_style_enable)
                except ValueError:
                    widgets_status.lineEdit_Receive_Str.setStyleSheet(MyMainWindow.str_lineedit_style_invalid)
                    _socket.b_continue_recv = False

            if b_spinbox_check_valid and b_lineedit_seperator_recv_check_valid and b_lineedit_recv_interval_check_valid:
                if not _socket.b_continue_recv:
                    widgets_status.pushButton_Receive.setEnabled(True)
                    widgets_status.pushButton_ClearCache.setEnabled(True)
            else:
                widgets_status.pushButton_Receive.setEnabled(False)
                widgets_status.pushButton_ClearCache.setEnabled(False)
        else:
            widgets_status.pushButton_Receive.setEnabled(False)
            widgets_status.pushButton_ClearCache.setEnabled(False)


    @staticmethod
    def ui_update_check_ip_port(widgets_status: SocketWidgetStruct):
        match_result_ip = re.match(r"((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}", widgets_status.lineEdit_IP.text())
        match_result_port = re.match(r"^\d+$", widgets_status.lineEdit_Port.text())
        if match_result_ip is None:
            widgets_status.lineEdit_IP.setStyleSheet(MyMainWindow.str_lineedit_style_invalid)
        else:
            widgets_status.lineEdit_IP.setStyleSheet(MyMainWindow.str_lineedit_style_enable)

        if match_result_port is None:
            widgets_status.lineEdit_Port.setStyleSheet(MyMainWindow.str_lineedit_style_invalid)
        else:
            widgets_status.lineEdit_Port.setStyleSheet(MyMainWindow.str_lineedit_style_enable)

        if match_result_ip is None or match_result_port is None:
            widgets_status.pushButton_CreateConnection.setEnabled(False)
        else:
            widgets_status.pushButton_CreateConnection.setEnabled(True)

if __name__ == '__main__':
    # format the application interface show as designer display
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    gui_app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    # print("Main thread", QThread.currentThread())
    sys.exit(gui_app.exec())
