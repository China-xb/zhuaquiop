import requests
import socket
from bs4 import BeautifulSoup

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
        response = requests.get(f"http://whois.pconline.com.cn/ipJson.jsp?ip={ip}")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            font_element = soup.find("font")
            if font_element is not None:
                font_content = font_element.text
                if '"pro": "' in font_content:
                    location = font_content.split('"pro": "')[1].split('"')[0]
                elif '"city": "' in font_content:
                    location = font_content.split('"city": "')[1].split('"')[0]
                else:
                    location = "Location information not found"
                return location
            else:
                print(f"Font element not found for IP {ip}")
    except Exception as e:
        print(f"Error fetching location for IP {ip} using http://whois.pconline.com.cn/ipJson.jsp?: {e}")

    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        if data['status'] == 'success':
            return data['countryCode']
    except Exception as e:
        print(f"Error fetching location for IP {ip} using ∗∗∗: {e}")
    return None

def scan_ports(ip):
    open_ports = []
    for port in [8443, 2053, 2083, 2087, 2096]:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((ip, port))
        if result == 0:
            open_ports.append(port)
    if not open_ports:
        open_ports.append(443)
    return open_ports

def convert_ips(input_urls, output_files):
    for input_url, output_file in zip(input_urls, output_files):
        ips = get_ips_from_url(input_url)

        with open(output_file, 'w') as f:
            for line in ips:
                # Split the line by comma and extract the required fields
                parts = line.split(',')
                if len(parts) == 3:
                    ip, port, location_info = parts
                    try:
                        socket.inet_aton(ip)
                        location = get_location(ip)
                        open_ports = scan_ports(ip)

                        # Write the formatted string to the output file
                        if location:
                            f.write(f"{ip},{port},{location}\n")
                        else:
                            f.write(f"{ip},{port},火星⭐\n")
                    except socket.error:
                        # If the IP is invalid, write the original line to the output file
                        f.write(f"{line}\n")
                else:
                    # If the line does not have the correct number of parts, write it to the output file
                    f.write(f"{line}\n")

if __name__ == "__main__":
    input_urls = ["https://ipdb.api.030101.xyz/?type=bestproxy", "https://ipdb.api.030101.xyz/?type=bestcf", 'https://raw.githubusercontent.com/China-xb/zidonghuaip/main/ip.txt', 'https://addressesapi.090227.xyz/CloudFlareYes', 'https://kzip.pages.dev/a.csv?token=mimausb8', 'https://cfno1.pages.dev/pure']  # 包含IP地址的txt文件的多个URL
    output_files = ["bestproxy.txt", "bestcf.txt", 'ip.txt', 'cfip.txt', 'kzip.txt', 'cfno1.txt']
    convert_ips(input_urls, output_files)
    
