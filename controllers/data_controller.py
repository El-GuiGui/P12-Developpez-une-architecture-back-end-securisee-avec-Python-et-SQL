from sqlalchemy.orm import Session
from models.client_model import Client
from models.contract_model import Contract
from models.event_model import Event
from views.data_view import DataView
from controllers.auth_controller import AuthController
from rich.console import Console
from rich.prompt import Prompt


class DataController:

    def __init__(self, db: Session, auth_controller: AuthController):
        self.db = db
        self.data_view = DataView()
        self.auth_controller = auth_controller
        self.console = Console()

    def start(self):
        while True:
            role = self.auth_controller.current_user.role.name
            action = self.data_view.display_data_menu(role)

            if action == "view_clients":
                self.view_clients()
            elif action == "view_contracts":
                self.view_contracts()
            elif action == "view_events":
                self.view_events()
            elif action == "create_client":
                self.create_client()
            elif action == "create_contract":
                self.create_contract()
            elif action == "create_event":
                self.create_event()
            elif action == "update_client":
                client_id = Prompt.ask("Enter Client ID to update")
                self.update_client(client_id)
            elif action == "update_contract":
                contract_id = Prompt.ask("Enter Contract ID to update")
                self.update_contract(contract_id)
            elif action == "update_event":
                event_id = Prompt.ask("Enter Event ID to update")
                self.update_event(event_id)
            elif action == "create_collaborator":
                self.create_collaborator()
            elif action == "update_collaborator":
                collaborator_id = Prompt.ask("Enter Collaborator ID to update")
                self.update_collaborator(collaborator_id)
            elif action == "delete_collaborator":
                collaborator_id = Prompt.ask("Enter Collaborator ID to delete")
                self.delete_collaborator(collaborator_id)
            elif action == "delete_client":
                client_id = Prompt.ask("Enter Client ID to delete")
                self.delete_client(client_id)
            elif action == "delete_contract":
                contract_id = Prompt.ask("Enter Contract ID to delete")
                self.delete_contract(contract_id)
            elif action == "delete_event":
                event_id = Prompt.ask("Enter Event ID to delete")
                self.delete_event(event_id)
            elif action == "filter_events_without_support":
                self.filter_events_without_support()
            elif action == "update_any_contract":
                contract_id = Prompt.ask("Enter Contract ID to update")
                self.update_contract(contract_id)
            elif action == "update_any_event":
                event_id = Prompt.ask("Enter Event ID to update")
                self.update_event(event_id)
            elif action == "return_to_main":
                break
            else:
                self.data_view.console.print(
                    "[bold red]Invalid choice or permission denied. Please try again.[/bold red]"
                )
        else:
            self.console.print("[bold yellow]You must be logged in to view this information.[/bold yellow]")

    def view_clients(self):
        clients = self.db.query(Client).all()
        self.data_view.display_clients(clients)

    def view_contracts(self):
        contracts = self.db.query(Contract).all()
        self.data_view.display_contracts(contracts)

    def view_events(self):
        events = self.db.query(Event).all()
        self.data_view.display_events(events)

    def create_client(self):
        if self.auth_controller.current_user.role.name != "Commercial":
            self.data_view.console.print(
                "[bold red]Permission denied. Only Commercials can create clients.[/bold red]"
            )
            return

        full_name = Prompt.ask("Enter full name")
        email = Prompt.ask("Enter email")
        phone = Prompt.ask("Enter phone number")
        company_name = Prompt.ask("Enter company name")
        commercial_contact = self.auth_controller.current_user.full_name

        new_client = Client(
            full_name=full_name,
            email=email,
            phone=phone,
            company_name=company_name,
            commercial_contact=commercial_contact,
        )
        self.db.add(new_client)
        self.db.commit()
        self.data_view.console.print(f"[bold green]Client '{full_name}' created successfully.[/bold green]")

    def update_client(self, client_id):
        client = self.db.query(Client).filter_by(id=client_id).first()
        if not client:
            self.data_view.console.print("[bold red]Client not found.[/bold red]")
            return

        if (
            self.auth_controller.current_user.role.name != "Commercial"
            or client.commercial_contact != self.auth_controller.current_user.full_name
        ):
            self.data_view.console.print(
                "[bold red]Permission denied. You can only update clients you are responsible for.[/bold red]"
            )
            return

        client.full_name = Prompt.ask("Enter full name", default=client.full_name)
        client.email = Prompt.ask("Enter email", default=client.email)
        client.phone = Prompt.ask("Enter phone number", default=client.phone)
        client.company_name = Prompt.ask("Enter company name", default=client.company_name)
        client.last_contact_date = Prompt.ask("Enter last contact date", default=str(client.last_contact_date))

        self.db.commit()
        self.data_view.console.print(f"[bold green]Client '{client.full_name}' updated successfully.[/bold green]")

    def delete_client(self, client_id):
        self.data_view.console.print(
            "[bold red]Deleting clients is not allowed according to the business rules.[/bold red]"
        )

    def create_contract(self):
        if self.auth_controller.current_user.role.name != "Commercial":
            self.data_view.console.print(
                "[bold red]Permission denied. Only Commercials can create contracts.[/bold red]"
            )
            return

        client_id = Prompt.ask("Enter client ID")
        client = self.db.query(Client).filter_by(id=client_id).first()
        if not client or client.commercial_contact != self.auth_controller.current_user.full_name:
            self.data_view.console.print(
                "[bold red]Permission denied. You can only create contracts for your own clients.[/bold red]"
            )
            return

        description = Prompt.ask("Enter contract description")
        total_amount = Prompt.ask("Enter total amount")
        date_signed = Prompt.ask("Enter date signed")
        is_signed = Prompt.ask("Is the contract signed? (yes/no)") == "yes"

        new_contract = Contract(
            client_id=client_id,
            description=description,
            total_amount=total_amount,
            date_signed=date_signed,
            is_signed=is_signed,
        )
        self.db.add(new_contract)
        self.db.commit()
        self.data_view.console.print(
            f"[bold green]Contract for client ID '{client_id}' created successfully.[/bold green]"
        )

    def update_contract(self, contract_id):
        contract = self.db.query(Contract).filter_by(id=contract_id).first()
        if not contract:
            self.data_view.console.print("[bold red]Contract not found.[/bold red]")
            return

        client = self.db.query(Client).filter_by(id=contract.client_id).first()
        if (
            self.auth_controller.current_user.role.name != "Commercial"
            or client.commercial_contact != self.auth_controller.current_user.full_name
        ):
            self.data_view.console.print(
                "[bold red]Permission denied. You can only update contracts for your own clients.[/bold red]"
            )
            return

        contract.description = Prompt.ask("Enter contract description", default=contract.description)
        contract.total_amount = Prompt.ask("Enter total amount", default=str(contract.total_amount))
        contract.date_signed = Prompt.ask("Enter date signed", default=str(contract.date_signed))
        contract.is_signed = (
            Prompt.ask("Is the contract signed? (yes/no)", default="yes" if contract.is_signed else "no") == "yes"
        )

        self.db.commit()
        self.data_view.console.print(f"[bold green]Contract '{contract.id}' updated successfully.[/bold green]")

    def delete_contract(self, contract_id):
        contract = self.db.query(Contract).filter_by(id=contract_id).first()
        if not contract:
            self.data_view.console.print("[bold red]Contract not found.[/bold red]")
            return

        self.db.delete(contract)
        self.db.commit()
        self.data_view.console.print(f"[bold green]Contract '{contract.id}' deleted successfully.[/bold green]")

    def create_event(self):
        if self.auth_controller.current_user.role.name != "Commercial":
            self.data_view.console.print("[bold red]Permission denied. Only Commercials can create events.[/bold red]")
            return

        contract_id = Prompt.ask("Enter contract ID")
        contract = self.db.query(Contract).filter_by(id=contract_id).first()
        client = self.db.query(Client).filter_by(id=contract.client_id).first()
        if not contract or client.commercial_contact != self.auth_controller.current_user.full_name:
            self.data_view.console.print(
                "[bold red]Permission denied. You can only create events for contracts of your own clients.[/bold red]"
            )
            return

        event_name = Prompt.ask("Enter event name")
        location = Prompt.ask("Enter event location")
        event_date_start = Prompt.ask("Enter event start date")
        event_date_end = Prompt.ask("Enter event end date")
        support_contact = Prompt.ask("Enter support contact name")
        status = Prompt.ask("Enter event status")

        new_event = Event(
            contract_id=contract_id,
            event_name=event_name,
            location=location,
            event_date_start=event_date_start,
            event_date_end=event_date_end,
            support_contact=support_contact,
            status=status,
        )
        self.db.add(new_event)
        self.db.commit()
        self.data_view.console.print(f"[bold green]Event '{event_name}' created successfully.[/bold green]")

    def update_event(self, event_id):
        event = self.db.query(Event).filter_by(id=event_id).first()
        if not event:
            self.data_view.console.print("[bold red]Event not found.[/bold red]")
            return

        contract = self.db.query(Contract).filter_by(id=event.contract_id).first()
        client = self.db.query(Client).filter_by(id=contract.client_id).first()
        if (
            self.auth_controller.current_user.role.name == "Commercial"
            and client.commercial_contact == self.auth_controller.current_user.full_name
        ):
            event.event_name = Prompt.ask("Enter event name", default=event.event_name)
            event.location = Prompt.ask("Enter event location", default=event.location)
            event.event_date_start = Prompt.ask("Enter event start date", default=str(event.event_date_start))
            event.event_date_end = Prompt.ask("Enter event end date", default=str(event.event_date_end))
            event.status = Prompt.ask("Enter event status", default=event.status)
        elif (
            self.auth_controller.current_user.role.name == "Support"
            and event.support_contact == self.auth_controller.current_user.full_name
        ):
            event.event_name = Prompt.ask("Enter event name", default=event.event_name)
            event.location = Prompt.ask("Enter event location", default=event.location)
            event.status = Prompt.ask("Enter event status", default=event.status)
        else:
            self.data_view.console.print(
                "[bold red]Permission denied. You can only update events you are responsible for.[/bold red]"
            )
            return

        self.db.commit()
        self.data_view.console.print(f"[bold green]Event '{event.event_name}' updated successfully.[/bold green]")

    def delete_event(self, event_id):
        event = self.db.query(Event).filter_by(id=event_id).first()
        if not event:
            self.data_view.console.print("[bold red]Event not found.[/bold red]")
            return

        self.db.delete(event)
        self.db.commit()
        self.data_view.console.print(f"[bold green]Event '{event.event_name}' deleted successfully.[/bold green]")

    def create_collaborator(self):
        """Crée un nouveau collaborateur (user) dans le système."""
        self.data_view.console.print("[bold green]Create a New Collaborator[/bold green]")
        employee_number = Prompt.ask("Enter employee number")
        full_name = Prompt.ask("Enter full name")
        email = Prompt.ask("Enter email")
        department = Prompt.ask("Enter department")
        role_name = Prompt.ask("Enter role (Admin/Commercial/Support)")
        password = Prompt.ask("Enter password", password=True)

        # Création du collaborateur
        result = self.auth_controller.signup_user(
            employee_number=employee_number,
            full_name=full_name,
            email=email,
            department=department,
            role_name=role_name,
            password=password,
        )

        if result:
            self.data_view.console.print(f"[bold green]Collaborator {full_name} created successfully![/bold green]")
        else:
            self.data_view.console.print(f"[bold red]Failed to create collaborator. Please try again.[/bold red]")

    def update_collaborator(self, collaborator_id):
        """Met à jour les informations d'un collaborateur (user)."""
        self.data_view.console.print("[bold green]Update Collaborator Information[/bold green]")

        user = self.db.query(User).filter(User.id == collaborator_id).first()
        if not user:
            self.data_view.console.print(f"[bold red]Collaborator with ID {collaborator_id} not found.[/bold red]")
            return

        full_name = Prompt.ask(f"Enter full name [{user.full_name}]") or user.full_name
        email = Prompt.ask(f"Enter email [{user.email}]") or user.email
        department = Prompt.ask(f"Enter department [{user.department}]") or user.department
        role_name = Prompt.ask(f"Enter role [{user.role.name}]") or user.role.name
        password = Prompt.ask("Enter new password (leave empty to keep current)", password=True) or None

        # Mise à jour des informations du collaborateur
        user.full_name = full_name
        user.email = email
        user.department = department
        user.role = self.db.query(Role).filter(Role.name == role_name).first()

        if password:
            user.set_password(password)

        self.db.commit()
        self.data_view.console.print(f"[bold green]Collaborator {full_name} updated successfully![/bold green]")

    def delete_collaborator(self, collaborator_id):
        """Supprime un collaborateur (user) du système."""
        self.data_view.console.print("[bold red]Delete Collaborator[/bold red]")

        user = self.db.query(User).filter(User.id == collaborator_id).first()
        if not user:
            self.data_view.console.print(f"[bold red]Collaborator with ID {collaborator_id} not found.[/bold red]")
            return

        self.db.delete(user)
        self.db.commit()
        self.data_view.console.print(f"[bold red]Collaborator {user.full_name} deleted successfully![/bold red]")
