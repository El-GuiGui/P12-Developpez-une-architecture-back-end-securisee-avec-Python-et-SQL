from rich.console import Console
from rich.prompt import Prompt


class AuthView:
    """
    Gère l'affichage des interactions liées à l'authentification.
    """

    def __init__(self):
        self.console = Console()

    def display_menu(self):
        """
        Affiche le menu d'authentification avec les options disponibles.
        Retourne l'option choisie par l'utilisateur.
        """
        self.console.rule("[bold green]Welcome to Epic Events Administration[/bold green]")
        self.console.rule(
            "[bold green]OK[/bold green] - [bold yellow]Information Message[/bold yellow] - [bold red]Error/Problem/Incorrect entry[/bold red]"
        )
        self.console.rule("[bold white]Authentication Menu :[/bold white]")
        self.console.print("[bold green]1. Login[/bold green]")
        self.console.print("[bold green]2. Exit[/bold green]")
        # self.console.print("[bold green]3. Signup[/bold green]")
        return Prompt.ask("Choose an option")

    def prompt_login(self):
        """
        Demande à l'utilisateur de saisir son email et son mot de passe.
        """
        email = Prompt.ask("[bold green]Email[/bold green]")
        password = Prompt.ask("[bold green]Password[/bold green]", password=True)
        return email, password

    def prompt_signup(self):
        """
        Demande à l'utilisateur les informations nécessaires pour créer un compte.
        """
        employee_number = Prompt.ask("[bold green]Employee Number[/bold green]")
        full_name = Prompt.ask("[bold green]Full Name[/bold green]")
        email = Prompt.ask("[bold green]Email[/bold green]")
        department = Prompt.ask("[bold green]Department[/bold green]")
        role_name = Prompt.ask("[bold green]Role[/bold green]")
        password = Prompt.ask("[bold green]Password[/bold green]", password=True)
        return employee_number, full_name, email, department, role_name, password

    def print_success(self, message):
        """
        Affiche un message de succès en vert.
        """
        self.console.print(f"[bold green]{message}[/bold green]")

    def print_error(self, message):
        """
        Affiche un message d'erreur en rouge.
        """
        self.console.print(f"[bold red]{message}[/bold red]")

    def print_info(self, message):
        """
        Affiche un message d'information en jaune.
        """
        self.console.print(f"[bold yellow]{message}[/bold yellow]")
