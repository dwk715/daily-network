#!/usr/bin/python
# -*- coding: utf-8 -*-
# Date: 2018/11/5
# Autor :  zlw zly
import time
import os
import re
from log import log_instance
'''
此模块用于解析网络设备执行命令后的返回结果
'''
'''
解析ping结果
result list 原始的ping操作输出
return dict 解析后的ping数据 eg {"loss":0,"avg":6}
'''


def ping(result):
    if result is None:
        log_instance.info("连接失败，请检查设备")
    else:
        for row in result:
            if row == '':
                pass
            else:
                matchObj = re.search(
                    r'.* rate is (.*?) percent\s[(](\d+)/(\d+)[)]\,.*max = (.*?)/(.*?)/(.*?).*',
                    row, re.M | re.I)
                over = float(matchObj.group(2))
                total = float(matchObj.group(3))
                percent = format((total - over) * 100 / total, "0.1f")
                # print(percent)
                avg = matchObj.group(5)
                ping_result = {
                    'loss': percent,
                    'avg': avg,
                }
    return ping_result


'''
解析cpu使用率和内存剩余率
cpu_mem_raw：list 需要包含CPU输出信息、内存输出信息
return dict 解析后的数据 eg: {"cpu":40,"mem":60}
'''


def cpu_mem(cpu_mem_raw):
    result = {"cpu": None, "mem": None}
    cpu_reg = re.compile(r'.*?utilization.*?:\s*?(?P<cpu>\d.*?)%.*',
                         re.S | re.M)
    switch_mem_reg = re.compile(
        r'.*?Pool Total:\s*?(?P<total>\d+)\s*.*?Free:\s*?(?P<free>\d+)\s*')
    router_mem_reg = re.compile(r'.*?\((?P<used_rate>\d+)%\).*')
    firewall_mem_reg = re.compile(
        r'.*?Free memory:.*?\((?P<free_rate>\d+)%\).*')
    if not cpu_mem_raw:
        log_instance.warning("raw cpu_mem is None!")
        return result
    for raw in cpu_mem_raw:
        if not raw.strip():
            continue
        if "utilization" in raw:
            cpu_match = cpu_reg.match(raw)
            if cpu_match:
                result['cpu'] = cpu_match.groupdict()['cpu']
        elif "memory" in raw:
            mem_regmatch = switch_mem_reg.match(raw) or firewall_mem_reg.match(
                raw) or router_mem_reg.match(raw)
            if mem_regmatch:
                mem_match = mem_regmatch.groupdict()
                if 'used_rate' in mem_match:
                    result['mem'] = 100 - (float(mem_match['used_rate']))
                elif 'free_rate' in mem_match:
                    result['mem'] = float(mem_match['free_rate'])
                elif 'total' in mem_match:
                    result['mem'] = format(
                        float(mem_match['free']) * 100 / float(
                            mem_match['total']), "0.1f")
    if not result["cpu"]:
        log_instance.warning("parse cpu  error!")
    if not result["mem"]:
        log_instance.warning("parse mem  error!")
    return result


'''
解析接口数
interface_raw：list 原始接口信息
return dict 解析后的数据 eg:{"total":40,"aviable":10}
'''


def interface(interface_raw):
    result = {"total": None, "aviable": None}
    if not interface_raw:
        log_instance.warning("raw interface is None!")
        return result
    for raw in interface_raw:
        if not raw.strip():
            continue
        if "up" in raw:
            result["total"] = len(re.findall("Ethernet", raw))
        else:
            result["aviable"] = len(re.findall("Ethernet", raw))
    if not result["total"]:
        log_instance.warning("parse total interface error!")
    if not result["aviable"]:
        log_instance.warning("parse aviable interface error!")
    return result


'''
解析流量
flow_raw：list 流量原始信息
return dict 解析后的流量数据 eg:{'in': '17.0', 'out': '51.0'}
'''


def flow(flow_raw):
    result = {"in": None, "out": None}
    if not flow_raw:
        log_instance.warning("raw flow is None!")
        return result
    flow_reg = re.compile(
        r'''.*?input.*?\s+(?P<in>\d+?)\s+b.*?/sec.*
  .*?output.*?\s+(?P<out>\d+?)\s+b.*?/sec.*''', re.S | re.M)
    for raw in flow_raw:
        if not raw.strip():
            continue
        flow_match = flow_reg.match(raw)
        if flow_match:
            for k, v in flow_match.groupdict().items():
                if 'bytes' in flow_result:
                    v = format(
                        float(re.findall("\d+", v)[0]) * 8 / (1024 * 1024),
                        "0.3f")
                    result[k] = v
                elif 'bit' in flow_result:
                    v = format(
                        float(re.findall("\d+", v)[0]) / (1024 * 1024), "0.3f")
                    result[k] = v
    if not result["in"]:
        log_instance.warning("parse in flow error!")
    if not result["out"]:
        log_instance.warning("parse out flow error!")
    return result
