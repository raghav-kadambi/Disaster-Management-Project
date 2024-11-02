import socket
import matplotlib.pyplot as plt
import numpy as np
import threading

clients = {}  # Dictionary to hold client information
disaster_severity = {
    1: "Low",
    2: "Medium",
    3: "High"
}

def update_graph():
    while True:
        if clients:
            plt.show() 
            plt.style.use('ggplot')  

            statuses = list(clients.values())
            client_ids = list(clients.keys())
            colors = ['green' if status['severity'] == 1 else 'yellow' if status['severity'] == 2 else 'red' for status in statuses]

            # Display severity on the y-axis and plot
            plt.scatter(range(len(client_ids)), [status['severity'] for status in statuses], c=colors, s=100)

            # Label each point with the corresponding location
            for i, client_id in enumerate(client_ids):
                plt.text(i, statuses[i]['severity'] + 0.1, statuses[i]['location'], fontsize=9, ha='center', va='bottom')

            plt.yticks([1, 2, 3], ['Low', 'Medium', 'High'])
            plt.xticks(range(len(client_ids)), rotation=45)
            plt.title("Disaster status")
            plt.xlabel("Location")
            plt.ylabel("Disaster Severity")
            plt.pause(1)

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def start_server(host='0.0.0.0', port=12345):
    if is_port_in_use(port):
        print(f"Port {port} is in use. Trying a different port...")
        port = 12346  # Change to an unused port

    plt.ion()  # Turn on interactive mode for real-time plotting
    
    threading.Thread(target=update_graph, daemon=True).start()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Server listening on {host}:{port}")

        while True:
            client_socket, addr = server_socket.accept()
            with client_socket:
                print(f"Connection from {addr}")
                client_id = f"Client {addr[1]}"
                # Receive severity level and location from the client
                data = client_socket.recv(1024).decode('utf-8').split(',')
                severity = int(data[0]) if data[0].isdigit() else 1  # Default to 1 (low) if invalid
                location = data[1] if len(data) > 1 else "Unknown"  # Default to "Unknown" if no location

                # Store client information
                clients[client_id] = {'severity': severity, 'location': location}
                # Send alert message
                alert_message = f"ALERT: A natural disaster is occurring in your area ({location})! Severity: {disaster_severity[severity]}"
                client_socket.sendall(alert_message.encode('utf-8'))
                print("Alert sent to", addr)

if __name__ == "__main__":
    start_server()
