import socket
import hashlib

HOST = "127.0.0.1"
PORT = 5555

logged_in_account = None


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def send(msg):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    client.send(msg.encode())
    response = client.recv(4096).decode()

    client.close()
    return response


def menu():
    print("\n BANK SYSTEM")
    print("1. Create account")
    print("2. Login")
    print("3. Check balance")
    print("4. Exit")


def create_account():
    name = input("Name: ")
    surname = input("Surname: ")
    pesel = input("PESEL: ")
    acc = input("Account number: ")

    password = input("Password: ")
    pwd_hash = hash_password(password)

    msg = f"CREATE|{name}|{surname}|{pesel}|{acc}|{pwd_hash}"
    print(send(msg))


def login():
    global logged_in_account

    acc = input("Account number: ")
    password = input("Password: ")

    pwd_hash = hash_password(password)

    msg = f"LOGIN|{acc}|{pwd_hash}"
    response = send(msg)

    if response == "LOGIN_OK":
        logged_in_account = acc
        print("Login successful")
    else:
        print("Login failed")


def check_balance():
    if not logged_in_account:
        print("You must login first")
        return

    msg = f"BALANCE|{logged_in_account}"
    print(send(msg))


while True:
    menu()
    choice = input("Choose option: ")

    if choice == "1":
        create_account()

    elif choice == "2":
        login()

    elif choice == "3":
        check_balance()

    elif choice == "4":
        print("Bye 🏦")
        break

    else:
        print("Invalid option")