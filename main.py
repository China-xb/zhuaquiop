import requests
import socket
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import re



from telegram import Bot
from telegram import Update
import re

def extract_info_from_message(message):
    # 使用正则表达式匹配IP地址和端口的模式
    ip_port_pattern = r"b(?:[0-9]{1,3}.){3}[0-9]{1,3}:d{4}b"
    # 查找所有文本中匹配IP地址和端口的部分
    ip_ports = re.findall(ip_port_pattern, message)
    return ip_ports

def write_ips_to_file(ip_ports, file_path):
    with open(file_path, 'w') as f:
        for ip_port in ip_ports:
            f.write(f"{ip_port}n")

if __name__ == "__main__":
    bot_token = "6701932453:AAE2hVVH1WGvHeLxHX-m2laWqnKgz9FD4Dg"
    channel_username = "cf_no1"
    bot = Bot(token=bot_token)
    updates = bot.get_updates(limit=3, timeout=10)

    all_ips_ports = []
    for update in updates = await bot.get_updates()
        ips_ports = extract_info_from_message(update.message.text)
        all_ips_ports.extend(ips_ports)
    write_ips_to_file(all_ips_ports, 'tg.txt')



def extract_ips_from_html(html_content):
    # 使用BeautifulSoup解析HTML内容，提取IP地址
    soup = BeautifulSoup(html_content, 'html.parser')
    # 使用正则表达式匹配IP地址的模式
    ip_pattern = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"
    # 查找所有文本中匹配IP地址模式的部分
    ips = re.findall(ip_pattern, soup.get_text())
    return ips

def scan_ports(ip):
    ports_to_scan = [443, 2053, 2087, 2083, 8443, 2096]
    for port in ports_to_scan:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(3)
            result = s.connect_ex((ip, port))
            if result == 0:
                return port
    return None

def get_ips_from_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            if "text/html" in response.headers.get("content-type", ""):
                # 如果是HTML内容，则提取其中的IP地址
                ips = extract_ips_from_html(response.content)
            else:
                # 否则按行分割文本获取IP地址
                ips = response.text.splitlines()
            return ips
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
    return "Unknown"

def convert_ips(input_urls, output_files):
    with ThreadPoolExecutor(max_workers=10) as executor:
        for input_url, output_file in zip(input_urls, output_files):
            ips = get_ips_from_url(input_url)  # 获取URL中的IP地址列表

            with open(output_file, 'w') as f:
                for ip in ips:
                    try:
                        country_code = get_location(ip)  # 获取IP地址的国家代码信息
                        open_port = scan_ports(ip)  # 扫描IP地址的开放端口
                        if open_port is not None:
                            f.write(f"{ip}:{open_port}#{country_code}\n")  # 保存带有开放端口和国家代码信息的格式
                        else:
                            if country_code == "Unknown":
                                f.write(f"{ip}#No geolocation detected\n")  # 保存未检测到地理位置的格式
                            else:
                                f.write(f"{ip}#{country_code}\n")  # 保存带有国家代码信息但未开放端口的格式
                    except Exception as e:
                        f.write(f"{ip}#Error occurred: {e}\n")  # 保存出现异常的IP地址及错误信息

if __name__ == "__main__":
    input_urls = ["https://ipdb.api.030101.xyz/?type=bestproxy", "https://ipdb.api.030101.xyz/?type=bestcf", 'https://raw.githubusercontent.com/China-xb/zidonghuaip/main/ip.txt', 'https://kzip.pages.dev/kzip.txt?token=mimausb8', 'https://addressesapi.090227.xyz/CloudFlareYes']  # 包含IP地址的txt文件的多个URL
    output_files = ["bestproxy.txt", "bestcf.txt", 'ip.txt', 'kzip.txt', 'cf.ip']
    convert_ips(input_urls, output_files)
