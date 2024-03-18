import requests
import concurrent.futures
from functools import lru_cache

@lru_cache(maxsize=None)
def get_location(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        if data['status'] == 'success':
            return f"{data['country']} - {data['city']}"  # 更详细的地理位置描述
    except Exception as e:
        print(f"Error fetching location for IP {ip}: {e}")
    return None

def process_ip(ip):
    location = get_location(ip)
    if location:
        return f"{ip}:443#{location}\n"
    else:
        return f"{ip}\n"

def convert_ips(input_urls, output_files):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for input_url, output_file in zip(input_urls, output_files):
            ips = get_ips_from_url(input_url)

            with open(output_file, 'w') as f:
                results = list(executor.map(process_ip, ips))
                for result in results:
                    f.write(result)

if __name__ == "__main__":
    input_urls = ["https://ipdb.api.030101.xyz/?type=bestproxy", "https://ipdb.api.030101.xyz/?type=bestcf",
                  'https://raw.githubusercontent.com/China-xb/zidonghuaip/main/ip.txt',
                  'https://addressesapi.090227.xyz/CloudFlareYes',
                  'https://kzip.pages.dev/kzip.txt?token=mimausb8']
    
    output_files = ["bestproxy.txt", "bestcf.txt", 'ip.txt', 'pure.txt', 'kzip.txt']
    convert_ips(input_urls, output_files)
