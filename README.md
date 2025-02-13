# Disaster Reporting System

A simple client-server application for reporting and visualizing disaster severity in real time. This project uses socket programming for communication and Matplotlib for graphical visualization.

## Features
- Clients can report disasters with severity levels (Low, Medium, High) and location details.
- Server receives and processes these disaster reports.
- Real-time graphical visualization of disaster locations and severity levels.


## Technologies Used
- Python
- Socket Programming
- Matplotlib
- Threading

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/disaster-reporting-system.git
   cd disaster-reporting-system
   ```
2. Install dependencies:
   ```bash
   pip install matplotlib
   ```

## Usage
### Running the Server
Start the server to listen for incoming disaster reports:
```bash
python server.py
```

### Running the Client
Clients can send disaster reports to the server:
```bash
python client.py
```
Follow the prompts to enter severity level and location details.

## How It Works
1. The client sends disaster severity, location, and timestamp to the server.
2. The server processes the information and updates the real-time visualization.
3. The server sends an alert message back to the client.
4. The graph updates dynamically with severity levels represented by different colors:
   - Green: Low
   - Yellow: Medium
   - Red: High


