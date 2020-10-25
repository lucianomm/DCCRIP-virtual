#!/usr/bin/python3

import socket
import os
import json
import threading
import sys


porta = 55151
listaMsg = ()

cmds = (
    "add <ip> <weight>",
    "del <ip>",
    "exit"
)

listaMsg = list()

class RoteadorVirtual:
    def __init__(self,ip,periodo):
        self.ipDict = {}
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"[log] -- binding to ip {ip} - port {porta}")
        self.sock.bind((ip,porta))
        self.periodo = periodo

    def __del__(self):
        print('[log] -- Deletando o Roteador')
        self.sock.close()

    def update(self):
        '''
        Percorre dicionário IP e faz update de pesos
        '''
        pass

    def enviaMsg(self,destIP,data):
        '''
        Envia mensagens
        '''
        self.sock.sendto(data,destIP,porta)

    def resolveMsg(self,msgJson):
        '''
        Trata mensagens
        '''
        mensagem = json.load(msgJson)
        if mensagem.type == 'data':
            self.enviaMsg(self.calculaRota(mensagem.destination),mensagem)

    def recvMsg(self):
        '''
        Recebe a mensagem JSON pelo socket
        '''
        self.sock.listen()
        conn, addr = self.sock.accept()
        with conn:
            print(f"[log] -- Receiving message from {addr}")
            data = conn.recv(1024)
            if not conn.recv(2):
                print("[ERROR] -- Size of message too large")
                return -1
        return data,addr

    def trace(self):
        '''
        Trata as mensagens de trace
        '''
        pass

    def calculaRota(self,ip):
        '''
        Calcula rota de menor peso
        '''
        return '127.0.0.1'

    def addIP(self,ip,weight):
        '''
        Adiciona um IP com o peso (custo de envio) para o banco de dados do Roteador
        '''
        print(f'Adding a new IP: {ip}, with weight {weight}')
        self.ipDict[ip] = weight

    def deleteIP(self,ip):
        '''
        Deleta um IP do banco de dados do roteador
        '''
        try:
            del self.ipDict[ip]
            print(f'Deleting IP {ip}')
        except KeyError:
            print('IP not found in cache')

def handleCmd(roteador):
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
                roteador.addIP(args[1],args[2])
            elif args[0] == 'del':
                roteador.deleteIP(args[1])
            else:
                print('Command unknown')
        except IndexError:
            print('Not enough arguments')

def setup(file):
    with open(file,'w') as commands:
        for line in commands:
            os.system(line)

if __name__ == "__main__":
    try:
        roteador = RoteadorVirtual(sys.argv[1],sys.argv[2]) #Setup do Roteador
    except IndexError:
        print('[ERROR] -- Too few arguments')
        print('Initialize program with <ip> <updateTime> [SETUP FILE].txt')
        quit()
    if sys.argv[3]:
        setup(sys.argv[3])
    print("Comandos de interface disponíveis:")
    print('\n'.join(cmds))
    cmdHandler = threading.Thread(target=handleCmd, daemon=True, args=((roteador,))) 
    cmdHandler.start()
    cmdHandler.join()
    pass