import telebot
import sqlite3
from PIL import Image, ImageDraw
import random

my_bot = telebot.TeleBot('5271306123:AAH-6pDgj1-PVOZnHzrV9WSVNtiNPhLymb4')

game_run, name_will_get, password_will_get, name_enter, password_enter = False, False, False, False, False
change_save, movement, dice_flag = 'not', 'player', False
flag_starve, dont_starve, dont_starve2, flag_starve2, can = False, False, False, False, False
id = 0000000000000

board_field = [

    ['w1', 'w2', 'w3', 'w4', 'w5', 'w6', 'w7', 'w8', 'w9', 'w10', 'w11', 'w12', 'w13', 'w14', 'w15'],
    ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],

    ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'b10', 'b11', 'b12', 'b13', 'b14', 'b15']

]


@my_bot.message_handler(commands=['start'])
def start_com(mess):
    global name_will_get, password_will_get, id
    name_will_get, password_will_get = False, False
    msg = f'<i>Привет</i>, {mess.from_user.first_name}!'
    my_bot.send_message(mess.chat.id, msg, parse_mode='html')
    id = mess.chat.id


@my_bot.message_handler(commands=['help', 'Help'])
def help_com(mess):
    mark = telebot.types.InlineKeyboardMarkup()
    mark.add(telebot.types.InlineKeyboardButton('Правила игры',
                                                url='https://selosovetov.ru/2016/11/25/dlinnye-nardy/'))
    mark.add(telebot.types.InlineKeyboardButton('Создатель бота', url='https://t.me/ds791358'))

    msg = f'Вы можете: \n' \
          f'Начать новую игру /Newgame\n' \
          f'Остановить игру и сдаться /Stopgame\n' \
          f'Посмотреть статистику /Stat\n' \
          f'Выйти из аккаунта /Quit\n' \
          'Во время игры все команды, кроме остановки и помощи будут проигнорированны. Рекомендуется пользоваться' \
          ' кнопками.'
    my_bot.send_message(mess.chat.id, msg, parse_mode='html', reply_markup=mark)


@my_bot.message_handler(commands=['register', 'Change'])
def registration_com(mess):
    if user.flag_registered is False:
        msg = 'Введите имя'
        my_bot.send_message(mess.chat.id, msg)
        global name_will_get, change_save
        name_will_get = True
        change_save = 'not'


@my_bot.message_handler(commands=['enter'])
def entry_com(mess):
    if user.flag_registered is False:
        msg = 'Для входа введите имя'
        my_bot.send_message(mess.chat.id, msg)
        global name_enter
        name_enter = True


@my_bot.message_handler(commands=['Stat'])
def check_registration(mess):
    if game_run is False:
        if user.flag_registered is True:
            msg = f'Статистика пользователя {user.name}:\n' \
                  f'Победы  {user.win}\n' \
                  f'Поражения  {user.lose}\n' \
                  f'Процент побед  {user.win_rate}'
            my_bot.send_message(mess.chat.id, msg)
        else:
            msg = 'Сначала зарегистрируйтесь /register \n' \
                  'Или войдите в аккаунт /enter'
            my_bot.send_message(mess.chat.id, msg)


@my_bot.message_handler(commands=['Quit'])
def quit_com(mess):
    if game_run is False:
        if user.flag_registered is True:
            msg = f'Вы вышли из аккаунта {user.name}'
            my_bot.send_message(mess.chat.id, msg)
            user.flag_registered = False
        else:
            msg = 'Сначала зарегистрируйтесь /register \n' \
                  'Или войдите в аккаунт /enter'
            my_bot.send_message(mess.chat.id, msg)


@my_bot.message_handler(commands=['Newgame'])
def startgame_com(mess):
    global game_run
    if game_run is False:
        if user.flag_registered is True:
            msg = 'Запуск новой игры'
            game_run = True
            my_bot.send_message(mess.chat.id, msg)
            board.draw_start(mess.chat.id)
            board_photo = open('data/new_board.jpg', 'rb')
            my_bot.send_photo(mess.chat.id, board_photo)
            # board.game_loop()
            global flag_starve
            flag_starve = True
        else:
            msg = 'Сначала зарегистрируйтесь /register \n' \
                  'Или войдите в аккаунт /enter'
            my_bot.send_message(mess.chat.id, msg)


