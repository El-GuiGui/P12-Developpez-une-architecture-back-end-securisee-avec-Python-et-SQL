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
        table = Table(title="Clients")
        table.add_column("Full Name", style="cyan", no_wrap=True)
        table.add_column("Email", style="green")
        table.add_column("Company", style="magenta")

        for client in clients:
            table.add_row(client.full_name, client.email, client.company_name)

        self.console.print(table)

    def display_contracts(self, contracts):
        table = Table(title="Contracts")
        table.add_column("Contract ID", style="cyan", no_wrap=True)
        table.add_column("Client ID", style="green")
        table.add_column("Total Amount", style="magenta")

        for contract in contracts:
            table.add_row(str(contract.id), str(contract.client_id), str(contract.total_amount))

        self.console.print(table)

    def display_events(self, events):
        table = Table(title="Events")
        table.add_column("Event Name", style="cyan", no_wrap=True)
        table.add_column("Location", style="green")
        table.add_column("Date Start", style="magenta")

        for event in events:
            table.add_row(event.event_name, event.location, str(event.event_date_start))

        self.console.print(table)
