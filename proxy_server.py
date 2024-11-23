import socket
import threading

# Define constants
PROXY_HOST = '127.0.0.1'  # Proxy server IP (localhost)
PROXY_PORT = 8080         # Proxy server port
BUFFER_SIZE = 4096        # Buffer size for receiving data

def handle_client(client_socket):
    """Handles the communication between the client and the destination server."""
    try:
        # Receive the client's request
        request = client_socket.recv(BUFFER_SIZE).decode(errors='ignore')
        print("[CLIENT REQUEST]\n", request)

        # Parse the request to extract the destination host and path
        lines = request.split('\r\n')
        first_line = lines[0]  # Example: GET http://example.com/ HTTP/1.1
        if not first_line:
            print("[ERROR]: Invalid HTTP request")
            return
        
        # Extract URL and path
        parts = first_line.split(' ')
        if len(parts) < 2:
            print("[ERROR]: Malformed HTTP request line")
            return
        url = parts[1]

        # Extract host and path from the URL
        http_pos = url.find("://")
        if http_pos != -1:
            url = url[(http_pos + 3):]  # Remove the protocol (http://)

        path_pos = url.find("/")  # Find the resource path
        if path_pos == -1:
            path_pos = len(url)
            path = "/"
        else:
            path = url[path_pos:]
        host = url[:path_pos]

        port = 80  # Default HTTP port
        if ":" in host:  # If a port is specified in the host
            host, port = host.split(":")
            port = int(port)

        print(f"Forwarding request to {host}:{port}{path}")

        # Connect to the destination server
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((host, port))

        # Modify the request to include only the path
        request = request.replace(url, path, 1)
        server_socket.send(request.encode())

        # Receive the response from the server and forward it to the client
        while True:
            response = server_socket.recv(BUFFER_SIZE)
            if len(response) > 0:
                client_socket.send(response)
            else:
                break

        # Close the server socket
        server_socket.close()
    except Exception as e:
        print("[ERROR]:", e)
    finally:
        # Close the client connection
        client_socket.close()


def start_proxy():
    """Starts the proxy server."""
    # Create a socket for the proxy server
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.bind((PROXY_HOST, PROXY_PORT))
    proxy_socket.listen(5)  # Maximum 5 concurrent connections

    print(f"Proxy server is running on {PROXY_HOST}:{PROXY_PORT}")

    while True:
        # Accept a new client connection
        client_socket, client_address = proxy_socket.accept()
        print(f"New connection from {client_address}")

        # Handle the client in a separate thread
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

# Entry point
if __name__ == "__main__":
    start_proxy()
