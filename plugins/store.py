#!/usr/bin/python
# -*- coding: utf-8 -*-
# Date: 2018/11/9
# Autor :  zlw dwk zly

import datetime
from pymongo import MongoClient
import copy
Client = MongoClient('mongodb://172.25.25.11:27017/')
try:
    db = Client['daily_network']
except Exception as e:
    print(e)
collection_line = db['line']
collection_device = db['device']
current_date = datetime.datetime.now().strftime("%Y-%m-%d")
hour = datetime.datetime.now().strftime("%H")


line = {
    "name": None,  # name --> string 线路名称
    "type": "line",  # type --> [] 数据类型
    "loss": [],  # loss --> [] 丢包率
    "delay": [],  # delay --> [] 线路延迟
    "flow_in_am": [],  # flow_in_am --> [] 上午的下行流量
    "flow_out_am": [],  # flow_out_am --> [] 上午的上行流量
    "flow_in_pm": [],  # flow_in_pm_ --> [] 下午的上行流量
    "flow_out_pm": []  # flow_out_pm --> []下午的下行流量
}

device = {
    "name": None,  # name --> string 设备名称
    "type": "device",  # type --> [] 数据类型
    "interface": [],  # interface --> [] 包含每天的接口总数，剩余数
    "cpu": [],  # cpu --> [] cpu百分比
    "memory": [],  # memory --> [] 内存百分比
}




def ping(line_name, result):
    loss = result['loss']
    delay = result['delay_avg']
    ping_line = copy.deepcopy(line)
    ping_line.update(
        {
            "name": line_name,
            "type": "line",
            "loss": [],
            "delay": [],
            "flow_in_am": [],
            "flow_out_am": [],
            "flow_in_pm": [],
            "flow_out_pm": []
        }
    )
    if collection_line.find_one({'name':line_name}) is None:
        collection_line.find_one_and_update(
            {'name':line_name},
            {'$set':ping_line},
            upsert=True
        )
    else:
        collection_line.find_one_and_update(
            {'name': line_name},  {'$push': {
            'loss': {
                'date': current_date,
                'loss': loss
            }}},upsert=True)

        collection_line.find_one_and_update({
            'name': line_name
        }, {'$push': {
            'delay': {
                'date': current_date,
                'delay': loss
            }
        }}, upsert=True)



def flow(line_name, result):
    flow_line = copy.deepcopy(line)
    flow_line.update(
        {
            "name": line_name,
            "type": "line",
            "loss": [],
            "delay": [],
            "flow_in_am": [],
            "flow_out_am": [],
            "flow_in_pm": [],
            "flow_out_pm": []
        }
    )
    if collection_line.find_one({'name':line_name}) is None:
        collection_line.find_one_and_update(
            {'name':line_name},
            {'$set':flow_line},
            upsert=True
        )
    else:
        if hour <12 :
            flow_in_am = result['in']
            flow_out_am = result['out']
            collection_line.find_one_and_update({
                'name': line_name
            }, {'$push': {
                'flow_in_am': {
                    'date': current_date,
                    'flow_in_am': flow_in_am
                }
            }})
            collection_line.find_one_and_update({
                'name': line_name
            }, {'$push': {
                'flow_out_am': {
                    'date': current_date,
                    'flow_out_am': flow_out_am
                }
            }})
        else:
            flow_in_pm = result['in']
            flow_out_pm = result['out']
            collection_line.find_one_and_update({
                'name': line_name
            }, {'$push': {
                'flow_in_pm': {
                    'date': current_date,
                    'flow_in_pm': flow_in_pm
                }
            }})
            collection_line.find_one_and_update({
                'name': line_name
            }, {'$push': {
                'flow_out_pm': {
                    'date': current_date,
                    'flow_out_pm': flow_out_pm
                }
            }})



def interface(device_name, result):
    total = result['total']
    aviliable = result['aviable']
    interface_device = copy.deepcopy(device)
    interface_device.update(
    {
    "name": device_name,  
    "type": "device",  
    "interface": [], 
    "cpu": [],  
    "memory": [],  
    }
    )
    
    if collection_device.find_one({'name':device_name}) is None:
        collection_line.find_one_and_update(
            {'name':device_name},
            {'$set':interface_device},
            upsert=True
        )
    else:
        collection_device.find_one_and_update({
                'name': device_name
            }, {'$push': {
                'interface': {
                    'date': current_date,
                    'interface': {
                        'date':{
                            'total': total,
                            'aviliable': aviliable
                        }
                    }
                }
            }})



def cpu_men(device_name, result):
    cpu = result['cpu']
    mem = result['mem']
    cpu_men_device = copy.deepcopy(device)
    cpu_men_device.update(
    {
    "name": device_name,  
    "type": "device",  
    "interface": [], 
    "cpu": [],  
    "memory": [],  
    }
    )
    if collection_device.find_one({'name':device_name}) is None:
        collection_device.find_one_and_update(
            {'name':device_name},
            {'$set':cpu_men_device},
            upsert=True
        )
    else:
        collection_device.find_one_and_update({
                'name': device_name
            }, {'$push': {
                'cpu': {
                    'date': current_date,
                    'interface': cpu
                }
            }})
        collection_device.find_one_and_update({
                'name': device_name
            }, {'$push': {
                'mem': {
                    'date': current_date,
                    'mem': mem
                }
            }})
