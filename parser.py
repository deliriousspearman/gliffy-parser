import csv
import json
import argparse

def read_csv(file_path):
    devices = {}
    try:
        with open(file_path, mode='r', encoding='utf-8-sig') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                ips = row.get("IP Address", "").split(',')  # Allow multiple IPs separated by commas
                name = row.get("Device Name", ips[0])  # Use first IP if name is missing
                url = row.get("URL", "")  # Optional URL field
                
                if name not in devices:
                    devices[name] = {"name": name, "ips": [], "url": url}
                
                devices[name]["ips"].extend(ips)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
    return list(devices.values())

def generate_gliffy_json(devices, output_file):
    gliffy_structure = {
        "stage": {
            "width": 1000,
            "height": 1000,
            "children": []
        }
    }
    
    x, y = 100, 100
    spacing = 150
    
    for index, device in enumerate(devices):
        graphic_info = {
            "type": "com.gliffy.shape.network.cisco.Router",  # Default to Router
            "title": device["name"],
            "description": f"IPs: {', '.join(device['ips'])}"
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
    parser = argparse.ArgumentParser(description="Convert a CSV file of IP addresses into a Gliffy JSON format.")
    parser.add_argument("input_csv", help="Path to input CSV file")
    parser.add_argument("output_json", help="Path to output JSON file")
    args = parser.parse_args()
    
    devices = read_csv(args.input_csv)
    if devices:
        generate_gliffy_json(devices, args.output_json)
    else:
        print("No valid IP addresses found in CSV.")

if __name__ == "__main__":
    main()
