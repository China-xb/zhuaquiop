import requests
import socket
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache

@lru_cache(maxsize=None)
def get_location(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        if data['status'] == 'success':
            return f"{data['country']}"
    except Exception as e:
        print(f"Error fetching location for IP {ip}: {e}")
    return None

def scan_ports(ip):
    open_ports = []
    for port in range(443, 6667):  # 扫描443至6666端口
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)  # 设置超时时间为1秒
        result = s.connect_ex((ip, port))
        if result == 0:
            open_ports.append(port)
        s.close()
    return open_ports

def process_ip(ip):
    ports = scan_ports(ip)
    location = get_location(ip)
    if ports and location:
        return f"{ip}:{ports}#{location}\n"
    elif location:
        return f"{ip}:443#{location}\n"
    else:
        return f"{ip}\n"

def convert_ips(input_urls, output_files):
    with ThreadPoolExecutor() as executor:
        for input_url, output_file in zip(input_urls, output_files):
            ips = get_ips_from_url(input_url)
            results = list(executor.map(process_ip, ips))
            
            with open(output_file, 'w') as f:
                for result in results:
                    f.write(result)

if __name__ == "__main__":
    # 定义 get_ips_from_url 函数获取IP地址列表
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

    input_urls = ["https://ipdb.api.030101.xyz/?type=bestproxy", "https://ipdb.api.030101.xyz/?type=bestcf",
                  'https://raw.githubusercontent.com/China-xb/zidonghuaip/main/ip.txt',
                  'https://addressesapi.090227.xyz/CloudFlareYes',
                  'https://kzip.pages.dev/kzip.txt?token=mimausb8']
    
    output_files = ["bestproxy.txt", "bestcf.txt", 'ip.txt', 'pure.txt', 'kzip.txt']
    convert_ips(input_urls, output_files)
