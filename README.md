# HTTP Proxy Server

A minimal multithreaded HTTP proxy server written with Python sockets. The project includes a proxy server, a simple client for testing requests through the proxy, and a sample HTML response file.

## Features

- Accepts client HTTP requests on `127.0.0.1:8080`.
- Parses the requested URL and destination host.
- Forwards requests to the target HTTP server.
- Streams the target server response back to the client.
- Handles each client connection in a separate thread.

## Tech Stack

- Python
- TCP sockets
- Threading

## Project Structure

```text
.
|-- proxy_server.py    # Multithreaded socket proxy
|-- proxy_client.py    # Test client that requests example.com through the proxy
`-- index.html         # Example HTML response/reference file
```

## Getting Started

Start the proxy:

```bash
python proxy_server.py
```

In another terminal, run the test client:

```bash
python proxy_client.py
```

## Notes

This implementation is for learning HTTP forwarding with sockets. It targets plain HTTP traffic and does not implement full HTTPS tunneling, caching, authentication, or production-grade request parsing.
