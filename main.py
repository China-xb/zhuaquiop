import requests
import socket

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

def get_location(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        if data['status'] == 'success':
            return f"{data['country']}"
    except Exception as e:
        print(f"Error fetching location for IP {ip}: {e}")
    return None

def scan_ports(ip):
    for port in range(443, 6667): 
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((ip, port))
        if result == 0:
            return port
        sock.close()
    return None

def convert_ips(input_urls, output_files):
    for input_url, output_file in zip(input_urls, output_files):
        ips = get_ips_from_url(input_url)  
        
        with open(output_file, 'w') as f:
            for ip in ips:
                port = scan_ports(ip)
                location = get_location(ip)
                if port and location:
                    f.write(f"{ip}:{port}#{location}\n")
                elif location:
                    f.write(f"{ip}:443#{location}\n")
                else:
                    f.write(f"{ip}\n")

if __name__ == "__main__":
    input_urls = ["https://ipdb.api.030101.xyz/?type=bestproxy", "https://ipdb.api.030101.xyz/?type=bestcf",
                  'https://raw.githubusercontent.com/China-xb/zidonghuaip/main/ip.txt',
                  'https://addressesapi.090227.xyz/CloudFlareYes',
                  'https://kzip.pages.dev/kzip.txt?token=mimausb8']
    
    output_files = ["bestproxy.txt", "bestcf.txt", 'ip.txt', 'pure.txt', 'kzip.txt']
    convert_ips(input_urls, output_files)
