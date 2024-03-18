import asyncio
import aiohttp
import socket
from functools import lru_cache

@lru_cache(maxsize=1024)  # 调整缓存大小为1024，根据实际情况调整最佳值
async def get_location(ip):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://ip-api.com/json/{ip}") as response:
                data = await response.json()
                if data['status'] == 'success':
                    return f"{data['country']}"
    except Exception as e:
        print(f"Error fetching location for IP {ip}: {e}")
    return None

async def scan_ports(ip):
    open_port = None
    for port in range(443, 6001):  # 扫描443至6000端口
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)  # 设置超时时间为1秒
        result = s.connect_ex((ip, port))
        if result == 0:  # 如果端口开放
            open_port = port
            break
        s.close()

    if open_port:
        return f"{ip}:{open_port}"
    else:
        return f"{ip}:443"  # 没有开放端口则默认为443端口

async def process_ip(ip):
    scanned_result = await scan_ports(ip)
    ip_address, port = scanned_result.split(':')
    location = await get_location(ip_address)

    if '#' in scanned_result:
        return f"{scanned_result}#{location}\n"
    elif location:
        return f"{ip_address}:{port}#{location}\n"
    else:
        return "\n"

async def convert_ips(input_urls, output_files):
    tasks = []
    for input_url, output_file in zip(input_urls, output_files):
        async with aiohttp.ClientSession() as session:
            ips = await get_ips_from_url(session, input_url)  # 获取URL中的IP地址列表
            tasks.extend([process_ip(ip) for ip in ips])

    results = await asyncio.gather(*tasks)

    for idx, result in enumerate(results):
        output_file = output_files[idx % len(output_files)]
        with open(output_file, 'a') as f:
            f.write(result)

async def get_ips_from_url(session, url):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                return (await response.text()).splitlines()
            else:
                print(f"Failed to fetch IPs from {url}. Status code: {response.status}")
    except Exception as e:
        print(f"Error fetching IPs from {url}: {e}")
    return []

if __name__ == "__main__":
    input_urls = ["https://ipdb.api.030101.xyz/?type=bestproxy", "https://ipdb.api.030101.xyz/?type=bestcf",
                  'https://raw.githubusercontent.com/China-xb/zidonghuaip/main/ip.txt',
                  'https://addressesapi.090227.xyz/CloudFlareYes',
                  'https://kzip.pages.dev/kzip.txt?token=mimausb8']  # 包含IP地址的txt文件的多个URL
    output_files = ["bestproxy.txt", "bestcf.txt", 'ip.txt', 'pure.txt', 'kzip.txt']

    asyncio.run(convert_ips(input_urls, output_files), max_workers=50)
