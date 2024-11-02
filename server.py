import socket
import matplotlib.pyplot as plt
import threading

clients = {}  # Dictionary to hold client information
disaster_severity = {
    1: "Low",
    2: "Medium",
    3: "High"
}

def update_graph():
    plt.style.use("dark_background")
    plt.ion()  # Enable interactive mode for real-time plotting
    plt.figure(figsize=(20, 10))  # Set figure size

    while True:
        if clients:
            statuses = list(clients.values())
            client_ids = list(clients.keys())
            colors = ['green' if status['severity'] == 1 else 
                      'yellow' if status['severity'] == 2 else 
                      'red' for status in statuses]

            plt.clf()  # Clear previous plot
            plt.scatter(range(len(client_ids)), [status['severity'] for status in statuses], c=colors, s=200)

            # Add labels for location and time to the plot
            for i, client_id in enumerate(client_ids):
                plt.annotate(statuses[i]['location'], (i, statuses[i]['severity']),
                             textcoords="offset points", xytext=(0, -15), ha='center', fontsize=8)
                plt.annotate(statuses[i]['time'], (i, statuses[i]['severity']),
                             textcoords="offset points", xytext=(0, -25), ha='center', fontsize=6)

            plt.yticks([1, 2, 3], ['Low', 'Medium', 'High'])
            plt.xticks(range(len(client_ids)), rotation=45)
            plt.ylim(0.5, 3.5)  # Set y-axis limits for better visibility
            plt.title("Disaster Status")
            plt.xlabel("Location")
            plt.ylabel("Disaster Severity")

            # Create a legend
            plt.scatter([], [], c='green', label='Low Severity')  # Dummy plot for legend
            plt.scatter([], [], c='yellow', label='Medium Severity')  # Dummy plot for legend
            plt.scatter([], [], c='red', label='High Severity')  # Dummy plot for legend
            plt.legend(title='Disaster Severity', loc='upper right', framealpha=0.9)

            plt.pause(1)

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def start_server(host='0.0.0.0', port=12345):
    while is_port_in_use(port):
        print(f"Port {port} is in use. Trying a different port...")
        port += 1

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
                # Receive severity, location, and disaster time from the client
                data = client_socket.recv(1024).decode('utf-8').split(',')
                severity = int(data[0]) if data[0].isdigit() and 1 <= int(data[0]) <= 3 else 1  # Default to 1 (low) if invalid
                location = data[1] if len(data) > 1 else "Unknown"  # Default to "Unknown" if no location
                disaster_time = data[2] if len(data) > 2 else "Unknown"  # Get disaster time

                # Update client information if the location already exists
                for client_key in list(clients.keys()):
                    if clients[client_key]['location'] == location:
                        clients[client_key]['severity'] = severity
                        clients[client_key]['time'] = disaster_time
                        print(f"Updated existing report for {location}")
                        break
                else:
                    # Store new client information if location doesn't exist
                    clients[client_id] = {'severity': severity, 'location': location, 'time': disaster_time}
                    print(f"Added new report for {location}")

                # Send alert message
                alert_message = f"ALERT: A natural disaster is occurring in your area ({location})! Severity: {disaster_severity[severity]}"
                client_socket.sendall(alert_message.encode('utf-8'))
                print("Alert sent to", addr)

if __name__ == "__main__":
    start_server()
