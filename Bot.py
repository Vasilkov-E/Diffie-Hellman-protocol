import telebot


# Diffie-Hellman protocol
def Factor(n):
    Ans = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            Ans.append(d)
            n //= d
        else:
            d += 1
    if n > 1:
        Ans.append(n)
    return Ans


def fun(a, x, c, p, i):
    if i > len(c) - 1:
        return a
    else:
        a = ((a ** 2) * (x ** int(c[i]))) % p
        i += 1
        # print(a)
        return fun(a, x, c, p, i)


def payment(secretkeyBob, secretkeyAlice, x, p):
    try:
        secretkeyBob = int(secretkeyBob)
        secretkeyAlice = int(secretkeyAlice)
        x = int(x)
        p = int(p)
        power = []
        powerbin = []
        primitiverootcheck = []
    except:
        return "Введены символы"
    else:
        FactorRez = Factor(p - 1)  # факторизация
        print("FactorRez = ", FactorRez)

        for d in FactorRez:  # получение степеней
            power.append(round(p / d))
        print("power = ", power)

        for a in power:  # преобразовываем в двоичный код степень
            powerbin.append(bin(a))

        print("powerbin = ", powerbin)

        for a in powerbin:  # убираем первые 3 символа с степени
            powerbin[powerbin.index(a)] = str(a[3:])
        print("powerbin = ", powerbin)

        a = x
        for powerbin in powerbin:  # расчет первообразного корня
            primitiverootcheck.append(str(fun(a, x, powerbin, p, i=0)))
        print("primitiverootcheck = ", primitiverootcheck)

        for a in primitiverootcheck:  # проверка первообразного корня
            if a == 1:
                print("вы ввели альфа который не является первообразным корнем")
                exit(0)  # должно прервать програму
        if a == 0:
            print("Число альфа является первообращзным корнем")
        # расчет ключей
        a = x
        keyalice = fun(a, x, bin(secretkeyAlice), p, i=3)
        keybob = fun(a, x, bin(secretkeyBob), p, i=3)

        print("секретный ключ Алисы: ", str(keyalice))
        print("Секретный ключ Боба: ", str(keybob))

        # общий секретный ключ

        sharedsecretkey = fun(a, x, bin(secretkeyAlice * secretkeyBob), p, i=3)
        return str(sharedsecretkey)


# BOT
bot = telebot.TeleBot('TOKEN')
keyboard1 = telebot.types.ReplyKeyboardMarkup()

keyboard1.row('Ответ', '/start')

list = []


@bot.message_handler(commands=['start'])
def start_message(message):
    list.clear()
    # list.append(None)
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start', reply_markup=keyboard1)
    bot.send_message(message.chat.id, "Введите секретный ключ Боба: ")
    print(111, list)


@bot.message_handler(content_types=['text'])
def send_text(message):
    print(222, list)
    if len(list) == 0:
        bot.send_message(message.chat.id, "Введите секретный ключ Алисы: ")
        list.append(message.text.lower())

    elif len(list) == 1:
        bot.send_message(
            message.chat.id,
            "Введите первообразный корень (основание альфа):  "
        )
        list.append(message.text.lower())
    elif len(list) == 2:
        bot.send_message(message.chat.id, "Введите случайное простое число (модуль р):  ")
        list.append(message.text.lower())
    elif len(list) == 3:
        list.append(message.text.lower())
        bot.send_message(message.chat.id, "Общий ключ: " + payment(list[0], list[1], list[2], list[3]))
    elif message.text.lower() == 'ответ':
        bot.send_message(message.chat.id, "Общий ключ: " + payment(list[0], list[1], list[2], list[3]))
    else:
        print(message.text.lower())
        bot.send_message(message.chat.id, "Введите 'Ответ'")


bot.polling()
