import requests
import socket

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
        elif data['status'] == 'fail':
            pass  # 尝试使用备用 API
    except Exception as e:
        print(f"Error fetching location for IP {ip} using ip-api.com: {e}")

    try:
        response = requests.get(f"https://ipleak.net/json/{ip}")
        data = response.json()
        return data['country']
    except Exception as e:
        print(f"Error fetching location for IP {ip} using ipleak.net: {e}")

    return "火星star"

def scan_ports(ip):
    open_ports = []
    for port in [8443, 2053, 2083, 2087]:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((ip, port))
        if result == 0:
            open_ports.append(port)
            break
    if not open_ports:
        open_ports.append(443)
    return open_ports

def convert_ips(input_urls, output_files):
    all_ips = []  # 存储所有 IP 地址

    # 获取所有 IP 地址
    for input_url in input_urls:
        all_ips.extend(get_ips_from_url(input_url))

    # 对每个 IP 地址进行国家代码定位和端口验证
    for ip in all_ips:
        location = get_location(ip)
        open_ports = scan_ports(ip)

        # 格式化保存信息
        info = f"{ip}:{open_ports[0]}#{location}\n" if open_ports else f"{ip}#火星star\n"

        # 保存信息到对应的文件
        for output_file in output_files:
            with open(output_file, 'a') as f:
                f.write(info)

if __name__ == "__main__":
    input_urls = ["https://ipdb.api.030101.xyz/?type=bestproxy", "https://ipdb.api.030101.xyz/?type=bestcf", 'https://raw.githubusercontent.com/China-xb/zidonghuaip/main/ip.txt', 'https://addressesapi.090227.xyz/CloudFlareYes' , 'https://kzip.pages.dev/a.csv?token=mimausb8']  # 包含IP地址的多个URL
    output_files = ["bestproxy.txt", "bestcf.txt", 'ip.txt', 'cfip.txt', 'kzip.txt']
    convert_ips(input_urls, output_files)
