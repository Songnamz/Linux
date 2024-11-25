from http.server import HTTPServer, SimpleHTTPRequestHandler
import logging
import socket


# Custom handler with logging
class LoggingHTTPRequestHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        logging.info("%s - - [%s] %s\n" %
                     (self.client_address[0],
                      self.log_date_time_string(),
                      format % args))

def get_local_ip():
    """Automatically fetch the local IP address."""
    try:
        # Use a dummy socket connection to determine local IP
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))  # Connect to a public DNS server
            return s.getsockname()[0]
    except Exception as e:
        logging.error(f"Unable to fetch local IP: {e}")
        return "127.0.0.1"  # Default to localhost in case of failure

def run(server_class=HTTPServer, handler_class=LoggingHTTPRequestHandler, port=8000):
    ip = get_local_ip()  # Dynamically fetch the IP address
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
    logging.info(f"Starting server on {ip}:{port}...")
    
    # Bind to the dynamically determined IP address and port
    server_address = (ip, port)
    httpd = server_class(server_address, handler_class)
    
    try:
        logging.info("Server running. Press Ctrl+C to stop.")
        logging.info(f"Access the server at http://{ip}:{port}")
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        logging.info("Shutting down server.")
        httpd.server_close()

if __name__ == "__main__":
    run(port=8000)

