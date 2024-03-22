import requests
import socket
import queue
import threading

# 创建一个队列来存储要获取国家代码的 IP 地址
ip_queue = queue.Queue()

# 创建一个线程池来获取国家代码
thread_pool = []
for i in range(50):  # 根据需要调整线程数
    thread = threading.Thread(target=get_country_code, args=(ip_queue,))
    thread_pool.append(thread)
    thread.start()

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

def get_country_code(ip_queue):
    while True:
        try:
            ip = ip_queue.get()
            location = get_location(ip)
            ip_queue.task_done()  # 标记任务完成
            if location:
                print(f"{ip}: {location}")
        except Exception as e:
            print(f"Error getting country code for IP {ip}: {e}")

def get_location(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        if data['status'] == 'success':
            return data['countryCode']
    except Exception as e:
        print(f"Error fetching location for IP {ip}: {e}")
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
                ip = line.split()[0]
                try:
                    socket.inet_aton(ip)
                except socket.error:
                    f.write(f"{line}\n")
                    continue

                ip_queue.put(ip)

        # 等待所有任务完成
        ip_queue.join()

if __name__ == "__main__":
    input_urls = ["https://ipdb.api.030101.xyz/?type=bestproxy", "https://ipdb.api.030101.xyz/?type=bestcf", 'https://raw.githubusercontent.com/China-xb/zidonghuaip/main/ip.txt', 'https://addressesapi.090227.xyz/CloudFlareYes' , 'https://kzip.pages.dev/a.csv?token=mimausb8']  # 包含IP地址的txt文件的多个URL
    output_files = ["bestproxy.txt", "bestcf.txt", 'ip.txt', 'cfip.txt', 'kzip.txt']
    convert_ips(input_urls, output_files)
