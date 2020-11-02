#!/usr/bin/python3

import socket
import os
import json
import math
import threading
import time
import sys


porta = 55151
enlaces =[]
rota_otima = []

cmds = (
    "add <ip> <weight>",
    "del <ip>",
    "exit"
)

class RoteadorVirtual:
    def __init__(self,ip,periodo):
        self.rotVizinho = ()
        self.cosnt_time = 4 * periodo
        self.rotas = {}
        self.rotaUpdate = {}
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[log] -- binding to ip {ip} - port {porta}")
        self.sock.bind((ip,porta))
        self.periodo = periodo

    def __del__(self):
        print('[log] -- Deletando o Roteador')
        self.sock.close()

    def recebeUpdate(self,ipDest):
        '''
        Percorre dicionário IP e faz update de pesos
        '''
        for ip in self.rotaUpdate.keys():
            if self.rotas[ip][0] > self.rotaUpdate[ip][0]:
                self.rotas[ip] = (self.rotaUpdate[ip][0],ipDest,time.time())
        pass

    def enviaUpdate(self):
        '''
        Envia mensagem do tipo update para os roteadores vizinhos
        '''
        for ip in self.rota.keys():
            if (self.rotas[ip][2] - time.time()) > self.cosnt_time:
                self.rotas.pop(ip)
                
        for ipEnv in self.rotVizinho():
            rotasEnv = split_horizon(ip)
            self.sock.sendto(rotasEnv,(ipEnv,porta))
        pass

    def enviaMsg(self,data):
        '''
        Envia mensagens
        '''
        msg = json.dump(data)
        destIP = calculaRota(data['destination'])
        self.sock.sendto(msg,(destIP,porta))

    def resolveMsg(self,msgJson):
        '''
        Trata mensagens
        '''
        mensagem = json.load(msgJson)
        if mensagem['type'] == 'data':
            if mensagem['destination'] == self.sock.getsockname():
                print("Mensagem de {}, payload:\n{}".format(mensagem['source'],mensagem['payload']))
            else:
                self.enviaMsg(mensagem)
        if mensagem['type'] == 'trace':
            self.trace(mensagem)

    def recvMsg(self):
        '''
        Recebe a mensagem JSON pelo socket
        '''
        self.sock.listen()
        conn, addr = self.sock.accept()
        with conn:
            print("[log] -- Receiving message from {}".format(addr))
            data = conn.recv(1024)
            if not conn.recv(2):
                print("[ERROR] -- Size of message too large")
                return -1
        return data,addr

    def trace(self,traceMsg):
        '''
        Trata as mensagens de trace
        '''
        rotIp = self.sock.getsockname()
        if traceMsg['destination'] == rotIp:
            print('[log] --- trace message received')
            mensagem['type']='data'
            mensagem['source'] = traceMsg['destination']
            mensagem['destination'] = traceMsg['source']
            mensagem['payload'] = traceMsg
            enviaMsg(mensagem)
        else:
            traceMsg['hops'].append(rotIp)
            enviaMsg(traceMsg)
        pass

    def calculaRota(self,ip):
        '''
        Calcula rota de menor peso
        '''
        otima = []
        for i in self.rotas:
            otimas_ip = [row[0] for row in otima]
            if i[0] not in otimas_ip:
                otima.append([i[0],i[1],i[2]])            
            else:
                indice = otimas_ip.index(i[0])
                if int(i[2]) <= int(otima[indice][2]):
                    otima[indice][1] = i[2]
        return otima
        #return '127.0.0.1'

    def addIP(self,ip,weight,nextDest):
        '''
        Adiciona um IP com o peso (custo de envio) para o banco de dados do Roteador
        '''
        print('Adding a new IP: {}, with weight {}, next destination {}'.format(ip,weight,nextDest))
        self.rotas[ip] = (weight,nextDest,time.time())
        self.rotVizinho.append(ip)

    def deleteIP(self,ip):
        '''
        Deleta um IP do banco de dados do roteador
        '''
        try:
            del self.rotas[ip]
            print('Deleting IP {}'.format(ip))
        except KeyError:
            print('IP not found in cache')

    def split_horizon(rotas,destino):   
        splitted = {}
        splitted = self.rotas
        for rota in self.rotas:
            if rota[1] == destino:
                splitted.pop(rota)
        return splitted     

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
                roteador.addIP(args[1],args[2],args[1])
            elif args[0] == 'del':
                roteador.deleteIP(args[1])
            else:
                print('Command unknown')
        except IndexError:
            print('Not enough arguments')


        

def setup(file):
    with open(file,'r') as commands:
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
        try:
            setup(sys.argv[3])
        except FileNotFoundError:
            print('[ERROR] -- file not found. \nTry using complete path')
    print("Comandos de interface disponíveis:")
    print('\n'.join(cmds))
    cmdHandler = threading.Thread(target=handleCmd, daemon=True, args=((roteador,))) 
    cmdHandler.start()
    cmdHandler.join()
    pass

#Teste