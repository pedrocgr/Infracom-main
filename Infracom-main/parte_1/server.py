import socket

# Definir o endereço IP e a porta do servidor
UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 6789
BUFFER_SIZE = 1024

# Cria um socket e vincula-o à porta especificada
serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))

# Função que recebe o nome do arquivo do cliente e o conteúdo do arquivo, 
# salvando-o no diretório do servidor
def receive_file():
    # Recebe o nome do arquivo do cliente e o endereço do cliente
    file_name, addr = serverSock.recvfrom(BUFFER_SIZE)
    file_name = file_name.decode()

    # Recebe o conteúdo do arquivo do cliente e escreve-o no arquivo do servidor
    with open("./server/RECEIVED_" + file_name, "wb") as file:
        while True:
            data, addr = serverSock.recvfrom(BUFFER_SIZE)

            # Verifica se o nome do arquivo foi recebido
            if data == file_name.encode():
                break

            # Escreve o conteúdo do arquivo no arquivo do servidor
            file.write(data)
            # Envia um ACK (confirmação) de volta para o cliente
            serverSock.sendto("ACK".encode(), addr)

    print("Arquivo salvo no servidor.")

    return file_name

# Função que envia o conteúdo do arquivo para o cliente
def send_file(file_name, addr):
    # Envia o nome do arquivo para o cliente
    serverSock.sendto(file_name.encode(), addr)

    # Lê o conteúdo do arquivo a ser enviado
    with open("./server/RECEIVED_" + file_name, "rb") as file:
        file_data = file.read()

    # Envia o conteúdo do arquivo para o cliente (em pedaços)
    for i in range(0, len(file_data), BUFFER_SIZE):
        serverSock.sendto(file_data[i:i+BUFFER_SIZE], addr)

        # Espera um ACK do cliente para confirmar o recebimento dos dados
        while True:
            data, addr = serverSock.recvfrom(BUFFER_SIZE)
            if data == "ACK".encode():
                break

    # Envia um comando para o cliente indicando que os dados do arquivo acabaram
    serverSock.sendto(file_name.encode(), addr)

# Função que reenvia o conteúdo do arquivo para o cliente, caso ele seja desconectado
def resend_file(file_name, addr):
    while True:
        message, addr = serverSock.recvfrom(BUFFER_SIZE)
        message = message.decode()

        if message == "CONNECTING":
            # Envia uma mensagem de conexão para o cliente
            serverSock.sendto("CONNECTED".encode(), addr)

            # Envia o arquivo novamente para o cliente
            send_file(file_name, addr)
            print("Arquivo reenviado.")
            break

def server():
    # Imprime mensagem indicando que o servidor foi iniciado
    print("Servidor iniciado.")
    
    # Define o endereço IP e a porta do servidor
    addr = (UDP_IP_ADDRESS, UDP_PORT_NO)

    # Recebe a quantidade de arquivos a serem recebidos
    while True:
        # Recebe a mensagem do cliente com a quantidade de arquivos e o endereço do cliente
        file_amount, addr = serverSock.recvfrom(BUFFER_SIZE) 
        
        # Verifica se a mensagem recebida contém somente números (ou seja, se é um valor válido)
        if file_amount.decode().isnumeric():
            break

    # Loop para receber todos os arquivos do cliente
    for i in range(int(file_amount.decode())):

        print("Recebendo arquivo...")
        
        # Chama a função receive_file() para receber o arquivo
        file_name = receive_file()
        
        print("Arquivo recebido.")

        print("Enviando arquivo de volta...")
        
        # Chama a função resend_file() para enviar o arquivo de volta para o cliente
        resend_file(file_name, addr)
        
        print("Arquivo enviado.")
    
    # Fecha o socket do servidor
    serverSock.close()

if __name__ == "__main__":
    # Chama a função server() quando o script é executado
    server()            
