PortSaber
PortSaber is a fast, user-friendly, and customizable port scanner written in Python. It efficiently scans TCP ports on a target IP address with concurrency and provides clear color-coded output. Scan reports are automatically saved with timestamped filenames in a dedicated results folder.

Features
Fast multi-threaded TCP port scanning using concurrent.futures.ThreadPoolExecutor

Colorized terminal output using colorama for easy identification of open/closed/error ports

Progress bar visualization with tqdm for scan progress tracking

Validates IP addresses and port ranges with user-friendly prompts if arguments are not provided

Command-line arguments support for IP, start/end ports, timeout, and output file saving

Automatically saves scan results in a portScanResults directory with concise, timestamped filenames

Gracefully handles keyboard interrupts (Ctrl+C) to stop scans safely

Installation
Ensure you have Python 3.x installed.

Install required dependencies:

bash
pip install colorama tqdm

Usage
You can run PortSaber interactively or use command-line arguments:

bash
python portSaber.py
This will prompt you for the target IP and port range.

Or provide arguments for quick scans:

bash
python portSaber.py -i 192.168.1.1 -s 1 -e 1024 -t 1.0 -o myscan.txt

Arguments:
Flag	Description	Default
-i, --ip	Target IP address	(prompt)
-s, --start	Start port	1
-e, --end	End port	1024
-t, --timeout	Timeout per port (seconds)	1.0
-o, --output	Output filename (optional)	Saves automatically in portScanResults folder with timestamped name if not specified

Example Output
Starting scan on 192.168.1.1 from port 1 to 1024...

Scanning ports: 100%|██████████| 1024/1024 [00:30<00:00, 33.92port/s]

========================================
Scan complete. Open ports (3):
 - Port 22
 - Port 80
 - Port 443
========================================

Open ports saved to portScanResults/PS_Report_250527_1530.txt
Folder Structure
portScanResults/ — Automatically created folder where scan reports are saved

portSaber.py — Main port scanner script

Notes
Only TCP ports are scanned.

Ensure you have appropriate permissions and legal authorization before scanning remote systems.

Large port ranges may take significant time depending on network speed and target response.
