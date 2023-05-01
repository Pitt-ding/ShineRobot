#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Version : PyCharm
# @Time    : 2023/1/8 2:47
# @Author  : Pitt.Ding
# @File    : shine_robot_socket_communication.py
# @Description :
import struct
import re
import time
from typing import Union
from socket import socket
from PyQt5.Qt import QObject, QThread
from PyQt5 import QtCore


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


class SocketCommunicate:
    def __init__(self):
        self.b_continue_send = False
        self.str_send_interval = '0'

    def socket_send_bytes(self, s_send: Union[bytes, str]) -> None:
        pass

    def socket_receive_bytes(self) -> Union[bytes, None]:
        pass

    def socket_send(self, _send_str: str) -> None:  # , _b_continue_send: bool, _send_interval: str
        """
        Base send widgets status quote send string function,use name tuple as input args,suit for both server and client
        """
        try:
            while True:
                # if widgets_status.checkBox_SendStringMode.isChecked():
                #     # send string
                #     if _int_checked + _float_checked + _str_checked == 1:
                #         if _int_checked:
                #             _send_fun(_int_text)
                #         elif _float_checked:
                #             _send_fun(_float_text)
                #         else:
                #             _send_fun(_str_text)
                #
                #     elif _int_checked + _float_checked + _str_checked == 2:
                #         if not _int_checked:
                #             if int(_float_seq) > int(_str_seq):
                #                 _send_fun(_float_text + _send_str_Separator_text + _str_text)
                #             else:
                #                 _send_fun(_str_text + _send_str_Separator_text + _float_text)
                #         elif not _float_checked:
                #             if int(_int_seq) > int(_str_seq):
                #                 _send_fun(_int_text + _send_str_Separator_text + _str_text)
                #             else:
                #                 _send_fun(_str_text + _send_str_Separator_text + _int_text)
                #         else:
                #             if int(_int_seq) > int(_float_seq):
                #                 _send_fun(_int_text + _send_str_Separator_text + _float_text)
                #             else:
                #                 _send_fun(_float_text + _send_str_Separator_text + _int_text)
                #
                #     elif _int_checked + _float_checked + _str_checked == 3:
                #         # 生成字列表，并对列表按键值做排序
                #         m_sequence_list = [[int(_int_seq), _int_text],
                #                            [int(_float_seq), _float_text],
                #                            [int(_str_seq), _str_text]]
                #         m_sequence_list.sort(key=lambda x: x[0], reverse=True)
                #         _send_fun(str(m_sequence_list[0][1]) + _send_str_Separator_text + str(m_sequence_list[1][1])
                #                   + _send_str_Separator_text + str(m_sequence_list[2][1]))
                #     else:
                #         _send_fun(_full_type_str_text)
                # else:
                #     # Send rawbytes
                #     if _int_checked + _float_checked + _str_checked == 1:
                #         if _int_checked:
                #             _send_fun(struct.pack("<h", int(_int_text)))
                #         elif _float_checked:
                #             _send_fun(struct.pack("<f", float(_float_text)))
                #         else:
                #             _send_fun(struct.pack("<f", str(_str_text)))
                #
                #     elif _int_checked + _float_checked + _str_checked == 2:
                #         if not _int_checked:
                #             if int(_float_seq) > int(_str_seq):
                #                 _send_fun(struct.pack("<f{}s".format(len(_str_text)), float(_float_text), _str_text.encode()))
                #             else:
                #                 _send_fun(struct.pack("<{}sf".format(len(_str_text)), _str_text.encode(), float(_float_text)))
                #         elif not _float_checked:
                #             if int(_int_seq) > int(_str_seq):
                #                 _send_fun(struct.pack("<h{}s".format(len(_str_text)), int(_int_text), _str_text.encode()))
                #             else:
                #                 _send_fun(struct.pack("<{}sh".format(len(_str_text)), _str_text.encode(), int(_int_text)))
                #         else:
                #             if int(_int_seq) > int(_float_seq):
                #                 _send_fun(struct.pack("<hf", int(_int_text), float(_float_text)))
                #             else:
                #                 _send_fun(struct.pack("<fh", float(_float_text), int(_int_text)))
                #
                #     elif _int_checked + _float_checked + _str_checked == 3:
                #         m_sequence_list = [
                #             [int(_int_seq), int(_int_text), "h"],
                #             [int(_float_seq), float(_float_text), "f"],
                #             [int(_str_seq), _str_text.encode(), "{}s".format(len(_str_text))]]
                #
                #         m_sequence_list.sort(key=lambda x: x[0], reverse=True)
                #         _send_fun(struct.pack("<" + m_sequence_list[0][2] + m_sequence_list[1][2] + m_sequence_list[2][2],
                #                               m_sequence_list[0][1], m_sequence_list[1][1], m_sequence_list[2][1]))
                #     else:
                #         list_re = re.findall(r"(h|f|\d+s)", _full_type_format_str_text)
                #         list_value = _full_type_str_text.split(_send_str_Separator_text)
                #         list_byte = bytes()
                #         for int_index in range(len(list_re)):
                #             if list_re[int_index] == "h":
                #                 list_byte += (struct.pack("<" + list_re[int_index], int(list_value[int_index])))
                #             elif list_re[int_index] == "f":
                #                 list_byte += (struct.pack("<" + list_re[int_index], float(list_value[int_index])))
                #             elif "s" in list_re[int_index]:
                #                 list_byte += (struct.pack("<" + list_re[int_index], list_value[int_index].encode()))
                #         _send_fun(list_byte)
                print("send continue: {}, send interval: {}".format(self.b_continue_send, self.str_send_interval))
                self.socket_send_bytes(_send_str)
                time.sleep(float(self.str_send_interval))
                if not self.b_continue_send:
                    break
        except ConnectionAbortedError:
            return

    def socket_receive(self, widgets_status: SocketWidgetStruct) -> None:
        """
        Base send widgets status quote receive string function,use name tuple as input args,suit for both server and client
        """
        _recv_fun = self.socket_receive_bytes
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
            while True:
                if widgets_status.checkBox_ReceiveStrMode.isChecked():
                    if _int_checked + _float_checked + _str_checked == 0:
                        try:
                            _full_type_str_text_lineedit.setText(_recv_fun().decode())
                        except AttributeError as e:
                            print(e)
                            _full_type_str_text_lineedit.clear()
                    if _int_checked + _float_checked + _str_checked == 1:
                        if _int_checked:
                            try:
                                _int_text_lineedit.clear()
                                m_int = int(_recv_fun().decode())
                                _int_text_lineedit.setText(str(m_int))
                            except ValueError:
                                _int_text_lineedit.clear()
                                _log_fun("Can't parse receive string bytes as type setting,please check")
                                return

                        elif _float_checked:
                            try:
                                _float_text_lineedit.clear()
                                m_float = float(_recv_fun().decode())
                                _float_text_lineedit.setText(str(m_float))
                            except ValueError:
                                _float_text_lineedit.clear()
                                _log_fun("Can't parse receive string bytes as type setting,please check")
                                return
                        else:
                            try:
                                _str_text_lineedit.clear()
                                m_str = _recv_fun().decode()
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
                                    _float_str, _string = _recv_fun().decode().split(_recv_str_Separator_text)
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
                                    _string, _float_str = _recv_fun().decode().split(_recv_str_Separator_text)
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
                                    _int_str, _string = _recv_fun().decode().split(_recv_str_Separator_text)
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
                                    _string, _int_str = _recv_fun().decode().split(_recv_str_Separator_text)
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
                                    _int_str, _float_str = _recv_fun().decode().split(_recv_str_Separator_text)
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
                                    _float_str, _int_str = _recv_fun().decode().split(_recv_str_Separator_text)
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
                            list_type[0][1], list_type[1][1], list_type[2][1] = _recv_fun().decode().split(
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
                            _tuple = struct.unpack(_full_type_format_str_text, _recv_fun())
                            _full_type_str_text_lineedit.setText(str(_tuple))
                        except (struct.error, ValueError):
                            _full_type_str_text_lineedit.clear()
                            _log_fun("Can't parse receive rawbytes as type setting,please check")

                    if _int_checked + _float_checked + _str_checked == 1:
                        if _int_checked:
                            try:
                                _int_text_lineedit.clear()
                                _int, = struct.unpack('<h', _recv_fun())
                                _int_text_lineedit.setText(str(_int))
                            except (struct.error, ValueError):
                                _int_text_lineedit.clear()
                                _log_fun("Can't parse receive rawbytes as type setting,please check")

                        elif _float_checked:
                            try:
                                _float_text_lineedit.clear()
                                _float, = struct.unpack('<f', _recv_fun())
                                _float_text_lineedit.setText(str(_float))
                            except (struct.error, ValueError):
                                _float_text_lineedit.clear()
                                _log_fun("Can't parse receive rawbytes as type setting,please check")

                        else:
                            try:
                                _str_text_lineedit.clear()
                                _string, = struct.unpack('<{}s'.format(_server_receive_rawbytes_length), _recv_fun())
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
                                                                 _recv_fun())
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
                                                                 _recv_fun())
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
                                                               _recv_fun())
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
                                                                _recv_fun())
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
                                    _int, _float = struct.unpack('<hf', _recv_fun())
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
                                    _float, _int = struct.unpack('<fh', _recv_fun())
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
                            list_type = sorted([[_int_seq, None, "h"], [_float_seq, None, "f"], [_str_seq, None, "{}s"]],
                                               key=lambda x: int(x[0]),
                                               reverse=True)
                            _unpack_format_str = "<" + list_type[0][2] + list_type[1][2] + list_type[2][2]
                            list_type[0][1], list_type[1][1], list_type[2][1] = list(
                                struct.unpack(_unpack_format_str.format(_server_receive_rawbytes_length), _recv_fun()))

                            _int_text_lineedit.setText([str(x[1]) for x in list_type if x[0] == _int_seq][0])
                            _float_text_lineedit.setText([str(x[1]) for x in list_type if x[0] == _float_seq][0])
                            _str_text_lineedit.setText([str(x[1].decode()) for x in list_type if x[0] == _str_seq][0])
                        except (struct.error, ValueError):
                            _int_text_lineedit.clear()
                            _float_text_lineedit.clear()
                            _str_text_lineedit.clear()
                            _log_fun("Can't parse receive rawbytes as type setting,please check")

                time.sleep(float(widgets_status.lineEdit_RecvInterval.text()))
                if not widgets_status.checkBox_RecvContinue.isChecked():
                    break
        # 检查调用Socket receive方法是否接收数据超时，如果是则发布信息并return
        except OSError as e:
            _log_fun(str(e))
            _log_fun("Doesn't receive any data, please check")
            return


