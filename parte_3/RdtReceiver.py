from Utils import BUFFER_SIZE, LOSS_RATE, PckgLossGenerator

class RdtReceiver:
    def __init__(self, socket):
        self.sequence_number = '0'
        self.socket = socket
        self.error = PckgLossGenerator(LOSS_RATE)

    def check_seq_num(self, seqnum):
        # print("seqnum: ", seqnum)
        # print("self.sequence_number: ", self.sequence_number)
        return seqnum == self.sequence_number

    def change_seq_num(self):
        return '0' if self.sequence_number == '1' else '1'

    def receive(self, address, seqnum):
        while not self.check_seq_num(seqnum):
            ack = self.change_seq_num().encode()
            # print(f"Resending ack {ack.decode()} due to duplicate!")
            self.socket.sendto(ack, address)

            message, _ = self.socket.recvfrom(BUFFER_SIZE)
            seqnum, _ = message.decode().split(',')

        else:
            ack = self.sequence_number.encode()
            # print(f"Correct package, ack {ack.decode()} will be sent!")
            self.socket.sendto(ack, address)

            self.sequence_number = self.change_seq_num()
