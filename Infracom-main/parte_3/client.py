import socket
from datetime import datetime
from RdtSender import RdtSender
from RdtReceiver import RdtReceiver
from Utils import IP_ADDRESS, PORT_NO, BUFFER_SIZE

class Client:
    def __init__(self):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.rdt_sender = RdtSender(self.clientSocket)
        self.rdt_receiver = RdtReceiver(self.clientSocket)
        self.client_name = ""

    def return_message(self, data):
        final_message = ""
        time = datetime.now()
        final_message += f"<{time.hour}:{time.minute}> CINtofome: {data}"
        return print(final_message)

    def registering(self):
        for i in range(2):
            if self.rdt_sender.is_waiting():
                response = input(f"<{datetime.now().hour}:{datetime.now().minute}> cliente: ")
                self.rdt_sender.send(response,
                                        (IP_ADDRESS, PORT_NO))
                
            if i == 1:
                self.client_name = response
            message, serverAddress = self.clientSocket.recvfrom(BUFFER_SIZE)
            seqnum, data = message.decode().split(',')
            self.rdt_receiver.receive(serverAddress, seqnum)

            self.return_message(data)
        return

    def handle_payment(self, necessary_response): 
        if necessary_response: 
            if self.rdt_sender.is_waiting():
                response = input(f"<{datetime.now().hour}:{datetime.now().minute}> cliente: ")
                self.rdt_sender.send(response + "," + self.client_name,
                                            (IP_ADDRESS, PORT_NO))

        while True:   
            message, serverAddress = self.clientSocket.recvfrom(BUFFER_SIZE)
            seqnum, data = message.decode().split(',')
            self.rdt_receiver.receive(serverAddress, seqnum)

            self.return_message(data)
            if data.lower()[-8:] == "ser pago" or data.lower() == "deseja confirmar o pagamento? (sim ou não)":
                if self.rdt_sender.is_waiting():
                    response = input(f"<{datetime.now().hour}:{datetime.now().minute}> cliente: ")
                    self.rdt_sender.send(response + "," + self.client_name,
                                                (IP_ADDRESS, PORT_NO))

            if data.lower() == "você pagou sua conta. obrigado!" or data.lower() == "pagamento cancelado.":
                break
        
        return

    def run(self):
        try:
            print("Type 'chefia' to start the service")

            while(input(f"<{datetime.now().hour}:{datetime.now().minute}> cliente: ").lower() != "chefia"):
                print("Type 'chefia' to start the service")

            if self.rdt_sender.is_waiting():
                self.rdt_sender.send("chefia",
                                    (IP_ADDRESS, PORT_NO))
                    
            message, serverAddress = self.clientSocket.recvfrom(BUFFER_SIZE)
            seqnum, data = message.decode().split(',')

            self.rdt_receiver.receive(serverAddress, seqnum)
            self.return_message(data)

            self.registering()

            while True:
                if self.rdt_sender.is_waiting():
                    response = input(f"<{datetime.now().hour}:{datetime.now().minute}> cliente:")
                    self.rdt_sender.send(response + "," + self.client_name,
                                        (IP_ADDRESS, PORT_NO))

                message, serverAddress = self.clientSocket.recvfrom(BUFFER_SIZE)
                seqnum, data = message.decode().split(',')
                self.rdt_receiver.receive(serverAddress, seqnum)
                
                self.return_message(data)

                if response.lower() == "pagar":
                    self.handle_payment(True)

                if data.lower() == "volte sempre ^^":
                    break

        except KeyboardInterrupt:
            self.clientSocket.close()

        self.clientSocket.close()


if __name__ == "__main__":
    client = Client()
    client.run()
