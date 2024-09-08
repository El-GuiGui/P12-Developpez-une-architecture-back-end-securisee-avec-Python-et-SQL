from sqlalchemy.orm import Session
from models.client_model import Client
from models.contract_model import Contract
from models.event_model import Event
from views.data_view import DataView
from models.user_model import User, Role
from controllers.auth_controller import AuthController
from rich.console import Console
from rich.prompt import Prompt
import sentry_sdk


class DataController:
    """
    Gère les opérations sur les données liées aux clients, contrats et événements.
    """

    def __init__(self, db: Session, auth_controller: AuthController):
        """
        Initialise le contrôleur de données avec la base de données et le contrôleur d'authentification.
        """
        self.db = db
        self.data_view = DataView()
        self.auth_controller = auth_controller
        self.console = Console()

    def start(self):
        """
        Démarre le menu principal pour gérer les opérations sur les données selon les permissions de l'utilisateur
                                    (affichage du menu dynamique selon rôle.).
        """
        while True:

            role = self.auth_controller.current_user.role.name
            action = self.data_view.display_data_menu(role)

            if action == "view_clients":
                if not self.auth_controller.is_authenticated():
                    return
                self.view_clients()
            elif action == "view_contracts":
                if not self.auth_controller.is_authenticated():
                    return
                self.view_contracts()
            elif action == "view_events":
                if not self.auth_controller.is_authenticated():
                    return
                self.view_events()
            elif action == "create_client":
                if not self.auth_controller.is_authenticated():
                    return
                self.create_client()
            elif action == "create_contract":
                if not self.auth_controller.is_authenticated():
                    return
                self.create_contract()
            elif action == "create_event":
                if not self.auth_controller.is_authenticated():
                    return
                self.create_event()
            elif action == "update_client":
                if not self.auth_controller.is_authenticated():
                    return
                client_id = Prompt.ask("Enter Client ID to update")
                self.update_client(client_id)
            elif action == "update_contract":
                if not self.auth_controller.is_authenticated():
                    return
                contract_id = Prompt.ask("Enter Contract ID to update")
                self.update_contract(contract_id)
            elif action == "update_event":
                if not self.auth_controller.is_authenticated():
                    return
                event_id = Prompt.ask("Enter Event ID to update")
                self.update_event(event_id)
            elif action == "create_collaborator":
                if not self.auth_controller.is_authenticated():
                    return
                self.create_collaborator()
            elif action == "update_collaborator":
                if not self.auth_controller.is_authenticated():
                    return
                collaborator_id = Prompt.ask("Enter Collaborator ID to update")
                self.update_collaborator(collaborator_id)
            elif action == "delete_collaborator":
                if not self.auth_controller.is_authenticated():
                    return
                collaborator_id = Prompt.ask("Enter Collaborator ID to delete")
                self.delete_collaborator(collaborator_id)
            elif action == "delete_client":
                if not self.auth_controller.is_authenticated():
                    return
                client_id = Prompt.ask("Enter Client ID to delete")
                self.delete_client(client_id)
            elif action == "delete_contract":
                if not self.auth_controller.is_authenticated():
                    return
                contract_id = Prompt.ask("Enter Contract ID to delete")
                self.delete_contract(contract_id)
            elif action == "delete_event":
                if not self.auth_controller.is_authenticated():
                    return
                event_id = Prompt.ask("Enter Event ID to delete")
                self.delete_event(event_id)
            elif action == "filter_events_without_support":
                if not self.auth_controller.is_authenticated():
                    return
                self.filter_events_without_support()
            elif action == "update_any_contract":
                if not self.auth_controller.is_authenticated():
                    return
                contract_id = Prompt.ask("Enter Contract ID to update")
                self.update_contract(contract_id)
            elif action == "update_any_event":
                if not self.auth_controller.is_authenticated():
                    return
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
        """
        Affiche la liste des clients.
        """
        clients = self.db.query(Client).all()
        self.data_view.display_clients(clients)

    def view_contracts(self):
        """
        Affiche la liste des contrats.
        """
        contracts = self.db.query(Contract).all()
        self.data_view.display_contracts(contracts)

    def view_events(self):
        """
        Affiche la liste des événements.
        """
        events = self.db.query(Event).all()
        self.data_view.display_events(events)

    def create_client(self):
        """
        Crée un nouveau client, accessible uniquement aux commerciaux.
        """
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

        # Faire une demande de confirmation avant l'envoi
        confirmation = Prompt.ask("Are you sure the information is correct? (yes/no)", choices=["yes", "no"])
        # Si "no" alors stop process !
        if confirmation == "no":
            self.auth_controller.console.print("[bold yellow]Action canceled.[/bold yellow]")
            return

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
        """
        Met à jour les informations d'un client existant.
        """
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

        # Faire une demande de confirmation avant l'envoi
        confirmation = Prompt.ask("Are you sure the information is correct? (yes/no)", choices=["yes", "no"])
        # Si "no" alors stop process !
        if confirmation == "no":
            self.auth_controller.console.print("[bold yellow]Action canceled.[/bold yellow]")
            return

        self.db.commit()
        self.data_view.console.print(f"[bold green]Client '{client.full_name}' updated successfully.[/bold green]")

    def delete_client(self, client_id):
        """
        Supprime un client.
        """

        if not self.auth_controller.current_user.role.name == "Admin":
            self.auth_controller.console.print(
                "[bold red]Deleting clients is not allowed according to the business rules.[/bold red]"
            )
            return

        client = self.db.query(Client).filter_by(id=client_id).first()

        if not client:
            self.auth_controller.console.print("[bold red]Client not found.[/bold red]")
            return

        # Faire une demande de confirmation avant l'envoi
        confirmation = Prompt.ask("Are you sure you want to delete this client? (yes/no)", choices=["yes", "no"])
        # Si "no" alors stop process !
        if confirmation == "no":
            self.auth_controller.console.print("[bold yellow]Action canceled.[/bold yellow]")
            return

        # Suppression du client
        self.db.delete(client)
        self.db.commit()
        self.auth_controller.console.print(
            f"[bold green]Client with ID {client_id} deleted successfully.[/bold green]"
        )

    def create_contract(self):
        """
        Crée un nouveau contrat pour un client, accessible uniquement aux commerciaux.
        """
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

        # description = Prompt.ask("Enter contract description")
        total_amount = Prompt.ask("Enter total amount")
        amount_due = Prompt.ask("Enter amount due")
        creation_date = Prompt.ask("Enter creation date (YYYY-MM-DD)")
        is_signed = Prompt.ask("Is the contract signed? (yes/no)") == "yes"

        # Faire une demande de confirmation avant l'envoi
        confirmation = Prompt.ask("Are you sure the information is correct? (yes/no)", choices=["yes", "no"])
        # Si "no" alors stop process !
        if confirmation == "no":
            self.auth_controller.console.print("[bold yellow]Action canceled.[/bold yellow]")
            return

        new_contract = Contract(
            client_id=client_id,
            # description=description,
            commercial_contact=self.auth_controller.current_user.full_name,
            total_amount=float(total_amount),
            amount_due=float(amount_due),
            creation_date=creation_date,
            signed=is_signed,
            user_id=self.auth_controller.current_user.id,
        )

        self.db.add(new_contract)
        self.db.commit()
        self.data_view.console.print(
            f"[bold green]Contract for client ID '{client_id}' created successfully.[/bold green]"
        )

    def update_contract(self, contract_id):
        """
        Met à jour un contrat existant.
        """
        contract = self.db.query(Contract).filter_by(id=contract_id).first()
        if not contract:
            self.data_view.console.print("[bold red]Contract not found.[/bold red]")
            return

        client = self.db.query(Client).filter_by(id=contract.client_id).first()

        # Vérification si l'utilisateur est un admin
        if self.auth_controller.current_user.role.name == "Admin":
            self.data_view.console.print(
                "[bold green]Admin privileges granted. You can update any contract.[/bold green]"
            )
        else:
            # Si l'utilisateur est un commercial, vérifier s'il est autorisé à modifier le contrat de ses clients
            if client.commercial_contact != self.auth_controller.current_user.full_name:
                self.data_view.console.print(
                    "[bold red]Permission denied. You can only update contracts for your own clients.[/bold red]"
                )
                return

        new_total_amount = Prompt.ask(
            f"Enter new total amount (current: {contract.total_amount})", default=str(contract.total_amount)
        )
        new_amount_due = Prompt.ask(
            f"Enter new amount due (current: {contract.amount_due})", default=str(contract.amount_due)
        )
        new_creation_date = Prompt.ask(
            f"Enter new creation date (YYYY-MM-DD) (current: {contract.creation_date})",
            default=str(contract.creation_date),
        )
        new_signed_status = (
            Prompt.ask(f"Is the contract signed? (yes/no) (current: {'yes' if contract.signed else 'no'})") == "yes"
        )

        # Faire une demande de confirmation avant l'envoi
        confirmation = Prompt.ask("Are you sure the information is correct? (yes/no)", choices=["yes", "no"])
        # Si "no" alors stop process !
        if confirmation == "no":
            self.auth_controller.console.print("[bold yellow]Action canceled.[/bold yellow]")
            return

        contract.total_amount = float(new_total_amount)
        contract.amount_due = float(new_amount_due)
        contract.creation_date = new_creation_date
        contract.signed = new_signed_status

        self.db.commit()
        self.data_view.console.print(f"[bold green]Contract '{contract.id}' updated successfully.[/bold green]")

    def delete_contract(self, contract_id):
        """
        Supprime un contrat existant.
        """
        contract = self.db.query(Contract).filter_by(id=contract_id).first()
        if not contract:
            self.data_view.console.print("[bold red]Contract not found.[/bold red]")
            return

        # Faire une demande de confirmation avant l'envoi
        confirmation = Prompt.ask("Are you sure the information is correct? (yes/no)", choices=["yes", "no"])
        # Si "no" alors stop process !
        if confirmation == "no":
            self.auth_controller.console.print("[bold yellow]Action canceled.[/bold yellow]")
            return

        self.db.delete(contract)
        self.db.commit()
        self.data_view.console.print(f"[bold green]Contract '{contract.id}' deleted successfully.[/bold green]")

    def create_event(self):
        """
        Crée un événement lié à un contrat, accessible uniquement aux commerciaux.
        """
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
        event_date_start = Prompt.ask("Enter event start date (YYYY-MM-DD)")
        event_date_end = Prompt.ask("Enter event end date (YYYY-MM-DD)")
        location = Prompt.ask("Enter event location")
        support_contact = Prompt.ask("Enter support contact")
        attendees = Prompt.ask("Enter number of attendees")
        notes = Prompt.ask("Enter notes (optional)", default="")
        client_id = Prompt.ask("Enter client id")
        client_contact = Prompt.ask("Enter client contact")

        # Faire une demande de confirmation avant l'envoi
        confirmation = Prompt.ask("Are you sure the information is correct? (yes/no)", choices=["yes", "no"])
        # Si "no" alors stop process !
        if confirmation == "no":
            self.auth_controller.console.print("[bold yellow]Action canceled.[/bold yellow]")
            return

        new_event = Event(
            contract_id=contract_id,
            event_name=event_name,
            client_id=client_id,
            event_date_start=event_date_start,
            event_date_end=event_date_end,
            location=location,
            support_contact=support_contact,
            attendees=attendees,
            notes=notes,
            client_contact=client_contact,
            user_id=self.auth_controller.current_user.id,
        )

        self.db.add(new_event)
        self.db.commit()
        self.data_view.console.print(f"[bold green]Event '{event_name}' created successfully.[/bold green]")

    def update_event(self, event_id):
        """
        Met à jour un événement existant.
        """
        event = self.db.query(Event).filter_by(id=event_id).first()
        if not event:
            self.data_view.console.print("[bold red]Event not found.[/bold red]")
            return

        contract = self.db.query(Contract).filter_by(id=event.contract_id).first()
        client = self.db.query(Client).filter_by(id=contract.client_id).first()
        # Vérification si l'utilisateur est un admin
        if self.auth_controller.current_user.role.name == "Admin":
            event.event_name = Prompt.ask("Enter event name", default=event.event_name)
            event.location = Prompt.ask("Enter event location", default=event.location)
            event.support_contact = Prompt.ask("Enter support contact", default=event.support_contact)
            event.event_date_start = Prompt.ask("Enter event start date", default=str(event.event_date_start))
            event.event_date_end = Prompt.ask("Enter event end date", default=str(event.event_date_end))

        # Si l'utilisateur est commercial :
        elif (
            self.auth_controller.current_user.role.name == "Commercial"
            and client.commercial_contact == self.auth_controller.current_user.full_name
        ):
            event.event_name = Prompt.ask("Enter event name", default=event.event_name)
            event.location = Prompt.ask("Enter event location", default=event.location)
            event.support_contact = Prompt.ask("Enter support contact", default=event.support_contact)
            event.event_date_start = Prompt.ask("Enter event start date", default=str(event.event_date_start))
            event.event_date_end = Prompt.ask("Enter event end date", default=str(event.event_date_end))

        # Si l'utilisateur est support :
        elif (
            self.auth_controller.current_user.role.name == "Support"
            and event.support_contact == self.auth_controller.current_user.full_name
        ):
            event.event_name = Prompt.ask("Enter event name", default=event.event_name)
            event.location = Prompt.ask("Enter event location", default=event.location)

        # Si l'utilisateur n'a pas les droits requis
        else:
            self.data_view.console.print(
                "[bold red]Permission denied. You can only update events you are responsible for.[/bold red]"
            )
            return

        # Faire une demande de confirmation avant l'envoi
        confirmation = Prompt.ask("Are you sure the information is correct? (yes/no)", choices=["yes", "no"])
        # Si "no" alors stop process !
        if confirmation == "no":
            self.auth_controller.console.print("[bold yellow]Action canceled.[/bold yellow]")
            return

        self.db.commit()
        self.data_view.console.print(f"[bold green]Event '{event.event_name}' updated successfully.[/bold green]")

    def delete_event(self, event_id):
        """
        Supprime un événement existant.
        """
        event = self.db.query(Event).filter_by(id=event_id).first()
        if not event:
            self.data_view.console.print("[bold red]Event not found.[/bold red]")
            return

        # Faire une demande de confirmation avant l'envoi
        confirmation = Prompt.ask("Are you sure the information is correct? (yes/no)", choices=["yes", "no"])
        # Si "no" alors stop process !
        if confirmation == "no":
            self.auth_controller.console.print("[bold yellow]Action canceled.[/bold yellow]")
            return

        self.db.delete(event)
        self.db.commit()
        self.data_view.console.print(f"[bold green]Event '{event.event_name}' deleted successfully.[/bold green]")

    def sign_contract(self, contract_id):
        """
        Signe un contrat existant et enregistre l'événement.
        """
        try:
            contract = self.db.query(Contract).filter(Contract.id == contract_id).first()
            if contract:
                contract.signed = True
                self.db.commit()
                sentry_sdk.capture_message(
                    f"Contract {contract_id} signed by {self.auth_controller.current_user.email}", level="info"
                )
            else:
                self.data_view.console.print(f"[bold red]Contract {contract_id} not found.[/bold red]")
        except Exception as e:
            sentry_sdk.capture_exception(e)
        raise

    def create_collaborator(self):
        """
        Crée un nouveau collaborateur (utilisateur) dans le système.
        """
        try:
            self.data_view.console.print("[bold green]Create a New Collaborator[/bold green]")
            employee_number = Prompt.ask("Enter employee number")
            full_name = Prompt.ask("Enter full name")
            email = Prompt.ask("Enter email")
            department = Prompt.ask("Enter department")
            role_name = Prompt.ask("Enter role (Admin/Commercial/Support)")
            password = Prompt.ask("Enter password", password=True)

            # Faire une demande de confirmation avant l'envoi
            confirmation = Prompt.ask("Are you sure the information is correct? (yes/no)", choices=["yes", "no"])
            # Si "no" alors stop process !
            if confirmation == "no":
                self.auth_controller.console.print("[bold yellow]Action canceled.[/bold yellow]")
                return

            # Création d'un collaborateur
            result = self.auth_controller.signup_user(
                employee_number=employee_number,
                full_name=full_name,
                email=email,
                department=department,
                role_name=role_name,
                password=password,
            )

            if result:
                self.data_view.console.print(
                    f"[bold green]Collaborator {full_name} created successfully![/bold green]"
                )
            else:
                self.data_view.console.print(f"[bold red]Failed to create collaborator. Please try again.[/bold red]")
            sentry_sdk.capture_message(
                f"Collaborator {full_name} created by {self.auth_controller.current_user.email}", level="info"
            )
        except Exception as e:
            sentry_sdk.capture_exception(e)
            raise

    def update_collaborator(self, collaborator_id):
        """
        Met à jour les informations d'un collaborateur.
        """
        try:
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

            # Faire une demande de confirmation avant l'envoi
            confirmation = Prompt.ask("Are you sure the information is correct? (yes/no)", choices=["yes", "no"])
            # Si "no" alors stop process !
            if confirmation == "no":
                self.auth_controller.console.print("[bold yellow]Action canceled.[/bold yellow]")
                return

            # Mise à jour des informations d'un collaborateur
            user.full_name = full_name
            user.email = email
            user.department = department
            user.role = self.db.query(Role).filter(Role.name == role_name).first()

            if password:
                user.set_password(password)

            self.db.commit()
            self.data_view.console.print(f"[bold green]Collaborator {full_name} updated successfully![/bold green]")
            sentry_sdk.capture_message(
                f"Collaborator {user.full_name} updated by {self.auth_controller.current_user.email}", level="info"
            )
        except Exception as e:
            sentry_sdk.capture_exception(e)
            raise

    def delete_collaborator(self, collaborator_id):
        """
        Supprime un collaborateur du système.
        """
        try:
            self.data_view.console.print("[bold red]Delete Collaborator[/bold red]")

            user = self.db.query(User).filter(User.id == collaborator_id).first()
            if not user:
                self.data_view.console.print(f"[bold red]Collaborator with ID {collaborator_id} not found.[/bold red]")
                return

            # Faire une demande de confirmation avant l'envoi
            confirmation = Prompt.ask("Are you sure the information is correct? (yes/no)", choices=["yes", "no"])
            # Si "no" alors stop process !
            if confirmation == "no":
                self.auth_controller.console.print("[bold yellow]Action canceled.[/bold yellow]")
                return

            self.db.delete(user)
            self.db.commit()
            self.data_view.console.print(f"[bold red]Collaborator {user.full_name} deleted successfully![/bold red]")
            sentry_sdk.capture_message(
                f"Collaborator {user.full_name} deleted by {self.auth_controller.current_user.email}", level="info"
            )
        except Exception as e:
            sentry_sdk.capture_exception(e)
            raise

    def filter_events_without_support(self):
        """
        Filtrer les événements qui n'ont pas de contact support assigné. Accessible uniquement aux Admins.
        """
        if self.auth_controller.current_user.role.name != "Admin":
            self.data_view.console.print(
                "[bold red]Permission denied. Only Admins can filter events without support contact.[/bold red]"
            )
            return

        events_without_support = self.db.query(Event).filter(Event.support_contact == None).all()

        if not events_without_support:
            self.data_view.console.print("[bold yellow]No events found without support contact.[/bold yellow]")
        else:
            self.data_view.display_events(events_without_support)
