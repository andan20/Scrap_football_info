import requests
from bs4 import BeautifulSoup
import telebot
from telebot import types


bot = telebot.TeleBot('5986190702:AAFDaHuHDXmk8f8BjMjH8O88rroazrH9oZI', parse_mode=None)

#Получение html кода странийы
def get_souped_page(page_url):
    '''
    In order not to be blocked for scraping its import to request pages with
    some settings to look more like an actual browser.

    this function takes a page_url from https://www.transfermarkt.com and returns the
    souped page
    '''



    headers = {'User-Agent':
           "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"}

    pageTree = requests.get(page_url, headers=headers)
    pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

    return(pageSoup)

#Получение биографической информации об игроке
def bio_player_pull(pageSoup):
    #Номер игрока, имя и фамилия
    player_name = pageSoup.select('h1')[0].get_text().strip()

    info = {}

    name_info = list(player_name.split())
    st = 2
    if name_info[0][0]=='#':
        number = name_info[0]
        name = name_info[1]
    else:
        number = 'no info'
        name = name_info[0]
        st = 1
    last_name = ""
    for i in range(st, len(name_info)):
        last_name += name_info[i]+" "
    info['number'] = number
    info['name'] = name
    info['last_name'] = last_name

    birthDate = pageSoup.find('div', {'class': 'data-header__details'}).find('span', {'itemprop': 'birthDate'}).text.strip()
    age = birthDate[30::].strip().replace('(', "").replace(')', "")
    birthDate = birthDate[:15].strip()
    info['birthDate'] = birthDate
    info['age'] = age

    city = pageSoup.find('div', {'class': 'data-header__details'}).find('span', {'itemprop': 'birthPlace'}).text.strip()
    info['birthCity'] = city

    nationality = pageSoup.find('div', {'class': 'data-header__details'}).find('span', {'itemprop': 'nationality'}).text.strip()
    info['nationality'] = nationality

    height = pageSoup.find('div', {'class': 'data-header__details'}).find('span', {'itemprop': 'height'}).text.strip()
    info['height'] = height

    position = pageSoup.find('div', {'class': 'data-header__details'}).find('span', {'itemprop': 'height'}).find_parent().find_next_sibling().find('span', {'class': 'data-header__content'}).text.strip()
    info['position'] = position

    try:
        agent = pageSoup.find('div', {'class': 'data-header__details'}).find('span', {'itemprop': 'height'}).find_parent().find_next_sibling().find_next_sibling().find('span').text.strip()
        info['agent'] = agent
    except:
        info['agent'] = 'no information'

    try:
        country = pageSoup.find('div', {'class': 'data-header__details'}).find('a', href=True, title=True).text.strip()
        info['country'] = country
    except:
        info['country'] = 'no information'

    cost = pageSoup.find('div', {'class': 'data-header__box--small'}).text.strip()
    info['cost'] = cost

    club = pageSoup.find('span', {'itemprop': 'affiliation'}).text.strip()
    info['club'] = club

    a = pageSoup.find('div', {'class':'data-header__club-info'}).find_all('span', {'class': 'data-header__content'})
    start = a[1].text
    finish = a[2].text
    info['startContract'] = start
    info['finishContract'] = finish

    return info


def transefers_info(pageSoup):
    history = []

    transfers = pageSoup.find('div', {'data-viewport': 'Transferhistorie'}).find_all('div', {'class': 'grid tm-player-transfer-history-grid'})

    for transfer in transfers:
        history.append({})
        history[-1]['season'] = transfer.find('div', {'class': 'grid__cell grid__cell--center tm-player-transfer-history-grid__season'}).text.strip()
        history[-1]['date'] = transfer.find('div', {'class': 'grid__cell grid__cell--center tm-player-transfer-history-grid__date'}).text.strip()
        history[-1]['oldClub'] = transfer.find('div', {'class': 'grid__cell grid__cell--center tm-player-transfer-history-grid__old-club'}).text.strip()
        history[-1]['newClub'] = transfer.find('div', {'class': 'grid__cell grid__cell--center tm-player-transfer-history-grid__new-club'}).text.strip()
        history[-1]['markeyValue'] = transfer.find('div', {'class': 'grid__cell grid__cell--center tm-player-transfer-history-grid__market-value'}).text.strip()
        history[-1]['cost'] = transfer.find('div', {'class': 'grid__cell grid__cell--center tm-player-transfer-history-grid__fee'}).text.strip()

    return history


def clubs_from_league(pageSoup):
    clubs = pageSoup.find('table', {'class': 'items'}).find('tbody').find_all('td', {'class': 'hauptlink no-border-links'})
    liga = {}
    for club in clubs:
        liga[club.text.strip()] = 'https://www.transfermarkt.com'+club.find('a').get('href')

    return liga

