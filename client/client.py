import socket
import hashlib

HOST = "127.0.0.1"
PORT = 5555

logged_in = None


def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()


def send(msg):
    c = socket.socket()
    c.connect((HOST, PORT))
    c.send(msg.encode())
    res = c.recv(4096).decode()
    c.close()
    return res


def menu():
    print("\nBANK SYSTEM")
    print("1. Create account")
    print("2. Login")
    print("3. Balance")
    print("4. Transfer")
    print("5. Deposit")
    print("6. Withdraw")
    print("7. Exit")


def create():
    n = input("Name: ")
    s = input("Surname: ")
    p = input("PESEL: ")
    a = input("Account: ")
    pw = hash_password(input("Password: "))

    print(send(f"CREATE|{n}|{s}|{p}|{a}|{pw}"))


def login():
    global logged_in

    a = input("Account: ")
    pw = hash_password(input("Password: "))

    res = send(f"LOGIN|{a}|{pw}")

    if res == "LOGIN_OK":
        logged_in = a
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

    to = input("To account: ")
    amount = input("Amount: ")

    print(send(f"TRANSFER|{logged_in}|{to}|{amount}"))


def deposit():
    if not logged_in:
        print("LOGIN REQUIRED")
        return

    amount = input("Amount: ")
    print(send(f"DEPOSIT|{logged_in}|{amount}"))


def withdraw():
    if not logged_in:
        print("LOGIN REQUIRED")
        return

    amount = input("Amount: ")
    print(send(f"WITHDRAW|{logged_in}|{amount}"))


while True:
    menu()
    c = input("> ")

    if c == "1":
        create()
    elif c == "2":
        login()
    elif c == "3":
        balance()
    elif c == "4":
        transfer()
    elif c == "5":
        deposit()
    elif c == "6":
        withdraw()
    elif c == "7":
        break
    else:
        print("INVALID COMMAND")