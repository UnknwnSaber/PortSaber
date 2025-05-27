# PortSaber Changelog

## [1.0] - Initial Stable Release

### Added
- Core multi-threaded TCP port scanning functionality with configurable port ranges.
- Support for scanning single IP addresses and entire subnets using CIDR notation (e.g., 192.168.1.0/24).
- Service detection on open ports via `socket.getservbyport()` to identify common services.
- Basic banner grabbing for open ports to capture service information.
- Configurable scan timeout and delay between port scans for flexible scanning speed and stealth.
- Colorized terminal output using `colorama` for clear distinction of open, closed, and error states.
- Real-time progress display with `tqdm` progress bar for better user feedback.
- Interactive input prompts when command-line arguments are omitted.
- Automatic creation of a dedicated `portScanResults` folder to store scan reports.
- Timestamped and concise report filenames for easy identification and management.
- Command-line interface with support for IP/subnet, port range, timeout, delay, and output options.
- Graceful handling of keyboard interrupts (Ctrl+C) to safely terminate scans without data loss.

### Changed
- Structured scanning logic to handle multiple hosts efficiently via multithreading.
- Improved output formatting for readability and detailed reporting.

### Fixed
- Enhanced input validation for IP addresses, subnets, and port ranges to prevent invalid inputs.
- Addressed concurrency and error handling to ensure stable scanning operations.

---

This release marks the first stable version of PortSaber, providing a reliable and feature-rich port scanning tool for network diagnostics and security testing.
