import discord

me = discord.Client()

@me.event
async def on_message(msg):
    if msg.content.lower().strip() == 'dumpall':
       ... # we will create some magic soon

@me.event
async def on_ready():
    print('Connected!')

with open('token.txt') as tkf:
    tk = tkf.readline()
me.run(tk) 
