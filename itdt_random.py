import json
import sys
import requests
import discord
import random
import interactions
import asyncio
from datetime import datetime 
from discord.ext import commands, tasks

db_url = "https://script.google.com/macros/s/AKfycbyfoaulAWtib6ixAFiqtoBc7LXGkUvZ_D6sEfXNsiMRLXHsvQSGf1Ir/exec"

res = requests.get(db_url)

song_db = json.loads(res.text)

TOKEN = 'OTg3MzI2MzY2MTA0MDQ3Njc2.GKXgG9.9ZrZQT__v9c9kgEFq_j8YK_OTamAwo4oOV4YVw'

bot = commands.Bot(command_prefix='@', intents=discord.Intents.all())

slash_client = interactions.Client(TOKEN, disable_sync=False)

@slash_client.command(
    name="random", 
    description="難易度表から1曲ランダムに表示します。",
    options = [
        interactions.Option(
            name="level",
            description="難易度を指定します(空欄で全曲)",
            type=interactions.OptionType.STRING,
            required=False,
        ),
    ])

async def _slash_random(ctx, level=None):
    fnlevel = None
    if not level is None:
        print('not empty')
        if level not in ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","99","???","(^^)"]:
            print('not defined')
            embed_err=discord.Embed(title="エラー", description="指定された難易度は存在しません。", color=0xff8080)
            await ctx.send(embeds=[interactions.Embed(**embed_err.to_dict())])
            sys.exit
        while fnlevel != level:
            print('searching')
            rnd = random.randrange(len(song_db))
            fnlevel = song_db[rnd]['level'] 
    else:
        rnd = random.randrange(len(song_db))
    title = song_db[rnd]['title']
    chlevel = song_db[rnd]['level']
    url = song_db[rnd]['url']
    embed=discord.Embed(title="ランダム選曲", color=0xff8080)
    embed.add_field(name="曲名", value=title, inline=False)
    embed.add_field(name="難易度", value="★" + chlevel, inline=False)
    embed.add_field(name="URL", value=url, inline=False)
    await ctx.send(embeds=[interactions.Embed(**embed.to_dict())])

@bot.event
async def on_ready():
    print('log in')
    print(song_db[0]['title'])

@tasks.loop(seconds=60)
async def loop():
    now = datetime.now().strftime('%H:%M')
    if now == '04:00':
        channel = bot.get_channel('987348863641878528')
        await channel.send('おはよう')  
    if now == '07:00':
        song_db = requests.get(db_url)
        print('songdb reloaded')
        
loop.start()

lp = asyncio.get_event_loop()
lp.create_task(bot.start(TOKEN))
lp.create_task(slash_client._ready())
lp.run_forever()

#slash_client.start()
#bot.run(TOKEN)



