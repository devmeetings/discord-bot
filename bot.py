#!/usr/bin/env python
# https://discordapp.com/api/oauth2/authorize?client_id=702902614362423378&permissions=268512256&scope=bot

import discord, pygsheets

TOKEN = 'NzAyOTAyNjE0MzYyNDIzMzc4.XqdSPQ.MV1vxkUy0FgjjoxXa7GRrqes11s'
reactions_list = ["❤️", "🧡", "💛", "💚", "💙", "💜"]
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
    print("Otwieranie Autoryzacja")
    gc = pygsheets.authorize()
    print("Otwieranie Spreadsheeta")
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
    if message.content.startswith("berserk"):
        await  message.channel.send("To był tylko przykład, doczytaj instrukcję do końca :wink:")
    else:
        if message.content.startswith((dict_servkey[str(message.guild.id)])):
            if "@" in message.content:
                lista_maili = email_list(message.guild.id)
                if message.content.endswith(tuple(lista_maili)):
                    if len(message.author.roles) == 1:
                        await message.author.add_roles(discord.utils.get(message.author.guild.roles, name="uczestnik"))
                        await message.delete()
                        await message.channel.send("Rola dodana :thumbsup:")
                        await message.guild.system_channel.send("Autoryzacja  "+str(message.author.name))
                    else:
                        await message.delete()
                        await message.channel.send("Nadano już inną rolę")
                else:
                    await message.delete()
                    await message.channel.send("Brak emaila w bazie")
            else:
                await message.channel.send("Musisz podać jeszcze maila")
    if message.content.startswith("vote") or message.content.startswith("Vote"):
        role1 = discord.utils.find(lambda r: r.name == 'moderator', message.guild.roles)
        role2 = discord.utils.find(lambda r: r.name == 'mentor', message.guild.roles)
        role3 = discord.utils.find(lambda r: r.name == 'organizator', message.guild.roles)
        role4 = discord.utils.find(lambda r: r.name == 'prowadzący', message.guild.roles)
        if role1 in message.author.roles or role2 in message.author.roles or role3 in message.author.roles or role4 in message.author.roles:
            in_text=message.content[4:]
            await message.delete()
            in_text=in_text.split(";")
            if len(in_text)!=0:
                if len(in_text)==1 or len(in_text)==2:
                    await message.channel.send("@everyone Zagłosuj poprzez reakcję\n"+in_text[0]+"\n❤️ - TAK\n🧡 - NIE")
                else:
                    out_text = "@everyone Zagłosuj poprzez reakcję\n"+in_text[0]
                    for x in zip(in_text[1:],reactions_list):
                        out_text+="\n"+x[0]+" - "+x[1]
                    await message.channel.send(out_text)
    if message.author == client.user:
        if message.content.startswith("@everyone Zagłosuj poprzez reakcję"):
            for x in reactions_list:
                if x in message.content:
                    await message.add_reaction(x)
print("W gotowości")
client.run(TOKEN)
