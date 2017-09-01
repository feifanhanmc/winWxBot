# -*- coding: utf-8 -*-
import socket
import json

config ={}

def load_config():
    with open('wx_xnr_conf.json', 'r') as f:
        return json.load(f)

def socket_client(msg):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((config['socket_host'], config['socket_port']))
        client.send(msg)
    except Exception,e:
        print e
    finally:
        client.close()

def push_msg(from_bot_id, to_group_name, m):
    msg = json.dumps({'from_bot_id': from_bot_id,'to_group_name': to_group_name, 'm': m})
    socket_client(msg)

def main():
    global config
    config = load_config()
    #目前仅支持发布文字内容
    push_msg(from_bot_id='bot_1', to_group_name='group001', m='测试 1下')

main()