@my_bot.message_handler(commands=['dices'])
def dices_com(mess):
    global movement, dice_flag

    if dice_flag is True:
        board.take_dice(mess.chat.id)
        movement, dice_flag = 'bot_AI', False


def send_cong(message, rate):
    msg = f'That your score : {rate}, We think about you, that {message}'
    my_bot.send_message(id, msg)


@my_bot.message_handler(commands=['Stopgame'])
def stopgame_com(mess):
    global game_run
    if game_run is False:
        msg = 'Сначала нужно начать игру /Newgame'
        my_bot.send_message(mess.chat.id, msg)
    else:
        msg = 'Вы проиграли! (сдались)'
        my_bot.send_message(mess.chat.id, msg)
        game_run = False
        user.lose += 1
        win_r = round(user.win / (user.win + user.lose), 1)
        user.win_rate = f'{win_r}%'
        con = sqlite3.connect("data/backgammon.db")
        cur = con.cursor()
        cur.execute('UPDATE Statistic SET lose=?, win_rate=? WHERE user_name=?', (user.lose, win_r, user.name))
        con.commit()
        con.close()


@my_bot.message_handler(commands=['dice'])
def dice_com(mess):
    global flag_starve, flag_starve2
    if flag_starve is True:
        board.draw_ones(board.img_one, board.img_three)
        flag_starve = False
    if flag_starve2 is True:
        board.draw_ones(board.img_six, board.img_one)
        flag_starve2 = False


@my_bot.message_handler(commands=['1_3'])
def one_com(mess):
    global dont_starve
    board_field[0][14], board_field[2][0] = board_field[2][0], board_field[0][14]
    board.draw_start(mess.chat.id)
    board_photo = open('data/new_board.jpg', 'rb')
    my_bot.send_photo(mess.chat.id, board_photo)
    msg = 'Ход чёрных'
    my_bot.send_message(mess.chat.id, msg)
    dont_starve = True
    starve(mess)


@my_bot.message_handler(commands=['1_6'])
def one_com(mess):
    global dont_starve, dont_starve2
    board_field[0][13], board_field[5][0] = board_field[5][0], board_field[0][13]
    board.draw_start(mess.chat.id)
    board_photo = open('data/new_board.jpg', 'rb')
    my_bot.send_photo(mess.chat.id, board_photo)
    msg = 'Ход чёрных'
    my_bot.send_message(mess.chat.id, msg)
    dont_starve2 = True
    starve(mess)


@my_bot.message_handler(commands=['Save'])
def save_com(mess):
    global change_save
    if change_save == 'question':
        msg = 'Данные успешно сохранены!'
        my_bot.send_message(mess.chat.id, msg)
        change_save = 'not'
        user.flag_registered = True
        create_user(user.name, user.password)


def starve(me):
    global flag_starve2, dont_starve, dont_starve2
    if dont_starve:
        board.draw_ones(board.img_two, board.img_five)
        board_field[11][0], board_field[6][14] = board_field[6][14], board_field[11][0]
        board.draw_start(me.chat.id)
        board_photo = open('data/new_board.jpg', 'rb')
        my_bot.send_photo(me.chat.id, board_photo)
        msg = 'Ваш ход'
        my_bot.send_message(me.chat.id, msg)
        flag_starve2 = True
        dont_starve = False
    elif dont_starve2:
        board.draw_ones(board.img_two, board.img_three)
        board_field[11][1], board_field[8][14] = board_field[8][14], board_field[11][1]
        board.draw_start(me.chat.id)
        board_photo = open('data/new_board.jpg', 'rb')
        my_bot.send_photo(me.chat.id, board_photo)
        msg = 'Ваш ход'
        my_bot.send_message(me.chat.id, msg)
        dont_starve2 = False


@my_bot.message_handler(content_types=['text'])
def get_text_mess(mess):
    global name_will_get, password_will_get, name_enter, password_enter
    if name_will_get:
        user.get_name(mess, 1)
    elif password_will_get:
        user.get_password(mess, 1)
    elif name_enter:
        user.get_name(mess, 2)
    elif password_enter:
        user.get_password(mess, 2)


