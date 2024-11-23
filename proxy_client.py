import socket

# Proxy server settings
PROXY_HOST = '127.0.0.1'  # Proxy server IP
PROXY_PORT = 8080         # Proxy server port

# Target URL and resource (for testing purposes, we'll use an example)
TARGET_URL = 'http://example.com'
TARGET_PATH = '/'  # Path of the resource on the server

def send_request():
    """Sends an HTTP request to the proxy server."""
    # Create a socket to connect to the proxy server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((PROXY_HOST, PROXY_PORT))

    # Construct the HTTP request (GET request for a resource)
    request = f"GET {TARGET_URL}{TARGET_PATH} HTTP/1.1\r\n"
    request += f"Host: example.com\r\n"
    request += "Connection: close\r\n\r\n"

    # Send the request to the proxy server
    client_socket.sendall(request.encode())

    # Receive the response from the proxy server
    response = b""
    while True:
        chunk = client_socket.recv(4096)
        if not chunk:
            break
        response += chunk

    # Print the response from the server
    print("[SERVER RESPONSE]:\n", response.decode(errors='ignore'))

    # Close the client socket
    client_socket.close()

if __name__ == "__main__":
    send_request()
