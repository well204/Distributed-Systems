from socket import socket, AF_INET, SOCK_DGRAM

class UDPClient:
	def __init__(self, serverHost: str, serverPort: int, timeout_duration: int = 2) -> None:
		self.__clientSocket = socket(AF_INET, SOCK_DGRAM)
		self.__serverHost = serverHost
		self.__serverPort = serverPort
		self.__timeout = timeout_duration
		self.__clientSocket.settimeout(self.__timeout)

	def sendRequest(self, request: str) -> None:     
		self.__clientSocket.sendto(request.encode('utf-8'), (self.__serverHost, self.__serverPort))

	def getResponse(self):
		data, server = self.__clientSocket.recvfrom(2048)
		return data, server

	def closeConection(self) -> None:
		self.__clientSocket.close()