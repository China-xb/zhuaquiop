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
            print(f"无法从 {url} 获取IPv4地址。状态码: {response.status_code}")
    except Exception as e:
        print(f"获取来自 {url} 的IPv4地址时发生错误：{e}")
    return []

def get_location(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success':
                return f"{data['country']}"
            else:
                print(f"获取IP {ip} 的位置信息时出错：状态: {data['status']}")
        else:
            print(f"获取IP {ip} 的位置信息时出错：状态码 {response.status_code}")
    except Exception as e:
        print(f"获取IP {ip} 的位置信息时出错：{e}")
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
            s.close()
    except socket.error as e:
        print(f"扫描IP {ip_address} 的端口时出错：{e}")

    return open_ports

def convert_ips_to_file(ip_addresses, output_file):
    with open(output_file, 'w') as f:
        for ip in ip_addresses:
            open_ports = scan_ports(ip)
            location = get_location(ip)
            
            if location:
                if open_ports:
                    port_string = ','.join(map(str, open_ports))
                    f.write(f"{ip}:{port_string}#{location}\n")
                else:
                    f.write(f"{ip}#{location}\n")
            else:
                if open_ports:
                    port_string = ','.join(map(str, open_ports))
                    f.write(f"{ip}:{port_string}\n")

if __name__ == "__main__":
    input_urls = ["https://example.com/ip_addresses.html", "https://anotherexample.com/ips.txt"]
    output_file = "ip_results.txt"

    all_ipv4_addresses = []
    for url in input_urls:
        ipv4_addresses = get_ipv4_addresses_from_url(url)
        all_ipv4_addresses.extend(ipv4_addresses)

    convert_ips_to_file(all_ipv4_addresses, output_file)
