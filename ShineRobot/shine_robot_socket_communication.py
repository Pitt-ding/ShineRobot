#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Version : PyCharm
# @Time    : 2023/1/8 2:47
# @Author  : Pitt.Ding
# @File    : shine_robot_socket_communication.py
# @Description :

import time
from typing import Union
from socket import socket
from PyQt5.Qt import QObject, QThread
from PyQt5 import QtCore


class SocketCommunicate:
    signal_record_result = QtCore.pyqtSignal(str)
    signal_socket_receive_bytes = QtCore.pyqtSignal(bytes)
    signal_socket_sending = QtCore.pyqtSignal(bool)
    signal_socket_receiving = QtCore.pyqtSignal(bool)

    def __init__(self):
        self.b_continue_send = False
        self.str_send_interval = "0"
        self.b_continue_recv = False
        self.str_recv_interval = "0"

    def socket_send_bytes(self, s_send: Union[bytes, str]) -> None:
        pass

    def socket_receive_bytes(self) -> Union[bytes, None]:
        pass

    def socket_send(self, _send_str: str) -> None:
        """
        Base send widgets status quote send string function,use name tuple as input args,suit for both server and client
        """
        try:
            while True:
                self.signal_socket_sending.emit(True)
                # print("send continue: {}, send interval: {}".format(self.b_continue_send, self.str_send_interval))
                self.socket_send_bytes(_send_str)
                time.sleep(float(self.str_send_interval))
                if not self.b_continue_send:
                    self.signal_socket_sending.emit(False)
                    break
        except ConnectionAbortedError:
            return

    def socket_receive(self) -> None:
        """
        Base send widgets status quote receive string function,use name tuple as input args,suit for both server and client
        """
        try:
            while True:
                self.signal_socket_receiving.emit(True)
                _recv_bytes = self.socket_receive_bytes()
                if _recv_bytes is not None:
                    self.signal_socket_receive_bytes.emit(_recv_bytes)

                time.sleep(float(self.str_recv_interval))
                if not self.b_continue_recv:
                    self.signal_socket_receiving.emit(False)
                    break
        # 检查调用Socket receive方法是否接收数据超时，如果是则发布信息并return
        except OSError as e:
            self.signal_record_result.emit(str(e))
            self.signal_record_result.emit("Doesn't receive any data, please check")
            return


class SocketServer(QObject, SocketCommunicate):
    """
    class for shine robot socket server communication, contain the function for create server,send and receive
    """
    # message log signal for write in GUI
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
            self.signal_socket_sending.emit(False)
            self.signal_socket_receiving.emit(False)
        except OSError as e:
            self.signal_record_result.emit("Socket server close error: " + str(e))
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
                    # print("send rawbytes")
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
                # self.signal_record_result.emit("Receive value type: {}".format(type(m_receive)))
                self.signal_record_result.emit("Socket server Receive value: {}".format(m_receive))
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
            self.socket_client = socket()
            self.socket_client.settimeout(3)
            self.socket_server_client_connect_ip, self.socket_server_client_connect_port = self._targetAddress
            self.socket_server_client_connect_port = int(self.socket_server_client_connect_port)

            self.socket_client.connect((self.socket_server_client_connect_ip, self.socket_server_client_connect_port))
            self.socket_client.close()
            self.signal_socket_server_client_closed.emit(True)
        except OSError as e:
            self.signal_record_result.emit("Socket server close client: " + str(e))
        finally:
            pass


class SocketClient(QObject, SocketCommunicate):
    """
    class for shine robot socket server communication, contain the function for create server,send and receive
    """
    # message log signal for write in GUI
    # socket server connect accepted signal
    signal_socket_client_connected = QtCore.pyqtSignal(bool)

    def __init__(self) -> None:
        super().__init__()
        self.socket_server_connect_ip = None
        self.socket_server_connect_port = None
        self.socket_client = socket()

        self.b_socket_client_shutup = False

    def create_socket_client(self, _ip_port: tuple) -> None:
        """
        create the socket server in thread
        :return: None
        """
        try:
            self.socket_server_connect_ip, self.socket_server_connect_port = _ip_port
            self.socket_server_connect_port = int(self.socket_server_connect_port)

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

    def close_socket_client(self) -> None:
        """
        close socket client and signal emit to update ui
        :return: None
        """
        self.socket_client.close()
        self.signal_socket_client_connected.emit(False)
        self.signal_record_result.emit("Socket client closed")

    def socket_send_bytes(self, s_send: Union[bytes, str]) -> None:
        """
        send data to client
        :param s_send: Union[bytes, str]
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
            # self.signal_record_result.emit("socket client Receive value type: {}".format(type(m_receive)))
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
        clear data which receive from client
        :return: None
        """
        try:
            self.socket_client.settimeout(1)
            m_receive = self.socket_client.recv(1024)
            # self.signal_record_result.emit("Socket client Receive value type: {}".format(type(m_receive)))
            self.signal_record_result.emit("Socket client Receive value: {}".format(m_receive))
            self.signal_record_result.emit("Socket client clear {} length bytes".format(len(m_receive)))
            return m_receive

        except (ValueError, TypeError) as e:
            self.signal_record_result.emit(str(e))
            return
        # 检查socket.recv()是否超时，如果超时则向调用方Raise osError错误
        except OSError:
            self.signal_record_result.emit("Socket client receive bytes timeout!")
