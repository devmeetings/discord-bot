#!/usr/bin/env python
# https://discordapp.com/api/oauth2/authorize?client_id=702902614362423378&permissions=268512256&scope=bot

import discord, pygsheets

TOKEN = 'NzAyOTAyNjE0MzYyNDIzMzc4.XqGzEg.bgokFRCOWY57HVsYuzwL5zGQoFs'
reactions_list = ["❤️", "🧡", "💛", "💚", "💙", "💜"]
print("Startujemy")


def email_check(guild_id, mail, username):
    global dict_serv
    gc = pygsheets.authorize()
    sh = gc.open('Lista maili 2')
    wk1 = sh.worksheet('title', "Lista")
    wk2 = sh.worksheet('title', "Liczby")
    a = wk2.get_col(1, include_tailing_empty=False)
    b = wk2.get_col(2, include_tailing_empty=False)
    c = wk2.get_col(3, include_tailing_empty=False)
    dict_serv = dict(zip(a, zip(b, c)))
    guild_list = dict_serv[str(guild_id)]
    if int(guild_list[1]) >= 40:
        return False
    else:
        a = wk1.rows
        wk1.insert_rows(a, number=1, values=[mail, username, guild_list[0]], inherit=True)
        return True


def intro():
    a = "@everyone Hej, chciałbym was pokrótce wprowadzić w obsługę discorda, przebieg warsztatów etc.\nPo pierwsze, kanały dzielą się na tekstowe i głosowe (na liście kanałów po lewej stronie są ikonki). Ten kanał jest kanałem tekstowym dla obsługi eventu, uczestnicy go nie widzą, istnieje również jego głosowy odpowiednik, niżej. Pozostałe kanały:\norganizacyjne - miejsce do wysyłania ogłoszeń do uczestników, warto dodawać oznaczenia - pinguje to wtedy daną grupę osób @everyone żeby ping poszedł do wszystkich, @uczestnik dla samych uczestników\nmaster - kanał na wszelkie rozmowy przed i po warsztatowe\npomoc - jeśli w trakcie warsztatu uczestnik będzie miał z czymś problem, może albo napisać o nim na tym kanale albo poprosić o dołączenie do danego kanału grupowego (głosowego). Kanał głosowy pozwala na streaming obrazu od uczestnika.\nChciałbym żeby każdy przed warsztatami upewnił się, że wszystko u niego działa, głównie kwestia mikrofonu i głośników na discordzie, bo potrafi być kapryśny\nJeśli mielibyście jakiekolwiek pytania, coś dokładniej wytłumaczyć, coś jest niejasne - piszcie śmiało tutaj, albo na PW"
    b = "Przebieg warsztatu:\nZaczynamy od 9:00, więc najlepiej już za 15 być gotowym i dołączyć. Ja, albo Julek zrobimy krótkie wprowadzenie techniczne, potem wy zaczynacie swoją część. \nJak do tej pory, wygląda to tak, że prowadzący streamuje prezentację na kanał głosowy warsztat, robi tam wprowadzenie teoretyczne, po skończeniu odpowiada na wszystkie pytania z kanału warsztat pytania daje zadania i uczestnicy kodują w podzielonych grupach. Jeśli mają jakiś problem to uderzają na kanał pomoc, a tam mentor lub prowadzący im pomaga z danym problemem. Warto wyznaczać jakieś ramy czasowe na zadania, żeby uczestnicy wiedzieli ile mają czasu.  Pod koniec tego czasu, można się zapytać czy już skończyli, czy jeszcze potrzebują trochę czasu. Wprowadziłem pod to głosowania, co i jak z nimi, napiszę za chwilę. Kiedy skończy się czas robienia zadań, zbieramy wszystkich z powrotem na warsztatowy (co najlepiej ogłosić na kanale ogłoszenia, pingując ich) i powtarzamy schemat, aż do końca. Przed ostatnią iteracją część czasu poświęcimy na puszczenie ankiety (wydaje mi się, że max 10 minut zajmie wypełnienie)\ngłosowania tworzymy pisząc na czacie komendę i albo możemy użyć wersji skróconej\n`vote Czy lubisz dżem?`, wtedy dostępne do głosowania opcje są TAK/NIE\nAlbo wersja rozbudowana, z własnymi odpowiedziami\n`vote Jaki dżem lubisz?;truskawkowy;morelowy;brzoskwiniowy;jagodowy`"
    c = "vote Czy lubisz dżem?"
    d = "vote Jaki dżem lubisz?;truskawkowy;morelowy;brzoskwiniowy;jagodowy"
    return [a, b, c, d]


