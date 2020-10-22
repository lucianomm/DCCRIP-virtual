#!/usr/bin/python3

import socket
import os
import json
import threading

ipDict = {}

cmds = (
    "add <ip> <weight>",
    "del <ip>",
    "exit"
)

def addIP(ip,weight):
    '''
    Adiciona um IP com o peso (custo de envio) para o banco de dados do Roteador
    '''
    print(f'Adding a new IP: {ip}, with weight {weight}')
    ipDict[ip] = weight

def deleteIP(ip):
    '''
    Deleta um IP do banco de dados do roteador
    '''
    try:
        del ipDict[ip]
        print(f'Deleting IP {ip}')
    except KeyError:
        print('IP not found in cache')

def handleCmd():
    '''
    Trata os comandos recebidos pelo usuário
    '''
    status = 'running'
    while(status!='exit'):
        args = input('--> ').split()
        try:
            if args[0] == 'exit':
                status = 'exit'
            elif args[0] == 'add':
                addIP(args[1],args[2])
            elif args[0] == 'del':
                deleteIP(args[1])
            else:
                print('Command unknown')
        except IndexError:
            print('Not enough arguments')

def messageJson(type,source,destination,payload = None):
    '''
    Recebe os parâmetros de possíveis mensagens e transforma em pacotes Json para envio padronizado
    '''
    pass

def updateRoutes():
    '''
    Atualiza as rotas conhecidas pelo roteador
    '''
    pass

def trace(msg):
    '''
    Trata a mensagem do tipo 'trace' para envio posterior
    '''
    pass

if __name__ == "__main__":
    print("Comandos de interface disponíveis:")
    print('\n'.join(cmds))
    cmdHandler = threading.Thread(target=handleCmd, daemon=True) 
    cmdHandler.start()
    pass