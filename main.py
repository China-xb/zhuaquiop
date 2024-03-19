import requests
import socket
import concurrent.futures
import functools
import os

@functools.lru_cache(maxsize=128)
def get_location(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        if data['status'] == 'success':
            return data['countryCode']
    except Exception as e:
        print(f"Error fetching location for IP {ip}: {e}")
    return "Unknown"

def scan_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((ip, port))
            if result == 0:
                return port
    except Exception as e:
        print(f"Error scanning port {port} for IP {ip}: {e}")
    return None

def scan_ports(ip):
    open_ports = []
    ports_to_scan = [443, 2053, 2087, 2083, 8443, 2096]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_port = {executor.submit(scan_port, ip, port): port for port in ports_to_scan}
        for future in concurrent.futures.as_completed(future_to_port):
            port = future_to_port[future]
            open_port = future.result()
            if open_port:
                open_ports.append(open_port)
                break  # 如果找到开放端口就停止扫描

    return open_ports

def get_ips_from_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text.splitlines()
        else:
            print(f"Failed to fetch IPs from {url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error fetching IPs from {url}: {e}")
    return []

def convert_ips(input_urls, output_files):
    for input_url, output_file in zip(input_urls, output_files):
        ips = get_ips_from_url(input_url)  # 获取URL中的IP地址列表

        with open(output_file, 'w') as f:
            for ip in ips:
                open_ports = scan_ports(ip)
                location = get_location(ip)

                if open_ports:
                    f.write(f"{ip}:{open_ports[0]}#{location}\n")
                else:
                    if location == "Unknown":
                        f.write(f"{ip}#No geolocation detected\n")
                    else:
                        f.write(f"{ip}#{location}\n")

if __name__ == "__main__":
    input_urls = ["https://ipdb.api.030101.xyz/?type=bestproxy", "https://ipdb.api.030101.xyz/?type=bestcf", 'https://raw.githubusercontent.com/China-xb/zidonghuaip/main/ip.txt', 'https://kzip.pages.dev/kzip.txt?token=mimausb8', 'https://addressesapi.090227.xyz/CloudFlareYes']  # 包含IP地址的txt文件的多个URL
    output_files = ["bestproxy.txt", "bestcf.txt", 'ip.txt', 'kzip.txt', 'cfip']

    convert_ips(input_urls, output_files)
