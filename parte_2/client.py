import socket
from RdtSender import RdtSender
from RdtReceiver import RdtReceiver
from Utils import IP_ADDRESS, PORT_NO, BUFFER_SIZE

class Client:
    def __init__(self):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.rdt_sender = RdtSender(self.clientSocket)
        self.rdt_receiver = RdtReceiver(self.clientSocket)

    def run(self):
        print("Client is connected!\n")

        for i in range(2):
            if self.rdt_sender.is_waiting():
                print("New package being sent to server, using RDT protocol...")
                self.rdt_sender.send("Message from client",
                                     (IP_ADDRESS, PORT_NO))

            print("Waiting for message from server...")
            message, serverAddress = self.clientSocket.recvfrom(BUFFER_SIZE)
            seqnum, _ = message.decode().split(',')
            print("Message received from server, using RDT protocol...")
            self.rdt_receiver.receive(serverAddress, seqnum)

            print("\n\n")

        self.clientSocket.close()


if __name__ == "__main__":
    client = Client()
    client.run()
