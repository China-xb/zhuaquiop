import requests
import socket
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

def get_ips_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        return response.text.splitlines()
    except Exception as e:
        print(f"无法从 {url} 获取IP地址：{e}")
        return []

def get_location(ip):
    try:
        response = requests.get(f"http://whois.pconline.com.cn/ipJson.jsp?ip={ip}")
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        font_element = soup.find("font")
        if font_element:
            font_content = font_element.text
            location = font_content.split('"pro": "')[1].split('"')[0] if '"pro": "' in font_content else (
                font_content.split('"city": "')[1].split('"')[0] if '"city": "' in font_content else "未知地区"
            )
            return location
        else:
            print(f"未找到IP {ip} 的字体元素")
    except Exception as e:
        print(f"获取IP {ip} 的位置时出错：{e}")
    return None

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
                        location = get_location(ip)  # 获取IP地址的地区信息
                        open_ports = []

                        if ":" in ip:
                            parts = ip.split(":")
                            ip = parts[0]
                            open_ports = [int(p) for p in parts[1].split(",")]

                        if not location:
                            location = "未知地区"

                        if not open_ports:
                            open_ports = [8443, 2053, 2083, 2087, 2096]

                        verified_ports = []
                        for port in open_ports:
                            result = scan_ports(ip, port)
                            if result:
                                verified_ports.append(result)
                                break

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
