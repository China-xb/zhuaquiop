原有的代码每次找到一个 IP 地址后，就直接把它写入文件。如果你想在每个 IP 后面附加端口号和位置信息，需要先获取这些信息，然后再一并写入文件。
注意，你的目标 URL（urls）列表包括两个网站，可能每个网站提供的信息格式及位置都不同，所以需要针对不同的网站解析不同的结构。将这些步骤进行修改，你可以得到下面这样的代码：

import requests
from bs4 import BeautifulSoup
import re
import os

# 目标URL列表
urls = ['https://monitor.gacjie.cn/page/cloudflare/ipv4.html', 
        'https://ip.164746.xyz'
        ]

# 正则表达式用于匹配IP地址
ip_pattern = r'd{1,3}.d{1,3}.d{1,3}.d{1,3}'

# 检查ip.txt文件是否存在, 如果存在则删除它
if os.path.exists('ip.txt'):
    os.remove('ip.txt')

# 创建一个文件来存储IP地址
with open('ip.txt', 'w') as file:
    for url in urls:
        # 发送HTTP请求获取网页内容
        response = requests.get(url)
        
        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 根据网站的不同结构找到包含IP地址的元素
        if url == 'https://monitor.gacjie.cn/page/cloudflare/ipv4.html':
            elements = soup.find_all('tr')
        elif url == 'https://ip.164746.xyz':
            elements = soup.find_all('tr')
        else:
            elements = soup.find_all('li')

        # 遍历所有元素,查找IP地址
        for element in elements:
            elementtext = element.gettext()
            ipmatches = re.findall(ippattern, element_text)
            
            # 如果找到IP地址
            for ip in ip_matches:
                # 获取端口信息，此处假设端口信息与IP在同一元素中，且位于IP后，以':'分隔
                portinfo = elementtext.split(ip + ':')-1
                # 获取位置信息，此处假设位置信息与IP在同一元素中，且在字符串尾部
                locationinfo = elementtext.split()-1

                # 将IP, 端口和位置信息一并写入文件
                file.write(ip + ':' + portinfo + ' ' + locationinfo + 'n')

print('IP地址已保存到ip.txt文件中。')

我想强调的是，所有的假设（如端口和位置信息的位置及其与IP的关系）可能需要根据你要爬取的网站的实际内容进行调整。你应该检查这些网站，确定他们是如何在HTML中布局这些信息的，并且可能需要对BeautifulSoup的用法进行更深入的学习，以便更好地解析这些网页。
