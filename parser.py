import csv
import json
import argparse
from collections import defaultdict
import ipaddress

def read_csv(file_path):
    devices = []
    try:
        with open(file_path, mode='r', encoding='utf-8-sig') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                ips = row.get("IP Address", "").split(',')  # Allow multiple IPs separated by commas
                name = row.get("Device Name", ips[0])  # Use first IP if name is missing
                url = row.get("URL", "")  # Optional URL field
                cidr = row.get("CIDR", "24")  # Optional CIDR field, defaults to /24
                
                for ip in ips:
                    devices.append({"name": name, "ip": ip.strip(), "cidr": cidr.strip(), "url": url})
    except Exception as e:
        print(f"Error reading CSV file: {e}")
    return devices

def group_by_ip_range(devices):
    grouped_devices = defaultdict(list)
    
    for device in devices:
        try:
            network = ipaddress.ip_network(f"{device['ip']}/{device['cidr']}", strict=False)
            grouped_devices[str(network)].append(device)
        except ValueError:
            print(f"Invalid IP Address: {device['ip']} with CIDR {device['cidr']}")
    
    return grouped_devices

def generate_gliffy_json(grouped_devices, output_file):
    gliffy_structure = {
        "stage": {
            "width": 1000,
            "height": 1000,
            "children": []
        }
    }
    
    x, y = 100, 100
    spacing = 150
    
    for network, devices in grouped_devices.items():
        for index, device in enumerate(devices):
            graphic_info = {
                "type": "com.gliffy.shape.network.cisco.Router",  # Default to Router
                "title": f"{device['name']} ({device['ip']}/{device['cidr']})",
                "description": f"Network: {network}"
            }
            
            if device["url"]:
                graphic_info["link"] = device["url"]
            
            gliffy_structure["stage"]["children"].append({
                "x": x,
                "y": y,
                "width": 120,
                "height": 60,
                "rotation": 0,
                "graphic": graphic_info
            })
            
            x += spacing
            if (index + 1) % 5 == 0:  # Move to the next row every 5 devices
                x = 100
                y += spacing
    
    with open(output_file, "w", encoding='utf-8') as json_file:
        json.dump(gliffy_structure, json_file, indent=4)
    print(f"Gliffy JSON exported to {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Convert a CSV file of IP addresses into a Gliffy JSON format, grouped by IP range.")
    parser.add_argument("-i", "--input", required=True, help="Path to input CSV file")
    parser.add_argument("-o", "--output", required=True, help="Path to output JSON file")
    args = parser.parse_args()
    
    devices = read_csv(args.input)
    grouped_devices = group_by_ip_range(devices)
    if grouped_devices:
        generate_gliffy_json(grouped_devices, args.output)
    else:
        print("No valid IP addresses found in CSV.")

if __name__ == "__main__":
    main()
