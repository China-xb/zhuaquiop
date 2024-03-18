import requests
from python_telegram_bot import Bot

def get_ips_from_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text.splitlines()
    except Exception as e:
        print(f"Error fetching IPs from {url}: {e}")
    return []

def get_location(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        if data['status'] == 'success':
            return data['countryCode']
    except Exception as e:
        print(f"Error fetching location for IP {ip}: {e}")
    return None

def convert_ips(input_urls, output_files, bot, chat_id):
    for input_url, output_file in zip(input_urls, output_files):
        ips = get_ips_from_url(input_url)

        with open(output_file, 'w') as f:
            for ip in ips:
                location = get_location(ip)
                if location:
                    f.write(f"{ip}:443#{location}n")
                else:
                    f.write(f"{ip}#Unknownn")
            bot.send_document(chat_id=chat_id, document=open(output_file, 'rb'))

if __name__ == "__main__":
    input_urls = ["https://ipdb.api.030101.xyz/?type=bestproxy", "https://ipdb.api.030101.xyz/?type=bestcf",'https://raw.githubusercontent.com/China-xb/zidonghuaip/main/ip.txt','https://addressesapi.090227.xyz/CloudFlareYes']
    output_files = ["bestproxy.txt", "bestcf.txt",'ip.txt','pure.txt']
    bot_token = "你的电报机器人令牌"  # 替换为你的电报机器人令牌
    chat_id = "你的电报聊天ID"  # 替换为你的电报聊天ID
    bot = Bot(token=bot_token)
    convert_ips(input_urls, output_files, bot, chat_id)
