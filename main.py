import requests
import socket
from bs4 import BeautifulSoup

def get_ips_from_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text.splitlines()
        else:
            print(f"无法从 {url} 获取IP地址。状态码：{response.status_code}")
    except Exception as e:
        print(f"从 {url} 获取IP地址时出错：{e}")
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
                    location = "未找到位置信息"
                return location
            else:
                print(f"未找到IP {ip} 的字体元素")
    except Exception as e:
        print(f"使用 http://whois.pconline.com.cn/ipJson.jsp? 获取IP {ip} 的位置时出错：{e}")

    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        if data['status'] == 'success':
            return data['countryCode']
    except Exception as e:
        print(f"使用 http://ip-api.com/json/ 获取IP {ip} 的位置时出错：{e}")
    return None

def scan_ports(ip):
    open_ports = []
    for port in [8443, 2053, 2083, 2087, 2096]:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)  # 设置超时时间为1秒
        result = s.connect_ex((ip, port))
        if result == 0:
            open_ports.append(port)
        s.close()  # 使用后关闭套接字
    if not open_ports:
        open_ports.append(443)
    return open_ports

def convert_ips(input_urls, output_files):
    for input_url, output_file in zip(input_urls, output_files):
        ips = get_ips_from_url(input_url)

        with open(output_file, 'w') as f:
            for ip in ips:
                try:
                    socket.inet_aton(ip)  # 检查IP地址的格式是否正确
                    location = get_location(ip)  # 获取IP地址的地区信息
                    open_ports = scan_ports(ip)  # 扫描IP地址的开放端口

                    # 将格式化后的字符串写入输出文件
                    if location:
                        f.write(f"{ip}#{location}\n")  # 更新输出格式
                    else:
                        f.write(f"{ip}#火星⭐\n")  # 如果未找到位置信息，则默认为“火星⭐”
                except socket.error:
                    # 如果IP无效，则将原始行写入输出文件
                    f.write(f"{ip}\n")
                except Exception as e:
                    print(f"处理IP {ip} 时出错：{e}")

if __name__ == "__main__":
    input_urls = ["https://ipdb.api.030101.xyz/?type=bestproxy", 
                  "https://ipdb.api.030101.xyz/?type=bestcf", 
                  'https://raw.githubusercontent.com/China-xb/zidonghuaip/main/ip.txt', 
                  'https://addressesapi.090227.xyz/CloudFlareYes', 
                  'https://kzip.pages.dev/a.csv?token=mimausb8', 
                  'https://cfno1.pages.dev/pure']  # 包含IP地址的URL列表
    output_files = ["bestproxy.txt", "bestcf.txt", 'ip.txt', 'cfip.txt', 'kzip.txt', 'cfno1.txt']
    convert_ips(input_urls, output_files)
