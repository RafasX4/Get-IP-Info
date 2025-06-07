# Coded By Rafas / 👀

import requests
import socket
import ipaddress
import time
import os
import sys
from colorama import init, Fore, Style, Back

init(autoreset=True)

COMMON_PORTS = [80, 443, 21, 22, 23, 25, 110, 143, 465, 993, 995, 3306, 3389, 5900]

def is_any_common_port_open(ip: str, timeout: float = 1.0) -> bool:
    for port in COMMON_PORTS:
        try:
            with socket.create_connection((ip, port), timeout=timeout):
                return True
        except (socket.timeout, ConnectionRefusedError, OSError):
            continue
    return False

ip = "192.168.1.1"
if is_any_common_port_open(ip):
    print(f"{ip} has at least one common port open.")
else:
    print(f"{ip} has no common ports open.")

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def print_banner():
    title = "YOUR TOOL NAME"
    version = "v1.0.0"
    width = 60
    padding_length = (width - len(title)) // 2
    title_spaces = " " * padding_length
    title_spaces_after = " " * (width - padding_length - len(title))
    version_padding = (width - len(version)) // 2
    version_spaces = " " * version_padding
    version_spaces_after = " " * (width - version_padding - len(version))
    border_line = "-" * width
    
    print(f"{Style.BRIGHT + Fore.BLUE}+{border_line}+{Style.RESET_ALL}")
    print(f"{Style.BRIGHT + Fore.BLUE}|{title_spaces}{Style.BRIGHT + Fore.CYAN}{title}{Style.RESET_ALL}{title_spaces_after}|{Style.RESET_ALL}")
    print(f"{Style.BRIGHT + Fore.BLUE}|{version_spaces}{Fore.CYAN}{version}{Style.RESET_ALL}{version_spaces_after}|{Style.RESET_ALL}")
    print(f"{Style.BRIGHT + Fore.BLUE}+{border_line}+{Style.RESET_ALL}")
    print("\n")

def is_valid_ip(ip_str):
    try:
        ip_object = ipaddress.ip_address(ip_str)
        return not ip_object.is_private and not ip_object.is_loopback
    except ValueError:
        return False

def get_ip_info(ip_address):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}?fields=status,message,country,regionName,city,isp,org,as,query")
        response.raise_for_status()
        data = response.json()
        if data.get("status") == "success":
            return data
        else:
            return {"query": ip_address, "status": "fail", "message": data.get("message", "Failed to get info")}
    except requests.exceptions.RequestException as e:
        return {"query": ip_address, "status": "fail", "message": f"Network error: {e}"}

def check_ports(ip_address):
    open_ports = []
    socket.setdefaulttimeout(0.5) 
    for port in COMMON_PORTS:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                result = sock.connect_ex((ip_address, port))
                if result == 0:
                    open_ports.append(port)
        except (socket.timeout, socket.error):
            continue
    return open_ports

def display_info(info, open_ports):
    query = info.get("query", "N/A")
    country = info.get("country", "N/A")
    region = info.get("regionName", "N/A")
    city = info.get("city", "N/A")
    isp = info.get("isp", "N/A")
    org = info.get("org", "N/A")
    as_info = info.get("as", "N/A")
    ports_str = ", ".join(map(str, open_ports)) if open_ports else "None Found"
    info_width = 62
    info_border = "-" * info_width

    print(f"{Style.BRIGHT + Fore.CYAN}[+] IP Information for: {Fore.WHITE}{query}{Style.RESET_ALL}")
    print(f"{Fore.BLUE}{info_border}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  - Country: {Fore.WHITE}{country}")
    print(f"{Fore.CYAN}  - Region:  {Fore.WHITE}{region}")
    print(f"{Fore.CYAN}  - City:    {Fore.WHITE}{city}")
    print(f"{Fore.CYAN}  - ISP:     {Fore.WHITE}{isp}")
    print(f"{Fore.CYAN}  - Org:     {Fore.WHITE}{org}")
    print(f"{Fore.CYAN}  - AS:      {Fore.WHITE}{as_info}")
    print(f"{Fore.CYAN}  - Open Ports (Common): {Fore.WHITE}{ports_str}")
    print(f"{Fore.BLUE}{info_border}{Style.RESET_ALL}\n")

def main():
    while True:
        clear_screen()
        print_banner()
        try:
            ip_input = input(f"{Style.BRIGHT + Fore.BLUE}(Nesm@IPINFO)-[{Fore.CYAN}Input{Fore.BLUE}]{Style.RESET_ALL}\n└──> {Style.BRIGHT + Fore.WHITE}Enter the ip - {Style.RESET_ALL}")
            
            if not ip_input:
                continue

            if is_valid_ip(ip_input):
                print(f"\n{Fore.YELLOW}loading ..{Style.RESET_ALL}")
                time.sleep(2) 
                
                ip_info = get_ip_info(ip_input)
                open_ports = []
                if ip_info.get("status") == "success":
                    open_ports = check_ports(ip_input)
                
                clear_screen()
                print_banner()
                if ip_info.get("status") == "success":
                    display_info(ip_info, open_ports)
                else:
                    error_message = ip_info.get("message", "Could not retrieve info.")
                    print(f"{Style.BRIGHT + Fore.RED}[!] Error: {Fore.WHITE}{error_message}{Style.RESET_ALL}\n")
                
                input(f"{Fore.GREEN}Press Enter to check another IP...{Style.RESET_ALL}")

            else:
                print(f"\n{Style.BRIGHT + Fore.RED}[!] This IP is invalid or incorrect.{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}    Please enter a different IP.{Style.RESET_ALL}")
                time.sleep(3)

        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Exiting Nesm IP INFO. Goodbye!{Style.RESET_ALL}")
            sys.exit(0)
        except Exception as e:
            print(f"\n{Style.BRIGHT + Fore.RED}[!] An unexpected error occurred: {Fore.WHITE}{e}{Style.RESET_ALL}")
            time.sleep(3)

if __name__ == "__main__":
    main()
