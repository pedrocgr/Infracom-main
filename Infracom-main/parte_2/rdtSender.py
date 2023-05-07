import socket
from Utils import BUFFER_SIZE, LOSS_RATE, PckgLossGenerator

class RdtSender:
    def __init__(self, socket):
        self.socket = socket
        self.sequence_number = '0'
        self.waiting = True
        self.error = PckgLossGenerator(LOSS_RATE)

    def check_ack(self, ack):
        return ack == self.sequence_number

    def change_seq_num(self):
        self.sequence_number = '0' if self.sequence_number == '1' else '1'

    def send(self, chunk, address):
        self.waiting = False
        print("package is being codified...")
        pkt = self.sequence_number + "," + chunk

        while not self.waiting:
            if self.error.is_lost():
                print("Package is lost!")
            else:
                print(
                    f"Sending... Package format: ({self.sequence_number}, \"{chunk}\")")
                self.socket.sendto(pkt.encode(), address)

            self.socket.settimeout(5)

            try:
                ack, address = self.socket.recvfrom(BUFFER_SIZE)

                if self.check_ack(ack.decode()):
                    print("Correct ack received!")
                    self.socket.settimeout(None)
                    self.change_seq_num()
                    self.waiting = True
            except socket.timeout:
                print("Timeout! Resending package...")

            

    def is_waiting(self):
        return self.waiting
