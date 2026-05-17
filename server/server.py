import socket
import threading
from database import Database

db = Database()

HOST = "127.0.0.1"
PORT = 5555

lock = threading.Lock()


def handle_client(conn, addr):
    conn.send("WELCOME\n".encode())

    buffer = ""

    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break

            buffer += data

            while "\n" in buffer:
                msg, buffer = buffer.split("\n", 1)
                parts = msg.split("|")
                cmd = parts[0]

                if cmd == "CREATE":
                    name, surname, pesel, acc, pwd_hash = parts[1:]
                    ok = db.create_user(name, surname, pesel, acc, pwd_hash)
                    conn.send(("OK\n" if ok else "ERROR\n").encode())

                elif cmd == "LOGIN":
                    acc, pwd_hash = parts[1:]
                    user = db.get_user_by_account(acc)
                    success = user and user[5] == pwd_hash
                    conn.send(("LOGIN_OK\n" if success else "LOGIN_FAIL\n").encode())

                elif cmd == "BALANCE":
                    acc = parts[1]
                    bal = db.get_balance(acc)
                    conn.send((str(bal) + "\n").encode())

                elif cmd == "TRANSFER":
                    from_acc, to_acc, amount = parts[1:]
                    amount = float(amount)
                    with lock:
                        res = db.transfer(from_acc, to_acc, amount)
                    conn.send((res + "\n").encode())

                elif cmd == "DEPOSIT":
                    acc, amount = parts[1:]
                    amount = float(amount)
                    with lock:
                        res = db.deposit(acc, amount)
                    conn.send((res + "\n").encode())

                elif cmd == "WITHDRAW":
                    acc, amount = parts[1:]
                    amount = float(amount)
                    with lock:
                        res = db.withdraw(acc, amount)
                    conn.send((res + "\n").encode())

        except:
            break

    conn.close()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("Server running on 127.0.0.1 5555")

while True:
    conn, addr = server.accept()
    threading.Thread(target=handle_client, args=(conn, addr)).start()