def create_user(name, password):
    con = sqlite3.connect("data/backgammon.db")
    cur = con.cursor()
    cur.execute('INSERT INTO User VALUES(?, ?)', (name, password))
    cur.execute('INSERT INTO Statistic Values(?, ?, ?, ?)', (name, 0, 0, 0.0))
    con.commit()
    con.close()


def cancel(par):
    global can
    mark = board_field
    mark.append(telebot.types.InlineKeyboardButton('Правила игры',
                                                   url='https://selosovetov.ru/2016/11/25/dlinnye-nardy/'))
    mark.append(telebot.types.InlineKeyboardButton('Создатель бота', url='https://t.me/ds791358'))
    for i in movement:
        # rad
        if can is True:
            can = False
        else:
            can = True


class User:
    def __init__(self):
        self.flag_registered = False
        self.name = ''
        self.password = ''
        self.win = 0
        self.lose = 0
        self.win_rate = '0.0%'

    def get_name(self, mess, n):
        name = mess.text
        self.con = sqlite3.connect("data/backgammon.db")
        self.cur = self.con.cursor()
        all_names = self.cur.execute('SELECT name from User')
        names = []
        for i in all_names:
            names.append(i[0])

        msg = ''
        if n == 1:
            if name in names:
                msg = 'Данное имя занято\n' \
                      'Введите другое'
            else:
                self.name = name
                msg = f'Ваше имя: {self.name}\n' \
                      f'Введите пароль'
                global password_will_get, name_will_get
                password_will_get = True
                name_will_get = False
        elif n == 2:
            if name in names:
                self.name = name
                msg = f'Ваше имя: {self.name}\n' \
                      f'Введите пароль'
                global password_enter, name_enter
                password_enter = True
                name_enter = False
            else:
                msg = 'такого пользователя не существует. Введите другое имя'

        my_bot.send_message(mess.chat.id, msg)
        self.con.close()

    def get_password(self, mess, n):
        self.password = mess.text
        msg = ''
        pas = ''
        if n == 1:
            msg = f'Ваше имя: {self.name}\n' \
                  f'Ваш пароль: {self.password}\n' \
                  'Хотите изменить данные /Change\n' \
                  'Или сохранить /Save ?'

        global change_save, password_will_get
        change_save = 'question'
        password_will_get = False

        if n == 2:
            self.con = sqlite3.connect("data/backgammon.db")
            self.cur = self.con.cursor()
            passes = self.cur.execute('SELECT password from User where name in (?, ?)', (self.name, ' '))
            for i in passes:
                pas = i[0]
            if self.password == pas:
                msg = f'вы успешно вощли в аккаунт {self.name}'
                user.flag_registered = True
                self.get_stat()
                global password_enter
                password_enter = False
            else:
                msg = 'Неверный пароль, попробуйте ещё раз'

        my_bot.send_message(mess.chat.id, msg)

    def get_stat(self):
        self.con = sqlite3.connect("data/backgammon.db")
        self.cur = self.con.cursor()
        db_stats = self.cur.execute('SELECT'
                                    ' win, lose, win_rate'
                                    ' from Statistic where user_name in (?, ?)', (self.name, ' '))
        for i in db_stats:
            self.win, self.lose, self.win_rate = i[0], i[1], f'{i[2]}%'

        self.con.close()

    def app_result(self):
        w = self.win
        l = self.lose
        if w > l:
            message = 'you are grate'
            self.win_rate = (w + l) / l
        else:
            message = 'you CAN try harder'
            self.win_rate = (l + w) / w
        self.win_rate = str(self.win_rate)
        send_cong(message, self.win_rate)


