#!/usr/bin/python
# -*- coding: utf-8 -*-
# Date: 2018/11/5
# Autor :  zlw zly
import time
import os
import re


def ping(result):
    ping_result_write = []
    for row in result:
        if row == '':
            pass
        else:
            matchObj = re.search(
                r'.* rate is (.*?) .*max = (.*?)/(.*?)/(.*?).*', row,
                re.M | re.I)
            percent = 100 - int(matchObj.group(1))
            avg = matchObj.group(3)

            ping_result = {
                'loss': percent,
                'avg': avg,
            }
            ping_result_write.append(ping_result)

    return ping_result_write


def cpu_mem(cpu_mem_raw):
    result = {}
    cpu_reg = re.compile(r'.*?utilization.*?:\s*?(?P<cpu>\d.*?)%.*',
                         re.S | re.M)
    switch_mem_reg = re.compile(
        r'.*?Pool Total:\s*?(?P<total>\d+)\s*.*?Free:\s*?(?P<free>\d+)\s*')
    router_mem_reg = re.compile(r'.*?\((?P<used_rate>\d+)%\).*')
    firewall_mem_reg = re.compile(
        r'.*?Free memory:.*?\((?P<free_rate>\d+)%\).*')
    cpu_regMatch = cpu_reg.match(cpu_mem_raw[1])
    mem_regMatch = switch_mem_reg.match(
        cpu_mem_raw[2]) or firewall_mem_reg.match(
            cpu_mem_raw[2]) or router_mem_reg.match(cpu_mem_raw[2])
    result['cpu'] = cpu_regMatch.groupdict()['cpu']
    #print(mem_regMatch.groupdict())
    if 'used_rate' in mem_regMatch.groupdict():
        result['mem'] = 100 - (float(mem_regMatch.groupdict()['used_rate']))
    if 'free_rate' in mem_regMatch.groupdict():
        result['mem'] = float(mem_regMatch.groupdict()['free_rate'])
    if 'total' in mem_regMatch.groupdict():
        #print ('free',mem_regMatch.groupdict()['free'],'tatal',mem_regMatch.groupdict()['total'])
        result['mem'] = format(
            float(mem_regMatch.groupdict()['free']) * 100 / float(
                mem_regMatch.groupdict()['total']), "0.1f")
    #print (result['cpu'],result['mem'])
    #save_cpu_mem(device,result)
    return result


'''
解析可用接口数
interface_raw：list [1]为接口原始信息
return int 可用接口数
'''


def interface(interface_raw):
    #save_interface(device,len(re.findall("Ethernet",interface_raw[1])))
    return len(re.findall("Ethernet", interface_raw[1]))


'''
解析流量
flow_raw：list 流量原始信息
return list 处理后的流量数据 eg:[{'in': '17.0', 'out': '51.0'},{'in': '8.0', 'out': '32.0'}]
'''


def flow(flow_raw):
    results = []
    flow_reg = re.compile(
        r'''.*?input.*?\s+(?P<in>\d+?)\s+b.*?/sec.*
  .*?output.*?\s+(?P<out>\d+?)\s+b.*?/sec.*''', re.S | re.M)
    for flow_result in flow_raw:
        if not flow_result.strip():
            continue
        result = {}
        regMatch = flow_reg.match(flow_result)
        linebits = regMatch.groupdict()
        for k, v in linebits.items():
            if 'bytes' in flow_result:
                v = format(
                    float(re.findall("\d+", v)[0]) * 8 / (1024 * 1024), "0.1f")
                result[k] = v
            if 'bit' in flow_result:
                v = format(
                    float(re.findall("\d+", v)[0]) / (1024 * 1024), "0.1f")
                result[k] = v
        results.append(result)
    #save_flow(device,results)
    return results