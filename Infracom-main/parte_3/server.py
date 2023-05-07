import socket
from Utils import IP_ADDRESS, PORT_NO, BUFFER_SIZE
from RdtReceiver import RdtReceiver
from RdtSender import RdtSender
from Messages import Messages
from Costumers import Costumers

class Server():
    def __init__(self):
        # Inicializa o socket do servidor e as instâncias das classes RdtReceiver, RdtSender, Messages e Costumers
        self.serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.rdt_receiver = RdtReceiver(self.serverSock)
        self.rdt_sender = RdtSender(self.serverSock)
        self.messages = Messages()
        self.costumers = Costumers()
        self.current_client = "" # Variável que guarda o ID do cliente atual
        self.addr = ()           # Endereço do cliente atual

    def register_client(self):
        # Cria um novo cliente e o adiciona à lista de clientes do restaurante
        new_costumer = {
            "ID": "",
            "table": 0,
            "personal_bill": 0, 
            "socket": self.addr, 
            "orders": {}
        }
        concat_data = []
        # Envia as mensagens para o cliente se registrar e espera pela resposta
        for msgs in self.messages.get_register_messages():
            if self.rdt_sender.is_waiting():
                self.rdt_sender.send(msgs, self.addr)

            msg, self.addr = self.serverSock.recvfrom(BUFFER_SIZE)
            seqnum, data = msg.decode().split(',')
            self.rdt_receiver.receive(self.addr, seqnum)

            concat_data.append(data)

        # Preenche os dados do novo cliente com as informações fornecidas pelo cliente
        new_costumer["table"] = concat_data[0]
        new_costumer["ID"] = concat_data[1]
        self.costumers.add_costumer(new_costumer["ID"], new_costumer)

    def show_menu(self):                     # Envia o cardápio para o cliente
        msg = self.messages.get_str_menu()
        if self.rdt_sender.is_waiting():
            self.rdt_sender.send(msg, self.addr)
        return

    def order_menu(self, client):             # Permite que o cliente faça um pedido no restaurante
        order_msg = self.messages.get_order_messages()

        while True:                           # Envia a mensagem com os itens do cardápio para o cliente e aguarda a resposta
            if self.rdt_sender.is_waiting():
                self.rdt_sender.send(order_msg["item"], self.addr)

            msg, self.addr = self.serverSock.recvfrom(BUFFER_SIZE)
            seqnum, data, _ = msg.decode().split(',')
            self.rdt_receiver.receive(self.addr, seqnum)

            # Verifica qual item do cardápio foi escolhido pelo cliente
            if data == "1" or data.lower() == "coca-cola":
                parsed_data = "1"
            elif data == "2" or data.lower() == "fanta":
                parsed_data = "2"
            elif data == "3" or data.lower() == "parmegiana":
                parsed_data = "3"
            elif data == "4" or data.lower() == "macarronada":
                parsed_data = "4"
            elif data == "5" or data.lower() == "pizza":
                parsed_data = "5"

            order = self.messages.get_menu()[parsed_data]
            self.costumers.add_order(client, order)
            print(self.costumers.get_table_sheet()[self.current_client])

            
            if self.rdt_sender.is_waiting():
                self.rdt_sender.send(order_msg["other_item"], self.addr)

            msg, self.addr = self.serverSock.recvfrom(BUFFER_SIZE)
            seqnum, data, _ = msg.decode().split(',')
            self.rdt_receiver.receive(self.addr, seqnum)

            if data.lower() == "não":
                if self.rdt_sender.is_waiting():
                    self.rdt_sender.send(order_msg["finish"], self.addr)
                return
            
    def show_bill(self, bill_type, client):
        if bill_type == "individual":
            bill = self.costumers.get_personal_bill(client)
            orders = self.costumers.get_table_sheet()[client]["orders"]
            msg = self.messages.get_bill(orders, bill, client)
        elif bill_type == "table":
            bill = self.costumers.get_table_bill()
            msg = self.messages.get_full_bill(bill, self.costumers.get_table_sheet())
        
        # Manda a conta se o servidor estiver esperando.
        if self.rdt_sender.is_waiting():
            self.rdt_sender.send(msg, self.addr)
        return
    
    def pay_bill(self, client):
        distribute = False
        personal_bill = self.costumers.get_personal_bill(client)
        table_bill = self.costumers.get_table_bill()

        message = self.messages.get_pay_bill(personal_bill, table_bill)
        if self.rdt_sender.is_waiting():
            self.rdt_sender.send(message, self.addr)  # Envia "Sua conta foi ... e a da mesa ... digite o valor a ser pago"

        while True:
            msg, self.addr = self.serverSock.recvfrom(BUFFER_SIZE)
            seqnum, data, self.current_client = msg.decode().split(',')
            self.rdt_receiver.receive(self.addr, seqnum)
            
            if float(data) > table_bill or float(data) < personal_bill:
                if self.rdt_sender.is_waiting():
                    self.rdt_sender.send(message, self.addr)
            elif float(data) > personal_bill and float(data) <= table_bill:
                message = "Você está pagando R$" + str(float(data) - personal_bill) + " a mais que sua conta\n"
                if self.rdt_sender.is_waiting():
                    self.rdt_sender.send(message, self.addr)

                message = "O valor excedente será distribuido para para os outros clientes."
                distribute = True
                if self.rdt_sender.is_waiting():
                    self.rdt_sender.send(message, self.addr)
                break
            elif float(data) == personal_bill:
                break

        message = "Deseja confirmar o pagamento? (sim ou não)"
        if self.rdt_sender.is_waiting():
            self.rdt_sender.send(message, self.addr)

        msg, self.addr = self.serverSock.recvfrom(BUFFER_SIZE)
        seqnum, data, self.current_client = msg.decode().split(',')
        self.rdt_receiver.receive(self.addr, seqnum)

        if data.lower() == "sim":
            self.costumers.pay_client_bill(client, personal_bill)
            if distribute:
                self.costumers.distribute_accumulative_bill(client, float(data) - personal_bill) # Chama a funcao que distribui o valor pago para as outras contas
            
            message = "Você pagou sua conta. Obrigado!"
            if self.rdt_sender.is_waiting():
                self.rdt_sender.send(message, self.addr)

        if data.lower() == "não":
            message = "Pagamento cancelado."
            if self.rdt_sender.is_waiting():
                self.rdt_sender.send(message, self.addr)

        return

    def check_out(self, client): 
        client_bill = self.costumers.get_table_sheet()[client]["personal_bill"]

        if client_bill > 0:
            message = "Você ainda não pagou a sua conta"   #Caso em que a conta ainda nao foi paga
            if self.rdt_sender.is_waiting():
                self.rdt_sender.send(message, self.addr)
            return False
        
        message = "Volte sempre ^^"
        if self.rdt_sender.is_waiting():
            self.rdt_sender.send(message, self.addr)
        del self.costumers.get_table_sheet()[client]
        return True

    def start(self): #Inicializacao do server
        self.serverSock.bind((IP_ADDRESS, PORT_NO))
        print("Server is connected!\n")
        while True:
            registered = False
            while True:
                msg, self.addr = self.serverSock.recvfrom(BUFFER_SIZE)
                if not registered:
                    seqnum, data = msg.decode().split(',')
                else:
                    seqnum, data, self.current_client = msg.decode().split(',')
                self.rdt_receiver.receive(self.addr, seqnum)

                if data.lower() == "chefia":
                    self.register_client()
                    print("Client registered. table_sheet:")
                    print(self.costumers.get_table_sheet())
                    registered = True
                    if self.rdt_sender.is_waiting():
                        self.rdt_sender.send(self.messages.get_pattern(), self.addr)
                elif data == "1" or data.lower() == "cardápio":
                    self.show_menu()
                elif data == "2" or data.lower() == "pedido":
                    self.order_menu(self.current_client)
                    print(self.costumers.get_table_sheet())
                elif data == "3" or data.lower() == "conta individual":
                    self.show_bill("individual", self.current_client)
                elif data == "4" or data.lower() == "conta da mesa":
                    self.show_bill("table", self.current_client)
                elif data.lower() == "pagar":
                    self.pay_bill(self.current_client)
                    print(self.costumers.get_table_sheet())
                elif data.lower() == "levantar":
                    succeed_check_out = self.check_out(self.current_client)
                    print(self.costumers.get_table_sheet())
                    if succeed_check_out:
                        break

if __name__ == "__main__":
    server = Server()
    server.start()
