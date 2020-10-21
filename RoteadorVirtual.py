import socket
import os
import json
import threading

cmds = (
    "add <ip> <weight>",
    "del <ip>"
)

def addIP(ip,weight):
    pass

def deleteIP(ip):
    pass

def recvCmd(argv1,argv2,argv3=None):
    if argv1 == 'add':
        addIP(argv2,argv3)
    elif argv1 == 'del':
        deleteIP(argv2)


if __name__ == "__main__":
    print("Comandos de interface disponíveis:")
    print('\n'.join(cmds))
    pass