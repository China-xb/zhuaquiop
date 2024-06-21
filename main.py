import os
import glob
import geoip2.database
import requests
from bs4 import BeautifulSoup

# 读取IPv4地址的文件
def read_ips(filename):
    try:
        with open(filename, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"The file {filename} was not found.")
        return []

# 使用geoip2获取IP的国家代码，如果失败则使用备用方法
def get_country_code(ip, reader):
    try:
        response = reader.country(ip)
        return response.country.iso_code
    except Exception as e:
        print(f"Error fetching data for IP {ip}: {e}")
        return get_location(ip)  # 使用备用方法获取国家代码

# 使用whois.pconline.com.cn和ip-api.com获取IP的地理位置信息
def get_location(ip):
    try:
        response = requests.get(f"http://whois.pconline.com.cn/ipJson.jsp?ip={ip}")
        if response.status_code == 200:
            data = response.json()
            if 'err' not in data or data['err'] == "":
                return data['proCode']  # 返回省代码作为国家代码的替代
            else:
                print(f"Error fetching location for IP {ip} using whois.pconline.com.cn: {data['err']}")
    except Exception as e:
        print(f"Error fetching location for IP {ip} using http://whois.pconline.com.cn/ipJson.jsp?: {e}")

    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        if data['status'] == 'success':
            return data['countryCode']
    except Exception as e:
        print(f"Error fetching location for IP {ip} using ip-api.com: {e}")

    return 'Unknown'  # 如果两个API都失败，则返回Unknown

# 保存IP到对应的国家代码文件，并去除重复的IP地址
def save_ip_to_file(ip, country_code):
    if ip and country_code:  # 确保IP和国家代码有效
        filename = f'{country_code}.txt'
        # 确保文件存在，如果不存在则创建
        if not os.path.exists(filename):
            open(filename, 'w').close()
        # 打开文件并检查IP地址是否已经存在
        with open(filename, 'r') as file:
            if ip + '\n' not in file.readlines():
                # 如果IP地址不存在，则写入
                with open(filename, 'a') as file:
                    file.write(ip + '\n')

# 删除所有.txt文件，除了特定的文件
def delete_existing_country_files(exceptions):
    for file in glob.glob('*.txt'):
        if file not in exceptions:
            try:
                os.remove(file)
            except OSError as e:
                print(f"Error deleting file {file}: {e}")

# 主函数
def main():
    # 指定不删除的文件列表
    exceptions = ['requirements.txt', 'dns_result.txt', 'Fission_domain.txt', 'Fission_ip.txt']

    # 删除所有现有的.txt文件，除了指定的文件
    delete_existing_country_files(exceptions)

    # 指定GeoLite2数据库文件的路径
    database_path = 'GeoLite2-Country.mmdb'
    with geoip2.database.Reader(database_path) as reader:
        ips = read_ips('Fission_ip.txt')
        for ip in ips:
            country_code = get_country_code(ip, reader)
            save_ip_to_file(ip, country_code)

if __name__ == '__main__':
    main()