class SocketServer(QObject, SocketCommunicate):
    """
    class for shine robot socket server communication, contain the function for create server,send and receive
    """
    # message log signal for write in GUI
    signal_record_result = QtCore.pyqtSignal(str)
    # socket server connect accepted signal
    signal_socket_server_accepted = QtCore.pyqtSignal(bool)
    signal_socket_server_closed = QtCore.pyqtSignal(bool)

    def __init__(self) -> None:
        super().__init__()
        self.socket_server_connect_ip, self.socket_server_connect_port = None, None
        self.socket_server = socket()

        self.b_socket_server_shutup = False
        self.socket_server_accept_client = socket()

    def create_socket_server(self, _ip_port):
        """
        create the socket server in thread
        :return: None
        """
        try:
            self.socket_server.__init__()
            # self.b_socket_server_shutup = False
            print("Socket server thread", QThread.currentThreadId())
            self.socket_server_connect_ip, self.socket_server_connect_port = _ip_port
            self.socket_server_connect_port = int(self.socket_server_connect_port)

            self.signal_record_result.emit("Socket server Creating...")
            self.signal_record_result.emit("Server IP:{}, Server Port:{}".format(self.socket_server_connect_ip, self.socket_server_connect_port))

            self.socket_server.bind((self.socket_server_connect_ip, self.socket_server_connect_port))

            self.signal_record_result.emit("Socket server bind finished")
            self.signal_record_result.emit("Socket server begin listening...")
            self.socket_server.listen()

            # socket_server.settimeout(3)
            self.signal_record_result.emit("Socket server begin accept client connection...")
            self.socket_server_accept_client, socket_server_accept_any = self.socket_server.accept()
            self.signal_record_result.emit("socket server accept client connection from {}".format(socket_server_accept_any))
            self.signal_socket_server_accepted.emit(True)

        except OSError as e:
            self.signal_record_result.emit("Socket server create connect: " + str(e))
            self.socket_server_accept_client.close()
            self.socket_server.close()

    def close_socket_server(self) -> None:
        """
        close socket server and accepted server and signal emit to update ui
        with decorate to declare slot function
        :return:
        """
        try:
            self.socket_server_accept_client.close()
            # !!!Clear accepted client after closed, if not there would be error
            self.signal_record_result.emit("Socket server accepted client closed")
            self.socket_server.close()

            self.signal_socket_server_accepted.emit(False)
            self.signal_record_result.emit("Socket server closed")
            self.signal_socket_server_closed.emit(True)
        except OSError as e:
            self.signal_record_result.emit("Socket server close: " + str(e))
            self.socket_server_accept_client.close()
            self.socket_server.close()

    def socket_send_bytes(self, s_send: Union[bytes, str]) -> None:
        """
        send data to client
        :return: None
        """
        try:
            if self.socket_server_accept_client is not None:
                if type(s_send) is bytes:
                    print("send rawbytes")
                    self.socket_server_accept_client.send(s_send)
                else:
                    self.signal_record_result.emit("socket server send data: " + s_send)
                    self.socket_server_accept_client.send(s_send.encode())
        except ConnectionAbortedError as e:
            self.signal_record_result.emit("Socket server send: " + str(e))
            raise ConnectionAbortedError

    def socket_receive_bytes(self) -> Union[bytes, None]:
        """
        receive data from client
        :return: None
        """
        if self.socket_server_accept_client is not None:
            try:
                self.socket_server_accept_client.settimeout(3)
                m_receive = self.socket_server_accept_client.recv(1024)
                self.signal_record_result.emit("Receive value type: {}".format(type(m_receive)))
                self.signal_record_result.emit("Receive value: {}".format(m_receive))
                return m_receive

            except (ValueError, TypeError) as e:
                self.signal_record_result.emit("Socket server receive: " + str(e))
                return
            # 检查socket.recv()是否超时，如果超时则向调用方Raise osError错误
            except OSError:
                raise OSError

    def socket_clear_cache(self) -> None:
        """
        clear receive data from client
        :return: None
        """
        if self.socket_server_accept_client is not None:
            try:
                self.socket_server_accept_client.settimeout(1)
                m_receive = self.socket_server_accept_client.recv(1024)
                self.signal_record_result.emit("Socket server Receive value type: {}".format(type(m_receive)))
                self.signal_record_result.emit("Socket server Receive value: {}".format(m_receive))
                self.signal_record_result.emit("Socket server clear {} length bytes".format(len(m_receive)))

            except (ValueError, TypeError) as e:
                self.signal_record_result.emit("Socket server receive error: " + str(e))
                return
            # 检查socket.recv()是否超时，如果超时则向调用方Raise osError错误
            except OSError:
                self.signal_record_result.emit("Socket server receive bytes timeout!")


