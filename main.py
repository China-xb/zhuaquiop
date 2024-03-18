import requests

# 修改telegram_bot_sendtext函数为telegram_bot_senddocument
def telegram_bot_senddocument(document, bot_token, bot_chatID):

    send_document = 'https://api.telegram.org/bot' + bot_token + '/sendDocument'
    files = {'document': open(document, 'rb')}
    data = {'chat_id' : bot_chatID}
    response = requests.post(send_document, files=files, data=data)

    return response.json()

def get_ips_from_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text.splitlines()
        else:
            log_message = f"Failed to fetch IPs from {url}. Status code: {response.status_code}"
            print(log_message)
            telegram_bot_sendtext(log_message, bot_token, bot_chatID)
    except Exception as e:
        log_message = f"Error fetching IPs from {url}: {e}"
        print(log_message)
        telegram_bot_sendtext(log_message, bot_token, bot_chatID)
    return []


def get_location(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        if data['status'] == 'success':
            return f"{data['country']}"
    except Exception as e:
        log_message = f"Error fetching location for IP {ip}: {e}"
        print(log_message)
        telegram_bot_sendtext(log_message, bot_token, bot_chatID)
    return None


def convert_ips(input_urls, output_files, bot_token, bot_chatID):
    for input_url, output_file in zip(input_urls, output_files):
        ips = get_ips_from_url(input_url)

        with open(output_file, 'w') as f:
            for ip in ips:
                location = get_location(ip)
                if location:
                    f.write(f"{ip}:443#{location}\n")
                else:
                    f.write(f"{ip}\n")
...
log_message = f"{output_file}文件更新完毕，已保存 {len(ips)} 条IP地址记录。"
print(log_message)
telegram_bot_senddocument(output_file, bot_token, bot_chatID)
...
if __name__ == "__main__":
    input_urls = ["https://ipdb.api.030101.xyz/?type=bestproxy", "https://ipdb.api.030101.xyz/?type=bestcf",'https://raw.githubusercontent.com/China-xb/zidonghuaip/main/ip.txt','https://addressesapi.090227.xyz/CloudFlareYes']
    output_files = ["bestproxy.txt", "bestcf.txt",'ip.txt','pure.txt']
    bot_token = '6701932453:AAE2hVVH1WGvHeLxHX-m2laWqnKgz9FD4Dg'
    bot_chatID = '1220184704'
    convert_ips(input_urls, output_files, bot_token, bot_chatID)
