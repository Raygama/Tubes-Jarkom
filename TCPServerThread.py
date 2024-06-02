from socket import *
import threading

# Fungsi yang akan dijalankan oleh setiap thread untuk menangani koneksi dengan client
def handle_client(connectionSocket):
    try:
        # Menerima pesan dari client
        message = connectionSocket.recv(1024).decode()
        print("Message from client: " + message)
        message_parts = message.split()
        request_method = message_parts[0]
        request_path = message_parts[1]

        # Hanya menerima request GET file html saja
        if request_method == 'GET':
            try:
                # Membuka file yang diminta
                file = open(request_path[1:], 'rb')
                file_content = file.read()
                file.close()
                response_header = "HTTP/1.1 200 OK\r\n"
                content_type_header = "Content-Type: text/html\r\n"
                content_length_header = "Content-Length: " + str(len(file_content)) + "\r\n"
                response = response_header + content_type_header + content_length_header + "\r\n"
                response_bytes = bytes(response, 'utf-8') + file_content
                # Mengirim response ke client
                connectionSocket.sendall(response_bytes)
            except FileNotFoundError:
                # Mengirim response 404 jika file tidak ditemukan
                response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n<html><body><h1>404 Not Found</h1></body></html>\r\n"
                connectionSocket.sendall(response.encode())
        else:
            # Mengirim response 400 jika request tidak valid
            response = "HTTP/1.1 400 Bad Request\r\nContent-Type: text/html\r\n\r\n<html><body><h1>400 Bad Request: Invalid file type</h1></body></html>\r\n"
            connectionSocket.sendall(response.encode())

    except IOError:
        # Mengirim response 404 jika terjadi error saat mengakses file
        connectionSocket.send("HTTP/1/1 404 Not Found\r\nContent-Type: text/html\r\n\r\n".encode())
        connectionSocket.send("<html><body><h1>404 Not Found</h1></body></html>\r\n".encode())

    # Menutup koneksi dengan client
    connectionSocket.close()

def tcp_server():
    serverHost = 'localhost'
    serverPort = 80
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind((serverHost, serverPort))
    serverSocket.listen(5)  # Mendengarkan hingga 5 koneksi simultan
    print('The Server is Ready to Receive')

    while True:
        # Menerima koneksi dari client
        connectionSocket, addr = serverSocket.accept()
        print(f"Connection established with {addr}")
        # Membuat thread baru untuk menangani koneksi dengan client
        client_thread = threading.Thread(target=handle_client, args=(connectionSocket,))
        client_thread.start()

if __name__ == "__main__":
    tcp_server()