class Board:
    def __init__(self):
        self.img_one = Image.open('data/dice_one.png')
        self.img_two = Image.open('data/dice_two.png')
        self.img_three = Image.open('data/dice_three.png')
        self.img_four = Image.open('data/dice_four.png')
        self.img_five = Image.open('data/dice_five.png')
        self.img_six = Image.open('data/dice_six.png')

    def draw_start(self, chat_id):
        self.chat_id = chat_id
        img = Image.open('data/empty_board.png')
        draw = ImageDraw.Draw(img)
        width = -38

        for i in range(len(board_field)):
            height = 600
            width += 45
            if i == 6:
                width += 50
            for j in board_field[i]:
                height -= 40
                if j[0] == 'w':
                    draw.ellipse((width, height, width + 40, height + 40), 'white', 'black')
                elif j[0] == 'b':
                    draw.ellipse((width, height, width + 40, height + 40), 'black', 'white')

            img.save('data/new_board.jpg')

    def draw_twise(self, im):

        img = Image.open('data/dice_board.jpg')

        for i in range(1, 5):
            img.paste(im, (170 * i, 180))

        my_bot.send_photo(self.chat_id, img)

    def draw_ones(self, first, second):

        img = Image.open('data/dice_board.jpg')

        img.paste(first, (170 * 2, 180))
        img.paste(second, (170 * 3, 180))

        my_bot.send_photo(self.chat_id, img)

    def take_dice(self, chat_id):

        self.chat_id = chat_id
        choices = [1, 2, 3, 4, 5, 6]

        taken1, taken2 = random.choice(choices), random.choice(choices)
        img1, img2 = 0, 0
        for i in range(2):
            if i == 0:
                if taken1 == 1:
                    img1 = self.img_one
                elif taken1 == 2:
                    img1 = self.img_two
                elif taken1 == 3:
                    img1 = self.img_three
                elif taken1 == 4:
                    img1 = self.img_four
                elif taken1 == 5:
                    img1 = self.img_five
                elif taken1 == 6:
                    img1 = self.img_six
            else:
                if taken2 == 1:
                    img2 = self.img_one
                elif taken2 == 2:
                    img2 = self.img_two
                elif taken2 == 3:
                    img2 = self.img_three
                elif taken2 == 4:
                    img2 = self.img_four
                elif taken2 == 5:
                    img2 = self.img_five
                elif taken2 == 6:
                    img2 = self.img_six

        if taken1 == taken2:
            self.draw_twise(img1)
        else:
            self.draw_ones(img1, img2)

        self.first_dice, self.second_dice = taken1, taken2

    def change_player(self):
        global movement
        movement = 'player'

        copy = list()
        for i in range(len(board_field), -1):
            copy.append([])
            for j in board_field[i]:
                copy[i].append(board_field[i][j])
        if copy[0] != board_field[-1] or board_field[2] != copy[9]:
            copy = []
            copy.append(board_field[0])
            for i in range(len(copy[0])):
                copy.append([])
            return 'error_of_writing'

    def find_move_piece(self, color, f, s):
        li_move = {}
        if color == 'w':
            for column in board_field:
                for place in column:
                    if place[0] == 'w':
                        li_move[place] = []
                        a, b = board_field.index(column) + f, board_field.index(column) + s
                        if a < len(board_field):
                            li_move[place].append(board_field[a])
                            li_move[place].append(board_field.index(board_field[a]))
                        else:
                            target = 2
                            li_move[place].append(board_field[abs(len(board_field) - a) - 1])
                        if b < len(board_field):
                            li_move[place].append(board_field[b])
                            li_move[place].append(board_field.index(board_field[b]))
                        else:
                            pass
                        break
            li_can = {}
            for key in li_move:
                li_can[key] = [[], []]
                if li_move[key][0][0][0] == '0' or li_move[key][0][0][0] == 'w':
                    li_can[key][0].append(li_move[key][0].index('0'))
                    li_can[key][0].append(li_move[key][1])
                if li_move[key][2][0][0] == '0' or li_move[key][2][0][0] == 'w':
                    li_can[key][1].append(li_move[key][2].index('0'))
                    li_can[key][1].append(li_move[key][3])
            self.change_player()

    def game_loop(self):
        if movement == 'player':
            my_bot.send_message(self.chat_id, 'бросьте кости /dices')
            global dice_flag
            dice_flag = True


board = Board()
user = User()
my_bot.polling(none_stop=True)
