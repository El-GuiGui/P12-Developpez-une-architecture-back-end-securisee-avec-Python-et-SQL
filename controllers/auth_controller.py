import jwt
import datetime
from models.user_model import User, Role
from sqlalchemy.orm import Session
from views.auth_view import AuthView
import config
from rich.console import Console
import os


SECRET_KEY = "epic-events-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 45


class AuthController:
    """
    Gère l'authentification des utilisateurs et la gestion des rôles.
    """

    def __init__(self, db: Session):
        """
        Initialise le contrôleur d'authentification avec la base de données et la vue associée.
        """
        self.db = db
        self.auth_view = AuthView()
        self.console = Console()
        self.token = None
        self.current_user = None

    def start(self):
        """
        Démarre le processus d'authentification avec un menu principal.
        """
        self.create_default_roles()

        while True:
            choice = self.auth_view.display_menu()

            if choice == "1":
                email, password = self.auth_view.prompt_login()
                if self.login_user(email, password):
                    self.access_data_menu()
            # elif choice == "3":
            # employee_number, full_name, email, department, role_name, password = self.auth_view.prompt_signup()
            # if self.signup_user(employee_number, full_name, email, department, role_name, password):
            # self.access_data_menu()
            elif choice == "2":
                self.console.print("[bold yellow]Exiting the application.[/bold yellow]")
                break
            else:
                self.console.print("[bold red]Invalid choice. Please try again.[/bold red]")

    def create_default_roles(self):
        """
        Crée les rôles par défaut dans la base de données s'ils n'existent pas.
        """
        roles = ["Admin", "Commercial", "Support"]
        for role_name in roles:
            role = self.db.query(Role).filter(Role.name == role_name).first()
            if not role:
                role = Role(name=role_name, description=f"{role_name} role")
                self.db.add(role)
                self.db.commit()
                self.console.print(f"[bold green]Role '{role_name}' was created/verified successfully.[/bold green]")
            else:
                self.console.print(f"[bold yellow]Everything is ok ![/bold yellow]")

    def create_access_token(self, data: dict, expires_delta: datetime.timedelta = None):
        """
        Crée un jeton d'accès JWT avec une durée d'expiration optionnelle.
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.datetime.utcnow() + expires_delta
        else:
            expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)

        # self.console.print(f"[bold yellow]Token will expire at: {expire}[/bold yellow]")

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def authenticate_user(self, email: str, password: str):
        """
        Authentifie un utilisateur en vérifiant son email et son mot de passe.
        """
        user = self.db.query(User).filter(User.email == email).first()
        if user and user.check_password(password):
            return user
        return None

    def verify_token(self, token: str):
        """
        Vérifie la validité duu token JWT.
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email = payload.get("sub")
            if email is None:
                return None
            return email
        except jwt.ExpiredSignatureError:
            self.console.print("[bold red]Token expired. You need to log in again.[/bold red]")
            self.delete_token()
            return None
        except jwt.InvalidTokenError:
            self.console.print("[bold red]Invalid token. Please log in again.[/bold red]")
            self.delete_token()
            return None

    def get_user_permissions(self, email: str):
        """
        Récupère le rôle de l'utilisateur à partir de son email.
        """
        user = self.db.query(User).filter(User.email == email).first()
        if user:
            return user.role.name
        return None

    def signup_user(self, employee_number, full_name, email, department, role_name, password):
        """
        Crée un nouvel utilisateur avec les informations fournies.
        """
        existing_user = self.db.query(User).filter(User.email == email).first()
        if existing_user:
            self.console.print(f"[bold red]User with email {email} already exists.[/bold red]")
            return None

        role = self.db.query(Role).filter(Role.name == role_name).first()
        if not role:
            self.console.print("[bold red]Role not found.[/bold red]")
            return None

        new_user = User(
            employee_number=employee_number, full_name=full_name, email=email, department=department, role=role
        )
        new_user.set_password(password)
        self.db.add(new_user)
        self.db.commit()
        self.console.print(f"[bold green]User '{full_name}' created successfully.[/bold green]")

        return new_user

    def login_user(self, email: str, password: str):
        """
        Authentifie un utilisateur et génère un jeton d'accès en cas de succès (dans un fichier texte en local).
        """
        user = self.authenticate_user(email, password)
        if user:
            access_token_expires = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = self.create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
            with open("token.txt", "w") as token_file:
                token_file.write(access_token)
            self.current_user = user
            self.token = access_token
            self.console.print("[bold green]Login successful[/bold green]")
            return access_token
        else:
            self.console.print("[bold red]Authentication failed[/bold red]")
            return None

    def is_authenticated(self):
        """
        Vérifie si un utilisateur est authentifié en validant son token.
        """
        try:
            with open("token.txt", "r") as token_file:
                self.token = token_file.read().strip()
                self.console.print("[bold cyan]Token loaded from file, verifying...[/bold cyan]")
        except FileNotFoundError:
            self.console.print("[bold red]Token file not found.[/bold red]")
            return False

        if self.token:
            email = self.verify_token(self.token)
            if email:
                self.console.print("[bold green]User authenticated.[/bold green]")
                return True
            else:
                # self.console.print("[bold red]Token expired or invalid.[/bold red]")
                self.delete_token()
                return False
        else:
            self.console.print("[bold red]No token found.[/bold red]")
        return False

    def access_data_menu(self):
        """
        Accède au menu de gestion des données après authentification.
        """
        if not self.is_authenticated():
            self.console.print("[bold red]You must be logged in to access this menu.[/bold red]")
            return

        from controllers.data_controller import DataController

        data_controller = DataController(self.db, self)
        data_controller.start()

    def delete_token(self):
        """
        Supprime le fichier contenant le token d'accès.
        """
        try:
            os.remove("token.txt")
            self.console.print("[bold yellow]Token deleted.[/bold yellow]")
        except FileNotFoundError:
            pass
