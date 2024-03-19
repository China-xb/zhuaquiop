import requests
import socket
from concurrent.futures import ThreadPoolExecutor
import functools

# 缓存已扫描的IP和开放端口
scanned_ips = {}

def memoize_scanned_ips(func):
    @functools.wraps(func)
    def wrapper(ip):
        if ip in scanned_ips:
            return scanned_ips[ip]
        result = func(ip)
        scanned_ips[ip] = result
        return result
    return wrapper

@memoize_scanned_ips
def scan_ports(ip):
    open_ports = []
    ports_to_scan = [443, 2053, 2087, 2083, 8443, 2096]
    
    for port in ports_to_scan:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.connect_ex((ip, port))
                if result == 0:
                    open_ports.append(port)
                    break  # 如果找到开放端口就停止扫描
        except Exception as e:
            print(f"Error scanning port {port} for IP {ip}: {e}")
    
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

def get_location(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        if data['status'] == 'success':
            return data['countryCode']
    except Exception as e:
        print(f"Error fetching location for IP {ip}: {e}")
    return "Unknown"

def convert_ip(ip, f):
    open_ports = scan_ports(ip)
    location = get_location(ip)
    if open_ports:
        f.write(f"{ip}:{open_ports[0]}#{location}\n")
    else:
        if location == "Unknown":
            f.write(f"{ip}#No geolocation detected\n")
        else:
            f.write(f"{ip}#{location}\n")

def convert_ips(input_url, output_file):
    ips = get_ips_from_url(input_url)  # 获取URL中的IP地址列表

    with open(output_file, 'w') as f:
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(convert_ip, ip, f) for ip in ips]
            for future in futures:
                try:
                    future.result()
                except Exception as e:
                    print(f"Error processing IP: {e}")

if __name__ == "__main__":
    input_urls = ["https://ipdb.api.030101.xyz/?type=bestproxy", "https://ipdb.api.030101.xyz/?type=bestcf", 'https://raw.githubusercontent.com/China-xb/zidonghuaip/main/ip.txt', 'https://kzip.pages.dev/kzip.txt?token=mimausb8', 'https://addressesapi.090227.xyz/CloudFlareYes']  # 包含IP地址的txt文件的多个URL
    output_files = ["bestproxy.txt", "bestcf.txt", 'ip.txt', 'kzip.txt', 'cf.txt']
    
    for input_url, output_file in zip(input_urls, output_files):
        convert_ips(input_url, output_file)
