#!/usr/bin/env python
# https://discordapp.com/api/oauth2/authorize?client_id=702902614362423378&permissions=268512256&scope=bot

import discord, pygsheets

TOKEN = 'NzAyOTAyNjE0MzYyNDIzMzc4.XqdSPQ.MV1vxkUy0FgjjoxXa7GRrqes11s'

print("Startujemy")


def email_list(server_id):
    server_id = str(server_id)
    gc = pygsheets.authorize()
    sh = gc.open('Lista uczestników Devmeetings')
    nazwa = dict_servID[server_id]
    wk1 = sh.worksheet('title', nazwa)
    a = wk1.get_col(1)
    while "" in a:
        a.remove("")
    return a


def refresh():
    global dict_servID, dict_servkey
    gc = pygsheets.authorize()
    sh = gc.open('Lista uczestników Devmeetings')
    dict_servID = {}
    dict_servkey = {}
    wk2 = sh.worksheet('title', 'BOT USTAWIENIA')
    wiersz = 1
    b = "A"
    c = b + str(wiersz)
    while wk2.get_value(c) != '':
        a = wk2.get_row(wiersz)
        while "" in a:
            a.remove("")
        dict_servID[a[0]] = a[1]
        dict_servkey[a[0]] = [a[2]]
        for x in range(3, len(a)):
            dict_servkey[a[0]].append(a[x])
        dict_servkey[a[0]] = tuple(dict_servkey[a[0]])
        wiersz += 1
        c = b + str(wiersz)


refresh()
print("załadowano słowniki")
# running up
client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


# commands
@client.event
async def on_message(message):
    if message.content == "refresh time":
        await message.delete()
        refresh()
        await message.channel.send(':white_check_mark:')
    if message.content == 'give me intel':
        await message.delete()
        await message.channel.send(message.guild.id)
    if message.content.startswith((dict_servkey[str(message.guild.id)])):
        if "@" in message.content:
            lista_maili = email_list(message.guild.id)
            if message.content.endswith(tuple(lista_maili)):
                if len(message.author.roles) == 1:
                    await message.author.add_roles(discord.utils.get(message.author.guild.roles, name="uczestnik"))
                    await message.delete()
                    await message.channel.send("Rola dodana :thumbsup:\nRole added :thumbsup:")
                else:
                    await message.delete()
                    await message.channel.send("Nadano już inną rolę\nYou already have another role")
            else:
                await message.delete()
                await message.channel.send("Brak emaila w bazie\nNo such email in database")
        else:
            await message.channel.send("Musisz podać jeszcze maila\nYou need to add your email")


print("W gotowości")
client.run(TOKEN)