# running up
client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


# commands
@client.event
async def on_message(message):
    if message.content == "refresh time":
        role = discord.utils.find(lambda r: r.name == 'moderator', message.guild.roles)
        if role in message.author.roles:
            await message.delete()
            refresh()
            await message.channel.send(':white_check_mark:')
    if message.content == 'give me intel':
        role = discord.utils.find(lambda r: r.name == 'moderator', message.guild.roles)
        if role in message.author.roles:
            await message.delete()
            await message.channel.send(message.guild.id)
    if message.content.startswith("vote") or message.content.startswith("Vote"):
        role1 = discord.utils.find(lambda r: r.name == 'moderator', message.guild.roles)
        role2 = discord.utils.find(lambda r: r.name == 'mentor', message.guild.roles)
        role3 = discord.utils.find(lambda r: r.name == 'organizator', message.guild.roles)
        role4 = discord.utils.find(lambda r: r.name == 'prowadzący', message.guild.roles)
        if role1 in message.author.roles or role2 in message.author.roles or role3 in message.author.roles or role4 in message.author.roles:
            in_text = message.content[4:]
            await message.delete()
            in_text = in_text.split(";")
            if len(in_text) != 0:
                if len(in_text) == 1 or len(in_text) == 2:
                    await message.channel.send(
                        "@everyone Zagłosuj poprzez reakcję\n" + in_text[0] + "\n❤️ - TAK\n🧡 - NIE")
                else:
                    out_text = "@everyone Zagłosuj poprzez reakcję\n" + in_text[0]
                    for x in zip(in_text[1:], reactions_list):
                        out_text += "\n" + x[0] + " - " + x[1]
                    await message.channel.send(out_text)
    if message.author == client.user:
        if message.content.startswith("@everyone Zagłosuj poprzez reakcję"):
            for x in reactions_list:
                if x in message.content:
                    await message.add_reaction(x)
    if message.content.lower().startswith("autoryzacja"):
        await message.delete()
        if "@" and "." in message.content:
            if len(message.author.roles) == 1:
                if email_check(message.guild.id, message.content.split()[1], message.author.name):
                    role5 = discord.utils.find(lambda r: r.name == 'uczestnik', message.guild.roles)
                    await message.author.add_roles(role5)
                    await message.channel.send("Rola dodana :thumbsup:")
                    await message.guild.system_channel.send("Autoryzowano  " + str(message.content.split()[1]))
                else:
                    await message.channel.send("Zapełniona ilość miejsc na warsztaty, spróbuj na kolejne zapisać się wcześniej")
            else:
                await message.channel.send("Nadano już inną rolę")
        else:
            await message.channel.send("Musisz podać prawidłowego maila")
    if message.content.lower().startswith("rezygnacja"):
        await message.delete()
        role5 = discord.utils.find(lambda r: r.name == 'uczestnik', message.guild.roles)
        if role5 in message.author.roles:
            await message.author.remove_roles(role5)
            await message.channel.send("Usunięto rolę, wpadnij na kolejne warsztaty")
        else:
            await message.channel.send("Obawiam się, że nie byłes zapisany na warsztaty ;)")
    if message.content == 'wprowadzenie':
        role = discord.utils.find(lambda r: r.name == 'moderator', message.guild.roles)
        if role in message.author.roles:
            await message.delete()
            intro_text = intro()
            for x in intro_text:
                await message.channel.send(x)


print("W gotowości")
client.run(TOKEN)
