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
    except Exception as e:
        print(f"Error fetching location for IP {ip}: {e}")
    return None

def scan_ports(ip, ports):
    for port in ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)  # 设置超时时间为1秒
        result = s.connect_ex((ip, port))
        s.close()
        if result == 0:
            return port
    return 443  # 如果所有端口都未开放，默认使用443端口

def convert_ips(input_urls, output_files, ports):
    for input_url, output_file in zip(input_urls, output_files):
        ips = get_ips_from_url(input_url)

        with open(output_file, 'w') as f:
            for ip in ips:
                ip_parts = ip.split(':')
                ip_address = ip_parts[0]
                ip_port = int(ip_parts[1]) if len(ip_parts) > 1 else scan_ports(ip_address, ports)
                
                location = get_location(ip_address)
                if location is not None:
                    f.write(f"{ip_address}:{ip_port}#{location}\n")
                else:
                    f.write(f"{ip_address}:{ip_port}#Unknown\n")

if __name__ == "__main__":
    input_urls = ["https://ipdb.api.030101.xyz/?type=bestproxy", "https://ipdb.api.030101.xyz/?type=bestcf", 'https://raw.githubusercontent.com/China-xb/zidonghuaip/main/ip.txt', 'https://addressesapi.090227.xyz/CloudFlareYes' , 'https://kzip.pages.dev/kzip.txt?token=mimausb8']
    output_files = ["bestproxy.txt", "bestcf.txt", 'ip.txt', 'cfip.txt', 'kzip.txt']
    ports = [443, 8443, 2053, 2083, 2087, 2096]
    convert_ips(input_urls, output_files, ports)
