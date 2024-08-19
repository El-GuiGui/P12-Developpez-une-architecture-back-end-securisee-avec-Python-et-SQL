from sqlalchemy.orm import Session
from models.client_model import Client
from models.contract_model import Contract
from models.event_model import Event
from views.data_view import DataView
from controllers.auth_controller import AuthController


class DataController:

    def __init__(self, db: Session, auth_controller: AuthController):
        self.db = db
        self.data_view = DataView()
        self.auth_controller = auth_controller

    def start(self):
        if self.auth_controller.is_authenticated():
            while True:
                choice = self.data_view.display_data_menu()

                if choice == "1":
                    self.view_clients()
                elif choice == "2":
                    self.view_contracts()
                elif choice == "3":
                    self.view_events()
                elif choice == "4":
                    print("Returning to main menu.")
                    break
                else:
                    print("Invalid choice. Please try again.")
        else:
            print("You must be logged in to view this information.")

    def view_clients(self):
        clients = self.db.query(Client).all()
        self.data_view.display_clients(clients)

    def view_contracts(self):
        contracts = self.db.query(Contract).all()
        self.data_view.display_contracts(contracts)

    def view_events(self):
        events = self.db.query(Event).all()
        self.data_view.display_events(events)
