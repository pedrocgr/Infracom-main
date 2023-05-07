import socket
from datetime import datetime
from RdtSender import RdtSender             
from RdtReceiver import RdtReceiver  
from Utils import IP_ADDRESS, PORT_NO, BUFFER_SIZE  # importa as constantes definidas em Utils.py

class Client:
    def __init__(self):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # cria um socket UDP
        self.rdt_sender = RdtSender(self.clientSocket)                        # inicializa o RdtSender
        self.rdt_receiver = RdtReceiver(self.clientSocket)                    # inicializa o RdtReceiver
        self.client_name = ""                                                 # inicializa o nome do cliente como uma string vazia

    def return_message(self, data):
        final_message = ""                                             # inicializa a variável final_message como uma string vazia
        time = datetime.now()                                          # obtém a hora atual
        final_message += f"<{time.hour}:{time.minute}> CINtofome: {data}"  # formata a mensagem
        return print(final_message)                                    # exibe a mensagem no console

    def registering(self):
        for i in range(2):
            if self.rdt_sender.is_waiting():                                                      # verifica se há uma mensagem a ser enviada
                response = input(f"<{datetime.now().hour}:{datetime.now().minute}> cliente: ")    # lê a entrada do usuário
                self.rdt_sender.send(response, (IP_ADDRESS, PORT_NO))                             # envia a mensagem para o servidor
                
            if i == 1:                                      # quando a segunda mensagem for enviada
                self.client_name = response                 # define o nome do cliente como a última mensagem enviada
            message, serverAddress = self.clientSocket.recvfrom(BUFFER_SIZE)  # recebe a mensagem do servidor
            seqnum, data = message.decode().split(',')       # extrai o número de sequência e o conteúdo da mensagem
            self.rdt_receiver.receive(serverAddress, seqnum)  # processa a mensagem recebida pelo RdtReceiver

            self.return_message(data)                  # exibe a mensagem no console
        return

    def handle_payment(self, necessary_response): 
        if necessary_response:                                              # se for necessário enviar uma resposta
            if self.rdt_sender.is_waiting():                                # verifica se há uma mensagem a ser enviada
                response = input(f"<{datetime.now().hour}:{datetime.now().minute}> cliente: ")  # lê a entrada do usuário
                self.rdt_sender.send(response + "," + self.client_name, (IP_ADDRESS, PORT_NO))  # envia a mensagem para o servidor

        while True:  # loop infinito
            message, serverAddress = self.clientSocket.recvfrom(BUFFER_SIZE)  # recebe a mensagem do servidor
            seqnum, data = message.decode().split(',')                        # extrai o número de sequência e o conteúdo da mensagem
            self.rdt_receiver.receive(serverAddress, seqnum)                  # processa a mensagem recebida pelo RdtReceiver

            self.return_message(data)                                                                            # exibe a mensagem no console
            if data.lower()[-8:] == "ser pago" or data.lower() == "deseja confirmar o pagamento? (sim ou não)":  # se a mensagem contém uma solicitação de pagamento
                if self.rdt_sender.is_waiting():                                                                 # verifica se há uma mensagem a
                    response = input(f"<{datetime.now().hour}:{datetime.now().minute}> cliente: ")
                    self.rdt_sender.send(response + "," + self.client_name,
                                                (IP_ADDRESS, PORT_NO))

            if data.lower() == "você pagou sua conta. obrigado!" or data.lower() == "pagamento cancelado.":
                break
        
        return
            

    def run(self):
        try:
            print("Type 'chefia' to start the service")                       # Inicia a interacao com o servidor

            while(input(f"<{datetime.now().hour}:{datetime.now().minute}> cliente: ").lower() != "chefia"):  # aguarda até que o usuário digite "chefia"
                print("Type 'chefia' to start the service")  # exibe uma mensagem no console

            if self.rdt_sender.is_waiting():                           # verifica se há uma mensagem a ser enviada
                self.rdt_sender.send("chefia", (IP_ADDRESS, PORT_NO))  # envia a mensagem para o servidor
                    
            message, serverAddress = self.clientSocket.recvfrom(BUFFER_SIZE)  # recebe a mensagem do servidor
            seqnum, data = message.decode().split(',')                        # extrai o número de sequência e o conteúdo da mensagem

            self.rdt_receiver.receive(serverAddress, seqnum)   # processa a mensagem recebida pelo RdtReceiver
            self.return_message(data)                          # exibe a mensagem no console

            self.registering()  # realiza o registro do cliente

            while True: 
                if self.rdt_sender.is_waiting():  # verifica se há uma mensagem a ser enviada
                    response = input(f"<{datetime.now().hour}:{datetime.now().minute}> cliente:")  # lê a entrada do usuário
                    self.rdt_sender.send(response + "," + self.client_name, (IP_ADDRESS, PORT_NO))  # envia a mensagem para o servidor

                message, serverAddress = self.clientSocket.recvfrom(BUFFER_SIZE)  # recebe a mensagem do servidor
                seqnum, data = message.decode().split(',')        # extrai o número de sequência e o conteúdo da mensagem
                self.rdt_receiver.receive(serverAddress, seqnum)  # processa a mensagem recebida pelo RdtReceiver
                
                self.return_message(data)                         # exibe a mensagem no console

                if response.lower() == "pagar":  # se o usuário deseja pagar
                    self.handle_payment(True)  # lida com a operação de pagamento

                if data.lower() == "volte sempre ^^":  # se a mensagem for de despedida
                    break  # sai do loop

        except KeyboardInterrupt:      # se o usuário pressionar Ctrl+C
            self.clientSocket.close()  # fecha o socket

        self.clientSocket.close()  


if __name__ == "__main__":
    client = Client()  # cria uma instância da classe Client
    client.run()  # executa o cliente
