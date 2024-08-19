class AuthView:

    def display_menu(self):
        print("1. Login")
        print("2. Signup")
        print("3. Exit")
        return input("Choose an option: ")

    def prompt_login(self):
        email = input("Email: ")
        password = input("Password: ")
        return email, password

    def prompt_signup(self):
        employee_number = input("Employee Number: ")
        full_name = input("Full Name: ")
        email = input("Email: ")
        department = input("Department: ")
        role_name = input("Role: ")
        password = input("Password: ")
        return employee_number, full_name, email, department, role_name, password
