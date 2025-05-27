import socket
import concurrent.futures
import ipaddress
import argparse
from colorama import Fore, Style, init
from tqdm import tqdm
import sys
import time
from datetime import datetime
import os

init(autoreset=True)

def get_service_name(port):
    try:
        return socket.getservbyport(port)
    except OSError:
        return "Unknown"

def grab_banner(ip, port, timeout=1):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((ip, port))
        sock.send(b'\r\n')
        banner = sock.recv(1024).decode(errors="ignore").strip()
        sock.close()
        return banner if banner else "No banner"
    except:
        return "No banner"

def scan_port(ip, port, timeout=1):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        sock.close()
        if result == 0:
            service = get_service_name(port)
            banner = grab_banner(ip, port, timeout)
            print(Fore.GREEN + f"Port {port} is OPEN ({service}) - Banner: {banner}")
            return port, True, service, banner
        else:
            print(Fore.RED + f"Port {port} is closed")
            return port, False, None, None
    except Exception as e:
        print(Fore.YELLOW + f"Error scanning port {port}: {e}")
        return port, False, None, None

def scan_ports(ip, start_port, end_port, timeout=1, delay=0):
    ports = range(start_port, end_port + 1)
    open_ports_local = []

    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            def delayed_scan(port):
                result = scan_port(ip, port, timeout)
                if delay > 0:
                    time.sleep(delay)
                return result

            results = list(tqdm(executor.map(delayed_scan, ports),
                                total=len(ports), desc=f"Scanning {ip}", unit="port"))
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\nScan interrupted by user. Exiting...")
        sys.exit()

    for port, is_open, service, banner in results:
        if is_open:
            open_ports_local.append((port, service, banner))

    return open_ports_local

def validate_ip(ip_str):
    try:
        if '/' in ip_str:
            ipaddress.ip_network(ip_str, strict=False)
        else:
            ipaddress.ip_address(ip_str)
        return True
    except ValueError:
        return False

def get_ip():
    while True:
        ip_str = input("Enter the target IP address or subnet (CIDR): ").strip()
        if validate_ip(ip_str):
            return ip_str
        else:
            print(Fore.RED + "Invalid IP address or subnet format. Please try again.")

def get_port(prompt, default):
    while True:
        val = input(f"{prompt} (default {default}): ").strip()
        if val == "":
            return default
        if val.isdigit():
            p = int(val)
            if 1 <= p <= 65535:
                return p
        print(Fore.RED + "Invalid port number. Enter a number between 1 and 65535.")

def main():
    parser = argparse.ArgumentParser(description="PortSaber: A simple port scanner with banner grabbing")
    parser.add_argument("-i", "--ip", help="Target IP address or subnet in CIDR notation (e.g., 192.168.1.0/24)")
    parser.add_argument("-s", "--start", type=int, default=1, help="Start port (default 1)")
    parser.add_argument("-e", "--end", type=int, default=1024, help="End port (default 1024)")
    parser.add_argument("-t", "--timeout", type=float, default=1.0, help="Timeout in seconds (default 1.0)")
    parser.add_argument("-o", "--output", help="Save full scan report to file (optional)")
    parser.add_argument("-d", "--delay", type=float, default=0.0, help="Delay in seconds between port scans (default 0)")
    args = parser.parse_args()

    if not args.ip:
        target_ip = get_ip()
        start_port = get_port("Enter the starting port", 1)
        end_port = get_port("Enter the ending port", 1024)
    else:
        if not validate_ip(args.ip):
            print(Fore.RED + "Invalid IP address or subnet provided via argument.")
            sys.exit(1)
        target_ip = args.ip
        start_port = args.start
        end_port = args.end

    if start_port > end_port:
        print(Fore.RED + "Error: Starting port must be less than or equal to ending port")
        sys.exit(1)

    try:
        if '/' in target_ip:
            network = ipaddress.ip_network(target_ip, strict=False)
            targets = list(network.hosts())
            print(f"\nStarting scan on subnet {target_ip} ({len(targets)} hosts) from port {start_port} to {end_port}...\n")
        else:
            targets = [ipaddress.ip_address(target_ip)]
            print(f"\nStarting scan on IP {target_ip} from port {start_port} to {end_port}...\n")
    except Exception as e:
        print(Fore.RED + f"Error parsing IP/subnet: {e}")
        sys.exit(1)

    full_report = []
    start_time = time.time()

    for ip in targets:
        print(Style.BRIGHT + f"\nScanning {ip} ...")
        found_open_ports = scan_ports(str(ip), start_port, end_port, args.timeout, args.delay)
        if found_open_ports:
            print(Fore.GREEN + f"Open ports on {ip} ({len(found_open_ports)}):")
            for port, service, banner in found_open_ports:
                print(Fore.GREEN + f" - Port {port} ({service}) - Banner: {banner}")
        else:
            print(Fore.YELLOW + f"No open ports found on {ip}.")
        full_report.append((str(ip), found_open_ports))

    elapsed = time.time() - start_time
    print(Style.BRIGHT + "\n" + "="*60)
    print(f"Scan completed in {elapsed:.2f} seconds.")
    print("="*60)

    folder = "portScanResults"
    os.makedirs(folder, exist_ok=True)
    timestamp = datetime.now().strftime("%y%m%d_%H%M")
    filename = f"PS_Report_{timestamp}.txt"
    filepath = os.path.join(folder, filename)

    try:
        with open(filepath, "w") as f:
            f.write(f"PortSaber Scan Report - {datetime.now()}\n")
            f.write(f"Target: {target_ip}\nPorts: {start_port}-{end_port}\nTimeout: {args.timeout}s\nDelay: {args.delay}s\n\n")
            for ip, ports in full_report:
                f.write(f"Host: {ip}\n")
                if ports:
                    for port, service, banner in ports:
                        f.write(f"  Port {port} OPEN ({service}) - Banner: {banner}\n")
                else:
                    f.write("  No open ports found.\n")
                f.write("\n")
        print(Fore.CYAN + f"\nFull scan report saved to {filepath}")
    except Exception as e:
        print(Fore.RED + f"Error saving report to file: {e}")

if __name__ == "__main__":
    main()
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\nScan interrupted by user. Exiting...")
        sys.exit()
    except Exception as e:
        print(Fore.RED + f"An error occurred: {e}")
        sys.exit(1)
