import requests
import socket
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import geoip2.database

# 初始化 GeoIP 数据库
reader = geoip2.database.Reader('GeoLite2-City.mmdb')

def get_ips_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        return response.text.splitlines()
    except Exception as e:
        print(f"无法从 {url} 获取IP地址：{e}")
        return []

def scan_ports(ip, port):
    try:
        with socket.create_connection((ip, port), timeout=1) as s:
            return port
    except (socket.timeout, socket.error):
        return None

def convert_ips(input_urls, output_files):
    with ThreadPoolExecutor(max_workers=5) as executor:
        for input_url, output_file in zip(input_urls, output_files):
            ips = get_ips_from_url(input_url)
            with open(output_file, 'w') as f:
                for ip in ips:
                    try:
                        socket.inet_aton(ip)  # 检查IP地址的格式是否正确
                        open_ports = []

                        if ":" in ip:
                            parts = ip.split(":")
                            ip = parts[0]
                            open_ports = [int(p) for p in parts[1].split(",")]

                        if not open_ports:
                            open_ports = [8443, 2053, 2083, 2087, 2096]

                        verified_ports = []
                        for port in open_ports:
                            result = scan_ports(ip, port)
                            if result:
                                verified_ports.append(result)
                                break

                        # 使用 GeoIP 进行地区获取
                        try:
                            response = reader.city(ip)
                            location = response.country.iso_code if response.country.iso_code else "未知地区"
                        except Exception as e:
                            print(f"Error fetching location for IP {ip} using GeoIP: {e}")
                            location = "未知地区"

                        f.write(f"{ip}:{','.join(map(str, verified_ports))}#{location}\n")  # 更新输出格式
                    except socket.error:
                        # 如果IP无效，则将原始行写入输出文件
                        f.write(f"{ip}\n")
                    except Exception as e:
                        print(f"处理IP {ip} 时出错：{e}")

if __name__ == "__main__":
    input_urls = [
        "https://ipdb.api.030101.xyz/?type=bestproxy", 
        "https://ipdb.api.030101.xyz/?type=bestcf", 
        'https://raw.githubusercontent.com/China-xb/zidonghuaip/main/ip.txt', 
        'https://addressesapi.090227.xyz/CloudFlareYes', 
        'https://kzip.pages.dev/a.csv?token=mimausb8', 
        'https://cfno1.pages.dev/pure'
    ]  # 包含IP地址的URL列表
    output_files = ["bestproxy.txt", "bestcf.txt", 'ip.txt', 'cfip.txt', 'kzip.txt', 'cfno1.txt']
    convert_ips(input_urls, output_files)
