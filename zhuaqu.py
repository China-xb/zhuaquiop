"""
必须安装的依赖包:
- requests: 发送HTTP请求
- beautifulsoup4: 解析HTML文档
安装依赖命令: pip install requests beautifulsoup4
"""

import re
import requests
from bs4 import BeautifulSoup

# 检查ip.txt文件是否存在，如果不存在则创建一个新文件
filename = "ip.txt"
try:
    with open(filename, 'x') as f:
        print(f"{filename} 文件创建成功")
except FileExistsError:
    print(f"{filename} 文件已存在")

# 整理目标URL列表
urls = ["https://monitor.gacjie.cn/page/cloudflare/ipv4.html","https://ip.164746.xyz"]

# IP正则表达式
ip_pattern = re.compile(r'b(?:[0-9]{1,3}.){3}[0-9]{1,3}b')

# 遍历URL列表
for url in urls:
    # 发送HTTP请求获取网页内容
    response = requests.get(url)
    # 使用BeautifulSoup解析HTML文档
    soup = BeautifulSoup(response.content, "html.parser")

    # 根据网站的不同结构找到包含IP地址的元素
    # 在这里我使用BeautifulSoup的 text 方法获取网页所有文本，然后用正则表达式查找IP地址
    ip_addresses = re.findall(ip_pattern, soup.text)

    # 如果找到ip地址，则写入文件ip.txt
    if ip_addresses:
        with open(filename, 'a') as f:
            for ip in ip_addresses:
                f.write(f'{ip}n')
        print(f"已成功写入 {len(ip_addresses)} 个IP地址到 {filename}")
    else:
        print(f"在 {url} 中未找到任何IP地址")
