import re
import requests
import socket

def get_ips_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text.splitlines()
    else:
        print(f"Failed to fetch IPs from {url}. Status code: {response.status_code}")
    return []

def get_country_from_ipleak(ip):
    url = "https://ipleak.net/"
    response = requests.get(url, proxies={"http": f"http://{ip}:8080", "https": f"https://{ip}:8080"})
    if response.status_code == 200:
        html = response.text
        country_code = None
        try:
            country_element = re.search(r'<span class="flag-icon flag-icon-([a-zA-Z]+)"', html)
            if country_element:
                country_code = country_element.group(1).upper()
            else:
                print(f"Failed to extract country code from {url}. Country code not found.")
        except IndexError:
            print(f"Failed to extract country code from {url}. Country code not found.")
        return country_code
    else:
        print(f"Failed to fetch country from {url}. Status code: {response.status_code}")
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
    for input_url, output_file in zip(input_urls, output_files):
        ips = get_ips_from_url(input_url)

        with open(output_file, 'w') as f:
            for line in ips:
                ip = line.split()[0]
                try:
                    socket.inet_aton(ip)
                except socket.error:
                    f.write(f"{line}\n")
                    continue

                open_ports = scan_ports(ip)
                country_code = get_country_from_ipleak(ip)
                f.write(f"{ip}:{open_ports[0]}#{country_code}\n")

if __name__ == "__main__":
    input_urls = ["https://ipdb.api.030101.xyz/?type=bestproxy", "https://ipdb.api.030101.xyz/?type=bestcf", 'https://raw.githubusercontent.com/China-xb/zidonghuaip/main/ip.txt', 'https://addressesapi.090227.xyz/CloudFlareYes' , 'https://kzip.pages.dev/kzip.txt?token=mimausb8']  # 包含 IP 地址的 txt 文件的多个 URL
    output_files = ["bestproxy.txt", "bestcf.txt", 'ip.txt', 'cfip.txt', 'kzip.txt']
    convert_ips(input_urls, output_files)
