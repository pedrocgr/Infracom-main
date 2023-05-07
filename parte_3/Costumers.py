class Costumers:
    def __init__(self):
        self.table_sheet = {}

    def get_table_sheet(self):
        return self.table_sheet
    
    def add_costumer(self, index, costumer):                             # Aqui criamos o dicionários e gerenciamos clientes e usamos isso para
        self.table_sheet[index] = costumer                               # cada necessidade (conta, adicionar pedido, pegar conta...)

    def add_order(self, client, order):
        count_orders = len(self.table_sheet[client]["orders"])
        self.table_sheet[client]["orders"][str(count_orders)] = order
        self.table_sheet[client]["personal_bill"] += order["price"]

    def get_personal_bill(self, client):
        return self.table_sheet[client]["personal_bill"]
    
    def get_table_bill(self):
        total = 0
        for costumers in self.table_sheet:                            # Para pegar a conta total da mesa, pegamos todos os clientes
            total += self.table_sheet[costumers]["personal_bill"]
        return total
    
    def distribute_accumulative_bill(self, client, bill):            # Metodo para distribuir o dinheiro pago a mais para os outros clientes
        count = len(self.table_sheet) - 1
        for costumer in self.table_sheet:
            if costumer != client and self.table_sheet[costumer]["personal_bill"] >= bill/count:
                self.table_sheet[costumer]["personal_bill"] -= bill/count

    def pay_client_bill(self, client, bill):
        self.table_sheet[client]["orders"] = {}
        self.table_sheet[client]["personal_bill"] -= bill