class SocketServerCloseClient(QObject):
    """
    class for close socket server which stub in accept function,create socket client connect to server and close self
    """
    signal_record_result = QtCore.pyqtSignal(str)
    signal_socket_server_client_closed = QtCore.pyqtSignal(bool)

    def __init__(self, _ip_port: tuple) -> None:
        super().__init__()
        # init variable for socket communication
        self.socket_client = socket()
        self._targetAddress = _ip_port
        self.socket_server_client_connect_ip, self.socket_server_client_connect_port = None, None

    def connect_to_server(self) -> None:
        """
        create socket server client for close server connection
        :return: None
        """
        try:
            # print('Address:{},port{}'.format(*self._targetAddress))
            self.socket_client = socket()
            self.socket_client.settimeout(3)
            self.socket_server_client_connect_ip, self.socket_server_client_connect_port = self._targetAddress
            self.socket_server_client_connect_port = int(self.socket_server_client_connect_port)

            self.socket_client.connect((self.socket_server_client_connect_ip, self.socket_server_client_connect_port))
            self.socket_client.close()
            self.signal_socket_server_client_closed.emit(True)
            # self.signal_close_socket_server_client_thread.emit(True)
        except OSError as e:
            self.signal_record_result.emit("Socket server close client: " + str(e))

        finally:
            pass


