import requests
from bs4 import BeautifulSoup
import re
import os

# 目标URL列表
urls = ['https://monitor.gacjie.cn/page/cloudflare/ipv4.html', 
        'https://ip.164746.xyz']

# 正则表达式用于匹配IP地址
ip_pattern = r"d{1,3}.d{1,3}.d{1,3}.d{1,3}"

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
        # 这个部分可能需要针对实际网页布局进行修改
        elements = soup.find_all('tr')

        # 遍历所有元素,查找IP地址
        for element in elements:
            element_text = element.get_text()
            ip_matches = re.findall(ip_pattern, element_text)
            
            # 如果找到IP地址
            for ip in ip_matches:
                # 写入IP地址
                file.write(ip + 'n')

print('IP地址已保存到ip.txt文件中。')
