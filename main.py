import requests
import socket
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

def scan_ports(ip):
    ports_to_scan = [443, 2053, 2087, 2083, 8443, 2096]
    try:
        ip_address = socket.gethostbyname(ip)  # 确保IP地址是有效的
        for port in ports_to_scan:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.connect_ex((ip_address, port))
                if result == 0:
                    return port
    except (socket.gaierror, socket.timeout):
        pass
    return None

def get_ips_from_url(url):
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            return response.text.splitlines()
        else:
            print(f"Failed to fetch IPs from {url}. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching IPs from {url}: {e}")
    return []

def get_location(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=30)
        data = response.json()
        if data['status'] == 'success':
            return data['countryCode']
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Error fetching location for IP {ip}: {e}")
    return "Unknown"

# 其他部分保持不变

if __name__ == "__main__":
    input_urls = ["https://ipdb.api.030101.xyz/?type=bestproxy", "https://ipdb.api.030101.xyz/?type=bestcf", 'https://raw.githubusercontent.com/China-xb/zidonghuaip/main/ip.txt', 'https://kzip.pages.dev/kzip.txt?token=mimausb8', 'https://addressesapi.090227.xyz/CloudFlareYes']
    output_files = ["bestproxy.txt", "bestcf.txt", 'ip.txt', 'kzip.txt', 'cf.ip']
    convert_ips(input_urls, output_files)
