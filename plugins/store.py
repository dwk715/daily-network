#!/usr/bin/python
# -*- coding: utf-8 -*-
# Date: 2018/11/9
# Author :  zlw dwk zly

import datetime
from pymongo import MongoClient
import copy
from .slack_bot import dn_say
import traceback
from .log import log_instance

try:
    Client = MongoClient('mongodb://172.25.25.11:27017/')
    db = Client['daily_network_dev']
    collection_line = db['line']
    collection_device = db['device']
except Exception as e:
    print(e)
    dn_say(traceback.format_exc())

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

"""将ping的结果写入数据库.
    
    根据linename创建ping文档，增量更新

    Args:
        linename:  string 线路名称
        result: Dictionary 结果{'loss': float,'delay_avg': float}

"""


def ping(line_name, result):
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    loss = result['loss']
    delay = result['delay_avg']
    ping_line = copy.deepcopy(line)
    ping_line.update({
        "name": line_name,
        "type": "line",
        "loss": [],
        "delay": [],
        "flow_in_am": [],
        "flow_out_am": [],
        "flow_in_pm": [],
        "flow_out_pm": []
    })
    if not collection_line.count_documents({'name': line_name}):
        collection_line.find_one_and_update({
            'name': line_name
        }, {'$set': ping_line},
            upsert=True)

    collection_line.find_one_and_update({
        'name': line_name
    }, {'$push': {
        'loss': {
            'date': current_date,
            'loss': loss
        }
    }})

    collection_line.find_one_and_update({
        'name': line_name
    }, {'$push': {
        'delay': {
            'date': current_date,
            'delay': delay
        }
    }})


"""将flow的结果写入数据库.
    
    根据linename创建flow文档，增量更新

    Args:
        linename:  string 线路名称
        result: Dictionary 结果{'in': float,'out': float}

"""


def flow(line_name, result):
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    hour = int(datetime.datetime.now().strftime("%H"))
    flow_line = copy.deepcopy(line)
    flow_line.update({
        "name": line_name,
        "type": "line",
        "loss": [],
        "delay": [],
        "flow_in_am": [],
        "flow_out_am": [],
        "flow_in_pm": [],
        "flow_out_pm": []
    })
    if not collection_line.count_documents({'name': line_name}):
        collection_line.find_one_and_update({
            'name': line_name
        }, {'$set': flow_line},
            upsert=True)

    if hour < 12:
        flow_in_am = result['in']
        flow_out_am = result['out']
        collection_line.find_one_and_update({
            'name': line_name
        }, {
            '$push': {
                'flow_in_am': {
                    'date': current_date,
                    'flow_in_am': flow_in_am
                }
            }
        })
        collection_line.find_one_and_update({
            'name': line_name
        }, {
            '$push': {
                'flow_out_am': {
                    'date': current_date,
                    'flow_out_am': flow_out_am
                }
            }
        })
    else:
        flow_in_pm = result['in']
        flow_out_pm = result['out']
        collection_line.find_one_and_update({
            'name': line_name
        }, {
            '$push': {
                'flow_in_pm': {
                    'date': current_date,
                    'flow_in_pm': flow_in_pm
                }
            }
        })
        collection_line.find_one_and_update({
            'name': line_name
        }, {
            '$push': {
                'flow_out_pm': {
                    'date': current_date,
                    'flow_out_pm': flow_out_pm
                }
            }
        })


"""将interface的结果写入数据库.
    
    根据linename创建interface文档，增量更新

    Args:
        linename:  string 线路名称
        result: Dictionary 结果{'total': float,'aviable': float}

"""


def interface(device_name, result):
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    total = result['total']
    aviliable = result['aviable']
    interface_device = copy.deepcopy(device)
    interface_device.update({
        "name": device_name,
        "type": "device",
        "interface": [],
        "cpu": [],
        "memory": [],
    })

    if not collection_device.count_documents({'name': device_name}):
        collection_device.find_one_and_update({
            'name': device_name
        }, {'$set': interface_device},
            upsert=True)

    collection_device.find_one_and_update({
        'name': device_name
    }, {
        '$push': {
            'interface': {
                'date': current_date,
                'total': total,
                'aviliable': aviliable
            }
        }
    })


"""将cpu_mem的结果写入数据库.
    
    根据linename创建cpu_mem文档，增量更新

    Args:
        linename:  string 线路名称
        result: Dictionary 结果{'cpu': float,'mem': float}

"""


def cpu_mem(device_name, result):
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    cpu = result['cpu']
    mem = result['mem']
    cpu_men_device = copy.deepcopy(device)
    cpu_men_device.update({
        "name": device_name,
        "type": "device",
        "interface": [],
        "cpu": [],
        "memory": [],
    })
    if not collection_device.count_documents({'name': device_name}):
        collection_device.find_one_and_update({
            'name': device_name
        }, {'$set': cpu_men_device},
            upsert=True)

    collection_device.find_one_and_update({
        'name': device_name
    }, {'$push': {
        'cpu': {
            'date': current_date,
            'use': cpu
        }
    }})
    collection_device.find_one_and_update({
        'name': device_name
    }, {'$push': {
        'memory': {
            'date': current_date,
            'remain': mem
        }
    }})
