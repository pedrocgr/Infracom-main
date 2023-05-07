import socket
from Utils import IP_ADDRESS, PORT_NO, BUFFER_SIZE
from RdtReceiver import RdtReceiver
from RdtSender import RdtSender

class Server():
    def __init__(self):
        self.serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.rdt_receiver = RdtReceiver(self.serverSock)
        self.rdt_sender = RdtSender(self.serverSock)

    def start(self):
        self.serverSock.bind((IP_ADDRESS, PORT_NO))
        print("Server is connected!\n")

        for i in range(2):
            print("Waiting for message from client...")
            msg, addr = self.serverSock.recvfrom(BUFFER_SIZE)
            seqnum, _ = msg.decode().split(',')

            print("Message received from client, using RDT protocol...")
            self.rdt_receiver.receive(addr, seqnum)

            if self.rdt_sender.is_waiting():
                print("New package being sent to client, using RDT protocol...")
                self.rdt_sender.send("Message from server", addr)

            print("\n\n")


if __name__ == "__main__":
    server = Server()
    server.start()
