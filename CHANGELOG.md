# PortSaber Changelog

## [Unreleased]

### Added
- Automatic saving of scan reports to a dedicated `portScanResults` folder, created if missing.
- Concise, timestamped report filenames in the format `PS_Report_YYMMDD_HHMM.txt` for easier management.
- Command-line option `-o / --output` to specify custom output filenames.
- Input validation for IP addresses to ensure valid targets.
- Interactive prompts for IP and port inputs when arguments are not provided.
- Port number validation to accept only values between 1 and 65535.
- Timeout parameter for socket connections, adjustable via CLI (`-t / --timeout`).
- Graceful handling of keyboard interrupts (`Ctrl+C`) to safely exit scans.
- Colored terminal output with `colorama` for easy identification of open (green), closed (r
