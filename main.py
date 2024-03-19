import requests
import socket
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

# 扫描端口函数
def scan_ports(ip):
    ports_to_scan = [443, 2053, 2087, 2083, 8443, 2096]
    for port in ports_to_scan:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        try:
            result = s.connect_ex((ip, port))
            if result == 0:
                s.close()
                return port
            s.close()
        except socket.timeout:
            continue
    return None

# 从URL获取IP地址列表
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

# 获取地理位置信息
def get_location(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=30)
        data = response.json()
        if data['status'] == 'success':
            return data['countryCode']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching location for IP {ip}: {e}")
    return "Unknown"

# 处理单个IP地址
def process_ip(ip, output_file):
    try:
        open_port = scan_ports(ip)  # 扫描端口
        location = get_location(ip)  # 获取地理位置
        with open(output_file, 'a') as f:
            if open_port:
                f.write(f"{ip}:{open_port}#{location}\n")
            else:
                if location == "Unknown":
                    f.write(f"{ip}#No geolocation detected\n")
                else:
                    f.write(f"{ip}#{location}\n")
    except Exception as e:
        print(f"Error processing IP {ip}: {e}")

# 处理多个URL中的IP地址
def convert_ips(input_urls, output_files):
    with ThreadPoolExecutor(max_workers=5) as executor:
        for input_url, output_file in zip(input_urls, output_files):
            try:
                ips = get_ips_from_url(input_url)  # 获取URL中的IP地址列表
                for ip in ips:
                    executor.submit(process_ip, ip, output_file)  # 提交任务给线程池处理
            except Exception as e:
                print(f"Error processing URL {input_url}: {e}")

if __name__ == "__main__":
    input_urls = ["https://ipdb.api.030101.xyz/?type=bestproxy", "https://ipdb.api.030101.xyz/?type=bestcf", 'https://raw.githubusercontent.com/China-xb/zidonghuaip/main/ip.txt', 'https://kzip.pages.dev/kzip.txt?token=mimausb8', 'https://addressesapi.090227.xyz/CloudFlareYes']  # 包含IP地址的txt文件的多个URL
    output_files = ["bestproxy.txt", "bestcf.txt", 'ip.txt', 'kzip.txt', 'cf.ip']
    convert_ips(input_urls, output_files)
