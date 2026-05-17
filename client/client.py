import socket
import hashlib

HOST = "127.0.0.1"
PORT = 5555

logged_in = None


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def send(msg):
    client = socket.socket()
    client.connect((HOST, PORT))
    client.send(msg.encode())
    res = client.recv(4096).decode()
    client.close()
    return res


def menu():
    print("\nBANK SYSTEM")
    print("1. Create account")
    print("2. Login")
    print("3. Balance")
    print("4. Transfer")
    print("5. Exit")


def create_account():
    name = input("Name: ")
    surname = input("Surname: ")
    pesel = input("PESEL: ")
    acc = input("Account number: ")
    password = hash_password(input("Password: "))

    print(send(f"CREATE|{name}|{surname}|{pesel}|{acc}|{password}"))


def login():
    global logged_in

    acc = input("Account number: ")
    password = hash_password(input("Password: "))

    res = send(f"LOGIN|{acc}|{password}")

    if res == "LOGIN_OK":
        logged_in = acc
        print("LOGIN OK")
    else:
        print("LOGIN FAIL")


def balance():
    if not logged_in:
        print("LOGIN REQUIRED")
        return

    print(send(f"BALANCE|{logged_in}"))


def transfer():
    if not logged_in:
        print("LOGIN REQUIRED")
        return

    to_acc = input("To account: ")
    amount = input("Amount: ")

    print(send(f"TRANSFER|{logged_in}|{to_acc}|{amount}"))


while True:
    menu()
    choice = input("> ")

    if choice == "1":
        create_account()
    elif choice == "2":
        login()
    elif choice == "3":
        balance()
    elif choice == "4":
        transfer()
    elif choice == "5":
        break