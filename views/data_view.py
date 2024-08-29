from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table


class DataView:
    def __init__(self):
        self.console = Console()

    def display_data_menu(self, role):
        self.console.rule("[bold green]Epic Events Administration[/bold green]")
        self.console.rule(
            "[bold green]OK[/bold green] - [bold yellow]Information Message[/bold yellow] - [bold red]Error/Problem/Incorrect entry[/bold red]"
        )
        self.console.rule("[bold white]Data Menu :[/bold white]")

        options = {}
        num = 1

        # Options disponibles pour tous
        self.console.print(f"[bold white]{num}. View Clients[/bold white]")
        options[str(num)] = "view_clients"
        num += 1

        self.console.print(f"[bold white]{num}. View Contracts[/bold white]")
        options[str(num)] = "view_contracts"
        num += 1

        self.console.print(f"[bold white]{num}. View Events[/bold white]")
        options[str(num)] = "view_events"
        num += 1

        # Options spécifiques aux rôles
        if role == "Commercial":
            self.console.print(f"[bold white]{num}. Create Client[/bold white]")
            options[str(num)] = "create_client"
            num += 1

            self.console.print(f"[bold white]{num}. Create Contract[/bold white]")
            options[str(num)] = "create_contract"
            num += 1

            self.console.print(f"[bold white]{num}. Create Event[/bold white]")
            options[str(num)] = "create_event"
            num += 1

            self.console.print(f"[bold white]{num}. Update Client[/bold white]")
            options[str(num)] = "update_client"
            num += 1

            self.console.print(f"[bold white]{num}. Update Contract[/bold white]")
            options[str(num)] = "update_contract"
            num += 1

        if role in ["Commercial", "Support"]:
            self.console.print(f"[bold white]{num}. Update Event[/bold white]")
            options[str(num)] = "update_event"
            num += 1

        if role == "Admin":
            self.console.print(f"[bold white]{num}. Create Collaborator[/bold white]")
            options[str(num)] = "create_collaborator"
            num += 1

            self.console.print(f"[bold white]{num}. Update Collaborator[/bold white]")
            options[str(num)] = "update_collaborator"
            num += 1

            self.console.print(f"[bold white]{num}. Delete Collaborator[/bold white]")
            options[str(num)] = "delete_collaborator"
            num += 1

            self.console.print(f"[bold white]{num}. Delete Client[/bold white]")
            options[str(num)] = "delete_client"
            num += 1

            self.console.print(f"[bold white]{num}. Delete Contract[/bold white]")
            options[str(num)] = "delete_contract"
            num += 1

            self.console.print(f"[bold white]{num}. Delete Event[/bold white]")
            options[str(num)] = "delete_event"
            num += 1

            self.console.print(f"[bold white]{num}. Filter Events without Support[/bold white]")
            options[str(num)] = "filter_events_without_support"
            num += 1

            self.console.print(f"[bold white]{num}. Update Any Contract[/bold white]")
            options[str(num)] = "update_any_contract"
            num += 1

            self.console.print(f"[bold white]{num}. Update Any Event[/bold white]")
            options[str(num)] = "update_any_event"
            num += 1

        self.console.print(f"[bold white]{num}. Return to Main Menu[/bold white]")
        options[str(num)] = "return_to_main"

        choice = Prompt.ask("Choose an option")
        return options.get(choice, "invalid")

    def display_clients(self, clients):
        table = Table(title="Clients", style="white")
        table.add_column("Client ID", style="white")
        table.add_column("Full Name", style="white", no_wrap=True)
        table.add_column("Email", style="white")
        table.add_column("Phone", style="white")
        table.add_column("Company", style="white")
        table.add_column("First Contact Date", style="white")
        table.add_column("Last Contact Date", style="white")
        table.add_column("Commercial Contact", style="white")

        for client in clients:
            table.add_row(
                str(client.id),
                client.full_name,
                client.email,
                client.phone,
                client.company_name,
                str(client.first_contact_date),
                str(client.last_contact_date),
                client.commercial_contact,
            )

        self.console.print(table)

    def display_contracts(self, contracts):
        table = Table(title="Contracts", style="white")
        table.add_column("Contract ID", style="white")
        table.add_column("Client Name", style="white")
        table.add_column("Description", style="white")
        table.add_column("Total Amount", style="white")
        table.add_column("Date Signed", style="white")
        table.add_column("Is Signed", style="white")

        for contract in contracts:
            table.add_row(
                str(contract.id),
                contract.client.full_name,
                contract.description,
                str(contract.total_amount),
                str(contract.date_signed),
                "Yes" if contract.is_signed else "No",
            )

        self.console.print(table)

    def display_events(self, events):
        table = Table(title="Events", style="white")
        table.add_column("Event ID", style="white")
        table.add_column("Event Name", style="white", no_wrap=True)
        table.add_column("Location", style="white")
        table.add_column("Date Start", style="white")
        table.add_column("Date End", style="white")
        table.add_column("Client Name", style="white")
        table.add_column("Support Contact", style="white")
        table.add_column("Status", style="white")

        for event in events:
            table.add_row(
                str(event.id),
                event.event_name,
                event.location,
                str(event.event_date_start),
                str(event.event_date_end),
                event.client.full_name,
                event.support_contact,
                event.status,
            )

        self.console.print(table)
