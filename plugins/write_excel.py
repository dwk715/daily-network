#!/usr/bin/python
# -*- coding: utf-8 -*-
# Date: 2018/11/5
# Autor :  zlw dwk zly

import os
import openpyxl
import time
from log import log_instance
'''
此模块用于将数据保存在excel文件中
读取excel/template.xlsx文件并另存为：
excel/易盛上海分公司日常巡检表_{日期}.xlsx
'''
'''
打开表格文件
return dict 包含需要保存的文件名，模板表格对象、表格最大行
'''


def open_xlsx():
    filename = 'excel/易盛上海分公司日常巡检表_' + time.strftime(
        '%Y-%m-%d', time.localtime()) + '.xlsx'
    open_file = filename if os.path.exists(filename) else 'excel/template.xlsx'
    try:
        wb = openpyxl.load_workbook(open_file)
        ws = wb.active
    except IOError as e:
        log_instance.critical("open file error!", e)
    if open_file == 'excel/template.xlsx':
        ws.cell(
            row=2, column=1).value = time.strftime('日期: %Y 年 %m 月 %d 日',
                                                   time.localtime())
    max = ws.max_row
    return ({"filename": filename, "wb": wb, "ws": ws, "max_raw": max})


'''
保存cpu、内存信息
device：str 设备名
cpu_mem_result：dict eg:{"cpu":40,"mem":60}
'''


def cpu_mem(device, cpu_mem_result):
    wb_info = open_xlsx()
    ws = wb_info["ws"]
    for work_row in range(5, wb_info['max_raw']):
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
    wb_info = open_xlsx()
    ws = wb_info["ws"]
    for work_row in range(5, wb_info['max_raw']):
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
    wb_info = open_xlsx()
    ws = wb_info["ws"]
    for i in range(5, wb_info['max_raw']):
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
    wb_info = open_xlsx()
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