class SocketClient(QObject, SocketCommunicate):
    """
    class for shine robot socket server communication, contain the function for create server,send and receive
    """
    # message log signal for write in GUI
    signal_record_result = QtCore.pyqtSignal(str)
    # socket server connect accepted signal
    signal_socket_client_connected = QtCore.pyqtSignal(bool)

    def __init__(self) -> None:
        super().__init__()
        self.socket_server_connect_ip = None
        self.socket_server_connect_port = None
        # self.socket_server_connect_ip, self.socket_server_connect_port = _ip_port
        # self.socket_server_connect_port = int(self.socket_server_connect_port)
        self.socket_client = socket()

        self.b_socket_client_shutup = False
        # self.nSocket_server_send = 0
        # self.nSocket_server_receive = 0
        # self.socket_server_accept_client = None

    def create_socket_client(self, _ip_port: tuple) -> None:
        """
        create the socket server in thread
        :return: None
        """
        try:
            self.socket_server_connect_ip, self.socket_server_connect_port = _ip_port
            self.socket_server_connect_port = int(self.socket_server_connect_port)
            # self.b_socket_client_shutup = False

            self.signal_record_result.emit("Socket client Creating...")
            self.signal_record_result.emit("Client target IP:{}, Client target Port:{}".format(self.socket_server_connect_ip, self.socket_server_connect_port))
            self.socket_client = socket()
            self.socket_client.settimeout(1)
            self.signal_record_result.emit("Socket client begin connect")
            self.socket_client.connect((self.socket_server_connect_ip, self.socket_server_connect_port))
            self.signal_record_result.emit("Socket Client success connect to target server")
            self.signal_socket_client_connected.emit(True)

        except OSError as e:
            self.signal_record_result.emit(str(e))
            # self.socket_client.close()

    def close_socket_client(self) -> None:
        """
        close socket client and signal emit to update ui
        with decorate to declare slot function
        :return:
        """
        self.socket_client.close()
        self.signal_socket_client_connected.emit(False)
        self.signal_record_result.emit("Socket client closed")
        # self.signal_socket_client_closed.emit(True)

    def socket_send_bytes(self, s_send: Union[bytes, str]) -> None:
        """
        send data to client
        :return: None
        """
        try:
            if type(s_send) is bytes:
                print("socket client send rawbytes")
                self.socket_client.send(s_send)
            else:
                self.signal_record_result.emit("socket client send data: " + s_send)
                self.socket_client.send(s_send.encode())
        except ConnectionAbortedError as e:
            self.signal_record_result.emit(str(e))
            return

    def socket_receive_bytes(self) -> Union[bytes, None]:
        """
        receive data from client
        :return: None
        """
        try:
            self.socket_client.settimeout(3)
            m_receive = self.socket_client.recv(1024)
            self.signal_record_result.emit("socket client Receive value type: {}".format(type(m_receive)))
            self.signal_record_result.emit("socket client Receive value: {}".format(m_receive))
            return m_receive

        except (ValueError, TypeError) as e:
            self.signal_record_result.emit(str(e))
            return
        # 检查socket.recv()是否超时，如果超时则向调用方Raise osError错误
        except OSError:
            raise OSError

    def socket_clear_cache(self) -> Union[bytes, None]:
        """
        receive data from client
        :return: None
        """
        try:
            self.socket_client.settimeout(1)
            m_receive = self.socket_client.recv(1024)
            self.signal_record_result.emit("Socket client Receive value type: {}".format(type(m_receive)))
            self.signal_record_result.emit("Socket client Receive value: {}".format(m_receive))
            self.signal_record_result.emit("Socket client clear {} length bytes".format(len(m_receive)))
            return m_receive

        except (ValueError, TypeError) as e:
            self.signal_record_result.emit(str(e))
            return
        # 检查socket.recv()是否超时，如果超时则向调用方Raise osError错误
        except OSError:
            self.signal_record_result.emit("Socket client receive bytes timeout!")
