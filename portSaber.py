import socket
import concurrent.futures


def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        sock.close()
        if result == 0:
            print(f"Port {port} is open")
        else:
            print(f"Port {port} is closed")
    except Exception as e:
        print(f"Error scanning port {port}: {e}")


def scan_ports(ip, start_port, end_port):
 # helps prevent the system from being overwhelmed by too many concurrent threads.

 with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
    for port in range(start_port, end_port + 1):
        executor.submit(scan_port, ip, port)

if __name__ == "__main__":
        try:
            target_ip = input("Enter the target IP address: ")
            start_port = int(input("Enter the starting port: "))
            end_port = int(input("Enter the ending port: "))
            if start_port > end_port:
                print("Error: Starting port must be less than or equal to ending port")
            else:
                scan_ports(target_ip, start_port, end_port)
        except ValueError:
            print("Error: Invalid input. Please enter valid numbers for ports.")
        except Exception as e:
            print(f"An error occurred: {e}")