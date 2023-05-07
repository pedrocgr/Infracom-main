import random

class PckgLossGenerator:
    def __init__(self, loss_rate):
        self.loss_rate = loss_rate

    def is_lost(self):
        return random.random() < self.loss_rate
    
    
IP_ADDRESS = "127.0.0.1"
PORT_NO = 6789
BUFFER_SIZE = 1024
LOSS_RATE = 0.0