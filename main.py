import requests
import socket
import re

def get_ipv4_addresses_from_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            ipv4_addresses = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', response.text)
            return ipv4_addresses
        else:
            print(f"Failed to fetch IPv4 addresses from {url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error fetching IPv4 addresses from {url}: {e}")
    return []

def get_location(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success':
                return f"{data['country']}"
            else:
                print(f"Error fetching location for IP {ip}: Status: {data['status']}")
        else:
            print(f"Error fetching location for IP {ip}: Status code {response.status_code}")
    except Exception as e:
        print(f"Error fetching location for IP {ip}: {e}")
    return None

def scan_ports(ip_address):
    open_ports = []
    try:
        for port in [443, 8443, 2053, 2087, 2083, 2096]:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            result = s.connect_ex((ip_address, port))
            if result == 0:
                open_ports.append(port)
                break
            s.close()
    except socket.error as e:
        print(f"Error scanning ports for IP {ip_address}: {e}")

    if open_ports:
        return (ip_address, open_ports)
    else:
        return None

def convert_ips_to_file(ip_addresses, output_file):
    with open(output_file, 'w') as f:
        for ip in ip_addresses:
            scanned_result = scan_ports(ip)
            location = get_location(ip)
            if scanned_result and location:
                ip_address, open_ports = scanned_result
                port_string = ','.join(map(str, open_ports))
                f.write(f"{ip_address}:{port_string}#{location}\n")
            elif scanned_result:
                ip_address, open_ports = scanned_result
                port_string = ','.join(map(str, open_ports))
                f.write(f"{ip_address}:{port_string}\n")
            elif location:
                f.write(f"{ip}#{location}\n")

if __name__ == "__main__":
    input_urls = ["https://example.com/ip_addresses.html", "https://anotherexample.com/ips.txt"]
    output_file = "ip_results.txt"

    all_ipv4_addresses = []
    for url in input_urls:
        ipv4_addresses = get_ipv4_addresses_from_url(url)
        all_ipv4_addresses.extend(ipv4_addresses)

    convert_ips_to_file(all_ipv4_addresses, output_file)
