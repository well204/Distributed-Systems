from utils import Stack
from socket import socket, AF_INET, SOCK_DGRAM

class UDPServer:
    def __init__(self, host:str, port: int):
        self.__host = host
        self.__port = port
        self.__serverSocket = socket(AF_INET, SOCK_DGRAM)
        self.__serverSocket.bind((self.__host, self.__port))
        self.__requestStack: 'Stack' = Stack()
            
    def getRequest(self): 
        data, addr = self.__serverSocket.recvfrom(1024)
        self.__requestStack.push((data, addr))
        return data, addr

    def sendResponse(self, response: str, addr):
        self.__serverSocket.sendto(response.encode('utf-8'), addr)
    
    def getRequestStack(self):
        return self.__requestStack