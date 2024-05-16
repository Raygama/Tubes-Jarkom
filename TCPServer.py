from socket import *

def tcp_server():
    serverHost = 'localhost'
    serverPort = 80
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
            print("message from client: " + message)
            message_parts = message.split()
            request_method = message_parts[0]
            request_path = message_parts[1]

            # Anggap hanya menerima request GET file html saja
            if request_method == 'GET' and request_path.endswith('.html'):
                try:
                    file = open(request_path[1:], 'rb')
                    file_content = file.read()
                    file.close()
                    response_header = "HTTP/1.1 200 OK\r\n"
                    content_type_header = "Content-Type: text/html\r\n"
                    content_length_header = "Content-Length: " + str(len(file_content)) + "\r\n"
                    response = response_header + content_type_header + content_length_header + "\r\n"
                    response_bytes = bytes(response, 'utf-8') + file_content
                    connectionSocket.sendall(response_bytes)
                except FileNotFoundError:
                    response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n<html><body><h1>404 Not Found</h1></body></html>\r\n"
            else:
                response = "HTTP/1.1 400 Bad Request\r\nContent-Type: text/html\r\n\r\n<html><body><h1>400 Bad Request: Invalid file type</h1></body></html>\r\n"

            connectionSocket.sendall(response.encode())

        except IOError:
            connectionSocket.send("HTTP/1/1 404 Not Found\r\nContent-Type: text/html\r\n\r\n".encode())
            connectionSocket.send("<html><body><h1>404 Not Found</h1></body></html>\r\n".encode())

        connectionSocket.close()

if __name__ == "__main__":
    tcp_server()
