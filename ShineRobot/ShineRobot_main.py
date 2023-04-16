#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Version : PyCharm
# @Time    : 2022/12/30 18:16
# @Author  : Pitt.Ding
# @File    : ShineRobot_main.py
# @Description :

import math
import sys
import time
import ctypes
import re
import struct
from collections import namedtuple
from PyQt5 import QtCore
from ShineRobot import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QAction
from PyQt5.Qt import QStandardItemModel, QCursor, Qt, QThread, pyqtSignal
from PyQt5.QtGui import QTextCursor
from shine_robot_socket_communication import SocketServer, SocketServerCloseClient, SocketClient
from functools import partial
from typing import Dict


name_tuple_Send = namedtuple("Send_widgets_Status", "fun_send int_checked int_seq int_text float_Checked float_seq float_text str_Checked str_seq str_text full_type_text full_type_format server_send_separator".split())
name_tuple_Receive = namedtuple("Receive_widgets_Status", "fun_receive int_checked int_seq int_text float_Checked float_seq float_text str_Checked str_seq str_text full_type_text full_type_format server_receive_separator".split())


class SocketWidgetStruct:
    def __int__(self):
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
        self.lineEdit_Receive_Str = None

        self.lineEdit_ReceiveFullType = None
        self.lineEdit_ReceiveFormatStr = None
        self.pushButton_Send = None
        self.pushButton_Receive = None


