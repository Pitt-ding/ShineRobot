#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : PR
# @Time     : 2023/6/17 20:19
# @File     : ShineRobot_WebService.py
# @Project  : ShineRobot

import sys
import time
import ast
import xml.dom.minidom

import requests
from lxml import etree
from requests.auth import HTTPDigestAuth
from ws4py.client import WebSocketBaseClient
from PyQt5.QtCore import QThread, QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow
from WebService_Qthread import Ui_MainWindow
import xml.etree.ElementTree as ET


class WebServiceGetPut(QObject):
    """
    WebService Get and Put method
    """
    signal_result_log = pyqtSignal(str)
    signal_get_result = pyqtSignal(str)
    signal_post_result = pyqtSignal(str)
    signal_get_signal_result = pyqtSignal(str)

    def __init__(self, _ip: str) -> None:
        super().__init__()
        self.IP = _ip
        self.PORT = 80
        self.USER = "Default User"
        self.PASSWORD = "robotics"
        self.DIGIT_AUTH = HTTPDigestAuth(self.USER, self.PASSWORD)

    def get(self, _url: str = '/rw/iosystem/signals') -> None:
        # digit_httpauth = HTTPDigestAuth(self.USER, self.PASSWORD)
        try:
            self.result_signal_emit('Get request URL: ' + _url)
            self.get_result = requests.get(url="http://{}:{}".format(self.IP, self.PORT) + _url, auth=self.DIGIT_AUTH)
            if self.get_result.status_code == 400:
                self.result_signal_emit(f'GET request failed, status code: {self.get_result.status_code}')
            elif self.get_result.status_code == 404:
                self.result_signal_emit(f'GET request failed, status code {self.get_result.status_code}')
            else:
                # self.get_signal_emit(self.get_result.text.replace('<?xml version="1.0" encoding="UTF-8"?>', "", 1))
                self.xml_to_html(self.get_result.text)
                self.result_signal_emit('GET request success')
        except requests.exceptions.ConnectionError as e:
            self.result_signal_emit(f"{e}")

    def get_signals(self) -> None:
        _url = '/rw/iosystem/signals'
        try:
            self.result_signal_emit('Get request URL: ' + _url)
            self.get_result = requests.get(url="http://{}:{}".format(self.IP, self.PORT) + _url, auth=self.DIGIT_AUTH)
            if self.get_result.status_code == 400:
                self.result_signal_emit(f'GET request failed, status code: {self.get_result.status_code}')
            elif self.get_result.status_code == 404:
                self.result_signal_emit(f'GET request failed, status code {self.get_result.status_code}')
            else:
                # self.get_signal_emit(self.get_result.text.replace('<?xml version="1.0" encoding="UTF-8"?>', "", 1))
                self.signal_get_signal_result.emit(self.get_result.text)
                self.result_signal_emit('GET request success')
        except requests.exceptions.ConnectionError as e:
            self.result_signal_emit(f"{e}")

    def post(self, _url: str, _data_params: str, _lvalue: str) -> None:
        _pay_load = ''

        try:
            var_value = ast.literal_eval(_lvalue)
            if isinstance(var_value, bool) or isinstance(var_value, int):
                _pay_load = {'{}'.format(_data_params): '{}'.format(str(_lvalue))}
            else:
                self.result_signal_emit('Input value must bool or int')
                return
        except ValueError as e:
            self.result_signal_emit(f'Value error: {e}')
            return
        except SyntaxError as e:
            self.result_signal_emit(f'Syntax error: {e}')
            return

        # # using HTTPDigestAuth to generate digest credentials
        # self.digit_httpauth = HTTPDigestAuth(self.USER, self.PASSWORD)
        self.result_signal_emit('POST URL: ' + 'http://{}:{}'.format(self.IP, self.PORT) + _url)
        self.result_signal_emit('POST DATA: ' + str(_pay_load))

        try:
            # initial the post cookies with first post command
            result_json = requests.post(url='http://{}:{}'.format(self.IP, self.PORT) + _url,
                                        auth=self.DIGIT_AUTH, data=_pay_load)
            # judge set status by status code
            if result_json.status_code == 204:
                self.post_signal_emit(f'POST Request success: status code {result_json.status_code}')
                if result_json.text:
                    self.post_signal_emit(result_json.text)
                self.result_signal_emit('POST Request success')
            else:
                self.result_signal_emit(f'POST Request failed: status code {result_json.status_code}')
        except requests.exceptions.ConnectionError as e:
            self.result_signal_emit(f'POST request Connect error: {e}')

    def xml_to_html(self, _str_xml):
        str_xsl = """<?xml version="1.0" encoding="ISO-8859-1"?>

        <xsl:stylesheet version="1.0"
        xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:in="http://www.w3.org/1999/xhtml">

        <xsl:template match="/">
        <html>
        <head>
        <style>
        #table_style
        {
        	border-collapse:collapse;
        	text-align:left;
        	width:100%;
        	border:1px solid #98bf21;
        	cellpadding="50";
        }
        #table_style th, #table_style td
        {
        	font-size:1em;
        	border:1px solid #98bf21;
        	padding:3px 7px 2px 7px;
        }
        </style>
        </head>
        <body>
        <h2>
        Title: 
        <xsl:value-of select="in:html/in:head/in:title"/>
        <br></br>
        Request URL:
        <u>
        <xsl:value-of select="in:html/in:head/in:base/@href"/>
        </u>
        <br></br>
        </h2>
        <table id="table_style">
        <tr bgcolor="#9acd32">
        <xsl:for-each select="in:html/in:body/in:div/in:ul/in:li[1]/in:span">
        <th><xsl:value-of select="@class"/></th>
        </xsl:for-each>
        </tr>



        <xsl:for-each select="in:html/in:body/in:div/in:ul/in:li">
        <tr>
        <xsl:for-each select="./in:span">
        <td>
        <xsl:value-of select="."/>
        </td>
        </xsl:for-each>
        </tr>
        </xsl:for-each>


        </table>
        </body>
        </html>
        </xsl:template>

        </xsl:stylesheet>"""

        xml_etree = etree.fromstring(_str_xml.encode())
        xsl_etree = etree.fromstring(str_xsl.encode())

        xml_file_content = etree.tostring(xml_etree)
        xsl_file_content = etree.tostring(xsl_etree)

        xml_dom = etree.XML(xml_file_content)
        xsl_dom = etree.XML(xsl_file_content)

        trans_dom = etree.XSLT(xsl_dom)
        html_result = trans_dom(xml_dom)
        # self.get_signal_emit(html_result.__str__())
        my_xml = xml.dom.minidom.parseString(_str_xml)
        pretty_xml = my_xml.toprettyxml()
        self.get_signal_emit(pretty_xml)

    def result_signal_emit(self, _str: str) -> None:
        self.signal_result_log.emit(time.strftime('%Y-%m-%d %H:%M:%S') + ' > ' + _str)

    def get_signal_emit(self, _str) -> None:
        self.signal_get_result.emit(_str)

    def post_signal_emit(self, _str) -> None:
        self.signal_post_result.emit(time.strftime('%Y-%m-%d %H:%M:%S') + ' > ' + _str)


