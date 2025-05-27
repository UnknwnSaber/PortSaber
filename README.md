# PortSaber

**PortSaber** is a fast, user-friendly, and customizable TCP port scanner written in Python. It efficiently scans specified ports on target IP addresses or subnets using concurrency, provides clear color-coded terminal output, and automatically saves detailed scan reports. PortSaber also features basic service detection and banner grabbing for enhanced scan realism and insight.

---

## Features

- **Fast multi-threaded TCP port scanning** using `concurrent.futures.ThreadPoolExecutor`
- **Service detection** by mapping open ports to common service names
- **Basic banner grabbing** to retrieve service banners (e.g., HTTP, FTP, SMTP greetings)
- **Color-coded terminal output** with `colorama` for easy identification:
  - Green for open ports with detected services and banners
  - Red for closed ports
  - Yellow for errors or exceptions during scanning
- **Scan progress bar** powered by `tqdm` for real-time progress visualization
- **Support for scanning individual IPs or entire subnets (CIDR notation)**
- **Customizable scan parameters** via command-line arguments or interactive prompts:
  - Target IP or subnet
  - Start and end ports
  - Timeout per port connection attempt
  - Delay between scans (to avoid detection or flooding)
  - Output filename (optional)
- **Automatic saving** of scan reports in a dedicated `portScanResults` folder, with concise timestamped filenames (`PS_Report_YYMMDD_HHMM.txt`)
- **Graceful handling of interrupts (Ctrl+C)** to safely stop scans and save progress

---

## Installation

Make sure you have Python 3.x installed. Then, install dependencies via pip:

```bash
pip install colorama tqdm
