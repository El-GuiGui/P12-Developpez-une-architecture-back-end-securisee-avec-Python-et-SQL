import jwt
import datetime
from models.user_model import User, Role
from sqlalchemy.orm import Session
from views.auth_view import AuthView
import config

SECRET_KEY = "epic-events-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 999999


class AuthController:

    def __init__(self, db: Session):
        self.db = db
        self.auth_view = AuthView()

    def start(self):
        self.create_default_roles()

        while True:
            choice = self.auth_view.display_menu()

            if choice == "1":
                email, password = self.auth_view.prompt_login()
                self.login_user(email, password)
            elif choice == "2":
                employee_number, full_name, email, department, role_name, password = self.auth_view.prompt_signup()
                self.signup_user(employee_number, full_name, email, department, role_name, password)
            elif choice == "3":
                print("Exiting the application.")
                break
            else:
                print("Invalid choice. Please try again.")

    def create_default_roles(self):
        roles = ["Admin", "Commercial", "Support"]
        for role_name in roles:
            role = self.db.query(Role).filter(Role.name == role_name).first()
            if not role:
                role = Role(name=role_name, description=f"{role_name} role")
                self.db.add(role)
                self.db.commit()
                print(f"Role '{role_name}' created successfully.")
            else:
                print(f"Role '{role_name}' already exists.")

    def create_access_token(self, data: dict, expires_delta: datetime.timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.datetime.utcnow() + expires_delta
        else:
            expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def authenticate_user(self, email: str, password: str):
        user = self.db.query(User).filter(User.email == email).first()
        if user and user.check_password(password):
            return user
        return None

    def verify_token(self, token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email = payload.get("sub")
            if email is None:
                return None
            return email
        except jwt.ExpiredSignatureError:
            print("Token expired")
            return None
        except jwt.PyJWTError:
            print("Invalid token")
            return None

    def get_user_permissions(self, email: str):
        user = self.db.query(User).filter(User.email == email).first()
        if user:
            return user.role.name
        return None

    def signup_user(self, employee_number, full_name, email, department, role_name, password):
        existing_user = self.db.query(User).filter(User.email == email).first()
        if existing_user:
            print(f"User with email {email} already exists.")
            return None

        role = self.db.query(Role).filter(Role.name == role_name).first()
        if not role:
            print("Role not found.")
            return None

        new_user = User(
            employee_number=employee_number, full_name=full_name, email=email, department=department, role=role
        )
        new_user.set_password(password)
        self.db.add(new_user)
        self.db.commit()
        print(f"User '{full_name}' created successfully.")

        return new_user

    def login_user(self, email: str, password: str):
        user = self.authenticate_user(email, password)
        if user:
            access_token_expires = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = self.create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
            with open("token.txt", "w") as token_file:
                token_file.write(access_token)
            print("Login successful")
            return access_token
        else:
            print("Authentication failed")
            return None
