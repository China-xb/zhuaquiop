import requests
import socket

def get_location(ip):
    try:
        # 尝试使用 ip-api.com 获取国家代码
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        if data['status'] == 'success':
            return data['countryCode']
    except Exception as e:
        print(f"Error fetching location for IP {ip} using ip-api.com: {e}")

    try:
        # 如果 ip-api.com 获取不成功，则使用 ipleak.net 获取国家代码
        response = requests.get("https://ipleak.net/json")
        data = response.json()
        return data['country_code']
    except Exception as e:
        print(f"Error fetching location for IP {ip} using ipleak.net: {e}")

    return None

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
    unique_ips = set()  # 使用集合来存储唯一的 IP 地址

    for input_url in input_urls:
        ips = get_ips_from_url(input_url)
        unique_ips.update(ips)  # 添加新IP地址到集合中

    for output_file in output_files:
        with open(output_file, 'w') as f:
            for ip in unique_ips:
                try:
                    socket.inet_aton(ip)  # 检查IP地址格式是否正确
                except socket.error:
                    f.write(f"{ip}\n")  # IP地址格式不正确，直接保存原文
                    continue

                location = get_location(ip)
                if location:
                    open_ports = scan_ports(ip)
                    f.write(f"{ip}:{open_ports[0]}#{location}\n")
                else:
                    f.write(f"{ip}:443#火星⭐\n")

if __name__ == "__main__":
    input_urls = ["https://ipdb.api.030101.xyz/?type=bestproxy", "https://ipdb.api.030101.xyz/?type=bestcf", 'https://raw.githubusercontent.com/China-xb/zidonghuaip/main/ip.txt', 'https://addressesapi.090227.xyz/CloudFlareYes' , 'https://kzip.pages.dev/a.csv?token=mimausb8']  # 包含IP地址的txt文件的多个URL
    output_files = ["bestproxy.txt", "bestcf.txt", 'ip.txt', 'cfip.txt', 'kzip.txt']
    convert_ips(input_urls, output_files)