class WebSocket(WebSocketBaseClient):
    def received_message(self, _msg: str) -> None:
        if _msg.is_text:
            # self.return_message("Events : ")
            self.return_message(_msg.data.decode("utf-8"))
        else:
            self.return_message("Received Illegal Event " + str(_msg))

    def return_message(self, _message: str) -> None:
        name_space = '{http://www.w3.org/1999/xhtml}'
        # print(_message)
        root_xml = ET.fromstring(_message)
        # print(root_xml)
        list_signal = root_xml.findall('.//{}li'.format(name_space))
        _emit_str = ''
        for _index in list_signal:
            try:
                _signal_name = 'signal name: ' + _index.attrib['title'] + "\n"
                _emit_str = _emit_str + _signal_name
                # _signal_value = 'signal value: ' + _index.findall('./{}span'.format(name_space))[0].text + "\n"
                _signal_value = _index.findall('./{}span'.format(name_space))[0].attrib['class'] + ': ' + _index.findall('./{}span'.format(name_space))[0].text + "\n"
                _emit_str = _emit_str + _signal_value
                _signal_status = _index.findall('./{}span'.format(name_space))[1].attrib['class'] + ': ' + _index.findall('./{}span'.format(name_space))[1].text + "\n"
                _emit_str = _emit_str + _signal_status
                self.signal_emit(time.strftime('%Y-%m-%d %H:%M:%S') + ' > ' + _emit_str)
            except IndexError:
                self.signal_emit(time.strftime('%Y-%m-%d %H:%M:%S') + ' > ' + _emit_str)
            except KeyError as e:
                self.signal_emit(time.strftime('%Y-%m-%d %H:%M:%S') + ' > ' + f'{e}')

    @staticmethod
    def signal_emit(_emit_str) -> None:
        print(_emit_str)


