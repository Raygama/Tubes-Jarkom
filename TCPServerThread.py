import socket
import threading

serverHost = '127.0.0.1'
serverPort = 12000

def handle_client(connectionSocket, addr):
    try:
        # Menerima message
        message = connectionSocket.recv(1024).decode()
        file = message.split()[1]
        r = open(file[1:])
        content = r.read()
        r.close()
        
        response_header = "HTTP/1.1 200 OK\r\n"
        content_type_header = "Content-Type: text/html\r\n"
        response = response_header + content_type_header + "\r\n" + content + "\r\n"
        connectionSocket.sendall(response.encode())

        print("Messaged successfully sent")
        connectionSocket.close()

    except IndexError:
        print("Waiting for request from client...")
        
    except IOError:
        r = open("./error.html", "r")
        content = r.read()
        r.close()

        response_header = "HTTP/1.1 200 OK\r\n"
        content_type_header = "Content-Type: text/html\r\n"
        response = response_header + content_type_header + "\r\n" + content + "\r\n"
        connectionSocket.sendall(response.encode())

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((serverHost, serverPort))
    server.listen()
    print(f"The Server is Ready to Receive on {serverHost}:{serverPort}")

    while True:
        connectionSocket, addr = server.accept()
        
        print(f"Connection established with {addr}")
        thread = threading.Thread(target=handle_client, args=(connectionSocket, addr))
        thread.start()
        print(f"Active connections {threading.active_count() - 1}")

if __name__ == "__main__":
    main()
