#!/usr/bin/env python

import socket
import os
import json
import threading

ipDict = {}

cmds = (
    "add <ip> <weight>",
    "del <ip>"
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
    print(f'Deleting IP {ip}')
    try:
        del ipDict[ip]
    except KeyError:
        print('IP not found in cache')

def recvCmd(argv1,argv2,argv3):
    '''
    Trata os comandos recebidos pelo usuário
    '''
    if argv1 == 'add':
        addIP(argv2,argv3)
    elif argv1 == 'del':
        deleteIP(argv2)

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
    cmdInput1,cmdInput2,*cmdInput3 = input('--> ').split()
    recvCmd(cmdInput1,cmdInput2,cmdInput3)
    pass