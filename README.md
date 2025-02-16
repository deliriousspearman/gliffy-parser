# CSV to Gliffy Network Diagram Converter

## Overview
This script converts a CSV file containing network devices, their IP addresses, CIDR ranges, and optional hyperlinks into a Gliffy-compatible JSON file for network diagram visualization.

## Features
- Parses a CSV file containing network devices and their corresponding IP addresses.
- Supports multiple IP addresses per device (comma-separated in CSV).
- Groups devices based on their IP range using specified CIDR.
- Allows an optional URL field to hyperlink devices in Gliffy.
- Generates a structured JSON file that can be imported into Gliffy for network visualization.
- Organizes devices in a grid layout for easy readability.

## Prerequisites
- Python 3.x

## Installation
No installation is required. Just clone or download the script and ensure Python is installed on your system.

## Usage
### Command-line Execution
```sh
python csv_to_gliffy.py -i <input_csv_file> -o <output_json_file>
```
Example:
```sh
python csv_to_gliffy.py -i network_devices.csv -o network_diagram.json
```

## CSV Format
The input CSV file should contain the following columns:
```
Device Name,IP Address,CIDR,URL (optional)
Router1,192.168.1.1,24,http://router1.local
Switch1,192.168.1.10,24,
Firewall1,192.168.1.20,26,http://firewall.local
Server1,10.0.0.1,16,http://server1.local
```
- **Device Name**: The name of the device.
- **IP Address**: One or more IP addresses (comma-separated).
- **CIDR**: The CIDR notation specifying the network range for grouping.
- **URL (optional)**: A hyperlink to the device's management interface or documentation.

## Output Format
The script generates a Gliffy-compatible JSON file structured as follows:
```json
{
    "stage": {
        "width": 1000,
        "height": 1000,
        "children": [
            {
                "x": 100,
                "y": 100,
                "width": 120,
                "height": 60,
                "rotation": 0,
                "graphic": {
                    "type": "com.gliffy.shape.network.cisco.Router",
                    "title": "Router1 (192.168.1.1/24)",
                    "description": "Network: 192.168.1.0/24",
                    "link": "http://router1.local"
                }
            }
        ]
    }
}
```

## Notes
- Ensure the CSV file uses **commas** to separate multiple IP addresses.
- If a URL is provided, it will be included as a hyperlink in the Gliffy JSON output.
- Devices are grouped based on their specified CIDR range.
- Devices with multiple IPs are duplicated in each applicable network group.
- Devices are arranged automatically in a grid layout for better visualization.

## License
This script is open-source and can be modified or redistributed freely.

## Contact
For issues or feature requests, please open a GitHub issue or contact the developer.
