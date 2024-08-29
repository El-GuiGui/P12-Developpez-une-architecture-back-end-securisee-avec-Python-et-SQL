from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table


class DataView:
    def __init__(self):
        self.console = Console()

    def display_data_menu(self):
        self.console.rule("[bold green]Epic Events Administration[/bold green]")
        self.console.rule(
            "[bold green]OK[/bold green] - [bold yellow]Information Message[/bold yellow] - [bold red]Error/Problem/Incorrect entry[/bold red]"
        )
        self.console.rule("[bold white]Data Menu :[/bold white]")
        self.console.print("[bold green]1. View Clients[/bold green]")
        self.console.print("[bold green]2. View Contracts[/bold green]")
        self.console.print("[bold green]3. View Events[/bold green]")
        self.console.print("[bold green]4. Return to Main Menu[/bold green]")
        return Prompt.ask("Choose an option")

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
