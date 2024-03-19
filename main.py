import requests

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

def verify_ports(ip, ports):
    for port in ports:
        try:
            response = requests.get(f"http://{ip}:{port}")
            if response.status_code in (200, 443, 8443, 2053, 2083, 2087, 2096):
                return port
        except Exception:
            continue
    return None

def convert_ips(input_urls, output_files, ports):
    for input_url, output_file in zip(input_urls, output_files):
        ips = get_ips_from_url(input_url)

        with open(output_file, 'w') as f:
            for ip in ips:
                location = get_location(ip.split(':')[0])  # 获取IP地址的位置，忽略端口（如果有）
                port = ip.split(':')[-1] if ':' in ip else verify_ports(ip, ports)
                if location and port:
                    # IP地址已经包含端口，直接写入文件
                    f.write(f"{ip}:{port}#{location}n")
                elif location:
                    # IP地址没有端口，但是位置已知，写入文件
                    f.write(f"{ip}#Unknownn")

if __name__ == "__main__":
    input_urls = ["https://ipdb.api.030101.xyz/?type=bestproxy", "https://ipdb.api.030101.xyz/?type=bestcf", 'https://raw.githubusercontent.com/China-xb/zidonghuaip/main/ip.txt', 'https://addressesapi.090227.xyz/CloudFlareYes' , 'https://kzip.pages.dev/kzip.txt?token=mimausb8']
    output_files = ["bestproxy.txt", "bestcf.txt", 'ip.txt', 'cfip.txt', 'kzip.txt']
    ports = [443, 8443, 2053, 2083, 2087, 2096]
    convert_ips(input_urls, output_files, ports)
