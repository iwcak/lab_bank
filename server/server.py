import socket
import threading
from database import Database

db = Database()

HOST = "127.0.0.1"
PORT = 5555


def handle_client(conn, addr):
    print("NEW CONNECTION:", addr)

    conn.send("WELCOME".encode())

    while True:
        try:
            msg = conn.recv(1024).decode()
            if not msg:
                break

            parts = msg.split("|")
            cmd = parts[0]

            if cmd == "CREATE":
                name, surname, pesel, acc, pwd_hash = parts[1:]
                ok = db.create_user(name, surname, pesel, acc, pwd_hash)
                conn.send(("OK" if ok else "ERROR").encode())

            elif cmd == "LOGIN":
                acc, pwd_hash = parts[1:]
                user = db.get_user_by_account(acc)

                if user and user[5] == pwd_hash:
                    conn.send("LOGIN_OK".encode())
                else:
                    conn.send("LOGIN_FAIL".encode())

            elif cmd == "BALANCE":
                acc = parts[1]
                bal = db.get_balance(acc)
                conn.send(str(bal).encode())

            elif cmd == "TRANSFER":
                from_acc, to_acc, amount = parts[1:]
                result = db.transfer(from_acc, to_acc, float(amount))
                conn.send(result.encode())

        except Exception as e:
            print("ERROR:", e)
            break

    conn.close()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("Server running on", HOST, PORT)

while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()