class MyMainWindow(QMainWindow, Ui_MainWindow):
    # initial the windows class
    # Signal should define in class not in instance
    signal_socket_server_not_accepted_close = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.right_click_menu = QMenu()
        # socket server
        self.socket_server = SocketServer()
        # socket server close client used to close blocking socket server
        self.socket_server_client = SocketServerCloseClient((self.lineEdit_SevIP.text(), self.lineEdit_SerPort.text()))

        # socket client
        self.socket_client = SocketClient()
        # socket communication thread
        self.Thread_socket_server = QThread()
        self.thread_close_socket_server = QThread()
        self.thread_socket_client = QThread()

        self.socket_server.moveToThread(self.Thread_socket_server)
        self.socket_server_client.moveToThread(self.thread_close_socket_server)

        # self.Thread_socket_server.started.connect(self.socket_server.create_socket_server)
        self.Thread_socket_server.start()
        self.thread_close_socket_server.start()
        # self.thread_socket_client.
        self.socket_client.moveToThread(self.thread_socket_client)
        self.thread_socket_client.start()

        # widgets status name tuple used as parameters by socket send and receive
        self.send_str_widgets_status = None
        self.send_rawbytes_widgets_status = None
        self.receive_str_widgets_status = None
        self.receive_rawbytes_widgets_status = None

        # append icon to taskbar in Windows system
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
        # call function which append widgets signal to slot

        # self.list_str_socket_widgets = "checkBox_SendString lineEdit_SendSeparator checkBox_SendRawbytes " \
        #         "checkBox_SendInt checkBox_SendFloat checkBox_SendStr " \
        #         "lineEdit_SendFullType lineEdit_SendFormatStr " \
        #         "checkBox_ReceiveStr lineEdit_ReceiveSeparator checkBox_ReceiveRawbytes" \
        #         "checkBox_ReceiveInt checkBox_ReceiveStr checkBox_ReceiveFloat " \
        #         "lineEdit_ReceiveFullType lineEdit_ReceiveFormatStr "
        # self.dict_widget_status_socket_server = {keyname: None for keyname in self.list_str_socket_widgets.split()}
        # self.dict_widget_status_socket_client = {'checkBox_SendString': 1, 'lineEdit_SendSeparator': None,
        #                                          'checkBox_SendRawbytes': None, 'checkBox_SendInt': None,
        #                                          'checkBox_SendFloat': None, 'checkBox_SendStr': None,
        #                                          'lineEdit_SendFullType': None,
        #                                          'lineEdit_SendFormatStr': None, 'checkBox_ReceiveStr': None,
        #                                          'lineEdit_ReceiveSeparator': None,
        #                                          'checkBox_ReceiveRawbytes': None, 'checkBox_ReceiveInt': None,
        #                                          'checkBox_ReceiveStr': None,
        #                                          'checkBox_ReceiveFloatlineEdit_ReceiveFullType': None,
        #                                          'lineEdit_ReceiveFormatStr': None}

        # server widgets
        self.server_widgets_status = SocketWidgetStruct()
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
        self.server_widgets_status.pushButton_Receive = self.pushButton_SerRecv
        # client widgets
        self.client_widgets_status = SocketWidgetStruct()
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

        self.client_widgets_status.checkBox_ReceiveStrMode = self.checkBox_ClntRecvStr
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
        self.client_widgets_status.pushButton_Receive = self.pushButton_ClntRecv

        self.init_append_customer_func()

    def init_append_customer_func(self):
        """
        customer the widgets signal to slot
        :return: none
        """
        self.pushButton_quaternion_euler.clicked.connect(self.quaternion_to_euler)
        self.pushButton_euler_quaternion.clicked.connect(self.euler_to_quaternion)
        self.pushButton_quaternion_clearinput.clicked.connect(self.clear_quaternion_input)
        self.pushButton_euler_clearinput.clicked.connect(self.clear_euler_input)
        self.pushButton_quaternion_copy.clicked.connect(self.copy_quaternion_result)
        self.pushButton_euler_copy.clicked.connect(self.copy_euler_result)
        self.textEdit_result_record.customContextMenuRequested.connect(self.qtextedit_custom_context_menu)
        # socket server send and receive event
        self.pushButton_SerCreateConn.clicked.connect(partial(self.socket_server.create_socket_server, (self.lineEdit_SevIP.text(), self.lineEdit_SerPort.text())), Qt.QueuedConnection)

        self.pushButton_SerCreateConn.clicked.connect(lambda: self.pushButton_SerCloseConn.setEnabled(True))
        self.pushButton_SerCreateConn.clicked.connect(lambda: self.pushButton_SerCreateConn.setDisabled(True))
        self.pushButton_SerCloseConn.clicked.connect(self.close_socket_server)
        self.pushButton_SerSend.clicked.connect(self.socket_server_send_message)
        self.pushButton_SerRecv.clicked.connect(self.socket_server_receive_message)
        self.socket_server.signal_socket_server_accepted.connect(partial(self.uiUpdate_Socket_Server_communicate_enable, widgets_status=self.server_widgets_status))
        # self.socket_server.signal_close_socket_server_thread.connect(self.close_socket_server_thread)
        self.socket_server.signal_record_result.connect(self.record_socket_communication_result)
        self.socket_server.signal_socket_server_closed.connect(self.pushButton_SerCreateConn.setEnabled)
        self.socket_server.signal_socket_server_closed.connect(self.pushButton_SerCloseConn.setDisabled)
        self.socket_server_client.signal_record_result.connect(self.record_socket_communication_result)
        self.socket_server_client.signal_socket_server_client_closed.connect(self.socket_server.close_socket_server)
        self.signal_socket_server_not_accepted_close.connect(self.socket_server_client.connect_to_Server)

        self.pushButton_ClntCreatConn.clicked.connect(partial(self.socket_client.create_socket_client, (self.lineEdit_ClntIP.text(), int(self.lineEdit_ClntPort.text()))))
        self.socket_client.signal_socket_client_connected.connect(self.pushButton_ClntCloseConn.setEnabled)
        self.socket_client.signal_socket_client_connected.connect(partial(self.uiUpdate_Socket_Server_communicate_enable, widgets_status=self.client_widgets_status))
        self.pushButton_ClntCloseConn.clicked.connect(self.socket_client.close_socket_client)
        self.socket_client.signal_record_result.connect(self.record_socket_communication_result)
        self.socket_client.signal_socket_client_closed.connect(self.pushButton_ClntCloseConn.setDisabled)

        self.checkBox_ServerSendString.clicked.connect(lambda: self.uiUpdate_checkbox_send_string_checked(self.server_widgets_status))
        self.checkBox_ServerSendRawbytes.clicked.connect(lambda: self.uiUpdate_checkbox_send_rawbytes_checked(self.server_widgets_status))
        self.checkBox_ServerReceiveString.clicked.connect(lambda: self.uiUpdate_checkbox_send_string_checked(self.server_widgets_status))
        self.checkBox_ServerReceiveRawbytes.clicked.connect(lambda: self.uiUpdate_checkbox_send_rawbytes_checked(self.server_widgets_status))
        self.checkBox_ClientSendString.clicked.connect(lambda: self.uiUpdate_checkbox_send_string_checked(self.client_widgets_status))
        self.checkBox_ClientSendRawbytes.clicked.connect(lambda: self.uiUpdate_checkbox_send_rawbytes_checked(self.client_widgets_status))
        self.checkBox_ClientReceiveString.clicked.connect(lambda: self.uiUpdate_checkbox_send_string_checked(self.client_widgets_status))
        self.checkBox_ClientReceiveRawbytes.clicked.connect(lambda: self.uiUpdate_checkbox_send_rawbytes_checked(self.client_widgets_status))
        # initial for checkbox sequence and values
        self.checkBox_SerSendInt.clicked.connect(self.uiUpdate_checkbox_toggle_init)
        self.checkBox_SerSendFloat.clicked.connect(self.uiUpdate_checkbox_toggle_init)
        self.checkBox_SerSendStr.clicked.connect(self.uiUpdate_checkbox_toggle_init)
        self.checkBox_SerRecvInt.clicked.connect(self.uiUpdate_checkbox_toggle_init)
        self.checkBox_SerRecvFloat.clicked.connect(self.uiUpdate_checkbox_toggle_init)
        self.checkBox_SerRecvStr.clicked.connect(self.uiUpdate_checkbox_toggle_init)

        self.checkBox_ClntSendInt.clicked.connect(self.uiUpdate_checkbox_toggle_init)
        self.checkBox_ClntSendFloat.clicked.connect(self.uiUpdate_checkbox_toggle_init)
        self.checkBox_ClntSendStr.clicked.connect(self.uiUpdate_checkbox_toggle_init)
        self.checkBox_ClntRecvInt.clicked.connect(self.uiUpdate_checkbox_toggle_init)
        self.checkBox_ClntRecvFloat.clicked.connect(self.uiUpdate_checkbox_toggle_init)
        self.checkBox_ClntRecvStr.clicked.connect(self.uiUpdate_checkbox_toggle_init)

        # check line edit widgets values
        self.lineEdit_SerSendInt_Value.textChanged.connect(lambda: self.uiUpdate_SerSendValueCheck(self.server_widgets_status))
        self.lineEdit_SerSendFloat_Value.textChanged.connect(lambda: self.uiUpdate_SerSendValueCheck(self.server_widgets_status))
        self.lineEdit_SerSendstr_Value.textChanged.connect(lambda: self.uiUpdate_SerSendValueCheck(self.server_widgets_status))

        self.lineEdit_ClntSendInt_Value.textChanged.connect(lambda: self.uiUpdate_SerSendValueCheck(self.client_widgets_status))
        self.lineEdit_ClntSendFloat_Value.textChanged.connect(lambda: self.uiUpdate_SerSendValueCheck(self.client_widgets_status))
        self.lineEdit_ClntSendStr_Value.textChanged.connect(lambda: self.uiUpdate_SerSendValueCheck(self.client_widgets_status))
        # check spin box widgets sequences
        self.spinBox_SerSendInt_Seq.textChanged.connect(lambda: self.uiUpdate_SerSendValueCheck(self.server_widgets_status))
        self.spinBox_SerSendFloat_Seq.textChanged.connect(lambda: self.uiUpdate_SerSendValueCheck(self.server_widgets_status))
        self.spinBox_SerSendStr_Seq.textChanged.connect(lambda: self.uiUpdate_SerSendValueCheck(self.server_widgets_status))
        self.spinBox_SerRecvInt_Seq.textChanged.connect(lambda: self.uiUpdate_serRecValueCheck(self.server_widgets_status))
        self.spinBox_SerRecvFloat_Seq.textChanged.connect(lambda: self.uiUpdate_serRecValueCheck(self.server_widgets_status))
        self.spinBox_SerRecvStr_Seq.textChanged.connect(lambda: self.uiUpdate_serRecValueCheck(self.server_widgets_status))

        self.spinBox_ClntSendInt_Seq.textChanged.connect(lambda: self.uiUpdate_SerSendValueCheck(self.client_widgets_status))
        self.spinBox_ClntSendFloat_Seq.textChanged.connect(lambda: self.uiUpdate_SerSendValueCheck(self.client_widgets_status))
        self.spinBox_ClntSendStr_Seq.textChanged.connect(lambda: self.uiUpdate_SerSendValueCheck(self.client_widgets_status))
        self.spinBox_ClntRecvInt_Seq.textChanged.connect(lambda: self.uiUpdate_serRecValueCheck(self.client_widgets_status))
        self.spinBox_ClntRecvFloat_Seq.textChanged.connect(lambda: self.uiUpdate_serRecValueCheck(self.client_widgets_status))
        self.spinBox_ClntRecvStr_Seq.textChanged.connect(lambda: self.uiUpdate_serRecValueCheck(self.client_widgets_status))

        # socket server send and receive full type mode, auto uncheck the single mode check box
        self.lineEdit_SerSendFullType.textChanged.connect(lambda: self.uiUpdate_server_full_type_mode(self.server_widgets_status))
        self.lineEdit_SerSendFormatStr.textChanged.connect(lambda: self.uiUpdate_server_full_type_mode(self.server_widgets_status))
        self.lineEdit_SerRecvFormatStr.textChanged.connect(lambda: self.uiUpdate_server_full_type_mode(self.server_widgets_status))
        self.lineEdit_ClntSendFullType.textChanged.connect(lambda: self.uiUpdate_server_full_type_mode(self.client_widgets_status))
        self.lineEdit_ClntSendFormatStr.textChanged.connect(lambda: self.uiUpdate_server_full_type_mode(self.client_widgets_status))
        self.lineEdit_ClntRecvFormatStr.textChanged.connect(lambda: self.uiUpdate_server_full_type_mode(self.client_widgets_status))
        # ------------------------------------------------------------------------------------------------------------------
        # -----------------------quaternion and euler convert function------------------------------------------------------
        # ------------------------------------------------------------------------------------------------------------------

    def quaternion_to_euler(self):
        """
        calculate the quaternion to euler
        quaternion and euler values all get or return to lineedit
        :return: none
        """
        _tuple_quaternion = tuple(float(x) for x in (self.lineEdit_quaternion_q1.text(),
                                                     self.lineEdit_quaternion_q2.text(),
                                                     self.lineEdit_quaternion_q3.text(),
                                                     self.lineEdit_quaternion_q4.text()))
        q1, q2, q3, q4 = _tuple_quaternion

        _record_str = 'Request convert quaternion to euler, input is: ' + str(list(_tuple_quaternion))
        self.record_convert_result(_record_str)

        angle_x = math.atan2(2 * (q1 * q2 + q3 * q4), 1 - 2 * (q2 * q2 + q3 * q3))
        angle_y = math.asin(2 * (q1 * q3 - q4 * q2))
        angle_z = math.atan2(2 * (q1 * q4 + q2 * q3), 1 - 2 * (q3 * q3 + q4 * q4))

        angle_x = math.degrees(angle_x)
        angle_y = math.degrees(angle_y)
        angle_z = math.degrees(angle_z)

        _list_quaternion_result = list([round(x, 3) for x in [angle_x, angle_y, angle_z]])
        self.lineEdit_quaternion_result.setText(str(_list_quaternion_result))

        _record_str = 'Convert Result: ' + str(_list_quaternion_result)
        self.record_convert_result(_record_str)

    def euler_to_quaternion(self):
        """
        calculate the euler to quaternion
        euler and quaternion values all get or return to lineedit
        :return: none
        """
        _tuple_input = tuple((float(x) for x in (self.lineEdit_euler_rotx.text(),
                                                 self.lineEdit_euler_roty.text(),
                                                 self.lineEdit_euler_rotz.text())))

        _record_str = 'Request convert euler to quaternion, input is: ' + str(list(_tuple_input))
        self.record_convert_result(_record_str)

        angle_x, angle_y, angle_z = map(math.radians, _tuple_input)
        sin_x = math.sin(angle_x / 2)
        sin_y = math.sin(angle_y / 2)
        sin_z = math.sin(angle_z / 2)

        cos_x = math.cos(angle_x / 2)
        cos_y = math.cos(angle_y / 2)
        cos_z = math.cos(angle_z / 2)

        q1 = cos_x * cos_y * cos_z + sin_x * sin_y * sin_z
        q2 = sin_x * cos_y * cos_z - cos_x * sin_y * sin_z
        q3 = cos_x * sin_y * cos_z + sin_x * cos_y * sin_z
        q4 = cos_x * cos_y * sin_z - sin_x * sin_y * cos_z
        _list_euler_result = list((round(x, 6) for x in (q1, q2, q3, q4)))
        self.lineEdit_euler_result.setText(str(_list_euler_result))

        _record_str = 'Convert Result: ' + str(_list_euler_result)
        self.record_convert_result(_record_str)

    def clear_quaternion_input(self):
        """
        clear the quaternion lineedit values
        :return: none
        """
        self.lineEdit_quaternion_q1.setText(str(0.0))
        self.lineEdit_quaternion_q2.setText(str(0.0))
        self.lineEdit_quaternion_q3.setText(str(0.0))
        self.lineEdit_quaternion_q4.setText(str(0.0))
        self.lineEdit_quaternion_result.setText('')

    def clear_euler_input(self):
        """
        clear the euler lineedit values
        :return: none
        """
        self.lineEdit_euler_rotx.setText(str(0.0))
        self.lineEdit_euler_roty.setText(str(0.0))
        self.lineEdit_euler_rotz.setText(str(0.0))
        self.lineEdit_euler_result.setText('')

    def record_convert_result(self, str_record: str):
        """
        write record and date to textedit
        :param str_record: string that need to write
        :return: none
        """
        _str_time = time.strftime('%Y-%m-%d: %H:%M:%S ', time.localtime())
        self.textEdit_result_record.append(_str_time + str_record)

    def copy_quaternion_result(self):
        """
        copy quaternion result form lineedit
        :return: none
        """
        self.lineEdit_quaternion_result.selectAll()
        self.lineEdit_quaternion_result.copy()
        self.lineEdit_quaternion_result.deselect()

    def copy_euler_result(self):
        """
        copy euler result from lineedit
        :return: none
        """
        self.lineEdit_euler_result.selectAll()
        self.lineEdit_euler_result.copy()
        self.lineEdit_euler_result.deselect()

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
    def close_socket_server(self):
        """
        close the socket server socket
        :return: none
        """
        try:
            if self.socket_server.socket_server_accept_client is None:
                self.signal_socket_server_not_accepted_close.emit()
            else:
                self.socket_server.close_socket_server()
        except OSError as e:
            self.record_socket_communication_result(str(e))
            self.record_socket_communication_result("OSError happened when close the socket server connection,"
                                                    " please check!")

    def socket_send_string(self, _send_widget_args: name_tuple_Send) -> None:
        """
        Base send widgets status quote send string function,use name tuple as input args,suit for both server and client
        """
        _send_fun, _int_checked, _int_seq, _int_text, _float_checked, _float_seq, _float_text,\
            _str_checked, _str_seq, _str_text, _full_type_str_text, _full_type_format_str_text, _send_str_Separator_text = _send_widget_args

        if _int_checked + _float_checked + _str_checked == 1:
            if _int_checked:
                _send_fun(_int_text)
            elif _float_checked:
                _send_fun(_float_text)
            else:
                _send_fun(_str_text)

        elif _int_checked + _float_checked + _str_checked == 2:
            if not _int_checked:
                if int(_float_seq) > int(_str_seq):
                    _send_fun(_float_text + _send_str_Separator_text + _str_text)
                else:
                    _send_fun(_str_text + _send_str_Separator_text + _float_text)
            elif not _float_checked:
                if int(_int_seq) > int(_str_seq):
                    _send_fun(_int_text + _send_str_Separator_text + _str_text)
                else:
                    _send_fun(_str_text + _send_str_Separator_text + _int_text)
            else:
                if int(_int_seq) > int(_float_seq):
                    _send_fun(_int_text + _send_str_Separator_text + _float_text)
                else:
                    _send_fun(_float_text + _send_str_Separator_text + _int_text)

        elif _int_checked + _float_checked + _str_checked == 3:
            # 生成字列表，并对列表按键值做排序
            m_sequence_list = [[int(_int_seq), _int_text],
                               [int(_float_seq), _float_text],
                               [int(_str_seq), _str_text]]
            m_sequence_list.sort(key=lambda x: x[0], reverse=True)
            _send_fun(str(m_sequence_list[0][1]) + _send_str_Separator_text + str(m_sequence_list[1][1])
                      + _send_str_Separator_text + str(m_sequence_list[2][1]))
        else:
            _send_fun(_full_type_str_text)

    def socket_send_rawbytes(self, _send_widget_args):
        """
        Base send widgets status quote send rawbytes function,use name tuple as input args,suit for both server and client
        """

        _send_fun, _int_checked, _int_seq, _int_text, _float_checked, _float_seq, _float_text, \
            _str_checked, _str_seq, _str_text, _full_type_str_text, \
            _full_type_format_str_text, _send_str_Separator_text = _send_widget_args

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
                    _send_fun(struct.pack("<f{}s".format(len(_str_text)), float(_float_text), _str_text.encode()))
                else:
                    _send_fun(struct.pack("<{}sf".format(len(_str_text)), _str_text.encode(), float(_float_text)))
            elif not _float_checked:
                if int(_int_seq) > int(_str_seq):
                    _send_fun(struct.pack("<h{}s".format(len(_str_text)), int(_int_text), _str_text.encode()))
                else:
                    _send_fun(struct.pack("<{}sh".format(len(_str_text)), _str_text.encode(), int(_int_text)))
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
            _send_fun(struct.pack("<" + m_sequence_list[0][2] + m_sequence_list[1][2] + m_sequence_list[2][2],
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

    def socket_server_send_message(self):
        """
        send message as the checkbox setting
        :return: None
        """

        try:
            if self.pushButton_SerSend.isEnabled():
                if self.checkBox_ServerSendString.isChecked():
                    self.send_str_widgets_status = name_tuple_Send(self.socket_server.socket_server_send,
                                                                   self.checkBox_SerSendInt.isChecked(),
                                                                   self.spinBox_SerSendInt_Seq.text(),
                                                                   self.lineEdit_SerSendInt_Value.text(),
                                                                   self.checkBox_SerSendFloat.isChecked(),
                                                                   self.spinBox_SerSendFloat_Seq.text(),
                                                                   self.lineEdit_SerSendFloat_Value.text(),
                                                                   self.checkBox_SerSendStr.isChecked(),
                                                                   self.spinBox_SerSendStr_Seq.text(),
                                                                   self.lineEdit_SerSendstr_Value.text(),
                                                                   self.lineEdit_SerSendFullType.text(),
                                                                   self.lineEdit_SerSendFormatStr.text(),
                                                                   self.lineEdit_ServerSendSeparator.text())
                    self.socket_send_string(self.send_str_widgets_status)

                elif self.checkBox_ServerSendRawbytes.isChecked():
                    self.send_rawbytes_widgets_status = name_tuple_Send(self.socket_server.socket_server_send,
                                                                   self.checkBox_SerSendInt.isChecked(),
                                                                   self.spinBox_SerSendInt_Seq.text(),
                                                                   self.lineEdit_SerSendInt_Value.text(),
                                                                   self.checkBox_SerSendFloat.isChecked(),
                                                                   self.spinBox_SerSendFloat_Seq.text(),
                                                                   self.lineEdit_SerSendFloat_Value.text(),
                                                                   self.checkBox_SerSendStr.isChecked(),
                                                                   self.spinBox_SerSendStr_Seq.text(),
                                                                   self.lineEdit_SerSendstr_Value.text(),
                                                                   self.lineEdit_SerSendFullType.text(),
                                                                   self.lineEdit_SerSendFormatStr.text(),
                                                                   self.lineEdit_ServerSendSeparator.text())
                    self.socket_send_rawbytes(self.send_rawbytes_widgets_status)

        except ValueError as e:
            self.record_socket_communication_result(str(e))
            self.record_socket_communication_result("Send value format error, please check!")
            return

    def socket_receive_string(self, _receive_widget_args):
        """
        Base send widgets status quote receive string function,use name tuple as input args,suit for both server and client
        """
        _recv_fun, _int_checked, _int_seq, _int_text_lineedit, _float_checked, _float_seq, _float_text_lineedit, \
            _str_checked, _str_seq, _str_text_lineedit, _full_type_str_text_lineedit, _full_type_format_str_text, \
            _recv_str_Separator_text = _receive_widget_args

        if _int_checked + _float_checked + _str_checked == 0:
            _full_type_str_text_lineedit.setText(_recv_fun().decode())
        if _int_checked + _float_checked + _str_checked == 1:
            if _int_checked:
                try:
                    m_int = int(_recv_fun().decode())
                    _int_text_lineedit.setText(str(m_int))
                except ValueError:
                    _int_text_lineedit.clear()
                    self.record_socket_communication_result("Receive value except INT but not ")
                    return

            elif _float_checked:
                try:
                    m_float = float(_recv_fun().decode())
                    _float_text_lineedit.setText(str(m_float))
                except ValueError:
                    _float_text_lineedit.clear()
                    self.record_socket_communication_result("Receive value except FLOAT but not ")
                    return

            else:
                try:
                    m_str = _recv_fun().decode()
                    _str_text_lineedit.setText(m_str)
                except ValueError:
                    _str_text_lineedit.clear()
                    self.record_socket_communication_result("Receive value except STRING but not ")
                    return

        elif _int_checked + _float_checked + _str_checked == 2:
            if not _int_checked:
                if int(_float_seq) > int(_str_seq):
                    try:
                        _float_str, _string = _recv_fun().decode().split(_recv_str_Separator_text)
                        _float_text_lineedit.setText(_float_str)
                        _str_text_lineedit.setText(_string)
                    except ValueError:
                        _float_text_lineedit.clear()
                        _str_text_lineedit.clear()
                        self.record_socket_communication_result("Receive values is not identical with Receive setting ")
                        return
                else:
                    try:
                        _string, _float_str = _recv_fun().decode().split(_recv_str_Separator_text)
                        _float_text_lineedit.setText(_float_str)
                        _str_text_lineedit.setText(_string)
                    except ValueError:
                        _float_text_lineedit.clear()
                        _str_text_lineedit.clear()
                        self.record_socket_communication_result("Receive values is not identical with Receive setting ")
                        return
            elif not _float_checked:
                if int(_int_seq) > int(_str_seq):
                    try:
                        _int_str, _string = _recv_fun().decode().split(_recv_str_Separator_text)
                        _int_text_lineedit.setText(_int_str)
                        _str_text_lineedit.setText(_string)
                    except ValueError:
                        _int_text_lineedit.clear()
                        _str_text_lineedit.clear()
                        self.record_socket_communication_result("Receive values is not identical with Receive setting ")
                        return
                else:
                    try:
                        _string, _int_str = _recv_fun().decode().split(_recv_str_Separator_text)
                        _int_text_lineedit.setText(_int_str)
                        _str_text_lineedit.setText(_string)
                    except ValueError:
                        _int_text_lineedit.clear()
                        _str_text_lineedit.clear()
                        self.record_socket_communication_result("Receive values is not identical with Receive setting ")
                        return
            else:
                if int(_int_seq) > int(_float_seq):
                    try:
                        _int_str, _float_str = _recv_fun().decode().split(_recv_str_Separator_text)
                        _int_text_lineedit.setText(_int_str)
                        _float_text_lineedit.setText(_float_str)
                    except ValueError:
                        _int_text_lineedit.clear()
                        _float_text_lineedit.clear()
                        self.record_socket_communication_result("Receive values is not identical with Receive setting ")
                        return
                else:
                    try:
                        _float_str, _int_str = _recv_fun().decode().split(_recv_str_Separator_text)
                        _int_text_lineedit.setText(_int_str)
                        _float_text_lineedit.setText(_float_str)
                    except ValueError:
                        _int_text_lineedit.clear()
                        _float_text_lineedit.clear()
                        self.record_socket_communication_result("Receive values is not identical with Receive setting ")
                        return

        elif _int_checked + _float_checked + _str_checked == 3:
            try:
                # sort receive sequence value as sequence settlement
                list_type = sorted([[_int_seq, None], [_float_seq, None], [_str_seq, None]], key=lambda x: int(x[0]), reverse=True)
                list_type[0][1], list_type[1][1], list_type[2][1] = _recv_fun().decode().split(_recv_str_Separator_text)
                _int_text_lineedit.setText([x[1] for x in list_type if x[0] == _int_seq][0])
                _float_text_lineedit.setText([x[1] for x in list_type if x[0] == _float_seq][0])
                _str_text_lineedit.setText([x[1] for x in list_type if x[0] == _str_seq][0])
            except ValueError:
                _int_text_lineedit.clear()
                _float_text_lineedit.clear()
                _str_text_lineedit.clear()
                self.record_socket_communication_result("Receive values is not identical with Receive setting ")
                return

    def socket_receive_rawbytes(self, _receive_widget_args):
        """
        Base send widgets status quote receive string function,use name tuple as input args,suit for both server and client
        """
        _recv_fun, _int_checked, _int_seq, _int_text_lineedit, _float_checked, _float_seq, _float_text_lineedit, \
            _str_checked, _str_seq, _str_text_lineedit, _full_type_str_text_lineedit, _full_type_format_str_text,\
            _recv_str_Separator_text = _receive_widget_args

        _server_receive_rawbytes_length = 5
        if _int_checked + _float_checked + _str_checked == 0:
            try:
                _tuple = struct.unpack(_full_type_format_str_text, _recv_fun())
                _full_type_str_text_lineedit.setText(str(_tuple))
            except (struct.error, ValueError):
                _full_type_str_text_lineedit.clear()
                self.record_socket_communication_result("Can't parse receive data,please check")

        if _int_checked + _float_checked + _str_checked == 1:
            if _int_checked:
                try:
                    _int, = struct.unpack('<h', _recv_fun())
                    _int_text_lineedit.setText(str(_int))
                except (struct.error, ValueError):
                    _int_text_lineedit.clear()
                    self.record_socket_communication_result("Can't parse receive data,please check")

            elif _float_checked:
                try:
                    _float, = struct.unpack('<f', _recv_fun())
                    _float_text_lineedit.setText(str(_float))
                except (struct.error, ValueError):
                    _float_text_lineedit.clear()
                    self.record_socket_communication_result("Can't parse receive data,please check")

            else:
                try:
                    _string, = struct.unpack('<{}s'.format(_server_receive_rawbytes_length), _recv_fun())
                    _str_text_lineedit.setText(str(_string.decode()))
                except (struct.error, ValueError):
                    _str_text_lineedit.clear()
                    self.record_socket_communication_result("Can't parse receive data,please check")

        elif _int_checked + _float_checked + _str_checked == 2:
            if not _int_checked:
                if int(_float_seq) > int(_str_seq):
                    try:
                        _float, _str = struct.unpack('<f{}s'.format(_server_receive_rawbytes_length), _recv_fun())
                        _float_text_lineedit.setText(str(_float))
                        _str_text_lineedit.setText(str(_str))
                    except (struct.error, ValueError):
                        _float_text_lineedit.clear()
                        _str_text_lineedit.clear()
                        self.record_socket_communication_result("Can't parse receive data,please check")

                else:
                    try:
                        _str, _float = struct.unpack('<{}sf'.format(_server_receive_rawbytes_length), _recv_fun())
                        _float_text_lineedit.setText(str(_float))
                        _str_text_lineedit.setText(str(_str))
                    except (struct.error, ValueError):
                        _float_text_lineedit.clear()
                        _str_text_lineedit.clear()
                        self.record_socket_communication_result("Can't parse receive data,please check")

            elif not _float_checked:
                if int(_int_seq) > int(_str_seq):
                    try:
                        _int, _str = struct.unpack('<h{}s'.format(_server_receive_rawbytes_length),
                                                   self.socket_server.socket_server_receive())
                        _int_text_lineedit.setText(str(_int))
                        _str_text_lineedit.setText(str(_str))
                    except (struct.error, ValueError):
                        _int_text_lineedit.clear()
                        _str_text_lineedit.clear()
                        self.record_socket_communication_result("Can't parse receive data,please check")
                else:
                    try:
                        _str, _int, = struct.unpack('<{}sh'.format(_server_receive_rawbytes_length), _recv_fun())
                        _int_text_lineedit.setText(str(_int))
                        _str_text_lineedit.setText(str(_str))
                    except (struct.error, ValueError):
                        _int_text_lineedit.clear()
                        _str_text_lineedit.clear()
                        self.record_socket_communication_result("Can't parse receive data,please check")
            else:
                if int(_int_seq) > int(_float_seq):
                    try:
                        _int, _float = struct.unpack('<hf', _recv_fun())
                        _int_text_lineedit.setText(str(_int))
                        _float_text_lineedit.setText(str(_float))
                    except (struct.error, ValueError):
                        _int_text_lineedit.clear()
                        _float_text_lineedit.clear()
                        self.record_socket_communication_result("Can't parse receive data,please check")
                else:
                    try:
                        _float, _int = struct.unpack('<fh', _recv_fun())
                        _int_text_lineedit.setText(str(_int))
                        _float_text_lineedit.setText(str(_float))
                    except (struct.error, ValueError):
                        _int_text_lineedit.clear()
                        _float_text_lineedit.clear()
                        self.record_socket_communication_result("Can't parse receive data,please check")
        elif _int_checked + _float_checked + _str_checked == 3:
            try:
                # append sort logic
                list_type = sorted([[_int_seq, None, "h"], [_float_seq, None, "f"], [_str_seq, None, "s"]], key=lambda x: int(x[0]),
                                   reverse=True)
                _unpack_format_str = "<" + list_type[0][2] + list_type[1][2] + "{" + "}" + list_type[2][2]
                list_type[0][1], list_type[1][1], list_type[2][1] = list(struct.unpack(_unpack_format_str.format(_server_receive_rawbytes_length), _recv_fun()))

                _int_text_lineedit.setText([str(x[1]) for x in list_type if x[0] == _int_seq][0])
                _float_text_lineedit.setText([str(x[1]) for x in list_type if x[0] == _float_seq][0])
                _str_text_lineedit.setText([str(x[1]) for x in list_type if x[0] == _str_seq][0])
            except (struct.error, ValueError):
                _int_text_lineedit.clear()
                _float_text_lineedit.clear()
                _str_text_lineedit.clear()
                self.record_socket_communication_result("Can't parse receive data,please check")

    def socket_server_receive_message(self):
        """
        socket server receive message from client
        :return:
        """
        try:
            if self.checkBox_ServerReceiveString.isChecked():
                self.receive_str_widgets_status = name_tuple_Receive(self.socket_server.socket_server_receive,
                                                                    self.checkBox_SerRecvInt.isChecked(),
                                                                    self.spinBox_SerRecvInt_Seq.text(),
                                                                    self.lineEdit_SerRecvInt_Value,
                                                                    self.checkBox_SerRecvFloat.isChecked(),
                                                                    self.spinBox_SerRecvFloat_Seq.text(),
                                                                    self.lineEdit_SerRecvFloat_Value,
                                                                    self.checkBox_SerRecvStr.isChecked(),
                                                                    self.spinBox_SerRecvStr_Seq.text(),
                                                                    self.lineEdit_SerRecvStr_Value,
                                                                    self.lineEdit_SerRecvFullType,
                                                                    self.lineEdit_SerRecvFormatStr.text(),
                                                                    self.lineEdit_ServerReceiveSeparator.text())

                self.socket_receive_string(self.receive_str_widgets_status)

            elif self.checkBox_ServerReceiveRawbytes.isChecked():
                self.receive_rawbytes_widgets_status = name_tuple_Receive(self.socket_server.socket_server_receive,
                                                                     self.checkBox_SerRecvInt.isChecked(),
                                                                     self.spinBox_SerRecvInt_Seq.text(),
                                                                     self.lineEdit_SerRecvInt_Value,
                                                                     self.checkBox_SerRecvFloat.isChecked(),
                                                                     self.spinBox_SerRecvFloat_Seq.text(),
                                                                     self.lineEdit_SerRecvFloat_Value,
                                                                     self.checkBox_SerRecvStr.isChecked(),
                                                                     self.spinBox_SerRecvStr_Seq.text(),
                                                                     self.lineEdit_SerRecvStr_Value,
                                                                     self.lineEdit_SerRecvFullType,
                                                                     self.lineEdit_SerRecvFormatStr.text(),
                                                                     self.lineEdit_ServerReceiveSeparator.text())

                self.socket_receive_rawbytes(self.receive_rawbytes_widgets_status)

        except TypeError as e:
            self.record_socket_communication_result(str(e))
            self.record_socket_communication_result("receive value error, please check!")
            return
        # 检查调用Socket receive方法是否接收数据超时，如果是则发布信息并return
        except OSError:
            self.record_socket_communication_result("Doesn't receive data, please check")
            return

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

    def uiUpdate_Socket_Server_communicate_enable(self, b_accepted: bool, widgets_status: SocketWidgetStruct) -> None:
        """
        enable send and receive widgets after socket server accept connection
        :param b_accepted:
        :param widgets_status:
        :return:
        """

        if b_accepted:
            # send widgets
            widgets_status.checkBox_SendStringMode.setEnabled(True)
            widgets_status.lineEdit_StrSendSeparator.setEnabled(True)
            widgets_status.checkBox_SendRawbytesMode.setEnabled(True)

            widgets_status.checkBox_Send_Int.setEnabled(True)
            widgets_status.checkBox_Send_Str.setEnabled(True)
            widgets_status.checkBox_Send_Float.setEnabled(True)

            widgets_status.lineEdit_SendFullType.setEnabled(True)
            widgets_status.lineEdit_SendFullType.setFocusPolicy(Qt.StrongFocus)
            widgets_status.lineEdit_SendFormatStr.setEnabled(True)
            widgets_status.lineEdit_SendFormatStr.setFocusPolicy(Qt.StrongFocus)

            # receive widgets
            widgets_status.checkBox_ReceiveStrMode.setEnabled(True)
            widgets_status.lineEdit_StrReceiveSeparator.setEnabled(True)
            widgets_status.checkBox_ReceiveRawbytesMode.setEnabled(True)

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
            widgets_status.lineEdit_StrSendSeparator.setEnabled(False)
            widgets_status.checkBox_SendRawbytesMode.setChecked(False)
            widgets_status.checkBox_SendRawbytesMode.setEnabled(False)

            widgets_status.checkBox_Send_Int.setChecked(False)
            widgets_status.checkBox_Send_Int.setEnabled(False)

            widgets_status.checkBox_Send_Float.setChecked(False)
            widgets_status.checkBox_Send_Float.setEnabled(False)

            widgets_status.checkBox_Send_Str.setChecked(False)
            widgets_status.checkBox_Send_Str.setEnabled(False)

            widgets_status.lineEdit_SendFullType.clear()
            widgets_status.lineEdit_SendFullType.setEnabled(False)
            widgets_status.lineEdit_SendFormatStr.clear()
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

            widgets_status.lineEdit_ReceiveFormatStr.clear()
            widgets_status.lineEdit_ReceiveFormatStr.setEnabled(False)

            widgets_status.lineEdit_ReceiveFullType.clear()
            widgets_status.lineEdit_ReceiveFullType.setFocusPolicy(Qt.NoFocus)
            widgets_status.lineEdit_ReceiveFullType.setEnabled(False)

            self.uiUpdate_checkbox_toggle_init()

        # if b_accepted:
        #     # send widgets
        #     self.checkBox_ServerSendString.setEnabled(True)
        #     self.lineEdit_ServerSendSeparator.setEnabled(True)
        #     self.checkBox_ServerSendRawbytes.setEnabled(True)
        #
        #     self.checkBox_SerSendInt.setEnabled(True)
        #     self.checkBox_SerSendStr.setEnabled(True)
        #     self.checkBox_SerSendFloat.setEnabled(True)
        #
        #     self.lineEdit_SerSendFullType.setEnabled(True)
        #     self.lineEdit_SerSendFullType.setFocusPolicy(Qt.StrongFocus)
        #     self.lineEdit_SerSendFormatStr.setEnabled(True)
        #     self.lineEdit_SerSendFormatStr.setFocusPolicy(Qt.StrongFocus)
        #
        #     # receive widgets
        #     self.checkBox_ServerReceiveString.setEnabled(True)
        #     self.lineEdit_ServerReceiveSeparator.setEnabled(True)
        #     self.checkBox_ServerReceiveRawbytes.setEnabled(True)
        #
        #     self.checkBox_SerRecvInt.setEnabled(True)
        #     self.checkBox_SerRecvStr.setEnabled(True)
        #     self.checkBox_SerRecvFloat.setEnabled(True)
        #     self.lineEdit_SerRecvFullType.setEnabled(True)
        #     self.lineEdit_SerRecvFullType.setFocusPolicy(Qt.StrongFocus)
        #     self.lineEdit_SerRecvFormatStr.setEnabled(True)
        #     self.lineEdit_SerRecvFormatStr.setFocusPolicy(Qt.StrongFocus)
        #
        # else:
        #     # send widgets
        #     self.checkBox_ServerSendString.setChecked(True)
        #     self.checkBox_ServerSendString.setEnabled(False)
        #     self.lineEdit_ServerSendSeparator.setEnabled(False)
        #     self.checkBox_ServerSendRawbytes.setChecked(False)
        #     self.checkBox_ServerSendRawbytes.setEnabled(False)
        #
        #     self.checkBox_SerSendInt.setChecked(False)
        #     # self.uiUpdate_checkbox_toggle_init()
        #     self.checkBox_SerSendInt.setEnabled(False)
        #
        #     self.checkBox_SerSendFloat.setChecked(False)
        #     # self.uiUpdate_checkbox_toggle_init()
        #     self.checkBox_SerSendFloat.setEnabled(False)
        #
        #     self.checkBox_SerSendStr.setChecked(False)
        #     # self.uiUpdate_checkbox_toggle_init()
        #     self.checkBox_SerSendStr.setEnabled(False)
        #
        #     self.lineEdit_SerSendFullType.clear()
        #     self.lineEdit_SerSendFullType.setEnabled(False)
        #     self.lineEdit_SerSendFormatStr.clear()
        #     self.lineEdit_SerSendFormatStr.setEnabled(False)
        #
        #     # receive widgets
        #     self.checkBox_ServerReceiveString.setChecked(True)
        #     self.checkBox_ServerReceiveString.setEnabled(False)
        #     self.lineEdit_ServerReceiveSeparator.setEnabled(False)
        #     self.checkBox_ServerReceiveRawbytes.setChecked(False)
        #     self.checkBox_ServerReceiveRawbytes.setEnabled(False)
        #
        #     self.checkBox_SerRecvInt.setChecked(False)
        #     # self.uiUpdate_checkbox_toggle_init()
        #     self.checkBox_SerRecvInt.setEnabled(False)
        #
        #     self.checkBox_SerRecvFloat.setChecked(False)
        #     # self.uiUpdate_checkbox_toggle_init()
        #     self.checkBox_SerRecvFloat.setEnabled(False)
        #
        #     self.checkBox_SerRecvStr.setChecked(False)
        #
        #     self.checkBox_SerRecvStr.setEnabled(False)
        #
        #     self.lineEdit_SerRecvFormatStr.clear()
        #     self.lineEdit_SerRecvFormatStr.setEnabled(False)
        #
        #     self.lineEdit_SerRecvFullType.clear()
        #     self.lineEdit_SerRecvFullType.setFocusPolicy(Qt.NoFocus)
        #     self.lineEdit_SerRecvFullType.setEnabled(False)
        #
        #     self.uiUpdate_checkbox_toggle_init()
        self.uiUpdate_checkbox_send_string_checked(self.server_widgets_status)
        self.uiUpdate_checkbox_send_string_checked(self.client_widgets_status)

    def uiUpdate_checkbox_send_string_checked(self, widgets_status: SocketWidgetStruct) -> None:
        """

        :return:
        """
        # server string checkbox checked
        if widgets_status.checkBox_SendStringMode.isChecked() and widgets_status.checkBox_SendStringMode.isEnabled():
            widgets_status.checkBox_SendRawbytesMode.setChecked(False)
            widgets_status.lineEdit_StrSendSeparator.setEnabled(True)
            # self.lineEdit_SerSendFormatStr.setEnabled(False)
        elif widgets_status.checkBox_SendStringMode.isEnabled():
            widgets_status.checkBox_SendRawbytesMode.setChecked(True)
            widgets_status.lineEdit_StrSendSeparator.setEnabled(False)
            # self.lineEdit_SerSendFormatStr.setEnabled(True)

        if widgets_status.checkBox_ReceiveStrMode.isChecked() and widgets_status.checkBox_ReceiveStrMode.isEnabled():
            widgets_status.checkBox_ReceiveRawbytesMode.setChecked(False)
            widgets_status.lineEdit_StrReceiveSeparator.setEnabled(True)
            # self.lineEdit_SerRecvFormatStr.setEnabled(False)
        elif widgets_status.checkBox_ReceiveStrMode.isEnabled():
            widgets_status.checkBox_ReceiveRawbytesMode.setChecked(True)
            widgets_status.lineEdit_StrReceiveSeparator.setEnabled(False)
            # self.lineEdit_SerRecvFormatStr.setEnabled(True)

        # client string checkbox checked
        # if widgets_status.checkBox_ClientSendString.isChecked() and widgets_status.checkBox_ClientSendString.isEnabled():
        #     widgets_status.checkBox_ClientSendRawbytes.setChecked(False)
        #     widgets_status.lineEdit_ClientSendSeparator.setEnabled(True)
        #
        # elif widgets_status.checkBox_ClientSendString.isEnabled():
        #     widgets_status.checkBox_ClientSendRawbytes.setChecked(True)
        #     widgets_status.lineEdit_ClientSendSeparator.setEnabled(False)
        #
        # if widgets_status.checkBox_ClientReceiveString.isChecked() and widgets_status.checkBox_ClientReceiveString.isEnabled():
        #     widgets_status.checkBox_ClientReceiveRawbytes.setChecked(False)
        #     widgets_status.lineEdit_ClientReceiveSeparator.setEnabled(True)
        #     # self.lineEdit_ClntRecvFormatStr.setEnabled(False)
        # elif widgets_status.checkBox_ClientReceiveString.isEnabled():
        #     widgets_status.checkBox_ClientReceiveRawbytes.setChecked(True)
        #     widgets_status.lineEdit_ClientReceiveSeparator.setEnabled(False)

        self.uiUpdate_checkbox_toggle_init()

    def uiUpdate_checkbox_send_rawbytes_checked(self, widgets_status: SocketWidgetStruct):
        """

        :return:
        """
        # server rawbytes checkbox checked
        if widgets_status.checkBox_SendRawbytesMode.isChecked() and widgets_status.checkBox_SendRawbytesMode.isEnabled():
            widgets_status.checkBox_SendStringMode.setChecked(False)
            widgets_status.lineEdit_StrSendSeparator.setEnabled(False)

        elif widgets_status.checkBox_SendRawbytesMode.isEnabled():
            widgets_status.checkBox_SendStringMode.setChecked(True)
            widgets_status.lineEdit_StrSendSeparator.setEnabled(True)

        if widgets_status.checkBox_ReceiveRawbytesMode.isChecked() and widgets_status.checkBox_ReceiveRawbytesMode.isEnabled():
            widgets_status.checkBox_ReceiveStrMode.setChecked(False)
            widgets_status.lineEdit_StrReceiveSeparator.setEnabled(False)

        elif widgets_status.checkBox_ReceiveRawbytesMode.isEnabled():
            widgets_status.checkBox_ReceiveStrMode.setChecked(True)
            widgets_status.lineEdit_StrReceiveSeparator.setEnabled(True)

        # client rawbytes checkbox checked
        # if self.checkBox_ClientSendRawbytes.isChecked() and self.checkBox_ClientSendRawbytes.isEnabled():
        #     self.checkBox_ClientSendString.setChecked(False)
        #     self.lineEdit_ClientSendSeparator.setEnabled(False)
        #
        # elif self.checkBox_ClientSendRawbytes.isEnabled():
        #     self.checkBox_ClientSendString.setChecked(True)
        #     self.lineEdit_ClientSendSeparator.setEnabled(True)
        #
        #
        # if self.checkBox_ClientReceiveRawbytes.isChecked() and self.checkBox_ClientReceiveRawbytes.isEnabled():
        #     self.checkBox_ClientReceiveString.setChecked(False)
        #     self.lineEdit_ClientReceiveSeparator.setEnabled(False)
        #
        # elif self.checkBox_ClientReceiveRawbytes.isEnabled():
        #     self.checkBox_ClientReceiveString.setChecked(True)
        #     self.lineEdit_ClientReceiveSeparator.setEnabled(True)

        self.uiUpdate_checkbox_toggle_init()

    def uiUpdate_server_full_type_mode(self, widgets_status: SocketWidgetStruct):
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

        # if self.lineEdit_SerSendFullType.text() != "" \
        #         or self.lineEdit_SerSendFormatStr.text() != "":
        #     self.checkBox_SerSendInt.setChecked(False)
        #     self.checkBox_SerSendFloat.setChecked(False)
        #     self.checkBox_SerSendStr.setChecked(False)
        #
        # if self.lineEdit_SerRecvFullType.text() != "" \
        #         or self.lineEdit_SerRecvFormatStr.text() != "":
        #     self.checkBox_SerRecvInt.setChecked(False)
        #     self.checkBox_SerRecvFloat.setChecked(False)
        #     self.checkBox_SerRecvStr.setChecked(False)

        self.uiUpdate_checkbox_toggle_init()

    def uiUpdate_checkbox_toggle_init(self):
        """

        :return:
        """
        # server send checkbox
        if self.checkBox_SerSendInt.isChecked():
            self.spinBox_SerSendInt_Seq.setEnabled(True)
            self.lineEdit_SerSendInt_Value.setEnabled(True)
        else:
            self.spinBox_SerSendInt_Seq.setValue(0)
            self.spinBox_SerSendInt_Seq.setEnabled(False)
            self.lineEdit_SerSendInt_Value.clear()
            self.lineEdit_SerSendInt_Value.setEnabled(False)
            self.spinBox_SerSendInt_Seq.setStyleSheet("QLineEdit{background-color:rgb(240, 240, 240)}")
            self.lineEdit_SerSendInt_Value.setStyleSheet("QLineEdit{background-color:rgb(240, 240, 240)}")

        if self.checkBox_SerSendFloat.isChecked():
            self.spinBox_SerSendFloat_Seq.setEnabled(True)
            self.lineEdit_SerSendFloat_Value.setEnabled(True)
        else:
            self.spinBox_SerSendFloat_Seq.setValue(0)
            self.spinBox_SerSendFloat_Seq.setEnabled(False)
            self.lineEdit_SerSendFloat_Value.clear()
            self.lineEdit_SerSendFloat_Value.setEnabled(False)
            self.spinBox_SerSendFloat_Seq.setStyleSheet("QLineEdit{background-color:rgb(240, 240, 240)}")
            self.lineEdit_SerSendFloat_Value.setStyleSheet("QLineEdit{background-color:rgb(240, 240, 240)}")

        if self.checkBox_SerSendStr.isChecked():
            self.spinBox_SerSendStr_Seq.setEnabled(True)
            self.lineEdit_SerSendstr_Value.setEnabled(True)
        else:
            self.spinBox_SerSendStr_Seq.setValue(0)
            self.spinBox_SerSendStr_Seq.setEnabled(False)
            self.lineEdit_SerSendstr_Value.clear()
            self.lineEdit_SerSendstr_Value.setEnabled(False)
            self.spinBox_SerSendStr_Seq.setStyleSheet("QLineEdit{background-color:rgb(240, 240, 240)}")
            self.lineEdit_SerSendstr_Value.setStyleSheet("QLineEdit{background-color:rgb(240, 240, 240)}")

        if self.checkBox_SerSendInt.isChecked() + self.checkBox_SerSendFloat.isChecked() + self.checkBox_SerSendStr.isChecked() == 0 \
                and self.checkBox_SerSendInt.isEnabled() + self.checkBox_SerSendFloat.isEnabled() + self.checkBox_SerSendStr.isEnabled() > 0:
            self.lineEdit_SerSendFullType.setEnabled(True)
            if self.checkBox_ServerSendString.isChecked():
                # self.lineEdit_SerSendFormatStr.clear()
                self.lineEdit_SerSendFormatStr.setEnabled(False)
                if self.lineEdit_SerSendFullType.text() != "":
                    self.lineEdit_ServerSendSeparator.setEnabled(False)
                else:
                    self.lineEdit_ServerSendSeparator.setEnabled(True)
            else:
                self.lineEdit_SerSendFormatStr.setEnabled(True)
        else:
            self.lineEdit_SerSendFullType.clear()
            self.lineEdit_SerSendFullType.setEnabled(False)
            self.lineEdit_SerSendFormatStr.clear()
            self.lineEdit_SerSendFormatStr.setEnabled(False)

        # server receive checkbox
        if self.checkBox_SerRecvInt.isChecked():
            print("server receive int")
            self.spinBox_SerRecvInt_Seq.setEnabled(True)
            self.lineEdit_SerRecvInt_Value.setEnabled(True)
            self.lineEdit_SerRecvInt_Value.setReadOnly(True)
            self.lineEdit_SerRecvInt_Value.setStyleSheet("QLineEdit{background-color:rgb(255, 255, 255)}")
        else:
            self.spinBox_SerRecvInt_Seq.setValue(0)
            self.spinBox_SerRecvInt_Seq.setEnabled(False)
            self.lineEdit_SerRecvInt_Value.clear()
            self.lineEdit_SerRecvInt_Value.setEnabled(False)
            self.spinBox_SerRecvInt_Seq.setStyleSheet("QLineEdit{background-color:rgb(240, 240, 240)}")
            self.lineEdit_SerRecvInt_Value.setStyleSheet("QLineEdit{background-color:rgb(240, 240, 240)}")

        if self.checkBox_SerRecvFloat.isChecked():
            self.spinBox_SerRecvFloat_Seq.setEnabled(True)
            self.lineEdit_SerRecvFloat_Value.setEnabled(True)
            self.lineEdit_SerRecvFloat_Value.setReadOnly(True)
            self.lineEdit_SerRecvFloat_Value.setStyleSheet("QLineEdit{background-color:rgb(255, 255, 255)}")
        else:
            self.spinBox_SerRecvFloat_Seq.setValue(0)
            self.spinBox_SerRecvFloat_Seq.setEnabled(False)
            self.lineEdit_SerRecvFloat_Value.clear()
            self.lineEdit_SerRecvFloat_Value.setEnabled(False)
            self.spinBox_SerRecvFloat_Seq.setStyleSheet("QLineEdit{background-color:rgb(240, 240, 240)}")
            self.lineEdit_SerRecvFloat_Value.setStyleSheet("QLineEdit{background-color:rgb(240, 240, 240)}")

        if self.checkBox_SerRecvStr.isChecked():
            self.spinBox_SerRecvStr_Seq.setEnabled(True)
            self.lineEdit_SerRecvStr_Value.setEnabled(True)
            self.lineEdit_SerRecvStr_Value.setReadOnly(True)
            self.lineEdit_SerRecvStr_Value.setStyleSheet("QLineEdit{background-color:rgb(255, 255, 255)}")
        else:
            self.spinBox_SerRecvStr_Seq.setValue(0)
            self.spinBox_SerRecvStr_Seq.setEnabled(False)
            self.lineEdit_SerRecvStr_Value.clear()
            self.lineEdit_SerRecvStr_Value.setEnabled(False)
            self.spinBox_SerRecvStr_Seq.setStyleSheet("QLineEdit{background-color:rgb(240, 240, 240)}")
            self.lineEdit_SerRecvStr_Value.setStyleSheet("QLineEdit{background-color:rgb(240, 240, 240)}")

        if self.checkBox_SerRecvInt.isChecked() + self.checkBox_SerRecvFloat.isChecked() + self.checkBox_SerRecvStr.isChecked() == 0 \
                and self.checkBox_SerRecvInt.isEnabled() + self.checkBox_SerRecvFloat.isEnabled() + self.checkBox_SerRecvStr.isEnabled() > 0:
            if self.checkBox_ServerReceiveString.isChecked():
                self.lineEdit_SerRecvFullType.setEnabled(True)
                # self.lineEdit_SerRecvFormatStr.clear()
                self.lineEdit_SerRecvFormatStr.setEnabled(False)
            else:
                self.lineEdit_SerRecvFullType.setEnabled(True)
                self.lineEdit_SerRecvFormatStr.setEnabled(True)
        else:
            self.lineEdit_SerRecvFullType.setEnabled(False)
            self.lineEdit_SerRecvFullType.clear()
            self.lineEdit_SerRecvFormatStr.clear()
            self.lineEdit_SerRecvFormatStr.setEnabled(False)
        # client send check box
        if self.checkBox_ClntSendInt.isChecked():
            self.spinBox_ClntSendInt_Seq.setEnabled(True)
            self.lineEdit_ClntSendInt_Value.setEnabled(True)
        else:
            self.spinBox_ClntSendInt_Seq.setValue(0)
            self.spinBox_ClntSendInt_Seq.setEnabled(False)
            self.lineEdit_ClntSendInt_Value.clear()
            self.lineEdit_ClntSendInt_Value.setEnabled(False)
            self.spinBox_ClntSendInt_Seq.setStyleSheet("QLineEdit{background-color:rgb(240, 240, 240)}")
            self.lineEdit_ClntSendInt_Value.setStyleSheet("QLineEdit{background-color:rgb(240, 240, 240)}")

        if self.checkBox_ClntSendFloat.isChecked():
            self.spinBox_ClntSendFloat_Seq.setEnabled(True)
            self.lineEdit_ClntSendFloat_Value.setEnabled(True)
        else:
            self.spinBox_ClntSendFloat_Seq.setValue(0)
            self.spinBox_ClntSendFloat_Seq.setEnabled(False)
            self.lineEdit_ClntSendFloat_Value.clear()
            self.lineEdit_ClntSendFloat_Value.setEnabled(False)
            self.spinBox_ClntSendFloat_Seq.setStyleSheet("QLineEdit{background-color:rgb(240, 240, 240)}")
            self.lineEdit_ClntSendFloat_Value.setStyleSheet("QLineEdit{background-color:rgb(240, 240, 240)}")

        if self.checkBox_ClntSendStr.isChecked():
            self.spinBox_ClntSendStr_Seq.setEnabled(True)
            self.lineEdit_ClntSendStr_Value.setEnabled(True)
        else:
            self.spinBox_ClntSendStr_Seq.setValue(0)
            self.spinBox_ClntSendStr_Seq.setEnabled(False)
            self.lineEdit_ClntSendStr_Value.clear()
            self.lineEdit_ClntSendStr_Value.setEnabled(False)
            self.spinBox_ClntSendStr_Seq.setStyleSheet("QLineEdit{background-color:rgb(240, 240, 240)}")
            self.lineEdit_ClntSendStr_Value.setStyleSheet("QLineEdit{background-color:rgb(240, 240, 240)}")

        if self.checkBox_ClntSendInt.isChecked() + self.checkBox_ClntSendFloat.isChecked() + self.checkBox_ClntSendStr.isChecked() == 0 \
                and self.checkBox_ClntSendInt.isEnabled() + self.checkBox_ClntSendFloat.isEnabled() + self.checkBox_ClntSendStr.isEnabled() > 0:
            self.lineEdit_ClntSendFullType.setEnabled(True)
            self.lineEdit_ClntSendFormatStr.setEnabled(True)
        else:
            self.lineEdit_ClntSendFullType.clear()
            self.lineEdit_ClntSendFullType.setEnabled(False)
            self.lineEdit_ClntSendFormatStr.clear()
            self.lineEdit_ClntSendFormatStr.setEnabled(False)

        # client receive checkbox
        if self.checkBox_ClntRecvInt.isChecked():
            self.spinBox_ClntRecvInt_Seq.setEnabled(True)
            self.lineEdit_ClntRecvInt_Value.setEnabled(True)
        else:
            self.spinBox_ClntRecvInt_Seq.setValue(0)
            self.spinBox_ClntRecvInt_Seq.setEnabled(False)
            self.lineEdit_ClntRecvInt_Value.clear()
            self.lineEdit_ClntRecvInt_Value.setEnabled(False)
            self.spinBox_ClntRecvInt_Seq.setStyleSheet("QLineEdit{background-color:rgb(240, 240, 240)}")
            self.lineEdit_ClntRecvInt_Value.setStyleSheet("QLineEdit{background-color:rgb(240, 240, 240)}")

        if self.checkBox_ClntRecvFloat.isChecked():
            self.spinBox_ClntRecvFloat_Seq.setEnabled(True)
            self.lineEdit_ClntRecvFloat_Value.setEnabled(True)
        else:
            self.spinBox_ClntRecvFloat_Seq.setValue(0)
            self.spinBox_ClntRecvFloat_Seq.setEnabled(False)
            self.lineEdit_ClntRecvFloat_Value.clear()
            self.lineEdit_ClntRecvFloat_Value.setEnabled(False)
            self.spinBox_ClntRecvFloat_Seq.setStyleSheet("QLineEdit{background-color:rgb(240, 240, 240)}")
            self.lineEdit_ClntRecvFloat_Value.setStyleSheet("QLineEdit{background-color:rgb(240, 240, 240)}")

        if self.checkBox_ClntRecvStr.isChecked():
            self.spinBox_ClntRecvStr_Seq.setEnabled(True)
            self.lineEdit_ClntRecvStr_Value.setEnabled(True)
        else:
            self.spinBox_ClntRecvStr_Seq.setValue(0)
            self.spinBox_ClntRecvStr_Seq.setEnabled(False)
            self.lineEdit_ClntRecvStr_Value.clear()
            self.lineEdit_ClntRecvStr_Value.setEnabled(False)
            self.lineEdit_ClntRecvStr_Value.setStyleSheet("QLineEdit{background-color:rgb(240, 240, 240)}")
            self.lineEdit_ClntRecvStr_Value.setStyleSheet("QLineEdit{background-color:rgb(240, 240, 240)}")

        if self.checkBox_ClntRecvInt.isChecked() + self.checkBox_ClntRecvFloat.isChecked() + self.checkBox_ClntRecvStr.isChecked() == 0 \
                and self.checkBox_ClntRecvInt.isEnabled() + self.checkBox_ClntRecvFloat.isEnabled() + self.checkBox_ClntRecvStr.isEnabled() > 0:
            self.lineEdit_ClntRecvFullType.setEnabled(True)
            self.lineEdit_ClntRecvFormatStr.setEnabled(True)
        else:
            self.lineEdit_ClntRecvFullType.clear()
            self.lineEdit_ClntRecvFullType.setEnabled(False)
            self.lineEdit_ClntRecvFormatStr.clear()
            self.lineEdit_ClntRecvFormatStr.setEnabled(False)

        self.uiUpdate_SerSendValueCheck(self.server_widgets_status)
        self.uiUpdate_serRecValueCheck(self.server_widgets_status)
        self.uiUpdate_SerSendValueCheck(self.client_widgets_status)
        self.uiUpdate_serRecValueCheck(self.client_widgets_status)

    def uiUpdate_SerSendValueCheck(self, widgets_status: SocketWidgetStruct):

        b_lineedit_check_valid = False
        b_spinbox_check_valid = False

        if widgets_status.checkBox_Send_Int.isChecked():
            ins_re_match = re.match(r"^\d+$", widgets_status.lineEdit_Send_Int.text())
            if ins_re_match is not None:
                widgets_status.lineEdit_Send_Int.setStyleSheet("background-color: rgb(255, 255, 255);")
                b_lineedit_check_valid = True
            else:
                widgets_status.lineEdit_Send_Int.setStyleSheet("background-color: rgb(253, 183, 184);")
                b_lineedit_check_valid = False

        if widgets_status.checkBox_Send_Float.isChecked():
            ins_re_match = re.match(r"^\d+\.\d+$", widgets_status.lineEdit_Send_Float.text())
            if ins_re_match is not None:
                widgets_status.lineEdit_Send_Float.setStyleSheet("background-color: rgb(255, 255, 255);")
                b_lineedit_check_valid = True
            else:
                widgets_status.lineEdit_Send_Float.setStyleSheet("background-color: rgb(253, 183, 184);")
                b_lineedit_check_valid = False

        if widgets_status.checkBox_Send_Str.isChecked():
            ins_re_match = re.match(r"^\S+$", widgets_status.lineEdit_Send_Str.text())
            if ins_re_match is not None:
                widgets_status.lineEdit_Send_Str.setStyleSheet("background-color: rgb(255, 255, 255);")
                b_lineedit_check_valid = True
            else:
                widgets_status.lineEdit_Send_Str.setStyleSheet("background-color: rgb(253, 183, 184);")
                b_lineedit_check_valid = False
            # Server send sequence check
        if widgets_status.checkBox_Send_Int.isChecked() + widgets_status.checkBox_Send_Float.isChecked() + widgets_status.checkBox_Send_Str.isChecked() == 0:
            if widgets_status.checkBox_SendStringMode.isChecked():
                if widgets_status.lineEdit_SendFullType.text() != "":
                    b_lineedit_check_valid = True
                    b_spinbox_check_valid = True
            else:
                if widgets_status.lineEdit_SendFullType.text() != "" and widgets_status.lineEdit_SendFormatStr.text() != "":
                    b_lineedit_check_valid = True
                    b_spinbox_check_valid = True

        elif widgets_status.checkBox_Send_Int.isChecked() + widgets_status.checkBox_Send_Float.isChecked() + widgets_status.checkBox_Send_Str.isChecked() == 1:
            if widgets_status.checkBox_Send_Int.isChecked():
                widgets_status.spinBox_Send_Int.setStyleSheet("QSpinBox{background-color:rgb(255, 255, 255)}")
            elif widgets_status.checkBox_Send_Float.isChecked():
                widgets_status.spinBox_Send_Float.setStyleSheet("QSpinBox{background-color:rgb(255, 255, 255)}")
            else:
                widgets_status.spinBox_Send_Str.setStyleSheet("QSpinBox{background-color:rgb(255, 255, 255)}")
            b_spinbox_check_valid = True
        elif widgets_status.checkBox_Send_Int.isChecked() + widgets_status.checkBox_Send_Float.isChecked() + widgets_status.checkBox_Send_Str.isChecked() == 2:
            if not widgets_status.checkBox_Send_Int.isChecked():
                if widgets_status.spinBox_Send_Float.text() == widgets_status.spinBox_Send_Str.text():
                    widgets_status.spinBox_Send_Float.setStyleSheet("QSpinBox{background-color: rgb(253, 183, 184)}")
                    widgets_status.spinBox_Send_Str.setStyleSheet("QSpinBox{background-color: rgb(253, 183, 184)}")
                    b_spinbox_check_valid = False
                else:
                    widgets_status.spinBox_Send_Float.setStyleSheet("QSpinBox{background-color: rgb(255, 255, 255)}")
                    widgets_status.spinBox_Send_Str.setStyleSheet("QSpinBox{background-color: rgb(255, 255, 255)}")
                    b_spinbox_check_valid = True

            elif not widgets_status.checkBox_Send_Float.isChecked():
                if widgets_status.spinBox_Send_Int.text() == widgets_status.spinBox_Send_Str.text():
                    widgets_status.spinBox_Send_Int.setStyleSheet("QSpinBox{background-color: rgb(253, 183, 184)}")
                    widgets_status.spinBox_Send_Str.setStyleSheet("QSpinBox{background-color: rgb(253, 183, 184)}")
                    b_spinbox_check_valid = False
                else:
                    widgets_status.spinBox_Send_Int.setStyleSheet("QSpinBox{background-color: rgb(255, 255, 255)}")
                    widgets_status.spinBox_Send_Str.setStyleSheet("QSpinBox{background-color: rgb(255, 255, 255)}")
                    b_spinbox_check_valid = True
            else:
                if widgets_status.spinBox_Send_Int.text() == widgets_status.spinBox_Send_Float.text():
                    widgets_status.spinBox_Send_Float.setStyleSheet("QSpinBox{background-color: rgb(253, 183, 184)}")
                    widgets_status.spinBox_Send_Int.setStyleSheet("QSpinBox{background-color: rgb(253, 183, 184)}")
                    b_spinbox_check_valid = False
                else:
                    widgets_status.spinBox_Send_Float.setStyleSheet("QSpinBox{background-color: rgb(255, 255, 255)}")
                    widgets_status.spinBox_Send_Int.setStyleSheet("QSpinBox{background-color: rgb(255, 255, 255)}")
                    b_spinbox_check_valid = True

        elif widgets_status.checkBox_Send_Int.isChecked() + widgets_status.checkBox_Send_Float.isChecked() + widgets_status.checkBox_Send_Str.isChecked() == 3:
            if widgets_status.spinBox_Send_Int.text() == widgets_status.spinBox_Send_Float.text():
                b_spinbox_check_valid = False
                widgets_status.spinBox_Send_Int.setStyleSheet("QSpinBox{background-color: rgb(253, 183, 184)}")
                widgets_status.spinBox_Send_Float.setStyleSheet("QSpinBox{background-color: rgb(253, 183, 184)}")
                if widgets_status.spinBox_Send_Int.text() == widgets_status.spinBox_Send_Str.text():
                    widgets_status.spinBox_Send_Int.setStyleSheet("QSpinBox{background-color: rgb(253, 183, 184)}")
                    widgets_status.spinBox_Send_Str.setStyleSheet("QSpinBox{background-color: rgb(253, 183, 184)}")
                else:
                    widgets_status.spinBox_Send_Str.setStyleSheet("QSpinBox{background-color: rgb(255, 255, 255)}")
            elif widgets_status.spinBox_Send_Int.text() == widgets_status.spinBox_Send_Str.text():
                b_spinbox_check_valid = False
                widgets_status.spinBox_Send_Float.setStyleSheet("QSpinBox{background-color: rgb(255, 255, 255)}")
                widgets_status.spinBox_Send_Int.setStyleSheet("QSpinBox{background-color: rgb(253, 183, 184)}")
                widgets_status.spinBox_Send_Str.setStyleSheet("QSpinBox{background-color: rgb(253, 183, 184)}")
                if widgets_status.spinBox_Send_Float.text() == widgets_status.spinBox_Send_Str.text():
                    widgets_status.spinBox_Send_Float.setStyleSheet("QSpinBox{background-color: rgb(253, 183, 184)}")
                    widgets_status.spinBox_Send_Str.setStyleSheet("QSpinBox{background-color: rgb(253, 183, 184)}")
                else:
                    widgets_status.spinBox_Send_Float.setStyleSheet("QSpinBox{background-color: rgb(255, 255, 255)}")
            elif widgets_status.spinBox_Send_Int.text() != widgets_status.spinBox_Send_Str.text():
                widgets_status.spinBox_Send_Int.setStyleSheet("QSpinBox{background-color: rgb(255, 255, 255)}")
                if widgets_status.spinBox_Send_Float.text() == widgets_status.spinBox_Send_Str.text():
                    b_spinbox_check_valid = False
                    widgets_status.spinBox_Send_Float.setStyleSheet("QSpinBox{background-color: rgb(253, 183, 184)}")
                    widgets_status.spinBox_Send_Str.setStyleSheet("QSpinBox{background-color: rgb(253, 183, 184)}")
                else:
                    b_spinbox_check_valid = True
                    widgets_status.spinBox_Send_Float.setStyleSheet("QSpinBox{background-color: rgb(255, 255, 255)}")
                    widgets_status.spinBox_Send_Str.setStyleSheet("QSpinBox{background-color: rgb(255, 255, 255)}")
        # server send value check
        # if self.checkBox_SerSendInt.isChecked():
        #     ins_re_match = re.match(r"^\d+$", self.lineEdit_SerSendInt_Value.text())
        #     if ins_re_match is not None:
        #         self.lineEdit_SerSendInt_Value.setStyleSheet("background-color: rgb(255, 255, 255);")
        #         b_lineedit_check_valid = True
        #     else:
        #         self.lineEdit_SerSendInt_Value.setStyleSheet("background-color: rgb(253, 183, 184);")
        #         b_lineedit_check_valid = False
        #
        # if self.checkBox_SerSendFloat.isChecked():
        #     ins_re_match = re.match(r"^\d+\.\d+$", self.lineEdit_SerSendFloat_Value.text())
        #     if ins_re_match is not None:
        #         self.lineEdit_SerSendFloat_Value.setStyleSheet("background-color: rgb(255, 255, 255);")
        #         b_lineedit_check_valid = True
        #     else:
        #         self.lineEdit_SerSendFloat_Value.setStyleSheet("background-color: rgb(253, 183, 184);")
        #         b_lineedit_check_valid = False
        #
        # if self.checkBox_SerSendStr.isChecked():
        #     ins_re_match = re.match(r"^\S+$", self.lineEdit_SerSendstr_Value.text())
        #     if ins_re_match is not None:
        #         self.lineEdit_SerSendstr_Value.setStyleSheet("background-color: rgb(255, 255, 255);")
        #         b_lineedit_check_valid = True
        #     else:
        #         self.lineEdit_SerSendstr_Value.setStyleSheet("background-color: rgb(253, 183, 184);")
        #         b_lineedit_check_valid = False
        # # Server send sequence check
        # if self.checkBox_SerSendInt.isChecked() + self.checkBox_SerSendFloat.isChecked() + self.checkBox_SerSendStr.isChecked() == 0:
        #     if self.checkBox_ServerSendString.isChecked():
        #         if self.lineEdit_SerSendFullType.text() != "":
        #             b_lineedit_check_valid = True
        #             b_spinbox_check_valid = True
        #     else:
        #         if self.lineEdit_SerSendFullType.text() != "" and self.lineEdit_SerSendFormatStr.text() != "":
        #             b_lineedit_check_valid = True
        #             b_spinbox_check_valid = True
        #
        # elif self.checkBox_SerSendInt.isChecked() + self.checkBox_SerSendFloat.isChecked() + self.checkBox_SerSendStr.isChecked() == 1:
        #     if self.checkBox_SerSendInt.isChecked():
        #         self.spinBox_SerSendInt_Seq.setStyleSheet("QSpinBox{background-color:rgb(255, 255, 255)}")
        #     elif self.checkBox_SerSendFloat.isChecked():
        #         self.spinBox_SerSendFloat_Seq.setStyleSheet("QSpinBox{background-color:rgb(255, 255, 255)}")
        #     else:
        #         self.spinBox_SerSendStr_Seq.setStyleSheet("QSpinBox{background-color:rgb(255, 255, 255)}")
        #     b_spinbox_check_valid = True
        # elif self.checkBox_SerSendInt.isChecked() + self.checkBox_SerSendFloat.isChecked() + self.checkBox_SerSendStr.isChecked() == 2:
        #     if not self.checkBox_SerSendInt.isChecked():
        #         if self.spinBox_SerSendFloat_Seq.text() == self.spinBox_SerSendStr_Seq.text():
        #             self.spinBox_SerSendFloat_Seq.setStyleSheet("QSpinBox{background-color: rgb(253, 183, 184)}")
        #             self.spinBox_SerSendStr_Seq.setStyleSheet("QSpinBox{background-color: rgb(253, 183, 184)}")
        #             b_spinbox_check_valid = False
        #         else:
        #             self.spinBox_SerSendFloat_Seq.setStyleSheet("QSpinBox{background-color: rgb(255, 255, 255)}")
        #             self.spinBox_SerSendStr_Seq.setStyleSheet("QSpinBox{background-color: rgb(255, 255, 255)}")
        #             b_spinbox_check_valid = True
        #
        #     elif not self.checkBox_SerSendFloat.isChecked():
        #         if self.spinBox_SerSendInt_Seq.text() == self.spinBox_SerSendStr_Seq.text():
        #             self.spinBox_SerSendInt_Seq.setStyleSheet("QSpinBox{background-color: rgb(253, 183, 184)}")
        #             self.spinBox_SerSendStr_Seq.setStyleSheet("QSpinBox{background-color: rgb(253, 183, 184)}")
        #             b_spinbox_check_valid = False
        #         else:
        #             self.spinBox_SerSendInt_Seq.setStyleSheet("QSpinBox{background-color: rgb(255, 255, 255)}")
        #             self.spinBox_SerSendStr_Seq.setStyleSheet("QSpinBox{background-color: rgb(255, 255, 255)}")
        #             b_spinbox_check_valid = True
        #     else:
        #         if self.spinBox_SerSendFloat_Seq.text() == self.spinBox_SerSendInt_Seq.text():
        #             self.spinBox_SerSendFloat_Seq.setStyleSheet("QSpinBox{background-color: rgb(253, 183, 184)}")
        #             self.spinBox_SerSendInt_Seq.setStyleSheet("QSpinBox{background-color: rgb(253, 183, 184)}")
        #             b_spinbox_check_valid = False
        #         else:
        #             self.spinBox_SerSendFloat_Seq.setStyleSheet("QSpinBox{background-color: rgb(255, 255, 255)}")
        #             self.spinBox_SerSendInt_Seq.setStyleSheet("QSpinBox{background-color: rgb(255, 255, 255)}")
        #             b_spinbox_check_valid = True
        #
        # elif self.checkBox_SerSendInt.isChecked() + self.checkBox_SerSendFloat.isChecked() + self.checkBox_SerSendStr.isChecked() == 3:
        #     if self.spinBox_SerSendInt_Seq.text() == self.spinBox_SerSendFloat_Seq.text():
        #         b_spinbox_check_valid = False
        #         self.spinBox_SerSendInt_Seq.setStyleSheet("QSpinBox{background-color: rgb(253, 183, 184)}")
        #         self.spinBox_SerSendFloat_Seq.setStyleSheet("QSpinBox{background-color: rgb(253, 183, 184)}")
        #         if self.spinBox_SerSendInt_Seq.text() == self.spinBox_SerSendStr_Seq.text():
        #             self.spinBox_SerSendInt_Seq.setStyleSheet("QSpinBox{background-color: rgb(253, 183, 184)}")
        #             self.spinBox_SerSendStr_Seq.setStyleSheet("QSpinBox{background-color: rgb(253, 183, 184)}")
        #         else:
        #             self.spinBox_SerSendStr_Seq.setStyleSheet("QSpinBox{background-color: rgb(255, 255, 255)}")
        #     elif self.spinBox_SerSendInt_Seq.text() == self.spinBox_SerSendStr_Seq.text():
        #         b_spinbox_check_valid = False
        #         self.spinBox_SerSendFloat_Seq.setStyleSheet("QSpinBox{background-color: rgb(255, 255, 255)}")
        #         self.spinBox_SerSendInt_Seq.setStyleSheet("QSpinBox{background-color: rgb(253, 183, 184)}")
        #         self.spinBox_SerSendStr_Seq.setStyleSheet("QSpinBox{background-color: rgb(253, 183, 184)}")
        #         if self.spinBox_SerSendFloat_Seq.text() == self.spinBox_SerSendStr_Seq.text():
        #             self.spinBox_SerSendFloat_Seq.setStyleSheet("QSpinBox{background-color: rgb(253, 183, 184)}")
        #             self.spinBox_SerSendStr_Seq.setStyleSheet("QSpinBox{background-color: rgb(253, 183, 184)}")
        #         else:
        #             self.spinBox_SerSendFloat_Seq.setStyleSheet("QSpinBox{background-color: rgb(255, 255, 255)}")
        #     elif self.spinBox_SerSendInt_Seq.text() != self.spinBox_SerSendStr_Seq.text():
        #         self.spinBox_SerSendInt_Seq.setStyleSheet("QSpinBox{background-color: rgb(255, 255, 255)}")
        #         if self.spinBox_SerSendFloat_Seq.text() == self.spinBox_SerSendStr_Seq.text():
        #             b_spinbox_check_valid = False
        #             self.spinBox_SerSendFloat_Seq.setStyleSheet("QSpinBox{background-color: rgb(253, 183, 184)}")
        #             self.spinBox_SerSendStr_Seq.setStyleSheet("QSpinBox{background-color: rgb(253, 183, 184)}")
        #         else:
        #             b_spinbox_check_valid = True
        #             self.spinBox_SerSendFloat_Seq.setStyleSheet("QSpinBox{background-color: rgb(255, 255, 255)}")
        #             self.spinBox_SerSendStr_Seq.setStyleSheet("QSpinBox{background-color: rgb(255, 255, 255)}")

        if b_spinbox_check_valid and b_lineedit_check_valid:
            widgets_status.pushButton_Send.setEnabled(True)
        else:
            widgets_status.pushButton_Send.setEnabled(False)

    def uiUpdate_serRecValueCheck(self, widgets_status: SocketWidgetStruct):
        """

        """
        b_spinbox_check_valid = False
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
                widgets_status.spinBox_Receive_Int.setStyleSheet("QSpinBox{background-color:rgb(255, 255, 255)}")
            elif widgets_status.checkBox_Receive_Float.isChecked():
                widgets_status.spinBox_Receive_Float.setStyleSheet("QSpinBox{background-color:rgb(255, 255, 255)}")
            else:
                widgets_status.spinBox_Receive_Str.setStyleSheet("QSpinBox{background-color:rgb(255, 255, 255)}")
            b_spinbox_check_valid = True
        elif widgets_status.checkBox_Receive_Int.isChecked() + widgets_status.checkBox_Receive_Float.isChecked() + widgets_status.checkBox_Receive_Str.isChecked() == 2:
            if not widgets_status.checkBox_Receive_Int.isChecked():
                if widgets_status.spinBox_Receive_Float.text() == widgets_status.spinBox_Receive_Str.text():
                    widgets_status.spinBox_Receive_Float.setStyleSheet("QSpinBox{background-color: rgb(253, 183, 184)}")
                    widgets_status.spinBox_Receive_Str.setStyleSheet("QSpinBox{background-color: rgb(253, 183, 184)}")
                    b_spinbox_check_valid = False
                else:
                    widgets_status.spinBox_Receive_Float.setStyleSheet("QSpinBox{background-color: rgb(255, 255, 255)}")
                    widgets_status.spinBox_Receive_Str.setStyleSheet("QSpinBox{background-color: rgb(255, 255, 255)}")
                    b_spinbox_check_valid = True

            elif not widgets_status.checkBox_Receive_Float.isChecked():
                if widgets_status.spinBox_Receive_Int.text() == widgets_status.spinBox_Receive_Str.text():
                    widgets_status.spinBox_Receive_Int.setStyleSheet("QSpinBox{background-color: rgb(253, 183, 184)}")
                    widgets_status.spinBox_Receive_Str.setStyleSheet("QSpinBox{background-color: rgb(253, 183, 184)}")
                    b_spinbox_check_valid = False
                else:
                    widgets_status.spinBox_Receive_Int.setStyleSheet("QSpinBox{background-color: rgb(255, 255, 255)}")
                    widgets_status.spinBox_Receive_Str.setStyleSheet("QSpinBox{background-color: rgb(255, 255, 255)}")
                    b_spinbox_check_valid = True
            else:
                if widgets_status.spinBox_Receive_Int.text() == widgets_status.spinBox_Receive_Float.text():
                    widgets_status.spinBox_Receive_Float.setStyleSheet("QSpinBox{background-color: rgb(253, 183, 184)}")
                    widgets_status.spinBox_Receive_Int.setStyleSheet("QSpinBox{background-color: rgb(253, 183, 184)}")
                    b_spinbox_check_valid = False
                else:
                    widgets_status.spinBox_Receive_Float.setStyleSheet("QSpinBox{background-color: rgb(255, 255, 255)}")
                    widgets_status.spinBox_Receive_Int.setStyleSheet("QSpinBox{background-color: rgb(255, 255, 255)}")
                    b_spinbox_check_valid = True

        elif widgets_status.checkBox_Receive_Int.isChecked() + widgets_status.checkBox_Receive_Float.isChecked() + widgets_status.checkBox_Receive_Str.isChecked() == 3:
            if widgets_status.spinBox_Receive_Int.text() == widgets_status.spinBox_Receive_Float.text():
                b_spinbox_check_valid = False
                widgets_status.spinBox_Receive_Int.setStyleSheet("QSpinBox{background-color: rgb(253, 183, 184)}")
                widgets_status.spinBox_Receive_Float.setStyleSheet("QSpinBox{background-color: rgb(253, 183, 184)}")
                if widgets_status.spinBox_Receive_Int.text() == widgets_status.spinBox_Receive_Str.text():
                    widgets_status.spinBox_Receive_Int.setStyleSheet("QSpinBox{background-color: rgb(253, 183, 184)}")
                    widgets_status.spinBox_Receive_Str.setStyleSheet("QSpinBox{background-color: rgb(253, 183, 184)}")
                else:
                    widgets_status.spinBox_Receive_Str.setStyleSheet("QSpinBox{background-color: rgb(255, 255, 255)}")
            elif widgets_status.spinBox_Receive_Int.text() == widgets_status.spinBox_Receive_Str.text():
                b_spinbox_check_valid = False
                widgets_status.spinBox_Receive_Float.setStyleSheet("QSpinBox{background-color: rgb(255, 255, 255)}")
                widgets_status.spinBox_Receive_Int.setStyleSheet("QSpinBox{background-color: rgb(253, 183, 184)}")
                widgets_status.spinBox_Receive_Str.setStyleSheet("QSpinBox{background-color: rgb(253, 183, 184)}")
                if widgets_status.spinBox_Receive_Float.text() == widgets_status.spinBox_Receive_Str.text():
                    widgets_status.spinBox_Receive_Float.setStyleSheet("QSpinBox{background-color: rgb(253, 183, 184)}")
                    widgets_status.spinBox_Receive_Str.setStyleSheet("QSpinBox{background-color: rgb(253, 183, 184)}")
                else:
                    widgets_status.spinBox_Receive_Float.setStyleSheet("QSpinBox{background-color: rgb(255, 255, 255)}")
            elif widgets_status.spinBox_Receive_Int.text() != widgets_status.spinBox_Receive_Str.text():
                widgets_status.spinBox_Receive_Int.setStyleSheet("QSpinBox{background-color: rgb(255, 255, 255)}")
                if widgets_status.spinBox_Receive_Float.text() == widgets_status.spinBox_Receive_Str.text():
                    b_spinbox_check_valid = False
                    widgets_status.spinBox_Receive_Float.setStyleSheet("QSpinBox{background-color: rgb(253, 183, 184)}")
                    widgets_status.spinBox_Receive_Str.setStyleSheet("QSpinBox{background-color: rgb(253, 183, 184)}")
                else:
                    b_spinbox_check_valid = True
                    widgets_status.spinBox_Receive_Float.setStyleSheet("QSpinBox{background-color: rgb(255, 255, 255)}")
                    widgets_status.spinBox_Receive_Str.setStyleSheet("QSpinBox{background-color: rgb(255, 255, 255)}")

        if b_spinbox_check_valid:
            widgets_status.pushButton_Receive.setEnabled(True)
        else:
            widgets_status.pushButton_Receive.setEnabled(False)


if __name__ == '__main__':
    # format the application interface show as designer display
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    gui_app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    # print("Main thread", QThread.currentThread())
    sys.exit(gui_app.exec())
