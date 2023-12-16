import socket
import threading
import logging
import os
import time

# Configuration constants
HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 22222  # SSH port

# Set up logging
log_directory = 'honeypot_logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

log_file_path = os.path.join(log_directory, 'honeypot_logs.txt')

# Log rotation configuration
log_rotation_threshold = 10  # MB
log_rotation_interval = 24  # hours

logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Dictionary to store honeytokens and their access timestamps
honeytokens = {}



def log_connection(client_socket, request, log_message):
    # Log the connection attempt
    log_entry = f"Connection from: {client_socket.getpeername()} - {request.decode('utf-8').strip()} - {log_message}\n"
    logging.info(log_entry)




def handle_client(client_socket):
    try:
        # This function handles the interaction with a single client
        request = client_socket.recv(1024)  # Receive the initial client request

        # Log the connection attempt
        log_connection(client_socket, request, "Initial request")

        # Emulate an SSH server response (you can make this more sophisticated)
        response = "SSH-2.0-OpenSSH_7.9p1 Debian-10+deb10u2\r\n"
        client_socket.send(response.encode())

        # Log the key exchange attempt
        kex_request = client_socket.recv(1024).decode('utf-8', 'replace').strip()
        log_connection(client_socket, request, f"Key exchange attempt: {kex_request}")

        # Emulate an SSH server response for key exchange
        kex_response = "SSH-2.0-OpenSSH_7.9p1 Debian-10+deb10u2\r\n"
        client_socket.send(kex_response.encode())

        # Log the command attempts
        while True:
            command_bytes = client_socket.recv(1024)
            if not command_bytes:
                break

            command = command_bytes.decode('utf-8', 'replace').strip()
            log_message = f"Command: {command}"

            # Log the connection attempt
            log_connection(client_socket, request, log_message)

            # Check if specific commands are detected and respond accordingly
            command_responses = {
                "rm -rf": "Permission denied: Deleting everything is not allowed!\r\n",
                "sudo": "Permission denied: Superuser access is not allowed!\r\n",
                "wget": "Permission denied: Downloading files is not allowed!\r\n",
                "curl": "Permission denied: Downloading files is not allowed!\r\n",
                "nc": "Permission denied: Network commands are not allowed!\r\n",
                "netcat": "Permission denied: Network commands are not allowed!\r\n",
                "chmod": "Permission denied: Changing file permissions is not allowed!\r\n",
                "passwd": "Permission denied: Changing passwords is not allowed!\r\n",
                "mkdir": "Permission denied: Creating directories is not allowed!\r\n",
                "echo": "Permission denied: Echoing commands is not allowed!\r\n",
                "kill": "Permission denied: Killing processes is not allowed!\r\n",
                "ifconfig": "Permission denied: Viewing network interfaces is not allowed!\r\n",
                "ls": "Permission denied: Listing directory contents is not allowed!\r\n",
                "cat": "Permission denied: Viewing file contents is not allowed!\r\n",
                "grep": "Permission denied: Searching through files is not allowed!\r\n",
                "vi": "Permission denied: Text editing is not allowed!\r\n",
                "nano": "Permission denied: Text editing is not allowed!\r\n",
                "echo *": "Permission denied: Wildcard expansion is not allowed!\r\n",
                "find": "Permission denied: Searching for files is not allowed!\r\n",
                "ps": "Permission denied: Viewing processes is not allowed!\r\n",
                "top": "Permission denied: Viewing system processes is not allowed!\r\n",
                "whoami": "Permission denied: Identifying the current user is not allowed!\r\n",
                "uname": "Permission denied: Retrieving system information is not allowed!\r\n",
                "df": "Permission denied: Displaying disk space is not allowed!\r\n",
                "du": "Permission denied: Displaying file and directory space usage is not allowed!\r\n",
                "ping": "Permission denied: Network pinging is not allowed!\r\n",
                "traceroute": "Permission denied: Tracing network routes is not allowed!\r\n",
                "ssh": "Permission denied: SSH connections are not allowed!\r\n",
            }

            for cmd, response_message in command_responses.items():
                if cmd in command:
                    client_socket.send(response_message.encode())
                    break
            else:
                # Default response for other commands
                response_message = "Command not found\r\n"
                client_socket.send(response_message.encode())

            # Check if a honeytoken is triggered
            if command in honeytokens:
                log_message = f"Honeytoken triggered: {command}"
                log_connection(client_socket, request, log_message)

    except socket.error as se:
        if se.errno == 107:  # Transport endpoint is not connected
            pass  # Ignore this specific error
        else:
            logging.error(f"Socket error: {se}")
    except Exception as e:
        logging.error(f"Error handling client: {e}")

    finally:
        # Close the client socket
        client_socket.close()



def start_honeypot():
    try:
        # Create a socket to listen for incoming connections
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST, PORT))
        server.listen(5)

        logging.info(f"[*] Listening on {HOST}:{PORT}")

        # Log rotation variables
        last_rotation_time = time.time()

        while True:
            # Check for log rotation
            if os.path.getsize(log_file_path) > (log_rotation_threshold * 1024 * 1024) or (time.time() - last_rotation_time) > (log_rotation_interval * 3600):
                logging.info("Performing log rotation.")
                logging.handlers.RotatingFileHandler(log_file_path, backupCount=5, maxBytes=log_rotation_threshold * 1024 * 1024)

                last_rotation_time = time.time()

            # Accept incoming connections
            client, addr = server.accept()

            # Handle each connection in a separate thread
            client_handler = threading.Thread(target=handle_client, args=(client,))
            client_handler.start()

    except socket.error as se:
        logging.error(f"Socket error: {se}")
    except Exception as e:
        logging.error(f"Error starting honeypot: {e}")

if __name__ == '__main__':
    # Add honeytokens to the dictionary
    honeytokens["fake_password"] = time.time()  
    honeytokens["admin@admin.com"] = time.time()
    honeytokens["hacker123"] = time.time()
    honeytokens["secretpassword"] =  time.time()
    honeytokens["root"] = time.time()
    honeytokens["backdoor_key"] = time.time()
    honeytokens["malicious_payload"] = time.time()
    honeytokens["fake_credit_card"] = time.time(),
    # Start the honeypot
    start_honeypot()
