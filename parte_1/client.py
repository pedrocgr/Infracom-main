import socket

UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 6789
BUFFER_SIZE = 1024

# Criando o socket UDP
clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Lendo o arquivo a ser enviado
with open("./client/file_to_send.txt", "rb") as file:
    file_data = file.read()

# Função para mandar arquivo ao servidor
def send_file(file_name):
    # enviando
    clientSock.sendto(file_name.encode(), (UDP_IP_ADDRESS, UDP_PORT_NO))

    # Ler arquivo a ser enviado
    with open("./client/" + file_name, "rb") as file:
        file_data = file.read()     

    # Manda dados do arquivo para o server (em chunks)
    for i in range(0, len(file_data), BUFFER_SIZE):
        clientSock.sendto(file_data[i:i+BUFFER_SIZE], (UDP_IP_ADDRESS, UDP_PORT_NO))
        print("waiting for ACK")
        # Esperando pelo acknowledgement do servidor
        while True:
            data, addr = clientSock.recvfrom(BUFFER_SIZE)
            if data == "ACK".encode():
                print("ACK RECEIVED")
                break

    # Comando p/ o server para parar de receber dados
    print("Sending file name to server for stop receiving data...")
    clientSock.sendto(file_name.encode(), (UDP_IP_ADDRESS, UDP_PORT_NO))

# FUNÇÃO QUE RECEBE ARQUIVO DO SERVIDOR
def receive_file():
    print("ENTROU NO RECEIVE FILE")

    # envia mensagem de conexao ao servidor
    print("Sending connect message to server...")
    connectingMessage = "CONNECTING"
    clientSock.sendto(connectingMessage.encode(), (UDP_IP_ADDRESS, UDP_PORT_NO))

    # espera a conexão
    while True:
        data, addr = clientSock.recvfrom(BUFFER_SIZE)
        print("Waiting for server to connect...")
        if data == "CONNECTED".encode():
            break
    print("Server connected. receiving file name...")

    # Recebe nome do arquivo do servidor
    file_name, addr = clientSock.recvfrom(BUFFER_SIZE)
    file_name = file_name.decode()

    print("File name received on CLIENT: " + file_name)

    # Recebe dados do arquivo do servidor e escreve no arquivo
    with open("./client/RECEIVED_" + file_name, "wb") as file:
        while True:
            print("Receiving data on CLIENT...")
            data, addr = clientSock.recvfrom(BUFFER_SIZE)

            # Para de receber dados quando comando é recebido pelo servidor
            if data == file_name.encode():
                print("BREAK")
                break

            file.write(data)
            # Mandando ACKs p/ o servidor
            clientSock.sendto("ACK".encode(), addr)
    print("File saved to disk on CLIENT.")


def client():
    print("Client started.")
    files = ["file_to_send.txt", "pdf_to_send.pdf", "img_to_send.png"]
    # files = ["file_to_send.txt"]
    clientSock.sendto(str(len(files)).encode(), (UDP_IP_ADDRESS, UDP_PORT_NO))

    # Manda e recebe todos arquivos
    for file in files:
        print("Sending file...")
        send_file(file)
        print("File sent.")

        print("Receiving file...")
        receive_file()
        print("File received.")

    # FECHANDO O SOCKET
    clientSock.close()

if __name__ == "__main__":
    client()
