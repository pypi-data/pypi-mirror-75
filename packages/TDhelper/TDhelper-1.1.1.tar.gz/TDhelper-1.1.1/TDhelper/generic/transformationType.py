#!/usr/bin/env python3.6
# -*- encoding: utf-8 -*-
'''
@File    :   transformationType.py
@Time    :   2020/07/30 23:34:47
@Author  :   Tang Jing 
@Version :   1.0.0
@Contact :   yeihizhi@163.com
@License :   (C)Copyright 2020
@Desc    :   类型转换
'''

# here put the import lib
import datetime
# code start
def transformation(value:any, transformationType):
    '''
    类型转换(目前仅只支持int,str,datetime,bool转换)
    - Params:
        - value: 需要转换的内容.
        - transformationType: 转换后的类型.
    '''
    try:
        if transformationType == int:
            value = int(value)
        if transformationType == str:
            if isinstance(value, datetime.datetime):
                # 日期类型转字符
                value = datetime.datetime.strftime(value, '%Y-%m-%d %H:%M:%S')
            else:
                value = str(value)
        if transformationType == datetime.datetime:
            if isinstance(value, str):
                value = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            else:
                raise Exception('value type must is str.')
        if transformationType == bool:
            if value:
                value = True
            else:
                value = False
    except Exception as e:
        raise e
    return value