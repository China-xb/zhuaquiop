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
    open_port = None
    for port in range(443, 6001):  # 扫描443至6000端口
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)  # 设置超时时间为1秒
        result = s.connect_ex((ip, port))
        if result == 0:  # 如果端口开放
            open_port = port
            break
        s.close()

    if open_port:
        return f"{ip}:{open_port}"
    else:
        return f"{ip}:443"  # 没有开放端口则默认为443端口

def process_ip(ip):
    scanned_result = scan_ports(ip)
    ip_address, port = scanned_result.split(':')
    location = get_location(ip_address)

    if '#' in scanned_result:
        return f"{scanned_result}#{location}\n"
    elif location:
        return f"{ip_address}:{port}#{location}\n"
    else:
        return "\n"

def convert_ips(input_urls, output_files):
    with ThreadPoolExecutor(max_workers=64) as executor:
        for input_url, output_file in zip(input_urls, output_files):
            ips = get_ips_from_url(input_url)  # 获取URL中的IP地址列表
            results = list(executor.map(process_ip, ips))

            with open(output_file, 'w') as f:
                for result in results:
                    f.write(result)

if __name__ == "__main__":
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
                  'https://kzip.pages.dev/kzip.txt?token=mimausb8']  # 包含IP地址的txt文件的多个URL
    output_files = ["bestproxy.txt", "bestcf.txt", 'ip.txt', 'pure.txt', 'kzip.txt']

    convert_ips(input_urls, output_files)
