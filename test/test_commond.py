# -*- coding: utf-8 -*-
from netmiko import ConnectHandler
from log import logmode

logger = logmode('test.log').getlog()

cisco_device = {
        'device_type': "cisco_asa",
        'ip': '172.16.230.136',
        'username': 'esunny',
        'password': 'Esunny123',
        'port': 22,  # optional, defaults to 22
        'secret': 'esunnytrunk',  # optional, defaults to ''
        'verbose': False,  # optional, defaults to False
    }

net_connect = ConnectHandler(**cisco_device)
net_connect.enable()

commands = [
    'terminal pager 0',
    'show int g 0/2 | in 1 minute',
    'show int g 0/3 | in 1 minute',
    'terminal pager 25'
]

result = []

for cmd in commands:
    result.append(net_connect.send_command(cmd))

for i in result:
    print(i)

with open('device_info_result.txt', mode='w', encoding='utf-8') as f:
    f.writelines(result)

logger.info('end job')

net_connect.disconnect()