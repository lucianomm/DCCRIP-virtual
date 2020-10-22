import socket
import os
import json
import threading

cmds = (
    "add <ip> <weight>",
    "del <ip>"
)

def addIP(ip,weight):
    '''
    Adiciona um IP com o peso (custo de envio) para o banco de dados do Roteador
    '''
    pass

def deleteIP(ip):
    '''
    Deleta um IP do banco de dados do roteador
    '''
    pass

def recvCmd(argv1,argv2,argv3=None):
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
    pass