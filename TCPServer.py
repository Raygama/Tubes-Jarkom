from socket import *

def tcp_server():
    serverHost = '127.0.0.1'
    serverPort = 12000
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind((serverHost, serverPort))
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocket.listen(1)
    print('The Server is Ready to Receive')

    while True:
        # Buat connection
        connectionSocket, addr = serverSocket.accept()
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


        connectionSocket.close()

if __name__ == "__main__":
    tcp_server()
