# SSH Botnet Simulation Project 🕸️

## 🔒 Overview
This project simulates a basic **SSH-based Botnet** in a controlled lab environment for **educational and ethical purposes only**. It demonstrates how a command-and-control (C2) server can remotely manage multiple compromised SSH bots, send commands, and simulate a DDoS attack using a SYN flood.

> ⚠️ This tool is built strictly for learning, testing, and red-teaming labs. Do **not** use it against unauthorized systems.

---

## 🧠 Features

- 📡 **Central Command-and-Control (C2) Server** to control all bots
- 🤖 **Bot Management**: Add, list, and interact with connected bots
- 💻 **Remote Command Execution** on multiple SSH clients
- 🐚 **Interactive Shell Mode** per bot
- 💥 **SYN Flood Attack Simulation** using Scapy (for lab DDoS testing)
- 🗃️ Persistent bot storage using JSON

---

## ⚙️ Technologies Used

- Python 3.x
- `paramiko` – for SSH session handling
- `Scapy` – for crafting SYN flood packets
- `socket`, `json`, `threading` – core modules for communication & threading

---

## 🚀 How It Works

### 1. Add Bots
The user adds bot details (host, username, password, and optional port) into a JSON file. The C2 server reads this file and attempts to connect to all listed bots.

### 2. Control Bots
Once connected, the C2 provides:
- Live terminal-based command execution
- Interactive session with any bot
- Bot listing with connection status

### 3. Launch SYN Flood (Simulated DDoS)
Using Scapy, the C2 can command a bot to simulate a SYN flood attack on a specified IP and port.


