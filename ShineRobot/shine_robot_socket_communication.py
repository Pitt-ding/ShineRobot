#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Version : PyCharm
# @Time    : 2023/1/8 2:47
# @Author  : Pitt.Ding
# @File    : shine_robot_socket_communication.py
# @Description :

from socket import socket
from PyQt5.Qt import QObject
from PyQt5 import QtCore


class SocketServer(QObject):
    """
    class for shine robot socket server communication, contain the function for create server,send and receive
    """
    # signal for class
    signal_record_result = QtCore.pyqtSignal(str)
    signal_socket_server_accepted = QtCore.pyqtSignal(bool)
    signal_close_socket_server_thread = QtCore.pyqtSignal(bool)

    def __init__(self, _ip_port):

        super().__init__()
        self.socket_server_connect_ip = '127.0.0.1'
        self.socket_server_connect_port = 1026
        self.socket_server_connect_ip, self.socket_server_connect_port = _ip_port
        self.socket_server_connect_port = int(self.socket_server_connect_port)
        self.socket_server = socket()

        self.b_socket_server_shutup = False
        self.nSocket_server_send = 0
        self.nSocket_server_receive = 0
        self.socket_server_accept_client = None

    def create_socket_server(self):
        """
        create the socket server in thread
        :return: None
        """
        try:

            self.b_socket_server_shutup = False
            self.nSocket_server_send = 0
            self.nSocket_server_receive = 0

            self.signal_record_result.emit("Socket server Creating...")
            self.signal_record_result.emit("Server IP:{}, Server Port:{}".format(self.socket_server_connect_ip, self.socket_server_connect_port))

            self.socket_server.bind((self.socket_server_connect_ip, self.socket_server_connect_port))
            self.signal_record_result.emit("socket server bind finished")
            self.signal_record_result.emit("socket server begin listening...")

            self.socket_server.listen()

            # socket_server.settimeout(3)
            self.socket_server_accept_client, socket_server_accept_any = self.socket_server.accept()
            if not self.b_socket_server_shutup:
                self.signal_record_result.emit("socket server accept client connection from {}".format(socket_server_accept_any))
                self.signal_socket_server_accepted.emit(True)

        except OSError as e:
            self.signal_record_result.emit(str(e))
            self.socket_server_accept_client.close()
            self.socket_server.close()

    @QtCore.pyqtSlot()
    def close_socket_server(self):
        """
        close socket server and accepted server and signal emit to update ui
        with decorate to declare slot function
        :return:
        """
        # self.socket_server_accept_client.shutdown(socket.SHUT_RDWR)
        self.socket_server_accept_client.close()
        self.socket_server.close()

        self.signal_socket_server_accepted.emit(False)
        self.signal_record_result.emit("socket server closed")
        self.signal_close_socket_server_thread.emit(True)

    @QtCore.pyqtSlot()
    def socket_server_send(self, s_send):
        """
        send data to client
        :return: None
        """
        if self.socket_server_accept_client is not None:
            if type(s_send) is bytes:
                print("send rawbytes")
                self.socket_server_accept_client.send(s_send)
            else:
                self.signal_record_result.emit("socket server send data: " + s_send)
                self.socket_server_accept_client.send(s_send.encode())
            # self.signal_socket_server_send.emit(True)

    @QtCore.pyqtSlot()
    def socket_server_receive(self):
        """
        receive data from client
        :return: None
        """
        if self.socket_server_accept_client is not None:
            try:
                self.socket_server_accept_client.settimeout(1)
                m_receive = self.socket_server_accept_client.recv(1024)
                self.signal_record_result.emit("Receive value type: {}".format(type(m_receive)))
                self.signal_record_result.emit("Receive value: {}".format(m_receive))
                return m_receive

            except (ValueError, TypeError) as e:
                self.signal_record_result.emit(str(e))
                return
            # 检查socket.recv()是否超时，如果超时则向调用方Raise错误
            except OSError:
                raise OSError


class SocketServerCloseClient(QObject):
    """
    class for close socket server which stub in accept function,create socket client connect to server and close self
    """
    signal_record_result = QtCore.pyqtSignal(str)
    signal_close_socket_server_client_connection = QtCore.pyqtSignal(bool)
    signal_close_socket_server_client_thread = QtCore.pyqtSignal(bool)

    def __init__(self, _ip_port):
        super().__init__()
        # init variable for socket communication
        # self.socket_client_connect_ip = '127.0.0.1'
        # self.socket_client_connect_port = 1025
        self.socket_client = socket()
        self._targetAddress = _ip_port

    def connect_to_Server(self):
        """
        create socket server client for close server connection
        :return: None
        """
        try:
            # print('Address:{},port{}'.format(*self._targetAddress))
            self.socket_client.settimeout(3)
            self.socket_client.connect(self._targetAddress)

            self.socket_client.close()
            self.signal_close_socket_server_client_connection.emit(True)
            self.signal_close_socket_server_client_thread.emit(True)
        except OSError as e:
            self.signal_record_result.emit(str(e))
            # socket_server_accept_client.close()
            # socket_server.close()
        finally:
            pass
