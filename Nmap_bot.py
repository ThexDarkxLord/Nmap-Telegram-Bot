import telebot
import threading
import socket
import time
import requests
import whois
import builtwith
import tldextract
from bs4 import BeautifulSoup
import re
#Made By The Dark Lord
bot_token = "ur telegram bot token"
bot = telebot.TeleBot(bot_token)

def scan_ports_and_vulnerabilities(target, ports, chat_id):
    open_ports = []
    vulnerabilities = []

    ports_to_scan = [19, 20, 21, 22, 23, 24, 25, 80, 53, 111, 110, 443, 8080, 139, 445, 512, 513, 514, 4444, 2049, 1524, 3306, 5900]


    ip_address = socket.gethostbyname(target)

    start_time = time.time()

    for port in ports_to_scan:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.1)
                result = s.connect_ex((target, port))
                if result == 0:

                    service = socket.getservbyport(port)
                    open_ports.append((port, service))
                    if port == 22:
                        vulnerabilities.append("● SSH brute-force vulnerability")
                    if port == 21:
                        vulnerabilities.append("● ftb brute-force vulnerability")

        except Exception as e:
            print(f"Error scanning port {port}: {e}")


    end_time = time.time()


    scan_time = end_time - start_time
    # Made By The Dark Lord
    response_message = f"● Scan results for {target} \n● (IP: {ip_address})\n"

    if open_ports:
        response_message += "● Open ports :\n"
        for port, service in open_ports:
            response_message += f'''\t\t\t\t\t\t● 𝙿𝚘𝚛𝚝  : {port} •  \t\t𝚂𝚎𝚛𝚟𝚒𝚌𝚎  : {service}\n'''
    else:
        response_message += "● No open ports found.\n"
    # Made By The Dark Lord
    cl = requests.head('https://' + target)
    het = cl.headers
    if 'server' in het and 'cloudflare' in het['server'].lower():
        response_message += '\n● Website Use CloudFlare'
    else:
        response_message += '\n● Website Dont Use CloudFlare'


    if vulnerabilities:
        response_message += "\n● Vulnerabilities :\n"
        for vuln in vulnerabilities:
            response_message += f"● {vuln}\n"
    else:
        response_message += '''
● 𝙉𝙤 𝙫𝙪𝙡𝙣𝙚𝙧𝙖𝙗𝙞𝙡𝙞𝙩𝙞𝙚𝙨 𝙛𝙤𝙪𝙣𝙙. \n'''

    hidden_paths = retrieve_hidden_paths(target)
    if hidden_paths:
        response_message += f"\n● 𝙷𝚒𝚍𝚍𝚎𝚗 𝚙𝚊𝚝𝚑𝚜 𝚏𝚘𝚛 {target}:\n"
        for path in hidden_paths:
            response_message += f"\t\t\t\t\t\t● {path}\n"
    else:
        response_message += "\n● No hidden paths found.\n"

    who = whois.whois(target)
    try:
        Rs = builtwith.parse('https://' + target)
    except:
        try:
            Rs = builtwith.parse('http://' + target)
        except:
            Rs = "Unknown (Failed to parse technologies)"

    try:
        tly = tldextract.extract(target).domain
    except:
        pass

    response_message += f'''● 𝙿𝚛𝚘𝚐𝚛𝚊𝚖𝚖𝚒𝚗𝚐 𝚕𝚊𝚗𝚐𝚞𝚊𝚐𝚎𝚜 ●\n
\t\t\t\t\t\t● {Rs}\n
● ㄒ卂尺Ꮆ乇ㄒ 丨几千ㄖ ●\n
\t\t\t\t\t\t● {who}\n'''

    #Made By The Dark Lord
    emails = extract_emails(f"https://{target}")
    if emails:
        response_message += "\n\n● 𝙴𝚖𝚊𝚒𝚕𝚜 𝙵𝚘𝚞𝚗𝚍 :\n"
        for email in emails:
            response_message += f'\t\t\t\t\t\t● {email}\n'
    else:
        response_message +=f'● No emails found on the page.'

    bot.send_message(chat_id, response_message)

def retrieve_hidden_paths(target):
    hidden_paths = []
    try:
        response = requests.get(f"https://{target}")
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a', href=True)
        for link in links:
            href = link['href']
            if href.startswith("/"):
                hidden_paths.append(href)
    except Exception as e:
        print(f"Error retrieving hidden paths: {e}")
    return hidden_paths

def extract_emails(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            content = response.text
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(email_pattern, content)
            return emails
        else:
            print(f"Failed to fetch content from {url}")
            return []
    except Exception as e:
        print(f"Error: {e}")
        return []

#Made By The Dark Lord
@bot.message_handler(commands=['start'])
def send_welcome(message):
    owner_button = telebot.types.InlineKeyboardButton(text='Owner', url="t.me/ThexDarkxLord")
    channel1_button = telebot.types.InlineKeyboardButton(text='Info Me 🚸', url="t.me/DARK_LORD_INFO")
    channel2_button = telebot.types.InlineKeyboardButton(text='Cyber Adex', url="t.me/Cyber_Adex")
    keyboard_markup = telebot.types.InlineKeyboardMarkup()
    keyboard_markup.add(owner_button, channel1_button, channel2_button)

    #Made By The Dark Lord
    bot.send_photo(message.chat.id, "https://t.me/DARK_LORD_INFO/5", caption=f"""
 ● Welcome {message.from_user.first_name} to the Nmap Bot!
● Send Domain Only .!!!
● : [ Owner ](t.me/ThexDarkxLord)
    """, parse_mode="markdown", reply_markup=keyboard_markup)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:

        target, *ports = message.text.split()
        ports = [int(port) for port in ports]
        # Made By The Dark Lord
        scanning_message = bot.send_message(message.chat.id, f"● Scanning ports and vulnerabilities for {target} ...")
        bot.send_chat_action(message.chat.id, 'typing')
        time.sleep(1)
        bot.delete_message(message.chat.id, scanning_message.message_id)
        threading.Thread(target=scan_ports_and_vulnerabilities, args=(target, ports, message.chat.id)).start()

    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")

bot.polling()
#Made By The Dark Lord