import requests
from bs4 import BeautifulSoup
import telebot
import config
from tabulate import tabulate


def get_raw_menu(url):
    res = requests.get(url)
    with open("tday.html","w+") as f:
        f.write(res.text)

def get_menu_table():
    with open("tday.html") as file:
        contents = file.read()
        soup = BeautifulSoup(contents, 'lxml')
        big_table = soup.table

    result = {}
    for i in big_table.find_all("td"):
        try:
            result[i.find(class_="table_item_name").text] = i.find(class_="table_item_exit").text
        except:
            pass

    headers = ["Блюдо", "БЖУ"]
    output = tabulate(result.items(),headers)
    output = '``` {} ```'.format(output)

    return output
bot = telebot.TeleBot(config.bot_token)

@bot.message_handler(commands==["menu"])
def send_menu(message):
    get_raw_menu("https://lamantin-kafe.ru/lamantin-menu-bistro/")
    bot.send_message(message.chat.id, get_menu_table(),parse_mode="Markdown")

def main():
    bot.infinity_polling()

if __name__ == "__main__":
    main()