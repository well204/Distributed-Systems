from server import UDPServer
from server import Despachante
# from threading import Thread

# Dicionário para armazenar as mensagens e suas respostas
message_store = {}

def main():
    despachante = Despachante()
    server_socket = UDPServer('localhost', 60000)
    
    print("Servidor UDP aguardando mensagens...")

    while True:
        data, addr = server_socket.getRequest()
        decoded_data = data.decode('utf-8')

        if decoded_data in message_store:
            # Se a mensagem já está no dicionário, envia a resposta armazenada
            print(f"DUPLICADO: {decoded_data}")
            response = message_store[decoded_data]
            server_socket.sendResponse(response, addr)
        else:
            # Processa a nova mensagem e armazena no dicionário
            print(f"Recebido de {addr}: {decoded_data}")
            theResponse = despachante.invoke(data)
            message_store[decoded_data] = theResponse  # Armazena a resposta
            server_socket.sendResponse(theResponse, addr)
            print(f"Enviado para {addr}: {theResponse}")
            print()

main()