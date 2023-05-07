
class Messages:
    def __init__(self):
        self.register_messages = ["Digite sua mesa", "Digite seu nome"]
        self.pattern = [
            "Digite uma das opções a seguir (o número ou por extenso)",
            "1 - Cardápio\n2 - Pedido\n3 - Conta individual\n4 - Conta da mesa"     
        ]
        self.menu = {
            "1": {
                "name": "Coca-cola",
                "price": 5.00
            },
            "2": {
                "name": "Fanta",
                "price": 5.00
            },
            "3": {
                "name": "Parmegiana",
                "price": 20.00
            },
            "4": {
                "name": "Macarronada",
                "price": 15.00
            },
            "5": {
                "name": "Pizza",
                "price": 30.00
            },
        }

        self.orders = {
            "item": "Digite qual o item que gostaria (número ou por extenso)",
            "other_item": "Gostaria de mais algum item? (sim ou não)",
            "finish": "É pra já!"
        }

    def get_register_messages(self):
        return self.register_messages
    
    def get_str_menu(self):
        str_menu = "\n1 - Coca-cola (R$ 5.00)\n2 - Fanta (R$ 5.00)\n3 - Parmegiana (R$ 20.00)\n4 - Macarronada (R$ 15.00)\n5 - Pizza (R$ 30.00)"
        return str_menu
    
    def get_menu(self):
        return self.menu
    
    def get_order_messages(self):
        return self.orders
    
    def get_pattern(self):
        return self.pattern[0] + "\n" + self.pattern[1]
    
    def get_bill(self, orders, total, client):    # conta individual
        str_bill = "\n| " + client + " |\n"
        for order in orders:
            str_bill += orders[order]["name"] + " => R$ " + str(orders[order]["price"]) + "\n"

        str_bill += "-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-\n"                # A conta eh enviada pelo str_bill para ser printada
        str_bill += "Total - R$ " + str(total) + "\n" 
        str_bill += "-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-\n"                # Concatenamos a mensagem toda.
        return str_bill
    
    def get_full_bill(self, total, table_sheet):  # conta da mesa 
        str_bill = ""
        for client in table_sheet:                
            str_bill += self.get_bill(table_sheet[client]["orders"], table_sheet[client]["personal_bill"], client) # loop pegando os clientes da mesa
    
        str_bill += "\nTotal da mesa -  R$" + str(total) + "\n"
        str_bill += "-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-\n"
        return str_bill
    
    def get_pay_bill(self, personal_bill, table_bill):
        str_aux = "Sua conta foi R$ " + str(personal_bill) + " e a da mesa R$ " + str(table_bill) + " . Digite o valor a ser pago"
        return str_aux

