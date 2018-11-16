#!/usr/bin/python
# -*- coding: utf-8 -*-
# Date: 2018/11/5
# Author :  zlw dwk zly

import os
import openpyxl
import time
from .log import log_instance
from .slack_bot import dn_say
import traceback
from pymongo import MongoClient
import datetime

'''
此模块用于将数据保存在excel文件中
读取excel/template.xlsx文件并另存为：
excel/易盛上海分公司日常巡检表_{日期}.xlsx
'''
'''
打开表格文件
return dict 包含需要保存的文件名，模板表格对象、表格最大行
'''

line_name_convert = {
    "SH_CNTC": "上海电信",
    "SH_CNUC": "上海联通",
    "HK_CNTC": "香港电信",
    "BJ_CNUC": "北京联通",
    "HK_PCCW": "电讯盈科",
    "HK_CNUC": "沪港联通",
    "SZ_CMCC": "深圳移动",
    "BJ_SX": "北京数讯",
    "SH_CNTC_MASTER": "上海电信（主）",
    "SH_CMCC_MASTER": "上海移动（主）",
    "SH_CMCC_BACKUP": "上海移动（备）",
    "SH_CNTC_BACKUP": "上海电信（备）",
}

try:
    Client = MongoClient('mongodb://172.25.25.11:27017/')
    db = Client['daily_network_dev']
    collection_line = db['line']
    collection_device = db['device']
except Exception as e:
    print(e)
    dn_say(traceback.format_exc())


def open_excel():
    filename = 'excel/易盛上海分公司日常巡检表_' + time.strftime(
        '%Y-%m-%d', time.localtime()) + '.xlsx'
    open_file = filename if os.path.exists(filename) else 'excel/template.xlsx'
    wb_info = {}
    try:
        wb = openpyxl.load_workbook(open_file)
        ws = wb.active
        if open_file == 'excel/template.xlsx':
            ws.cell(
                row=2, column=1).value = time.strftime('日期: %Y 年 %m 月 %d 日',
                                                       time.localtime())
        max = ws.max_row
        wb_info.update({"filename": filename, "wb": wb, "ws": ws, "max_row": max})
    except IOError as e:
        log_instance.critical("open file error!", e)
        dn_say(traceback.format_exc())
    return wb_info


def read_db_to_write_excel():
    wb_info = open_excel()
    print(wb_info['filename'])
    ws = wb_info['ws']
    max_row = wb_info['max_row']
    devices = collection_device.find({})
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    for row in range(5, max_row):
        device_name = ws.cell(row=row, column=1).value
        if collection_device.count_documents({'name': device_name}) == 1:
            device_info = collection_device.find_one({'name': device_name})
            if device_info['interface']:
                # 剩余接口写入
                ws.cell(row=row, column=3).value = str(device_info['interface'][-1]['available'])
#               # cpu使用率写入
                ws.cell(row=row, column=5).value = str(device_info['cpu'][-1]['use'])
                # memory剩余写入
                ws.cell(row=row, column=5).value = str(device_info['memory'][-1]['remain'])


#




        



'''
保存cpu、内存信息
device：str 设备名
cpu_mem_result：dict eg:{"cpu":40,"mem":60}
'''


def cpu_mem(device, cpu_mem_result):
    wb_info = open_excel()
    ws = wb_info["ws"]
    for work_row in range(5, wb_info['max_row']):
        if (ws.cell(row=work_row, column=1).value == device):
            ws.cell(row=work_row, column=5).value = str(cpu_mem_result['cpu'])
            ws.cell(row=work_row, column=7).value = str(cpu_mem_result['mem'])
            break
    wb_info["wb"].save(wb_info["filename"])


'''
保存可用端口数
device：str 设备名
interface_result：dict eg:{"total":40,"aviable":10}
'''


def interface(device, interface_result):
    wb_info = open_excel()
    ws = wb_info["ws"]
    for work_row in range(5, wb_info['max_row']):
        if (ws.cell(row=work_row, column=1).value == device):
            ws.cell(
                row=work_row,
                column=3).value = str(interface_result['aviable'])
            break
    wb_info["wb"].save(wb_info["filename"])


'''
根据当前时间保存流量结果
device：str 设备名
flow_result：dict eg:{'in': '17.0', 'out': '51.0'}
'''


def flow(device, flow_result):
    hour = time.strftime('%H', time.localtime())
    col = 7 if (int(hour) < 12) else 8
    wb_info = open_excel()
    ws = wb_info["ws"]
    for i in range(5, wb_info['max_row']):
        if (ws.cell(row=i, column=4).value == device
                and not ws.cell(row=i, column=col).value):
            ws.cell(row=i, column=(col + 2)).value = str(flow_result['in'])
            ws.cell(row=i, column=col).value = str(flow_result['out'])
            wb_info["wb"].save(wb_info["filename"])
            return True


'''
保存ping结果
device：str 设备名
ping_result：list 处理后的ping数据 eg {"loss":0,"avg":6}
'''


def ping(device, ping_result):
    wb_info = open_excel()
    ws = wb_info["ws"]
    for i in range(5, 32):
        if (ws.cell(row=i, column=4).value == device
                and not ws.cell(row=i, column=5).value):
            ws.cell(row=i, column=5).value = str(ping_result['loss'])
            ws.cell(row=i, column=6).value = str(ping_result['delay_avg'])
            if (float(ping_result['loss']) > 0):
                ws.cell(
                    row=i, column=5).fill = openpyxl.styles.PatternFill(
                    "solid", fgColor="FFC125")
            wb_info["wb"].save(wb_info["filename"])
            return True
