class DataView:

    def display_data_menu(self):
        print("1. View Clients")
        print("2. View Contracts")
        print("3. View Events")
        print("4. Return to Main Menu")
        return input("Choose an option: ")

    def display_clients(self, clients):
        for client in clients:
            print(f"Client: {client.full_name}, Email: {client.email}, Company: {client.company_name}")

    def display_contracts(self, contracts):
        for contract in contracts:
            print(f"Contract ID: {contract.id}, Client: {contract.client_id}, Total Amount: {contract.total_amount}")

    def display_events(self, events):
        for event in events:
            print(f"Event: {event.event_name}, Location: {event.location}, Date: {event.event_date_start}")
