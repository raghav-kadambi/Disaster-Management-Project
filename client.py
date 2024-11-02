import socket

def start_client(server_host='localhost', server_port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((server_host, server_port))
        print("Welcome to the Disaster Reporting System!")
        
        severity = input("Enter the severity of the disaster (1: Low, 2: Medium, 3: High): ")
        location = input("Enter your location: ")

        # Send severity and location as a comma-separated string
        client_socket.sendall(f"{severity},{location}".encode('utf-8'))
        
        alert_message = client_socket.recv(1024).decode('utf-8')
        print("Received:", alert_message)

if __name__ == "__main__":
    start_client()