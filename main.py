import requests
import socket

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
    for port in [443, 8443, 2053, 2087, 2083, 2096]:  # 要扫描的端口列表
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)  # 设置超时时间为1秒
        result = s.connect_ex((ip, port))
        if result == 0:  # 如果端口开放
            open_ports.append(port)
            break  # 找到开放端口后立即停止扫描其他端口
        s.close()

    if open_ports:
        return (ip, open_ports)
    else:
        return None

def convert_ips(input_urls, output_files):
    for input_url, output_file in zip(input_urls, output_files):
        ips = get_ips_from_url(input_url)  # 获取URL中的IP地址列表
        
        with open(output_file, 'w') as f:
            for ip in ips:
                scanned_result = scan_ports(ip)
                if scanned_result:
                    ip_address, open_ports = scanned_result
                    location = get_location(ip_address)
                    if location:
                        f.write(f"{ip_address}:{open_ports}#{location}\n")
                else:
                    f.write(f"{ip}\n")

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

if __name__ == "__main__":
    input_urls = ["https://ipdb.api.030101.xyz/?type=bestproxy", "https://ipdb.api.030101.xyz/?type=bestcf",
                  'https://raw.githubusercontent.com/China-xb/zidonghuaip/main/ip.txt',
                  'https://addressesapi.090227.xyz/CloudFlareYes',
                  'https://kzip.pages.dev/kzip.txt?token=mimausb8']  # 包含IP地址的txt文件的多个URL
    output_files = ["bestproxy.txt", "bestcf.txt", 'ip.txt', 'pure.txt', 'kzip.txt']

    convert_ips(input_urls, output_files)
