#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Version : PyCharm
# @Time    : 2023/4/27 0:10
# @Author  : Pitt.Ding
# @File    : Pyqt_Quaternion_Euler.py
# @Description :

import math
import time


class QuaternionEuler:
    def __int__(self):
        self.lineedit_q1 = None
        self.lineedit_q2 = None
        self.lineedit_q3 = None
        self.lineedit_q4 = None
        self.lineedit_rotx = None
        self.lineedit_roty = None
        self.lineedit_rotz = None
        self.lineedit_quaternion_euler = None
        self.lineedit_euler_quaternion = None
        self.textedit_log = None
        # self.log_fun = None

    def quaternion_to_euler(self) -> None:
        """
        calculate the quaternion to euler
        quaternion and euler values all get or return to lineedit
        :return: none
        """
        _tuple_quaternion = tuple(float(x) for x in (self.lineedit_q1.text(),
                                                     self.lineedit_q2.text(),
                                                     self.lineedit_q3.text(),
                                                     self.lineedit_q4.text()))
        q1, q2, q3, q4 = _tuple_quaternion

        _record_str = 'Request convert quaternion to euler, input is: ' + str(list(_tuple_quaternion))
        self.record_convert_result(_record_str)

        unit = q1 * q1 + q2 * q2 + q3 * q3 + q4 * q4
        test = q1 * q3 - q2 * q4
        # print("Unit: {},test: {}".format(unit, test))

        if test > 0.499 * unit:
            angle_x = 0
            angle_y = math.asin(2 * (q1 * q3 - q2 * q4))
            # print("z para1: {},para2: {}".format(2 * (q1 * q4 + q2 * q3), 1 - 2 * (q3 * q3 + q4 * q4)))
            angle_z = -2 * math.atan2(q2, q1)
            # print("angle_z: {}".format(angle_z))
        elif test < -0.499 * unit:
            angle_x = 0
            angle_y = math.asin(2 * (q1 * q3 - q2 * q4))
            # print("z para1: {},para2: {}".format(2 * (q1 * q4 + q2 * q3), 1 - 2 * (q3 * q3 + q4 * q4)))
            angle_z = 2 * math.atan2(q2, q1)
            # print("angle_z: {}".format(angle_z))
        else:
            angle_x = math.atan2(2 * (q1 * q2 + q3 * q4), 1 - 2 * (q2 * q2 + q3 * q3))
            angle_y = math.asin(2 * (q1 * q3 - q2 * q4))
            # print("z para1: {},para2: {}".format(2 * (q1 * q4 + q2 * q3), 1 - 2 * (q3 * q3 + q4 * q4)))
            angle_z = math.atan2(2 * (q1 * q4 + q2 * q3), 1 - 2 * (q3 * q3 + q4 * q4))
            # print("angle_z: {}".format(angle_z))

        angle_x = math.degrees(angle_x)
        angle_y = math.degrees(angle_y)
        angle_z = math.degrees(angle_z)

        _list_quaternion_result = list([round(x, 3) for x in [angle_x, angle_y, angle_z]])
        self.lineedit_quaternion_euler.setText(str(_list_quaternion_result))

        _record_str = 'Convert Result: ' + str(_list_quaternion_result)
        self.record_convert_result(_record_str)

    def euler_to_quaternion(self) -> None:
        """
        calculate the euler to quaternion
        euler and quaternion values all get or return to lineedit
        :return: none
        """
        _tuple_input = tuple((float(x) for x in (self.lineedit_rotx.text(),
                                                 self.lineedit_roty.text(),
                                                 self.lineedit_rotz.text())))

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
        self.lineedit_euler_quaternion.setText(str(_list_euler_result))

        _record_str = 'Convert Result: ' + str(_list_euler_result)
        self.record_convert_result(_record_str)

    def clear_quaternion_input(self):
        """
        clear the quaternion lineedit values
        :return: none
        """
        self.lineedit_q1.setText(str(0.0))
        self.lineedit_q2.setText(str(0.0))
        self.lineedit_q3.setText(str(0.0))
        self.lineedit_q4.setText(str(0.0))
        self.lineedit_quaternion_euler.setText('')

    def clear_euler_input(self):
        """
        clear the euler lineedit values
        :return: none
        """
        self.lineedit_rotx.setText(str(0.0))
        self.lineedit_rotx.setText(str(0.0))
        self.lineedit_rotx.setText(str(0.0))
        self.lineedit_euler_quaternion.setText('')

    def record_convert_result(self, str_record: str):
        """
        write record and date to textedit
        :param str_record: string that need to write
        :return: none
        """
        _str_time = time.strftime('%Y-%m-%d: %H:%M:%S ', time.localtime())
        self.textedit_log.append(_str_time + str_record)

    def copy_quaternion_result(self):
        """
        copy quaternion result form lineedit
        :return: none
        """
        self.lineedit_quaternion_euler.selectAll()
        self.lineedit_quaternion_euler.copy()
        self.lineedit_quaternion_euler.deselect()

    def copy_euler_result(self):
        """
        copy euler result from lineedit
        :return: none
        """
        self.lineedit_euler_quaternion.selectAll()
        self.lineedit_euler_quaternion.copy()
        self.lineedit_euler_quaternion.deselect()