class WebService(QObject):
    """
    通过pyqt5 qthread父类声明线程来生成线程实例
    """
    signal_recvMessage = pyqtSignal(str)
    signal_result_record = pyqtSignal(str)

    def __init__(self, _ip: str = '127.0.0.1'):
        super().__init__()
        self.IP = _ip
        self.PORT = 80
        self.USER = "Default User"
        self.PASSWORD = "robotics"
        self.DIGIT_AUTH = HTTPDigestAuth(self.USER, self.PASSWORD)
        self.SUBSCRIBE_URL = 'http://{}:{}'.format(self.IP, self.PORT) + '/subscription'
        self.LOCATION = None
        self.COOKIE = None
        self.header = None

    def subscribe(self, _pay_load: dict) -> None:
        # print('pay_load: {}'.format(dict(_pay_load)))
        self.session = requests.Session()
        try:
            self.subscribe_signal_emit('SUBSCRIBE request Pay load: ' + str(_pay_load))
            result = self.session.post(url=self.SUBSCRIBE_URL, auth=self.DIGIT_AUTH, data=_pay_load)
        except requests.exceptions.ConnectionError as e:
            self.subscribe_signal_emit(f'SUBSCRIBE request Connect error: {e}')
            return

        if result.status_code == 201:
            print('SUBSCRIBE request success')
            self.subscribe_signal_emit(f'SUBSCRIBE request success')
            self.LOCATION = result.headers['Location']
            self.COOKIE = '-http-session-={0}; ABBCX={1}'.format(result.cookies['-http-session-'], result.cookies['ABBCX'])
            self.header = [('Cookie', self.COOKIE)]
            self.web_socket = WebSocket(url=self.LOCATION,
                                        protocols=['robapi2_subscription'],
                                        headers=self.header)
            # 通过重新赋值web_socket.return_message为signal_recvMessage.emit，web_socket实例可以调用Webservice的信号输出
            self.web_socket.signal_emit = self.signal_recvMessage.emit
            self.web_socket.connect()
            self.web_socket.run()

        else:
            self.subscribe_signal_emit(f'SUBSCRIBE request failed, status code: {result.status_code}')

    def run(self) -> None:
        print('Subscribe start to run')
        self.subscribe({'resources': ['1', '2', '3', '4'],
                        '1': '/rw/panel/speedratio',
                        '1-p': '1',
                        '2': '/rw/iosystem/signals/do_ws_signal;state',
                        '2-p': '1',
                        '3': '/rw/panel/opmode',
                        '3-p': '1',
                        '4': '/rw/panel/ctrlstate',
                        '4-p': '1'
                        })

    def subscribe_signal_emit(self, _str):
        self.signal_result_record.emit(time.strftime('%Y-%m-%d %H:%M:%S') + ' > ' + _str)


class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.web_service = WebService()
        self.web_Service_thread = QThread()
        self.web_service.moveToThread(self.web_Service_thread)
        self.web_service.signal_recvMessage.connect(self.textEdit_textedit.setPlainText)
        self.pushButton_subscribe.clicked.connect(self.web_service.run)
        self.web_Service_thread.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_window = MyMainWindow()
    my_window.show()
    sys.exit(app.exec())
