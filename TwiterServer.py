from server import UDPServer
from server import Despachante
# from threading import Thread

def main():
    despachante = Despachante()
    server_socket = UDPServer('localhost', 60000)

    # Vincula o socket a um endereço e porta
    print("Servidor UDP aguardando mensagens...")

    while True:
        # Recebe dados do cliente
        lastStackTop = None
        if(not server_socket.getRequestStack().is_empty()):
            lastStackTop = server_socket.getRequestStack().peek()
        data, addr = server_socket.getRequest()
        
        if(lastStackTop == (data, addr)):
            print('DUPLICADO: ', end='')
            
        print(f"Recebido de {addr}: {data.decode('utf-8')}")
        print()
        theResponse = despachante.invoke(data)
        if (server_socket.getMaxRequest() > 1):
            server_socket.sendResponse(theResponse,addr)
            print(f"Enviado para {addr}: {theResponse}")
            print()
		
# Thread(target=main()).start()
main()