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
import struct
from PyQt5 import QtCore
from ShineRobot import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QAction
from PyQt5.Qt import QStandardItemModel, QCursor, Qt, QThread
from PyQt5.QtGui import QTextCursor
from shine_robot_socket_communication import SocketServer, SocketServerCloseClient


class MyMainWindow(QMainWindow, Ui_MainWindow):
    # initial the windows class
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.right_click_menu = QMenu()
        self.socket_server_client = SocketServerCloseClient((self.lineEdit_SevIP.text(), self.lineEdit_SerPort.text()))
        self.thread_close_socket_server = QThread()
        self.socket_server = SocketServer((self.lineEdit_SevIP.text(), self.lineEdit_SerPort.text()))
        self.Thread_socket_server = QThread()

        # append icon to taskbar in Windows system
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
        # call function which append widgets signal to slot
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
        # socket communication
        self.pushButton_SerCreateConn.clicked.connect(self.create_server_socket)
        self.pushButton_SerCreateConn.clicked.connect(self.pushButton_SerCloseConn.setDisabled)
        self.pushButton_SerCloseConn.clicked.connect(self.close_socket_server)
        self.pushButton_SerSend.clicked.connect(self.socket_server_send_message)
        self.pushButton_SerRecv.clicked.connect(self.socket_server_receive_message)

        self.checkBox_ServerSendString.clicked.connect(self.uiUpdate_checkbox_checked_String)
        self.checkBox_ServerSendRawbytes.clicked.connect(self.uiUpdate_checkbox_checked_Rawbytes)
        self.checkBox_ServerReceiveString.clicked.connect(self.uiUpdate_checkbox_checked_String)
        self.checkBox_ServerReceiveRawbytes.clicked.connect(self.uiUpdate_checkbox_checked_Rawbytes)
        self.checkBox_ClientSendString.clicked.connect(self.uiUpdate_checkbox_checked_String)
        self.checkBox_ClientSendRawbytes.clicked.connect(self.uiUpdate_checkbox_checked_Rawbytes)
        self.checkBox_ClientReceiveString.clicked.connect(self.uiUpdate_checkbox_checked_String)
        self.checkBox_ClientReceiveRawbytes.clicked.connect(self.uiUpdate_checkbox_checked_Rawbytes)
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

        # socket server send and receive full type mode, auto uncheck the single mode check box
        self.lineEdit_SerSendFullType.textChanged.connect(self.uiUpdate_server_full_type_mode)
        self.lineEdit_SerSendFormatStr.textChanged.connect(self.uiUpdate_server_full_type_mode)
        self.lineEdit_SerRecvFormatStr.textChanged.connect(self.uiUpdate_server_full_type_mode)
        # self.lineEdit_SerRecvFormatStr.textChanged.connect(self.uiUpdate_socket_server_receive_full_type_mode)

        # self.pushButton_ClntCreateConn.clicked.connect(self.Create_Client_Socket)
        # self.pushButton_ClntCloseConn.clicked.connect(self.Close_Client_Socket)

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

    def create_server_socket(self):
        """
        create the socket server connection
        :return: no return
        """
        print('began create socket server')
        self.socket_server = SocketServer((self.lineEdit_SevIP.text(), self.lineEdit_SerPort.text()))
        # signal and slot connect
        self.socket_server.signal_socket_server_accepted.connect(self.uiUpdate_Socket_Server_communicate_enable)
        self.socket_server.signal_close_socket_server_thread.connect(self.close_socket_server_thread)
        # self.socket_server.signal_close_socket_server_thread.connect(self.uiUpdate_socket_server_communicate_disable)
        # self.socket_server.signal_socket_server_send.connect(self.pushButton_SerSend.setEnabled)
        # self.socket_server.signal_socket_server_received.connect(self.pushButton_SerRecv.setEnabled)
        self.socket_server.signal_record_result.connect(self.record_socket_communication_result)
        # thread function
        self.socket_server.moveToThread(self.Thread_socket_server)
        self.Thread_socket_server.started.connect(self.socket_server.create_socket_server)
        self.Thread_socket_server.start()

    def close_socket_server(self):
        """
        close the socket server socket
        :return: none
        """
        try:
            if self.socket_server.socket_server_accept_client is None:
                # create socket client thread to connect socket server and shut up it
                self.socket_server_client = SocketServerCloseClient((self.lineEdit_SevIP.text(), int(self.lineEdit_SerPort.text())))
                # signal and slot connect
                self.socket_server_client.signal_record_result.connect(self.record_socket_communication_result)
                self.socket_server_client.signal_close_socket_server_client_connection.connect(self.socket_server.close_socket_server)
                self.socket_server_client.signal_close_socket_server_client_thread.connect(self.close_socket_server_client_thread)

                self.socket_server_client.moveToThread(self.thread_close_socket_server)
                self.thread_close_socket_server.started.connect(self.socket_server_client.connect_to_Server)
                self.thread_close_socket_server.start()
            else:
                self.socket_server.close_socket_server()

            self.socket_server.b_socket_server_shutup = True
        except OSError as e:
            self.record_socket_communication_result(str(e))
            self.record_socket_communication_result("OSError happened when close the socket server connection,"
                                                    " please check!")

    def close_socket_server_thread(self):
        """
        close socket server thread after socket server are closed
        :return: None
        """
        if not self.Thread_socket_server.isFinished():
            if self.Thread_socket_server.isRunning():
                print('socket server thread still running')
            print('socket server thread haven\'t finished')
            self.Thread_socket_server.quit()
            if self.Thread_socket_server.wait() is True:
                print('socket server thread end')

    def close_socket_server_client_thread(self):
        """
        close socket server client thread after socket server are closed
        :return:
        """
        if not self.thread_close_socket_server.isFinished():
            self.thread_close_socket_server.quit()
            self.thread_close_socket_server.wait()
        print('close socket server client thread and update ui')
        # self.uiUpdate_socket_server_communicate_disable()

    def socket_server_send_message(self):
        """
        send message as the checkbox setting
        :return: None
        """
        if self.checkBox_SerSendInt.isChecked() + self.checkBox_SerSendFloat.isChecked() + self.checkBox_SerSendStr.isChecked() == 1:
            if self.checkBox_SerSendInt.isChecked():
                self.socket_server.socket_server_send(self.lineEdit_SerSendInt_Value.text())

            elif self.checkBox_SerSendFloat.isChecked():
                self.socket_server.socket_server_send(self.lineEdit_SerSendFloat_Value.text())
            else:
                self.socket_server.socket_server_send(self.lineEdit_SerSendstr_Value.text())
        elif self.checkBox_SerSendInt.isChecked() + self.checkBox_SerSendFloat.isChecked() + self.checkBox_SerSendStr.isChecked() == 2:
            if not self.checkBox_SerSendInt.isChecked():
                pass
            elif not self.checkBox_SerSendFloat.isChecked():
                pass
            else:
                pass
        elif self.checkBox_SerSendInt.isChecked() + self.checkBox_SerSendFloat.isChecked() + self.checkBox_SerSendStr.isChecked() == 3:
            pass

    def socket_server_receive_message(self):
        """

        :return:
        """
        if self.checkBox_SerSendInt.isChecked() + self.checkBox_SerSendFloat.isChecked() + self.checkBox_SerSendStr.isChecked() == 1:
            if self.checkBox_SerSendInt.isChecked():
                pass
                # self.spinBox_SerSendInt_Seq.setStyleSheet("QSpinBox{background-color:rgb(255, 85, 0)}")
                # self.spinBox_SerSendInt_Seq.setBackgroundRole(rgb(255, 85, 0))
            elif self.checkBox_SerSendFloat.isChecked():
                pass
                # self.spinBox_SerSendInt_Seq.setStyleSheet("QSpinBox{background-color:rgb(255, 85, 0)}")
            else:
                pass
        elif self.checkBox_SerSendInt.isChecked() + self.checkBox_SerSendFloat.isChecked() + self.checkBox_SerSendStr.isChecked() == 2:
            if not self.checkBox_SerSendInt.isChecked():
                pass
            elif not self.checkBox_SerSendFloat.isChecked():
                pass
            else:
                pass
        elif self.checkBox_SerSendInt.isChecked() + self.checkBox_SerSendFloat.isChecked() + self.checkBox_SerSendStr.isChecked() == 3:
            pass

    def record_socket_communication_result(self, str_record: str):
        """
        write record and date to textedit
        :param str_record: string that need to write
        :return: none
        """
        _str_time = time.strftime('%Y-%m-%d: %H:%M:%S ', time.localtime())
        self.textEdit_Log.append(_str_time + str_record)
        self.textEdit_Log.moveCursor(QTextCursor.End)

    def check_server_send_value(self):
        pass
        if self.checkBox_SerSendInt.isChecked() + self.checkBox_SerSendFloat.isChecked() + self.checkBox_SerSendStr.isChecked() == 1:
            if self.checkBox_SerSendInt.isChecked():
                self.socket_server.socket_server_send(self.lineEdit_SerSendInt_Value.text())

            elif self.checkBox_SerSendFloat.isChecked():
                self.socket_server.socket_server_send(self.lineEdit_SerSendFloat_Value.text())
            else:
                self.socket_server.socket_server_send(self.lineEdit_SerSendstr_Value.text())
        elif self.checkBox_SerSendInt.isChecked() + self.checkBox_SerSendFloat.isChecked() + self.checkBox_SerSendStr.isChecked() == 2:
            if not self.checkBox_SerSendInt.isChecked():
                pass
            elif not self.checkBox_SerSendFloat.isChecked():
                pass
            else:
                pass
        elif self.checkBox_SerSendInt.isChecked() + self.checkBox_SerSendFloat.isChecked() + self.checkBox_SerSendStr.isChecked() == 3:
            pass
    # ------------------------------------------------------------------------------------------------------------------
    # -----------------------------------uiUpdate-----------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    def uiUpdate_Socket_Server_communicate_enable(self, b_accepted):
        """
        enable send and receive widgets after socket server accept connection
        :param b_accepted:
        :return:None
        """
        if b_accepted:
            # send widgets
            self.checkBox_ServerSendString.setEnabled(True)
            self.lineEdit_ServerSendSeparator.setEnabled(True)
            self.checkBox_ServerSendRawbytes.setEnabled(True)

            self.checkBox_SerSendInt.setEnabled(True)
            self.checkBox_SerSendStr.setEnabled(True)
            self.checkBox_SerSendFloat.setEnabled(True)

            self.lineEdit_SerSendFullType.setEnabled(True)
            self.lineEdit_SerSendFormatStr.setEnabled(True)

            # receive widgets
            self.checkBox_ServerReceiveString.setEnabled(True)
            self.lineEdit_ServerReceiveSeparator.setEnabled(True)
            self.checkBox_ServerReceiveRawbytes.setEnabled(True)

            self.checkBox_SerRecvInt.setEnabled(True)
            self.checkBox_SerRecvStr.setEnabled(True)
            self.checkBox_SerRecvFloat.setEnabled(True)
            self.lineEdit_SerRecvFullType.setEnabled(True)
            self.lineEdit_SerRecvFullType.setFocusPolicy(Qt.StrongFocus)
            self.lineEdit_SerRecvFormatStr.setEnabled(True)
            self.lineEdit_SerRecvFormatStr.setFocusPolicy(Qt.StrongFocus)

            self.pushButton_SerCloseConn.setEnabled(True)
            self.pushButton_SerCreateConn.setEnabled(False)
        else:
            # send widgets
            self.checkBox_ServerSendString.setEnabled(False)
            self.lineEdit_ServerSendSeparator.setEnabled(False)
            self.checkBox_ServerSendRawbytes.setEnabled(False)

            self.checkBox_SerSendInt.setChecked(False)
            self.checkBox_SerSendInt.setEnabled(False)
            self.spinBox_SerSendInt_Seq.setValue(0)
            self.lineEdit_SerSendInt_Value.clear()

            self.checkBox_SerSendFloat.setChecked(False)
            self.checkBox_SerSendFloat.setEnabled(False)
            self.lineEdit_SerSendFloat_Value.clear()
            self.spinBox_SerSendFloat_Seq.setValue(0)

            self.checkBox_SerSendStr.setChecked(False)
            self.checkBox_SerSendStr.setEnabled(False)
            self.lineEdit_SerSendstr_Value.clear()
            self.spinBox_SerSendStr_Seq.setValue(0)

            self.lineEdit_SerSendFullType.clear()
            self.lineEdit_SerSendFullType.setEnabled(False)
            self.lineEdit_SerSendFormatStr.clear()
            self.lineEdit_SerSendFormatStr.setEnabled(False)

            # receive widgets
            self.checkBox_ServerReceiveString.setEnabled(False)
            self.lineEdit_ServerReceiveSeparator.setEnabled(False)
            self.checkBox_ServerReceiveRawbytes.setEnabled(False)

            self.lineEdit_SerRecvInt_Value.clear()
            self.spinBox_SerRecvInt_Seq.setValue(0)
            self.checkBox_SerRecvInt.setChecked(False)
            self.checkBox_SerRecvInt.setEnabled(False)

            self.lineEdit_SerRecvFloat_Value.clear()
            self.spinBox_SerRecvFloat_Seq.setValue(0)
            self.checkBox_SerRecvFloat.setChecked(False)
            self.checkBox_SerRecvFloat.setEnabled(False)

            self.lineEdit_SerRecvStr_Value.clear()
            self.spinBox_SerRecvStr_Seq.setValue(0)
            self.checkBox_SerRecvStr.setChecked(False)
            self.checkBox_SerRecvStr.setEnabled(False)

            self.lineEdit_SerRecvFormatStr.clear()
            self.lineEdit_SerRecvFormatStr.setEnabled(False)

            self.lineEdit_SerRecvFullType.clear()
            self.lineEdit_SerRecvFullType.setFocusPolicy(Qt.NoFocus)
            self.lineEdit_SerRecvFullType.setEnabled(False)

            self.pushButton_SerCloseConn.setEnabled(False)
            self.pushButton_SerCreateConn.setEnabled(True)

    def uiUpdate_checkbox_checked_String(self):
        """

        :return:
        """
        # server string checkbox checked
        if self.checkBox_ServerSendString.isChecked():
            self.checkBox_ServerSendRawbytes.setChecked(False)
            self.lineEdit_ServerSendSeparator.setEnabled(True)
        elif self.checkBox_ServerSendString.isEnabled():
            self.checkBox_ServerSendRawbytes.setChecked(True)
            self.lineEdit_ServerSendSeparator.setEnabled(False)

        if self.checkBox_ServerReceiveString.isChecked():
            self.checkBox_ServerReceiveRawbytes.setChecked(False)
            self.lineEdit_ServerReceiveSeparator.setEnabled(True)
        elif self.checkBox_ServerReceiveString.isEnabled():
            self.checkBox_ServerReceiveRawbytes.setChecked(True)
            self.lineEdit_ServerReceiveSeparator.setEnabled(False)
        # client string checkbox checked
        if self.checkBox_ClientSendString.isChecked():
            self.checkBox_ClientSendRawbytes.setChecked(False)
            self.lineEdit_ClientSendSeparator.setEnabled(True)
        elif self.checkBox_ClientSendString.isEnabled():
            self.checkBox_ClientSendRawbytes.setChecked(True)
            self.lineEdit_ClientSendSeparator.setEnabled(False)

        if self.checkBox_ClientReceiveString.isChecked():
            self.checkBox_ClientReceiveRawbytes.setChecked(False)
            self.lineEdit_ClientReceiveSeparator.setEnabled(True)
        elif self.checkBox_ClientReceiveString.isEnabled():
            self.checkBox_ClientReceiveRawbytes.setChecked(True)
            self.lineEdit_ClientReceiveSeparator.setEnabled(False)

    def uiUpdate_checkbox_checked_Rawbytes(self):
        """

        :return:
        """
        # server rawbytes checkbox checked
        if self.checkBox_ServerSendRawbytes.isChecked():
            self.checkBox_ServerSendString.setChecked(False)
            self.lineEdit_ServerSendSeparator.setEnabled(False)
        elif self.checkBox_ServerSendRawbytes.isEnabled():
            self.checkBox_ServerSendString.setChecked(True)
            self.lineEdit_ServerSendSeparator.setEnabled(True)

        if self.checkBox_ServerReceiveRawbytes.isChecked():
            self.checkBox_ServerReceiveString.setChecked(False)
            self.lineEdit_ServerReceiveSeparator.setEnabled(False)
        elif self.checkBox_ServerReceiveRawbytes.isEnabled():
            self.checkBox_ServerReceiveString.setChecked(True)
            self.lineEdit_ServerReceiveSeparator.setEnabled(True)
        # client rawbytes checkbox checked
        if self.checkBox_ClientSendRawbytes.isChecked():
            self.checkBox_ClientSendString.setChecked(False)
            self.lineEdit_ClientSendSeparator.setEnabled(False)
        elif self.checkBox_ClientSendRawbytes.isEnabled():
            self.checkBox_ClientSendString.setChecked(True)
            self.lineEdit_ClientSendSeparator.setEnabled(True)

        if self.checkBox_ClientReceiveRawbytes.isChecked():
            self.checkBox_ClientReceiveString.setChecked(False)
            self.lineEdit_ClientReceiveSeparator.setEnabled(False)
        elif self.checkBox_ClientReceiveRawbytes.isEnabled():
            self.checkBox_ClientReceiveString.setChecked(True)
            self.lineEdit_ClientReceiveSeparator.setEnabled(True)

    def uiUpdate_server_full_type_mode(self):
        """
        clear send single mode sequence and values if full type mode string are changed
        :return:
        """
        # judge if the serSendFullType are clear by single mode, this would avoid the checkbox setCheck automatically!
        if self.lineEdit_SerSendFullType.text() != "":
            self.checkBox_SerSendInt.setChecked(False)
            self.checkBox_SerSendFloat.setChecked(False)
            self.checkBox_SerSendStr.setChecked(False)
            self.lineEdit_SerSendFormatStr.setReadOnly(False)

        if self.lineEdit_SerRecvFormatStr.text() != "":
            self.checkBox_SerRecvInt.setChecked(False)
            self.checkBox_SerRecvFloat.setChecked(False)
            self.checkBox_SerRecvStr.setChecked(False)
            self.lineEdit_SerRecvFullType.setReadOnly(True)

        self.uiUpdate_checkbox_toggle_init()

    def uiUpdate_checkbox_toggle_init(self):
        """

        :return:
        """
        # server send checkbox
        if self.checkBox_SerSendInt.isChecked():
            print("Checkbox is checked")
            self.spinBox_SerSendInt_Seq.setEnabled(True)
            self.lineEdit_SerSendInt_Value.setEnabled(True)

            # self.checkBox_SerSendInt.setChecked(True)
            self.lineEdit_SerSendFormatStr.setReadOnly(True)
            self.lineEdit_SerSendFullType.clear()
            # self.lineEdit_SerSendInt_Value.setStyleSheet("QLineEdit{background-color:rgb(255, 255, 255)}")
        else:
            print("CheckBox is not checked")
            self.spinBox_SerSendInt_Seq.setValue(0)
            self.spinBox_SerSendInt_Seq.setEnabled(False)
            self.lineEdit_SerSendInt_Value.clear()
            self.lineEdit_SerSendInt_Value.setEnabled(False)

        if self.checkBox_SerSendFloat.isChecked():
            self.spinBox_SerSendFloat_Seq.setEnabled(True)
            self.lineEdit_SerSendFloat_Value.setEnabled(True)

            self.checkBox_SerSendFloat.setChecked(True)
            self.lineEdit_SerSendFormatStr.setReadOnly(True)
            self.lineEdit_SerSendFullType.clear()
        else:
            self.spinBox_SerSendFloat_Seq.setValue(0)
            self.spinBox_SerSendFloat_Seq.setEnabled(False)
            self.lineEdit_SerSendFloat_Value.clear()
            self.lineEdit_SerSendFloat_Value.setEnabled(False)

        if self.checkBox_SerSendStr.isChecked():
            self.spinBox_SerSendStr_Seq.setEnabled(True)
            self.lineEdit_SerSendstr_Value.setEnabled(True)

            self.checkBox_SerSendStr.setChecked(True)
            self.lineEdit_SerSendFormatStr.setReadOnly(True)
            self.lineEdit_SerSendFullType.clear()
        else:
            self.spinBox_SerSendStr_Seq.setValue(0)
            self.spinBox_SerSendStr_Seq.setEnabled(False)
            self.lineEdit_SerSendstr_Value.clear()
            self.lineEdit_SerSendstr_Value.setEnabled(False)
        # server receive checkbox
        if self.checkBox_SerRecvInt.isChecked():
            self.spinBox_SerRecvInt_Seq.setEnabled(True)
            self.lineEdit_SerRecvInt_Value.setEnabled(True)

            self.checkBox_SerRecvInt.setChecked(True)
            # self.lineEdit_SerRecvFormatStr.setReadOnly(True)
            self.lineEdit_SerRecvFullType.clear()
            self.lineEdit_SerRecvFormatStr.clear()
        else:
            self.spinBox_SerRecvInt_Seq.setValue(0)
            self.spinBox_SerRecvInt_Seq.setEnabled(False)
            self.lineEdit_SerRecvInt_Value.clear()
            self.lineEdit_SerRecvInt_Value.setEnabled(False)

        if self.checkBox_SerRecvFloat.isChecked():
            self.spinBox_SerRecvFloat_Seq.setEnabled(True)
            self.lineEdit_SerRecvFloat_Value.setEnabled(True)

            self.checkBox_SerRecvFloat.setChecked(True)
            # self.lineEdit_SerRecvFormatStr.setReadOnly(True)
            self.lineEdit_SerRecvFullType.clear()
            self.lineEdit_SerRecvFormatStr.clear()
        else:
            self.spinBox_SerRecvFloat_Seq.setValue(0)
            self.spinBox_SerRecvFloat_Seq.setEnabled(False)
            self.lineEdit_SerRecvFloat_Value.clear()
            self.lineEdit_SerRecvFloat_Value.setEnabled(False)

        if self.checkBox_SerRecvStr.isChecked():
            self.spinBox_SerRecvStr_Seq.setEnabled(True)
            self.lineEdit_SerRecvStr_Value.setEnabled(True)

            self.checkBox_SerRecvStr.setChecked(True)
            # self.lineEdit_SerRecvFormatStr.setReadOnly(True)
            self.lineEdit_SerRecvFullType.clear()
            self.lineEdit_SerRecvFormatStr.clear()
        else:
            self.spinBox_SerRecvStr_Seq.setValue(0)
            self.spinBox_SerRecvStr_Seq.setEnabled(False)
            self.lineEdit_SerRecvStr_Value.clear()
            self.lineEdit_SerRecvStr_Value.setEnabled(False)
        # client send check box
        if self.checkBox_ClntSendInt.isChecked():
            self.spinBox_ClntSendInt_Seq.setEnabled(True)
            self.lineEdit_ClntSendInt_Value.setEnabled(True)
        else:
            self.spinBox_ClntSendInt_Seq.setValue(0)
            self.spinBox_ClntSendInt_Seq.setEnabled(False)
            self.lineEdit_ClntSendInt_Value.clear()
            self.lineEdit_ClntSendInt_Value.setEnabled(False)

        if self.checkBox_ClntSendFloat.isChecked():
            self.spinBox_ClntSendFloat_Seq.setEnabled(True)
            self.lineEdit_ClntSendFloat_Value.setEnabled(True)
        else:
            self.spinBox_ClntSendFloat_Seq.setValue(0)
            self.spinBox_ClntSendFloat_Seq.setEnabled(False)
            self.lineEdit_ClntSendFloat_Value.clear()
            self.lineEdit_ClntSendFloat_Value.setEnabled(False)

        if self.checkBox_ClntSendStr.isChecked():
            self.spinBox_ClntSendStr_Seq.setEnabled(True)
            self.lineEdit_ClntSendStr_Value.setEnabled(True)
        else:
            self.spinBox_ClntSendStr_Seq.setValue(0)
            self.spinBox_ClntSendStr_Seq.setEnabled(False)
            self.lineEdit_ClntSendStr_Value.clear()
            self.lineEdit_ClntSendStr_Value.setEnabled(False)
        # client receive checkbox
        if self.checkBox_ClntRecvInt.isChecked():
            self.spinBox_ClntRecvInt_Seq.setEnabled(True)
            self.lineEdit_ClntRecvInt_Value.setEnabled(True)
        else:
            self.spinBox_ClntRecvInt_Seq.setValue(0)
            self.spinBox_ClntRecvInt_Seq.setEnabled(False)
            self.lineEdit_ClntRecvInt_Value.clear()
            self.lineEdit_ClntRecvInt_Value.setEnabled(False)

        if self.checkBox_ClntRecvFloat.isChecked():
            self.spinBox_ClntRecvFloat_Seq.setEnabled(True)
            self.lineEdit_ClntRecvFloat_Value.setEnabled(True)
        else:
            self.spinBox_ClntRecvFloat_Seq.setValue(0)
            self.spinBox_ClntRecvFloat_Seq.setEnabled(False)
            self.lineEdit_ClntRecvFloat_Value.clear()
            self.lineEdit_ClntRecvFloat_Value.setEnabled(False)

        if self.checkBox_ClntRecvStr.isChecked():
            self.spinBox_ClntRecvStr_Seq.setEnabled(True)
            self.lineEdit_ClntRecvStr_Value.setEnabled(True)
        else:
            self.spinBox_ClntRecvStr_Seq.setValue(0)
            self.spinBox_ClntRecvStr_Seq.setEnabled(False)
            self.lineEdit_ClntRecvStr_Value.clear()
            self.lineEdit_ClntRecvStr_Value.setEnabled(False)
        self.uiUpdate_SerSendValueCheck()

    def uiUpdate_SerSendValueCheck(self):
        if self.checkBox_SerSendInt.isChecked() + self.checkBox_SerSendFloat.isChecked() + self.checkBox_SerSendStr.isChecked() == 1:
            if self.checkBox_SerSendInt.isChecked():
                pass
                # self.spinBox_SerSendInt_Seq.setStyleSheet("QSpinBox{background-color:rgb(255, 85, 0)}")
                # self.spinBox_SerSendInt_Seq.setBackgroundRole(rgb(255, 85, 0))
            elif self.checkBox_SerSendFloat.isChecked():
                pass
                # self.spinBox_SerSendInt_Seq.setStyleSheet("QSpinBox{background-color:rgb(255, 85, 0)}")
            else:
                pass
        elif self.checkBox_SerSendInt.isChecked() + self.checkBox_SerSendFloat.isChecked() + self.checkBox_SerSendStr.isChecked() == 2:
            if not self.checkBox_SerSendInt.isChecked():
                pass
            elif not self.checkBox_SerSendFloat.isChecked():
                pass
            else:
                pass
        elif self.checkBox_SerSendInt.isChecked() + self.checkBox_SerSendFloat.isChecked() + self.checkBox_SerSendStr.isChecked() == 3:
            pass


if __name__ == '__main__':
    # format the application interface show as designer display
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    gui_app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(gui_app.exec())