def players_from_club(pageSoup):
    players = pageSoup.find_all('span', {'class': 'hide-for-small'})
    club = {}
    for player in players:
        pl = player.find('a')
        x = pl.text.strip()
        if x!='':
            club[x] = 'https://www.transfermarkt.com'+pl.get('href')

    return club


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(793220243, f'{message.from_user.first_name} {message.from_user.last_name} - {message.from_user.username} - {message.text}')
    markup_leagues = types.InlineKeyboardMarkup(row_width=1)
    apl = types.InlineKeyboardButton('Английская Премьер-лига', callback_data='0www.transfermarkt.com/premier-league/startseite/wettbewerb/GB1')
    laliga = types.InlineKeyboardButton('ЛаЛига', callback_data='0www.transfermarkt.com/laliga/startseite/wettbewerb/ES1')
    bundesliga = types.InlineKeyboardButton('Бундеслига', callback_data='0www.transfermarkt.com/bundesliga/startseite/wettbewerb/L1')
    seriea = types.InlineKeyboardButton('Серия А', callback_data='0www.transfermarkt.com/serie-a/startseite/wettbewerb/IT1')
    ligueone = types.InlineKeyboardButton('Лига 1', callback_data='0www.transfermarkt.com/ligue-1/startseite/wettbewerb/FR1')
    eredevise = types.InlineKeyboardButton('Эредевизи', callback_data='0www.transfermarkt.com/eredivisie/startseite/wettbewerb/NL1')
    portu = types.InlineKeyboardButton('Лига Нос', callback_data='0www.transfermarkt.com/liga-nos/startseite/wettbewerb/PO1')
    rpl = types.InlineKeyboardButton('Российская Премьер-Лига', callback_data='0www.transfermarkt.com/premier-liga/startseite/wettbewerb/RU1')
    fnl = types.InlineKeyboardButton('ФНЛ', callback_data='0www.transfermarkt.com/1-division/startseite/wettbewerb/RU2')
    markup_leagues.add(apl, laliga, bundesliga, seriea, ligueone, eredevise, portu, rpl, fnl)

    bot.send_message(message.chat.id, 'Привет!\nЭто бот в котором ты можешь получить информацию о любом футболисте\n\nВыбери лигу👇', reply_markup=markup_leagues)

@bot.message_handler(content_types=['text'])
def ok(message):
    bot.send_message(message.chat.id, '/start')
    bot.send_message(793220243,
                     f'{message.from_user.first_name} {message.from_user.last_name} - {message.from_user.username} - {message.text}')

@bot.callback_query_handler(func=lambda call:True)
def callback1(call):
    if call.message:
        bot.send_message(793220243,f'{call.data}')
        if call.data[0]=='0':
            soup = get_souped_page('https://'+call.data[1:])
            clubs = clubs_from_league(soup)
            clubs_list = list(clubs)
            markup_clubs = types.InlineKeyboardMarkup(row_width=1)
            for club in clubs_list:
                x = len(clubs[club])
                new = types.InlineKeyboardButton(club, callback_data=('1'+clubs[club][30:x-15]))
                markup_clubs.add(new)
            bot.send_message(call.message.chat.id, 'Выбери клуб👇', reply_markup=markup_clubs)

        elif call.data[0]=='1':
            soup = get_souped_page('https://www.transfermarkt.com/' + call.data[1:])
            players = players_from_club(soup)
            players_list = list(players)
            markup_players = types.InlineKeyboardMarkup(row_width=1)
            for player in players_list:
                new = types.InlineKeyboardButton(player, callback_data=('2'+players[player][29:]))
                markup_players.add(new)
            bot.send_message(call.message.chat.id, 'Выбери игрока👇', reply_markup=markup_players)
        elif call.data[0] == '2':
            soup = get_souped_page('https://www.transfermarkt.com' + call.data[1:])
            bio_info = bio_player_pull(soup)
            transfer_history = transefers_info(soup)
            bot.send_message(call.message.chat.id, 'Биографическая информация👇')
            bot.send_message(call.message.chat.id, f'''Игровой номер: {bio_info['number']}\n
Имя: {bio_info['name']}\n
Фамилия: {bio_info['last_name']}\n
Дата рождения: {bio_info['birthDate']}\n
Возраст: {bio_info['age']}\n
Город рождения: {bio_info['birthCity']}\n
Национальность: {bio_info['nationality']}\n
Рост: {bio_info['height']}\n
Позиция: {bio_info['position']}\n
Агент: {bio_info['agent']}\n
Игрок сборной: {bio_info['country']}\n
Рыночная стоимость: {bio_info['cost']}\n
Клуб: {bio_info['club']}\n
В клубе с: {bio_info['startContract']}\n
Контракт до: {bio_info['finishContract']}
''')
            bot.send_message(call.message.chat.id, 'Информация о переходах👇')
            for tr in transfer_history:
                bot.send_message(call.message.chat.id, f'''Сезон: {tr['season']}\n
Дата: {tr['date']}\n
Из: {tr['oldClub']}\n
В: {tr['newClub']}\n
Рыночная стоимость: {tr['markeyValue']}\n
Цена трансфера: {tr['cost']}\n
''')


bot.infinity_polling()