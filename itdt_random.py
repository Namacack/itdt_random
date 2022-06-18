import json
import time
import requests
import discord
import random
import interactions
import asyncio
from datetime import datetime 
from discord.ext import commands, tasks
from enum import Enum, IntEnum

db_url = "https://script.google.com/macros/s/AKfycbyfoaulAWtib6ixAFiqtoBc7LXGkUvZ_D6sEfXNsiMRLXHsvQSGf1Ir/exec"

res = requests.get(db_url)

song_db = json.loads(res.text)

TOKEN = 'OTg3MzI2MzY2MTA0MDQ3Njc2.GKXgG9.9ZrZQT__v9c9kgEFq_j8YK_OTamAwo4oOV4YVw'

bot = commands.Bot(command_prefix='@', intents=discord.Intents.all())

slash_client = interactions.Client(TOKEN, disable_sync=False)

dan_level = {
    "ビギナー":[0,0,0,1],
    "初段":[1,1,2,2],
    "二段":[3,4,4,4],
    "三段":[5,5,5,6],
    "四段":[7,7,8,8],
    "五段":[9,9,9,9],
    "六段":[10,10,10,11],
    "七段":[11,12,12,13],
    "八段":[13,13,14,14],
    "九段":[15,15,16,16],
    "十段":[17,17,17,18],
    "皆伝":[19,19,19,20],
    "Overjoy":[20,20,20,21],
}

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
    error = False
    fnlevel = None
    if not level is None:
        print('not empty')
        if level not in ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","99","???","(^^)"]:
            print('not defined')
            embed_err=discord.Embed(title="エラー", description="指定された難易度は存在しません。", color=0xff8080)
            await ctx.send(embeds=[interactions.Embed(**embed_err.to_dict())])
            error = True
        else:
            while fnlevel != level:
                #print('searching')
                rnd = random.randrange(len(song_db))
                fnlevel = song_db[rnd]['level'] 
    else:
        rnd = random.randrange(len(song_db))
    if  error != True:
        title = song_db[rnd]['title'].replace('_','\_')
        chlevel = song_db[rnd]['level']
        url = song_db[rnd]['url']
        embed=discord.Embed(title="ランダム選曲", color=0xff8080)
        embed.add_field(name="曲名", value=title, inline=False)
        embed.add_field(name="難易度", value="★" + chlevel, inline=False)
        embed.add_field(name="URL", value=url, inline=False)
        await ctx.send(embeds=[interactions.Embed(**embed.to_dict())])

@slash_client.command(
    name="random_range", 
    description="範囲内の難易度から1曲ランダムに表示します。???,(^^)は対象外です。",
    options = [
        interactions.Option(
            name="min",
            description="最低難易度を指定します(空欄で0)",
            type=interactions.OptionType.INTEGER,
            required=False,
        ),
        interactions.Option(
            name="max",
            description="最高難易度を指定します(空欄で25)",
            type=interactions.OptionType.INTEGER,
            required=False,
        ),
    ])

async def _slash_random_range(ctx, min=0, max=25):
    error = False
    fnlevel = -1
    if min < -1 : min = 0
    if max > 100 : max = 99
    if min>max:
        print('incorrect')
        embed_err=discord.Embed(title="エラー", description="入力形式が正しくありません。", color=0xff8080)
        await ctx.send(embeds=[interactions.Embed(**embed_err.to_dict())])
        error = True
    else:
        while not(fnlevel >= min and fnlevel <= max):
            rnd = random.randrange(len(song_db))
            if song_db[rnd]['level'] in ["???","(^^)"]:
                fnlevel = 101
            else:
                fnlevel = int(song_db[rnd]['level']) 

    if  error != True:
        title = song_db[rnd]['title'].replace('_','\_')
        chlevel = song_db[rnd]['level']
        url = song_db[rnd]['url']
        embed=discord.Embed(title="範囲ランダム選曲", color=0xff8080)
        embed.add_field(name="曲名", value=title, inline=False)
        embed.add_field(name="難易度", value="★" + chlevel, inline=False)
        embed.add_field(name="URL", value=url, inline=False)
        await ctx.send(embeds=[interactions.Embed(**embed.to_dict())])

@slash_client.command(
    name="random_nd", 
    description="指定されたND名を含むの譜面から1曲ランダムに表示します。",
    options = [
        interactions.Option(
            name="nd",
            description="ND名を指定します",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ])

async def _slash_random_nd(ctx, nd):
    error = False
    nd = "obj:" + nd
    fnd = ""
    count = 0
    while not(nd in fnd):
        rnd = random.randrange(len(song_db))
        fnd = song_db[rnd]['subtitle']
        count += 1
        if count > len(song_db):
            embed_err=discord.Embed(title="エラー", description="指定されたNDの譜面が見つかりませんでした。", color=0xff8080)
            await ctx.send(embeds=[interactions.Embed(**embed_err.to_dict())])
            error = True
            break
    if  error != True:
        title = song_db[rnd]['title'].replace('_','\_')
        chlevel = song_db[rnd]['level']
        url = song_db[rnd]['url']
        embed=discord.Embed(title="ND指定ランダム選曲", color=0xff8080)
        embed.add_field(name="曲名", value=title, inline=False)
        embed.add_field(name="難易度", value="★" + chlevel, inline=False)
        embed.add_field(name="URL", value=url, inline=False)
        await ctx.send(embeds=[interactions.Embed(**embed.to_dict())])

@slash_client.command(
    name="random_dan", 
    description="指定された段位相当のコースをランダムに生成します。",
    options = [
        interactions.Option(
            name="dan",
            description="段位を指定します。(ビギナー,初段～十段,皆伝,Overjoy)",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ])

async def _slash_random_dan(ctx, dan):
    error = False
    titles = ["","","",""]
    chlevels = [-1,-1,-1,-1]
    urls = ["","","",""]
    fnlevel = None
    if dan not in ["ビギナー","初段","二段","三段","四段","五段","六段","七段","八段","九段","十段","皆伝","Overjoy"]:
            print('not defined')
            embed_err=discord.Embed(title="エラー", description="指定された段位は存在しません。", color=0xff8080)
            await ctx.send(embeds=[interactions.Embed(**embed_err.to_dict())])
            error = True
    if  error != True:
        for i in range(4):
            fnlevel = None
            while fnlevel != dan_level[dan][i]:
                rnd = random.randrange(len(song_db))
                if song_db[rnd]['level'] in ["???","(^^)"]:
                    fnlevel = 101
                else:
                    fnlevel = int(song_db[rnd]['level'])
            titles[i] = song_db[rnd]['title'].replace('_','\_')
            chlevels[i] = song_db[rnd]['level']
            urls[i] = song_db[rnd]['url']
        embed=discord.Embed(title="ランダム段位")
        embed.add_field(name="1曲目", value="★" + chlevels[0] + " " + titles[0], inline=False)
        embed.add_field(name="URL", value=urls[0], inline=True)
        embed.add_field(name="2曲目", value="★" + chlevels[1] + " " + titles[1], inline=False)
        embed.add_field(name="URL", value=urls[1], inline=True)
        embed.add_field(name="3曲目", value="★" + chlevels[2] + " " + titles[2], inline=False)
        embed.add_field(name="URL", value=urls[2], inline=True)
        embed.add_field(name="4曲目", value="★" + chlevels[3] + " " + titles[3], inline=False)
        embed.add_field(name="URL", value=urls[3], inline=True)
        await ctx.send(embeds=[interactions.Embed(**embed.to_dict())])

@bot.event
async def on_ready():
    print('log in')
    activity = discord.Activity(name='アイドルマスター シンデレラガールズ スターライトステージ', type=discord.ActivityType.playing)
    await bot.change_presence(activity=activity)

@tasks.loop(seconds=60)
async def loop():
    #print('roop')
    now = datetime.now().strftime('%H:%M')
    if now == '04:00':
        res = requests.get(db_url)
        song_db = json.loads(res.text)
        print('songdb reloaded')
        rnd = random.randrange(len(song_db))
        channel = bot.get_channel(987348863641878528)
        title = song_db[rnd]['title']
        chlevel = song_db[rnd]['level']
        url = song_db[rnd]['url']
        embed=discord.Embed(title="今日の譜面", color=0xff8080)
        embed.add_field(name="曲名", value=title, inline=False)
        embed.add_field(name="難易度", value="★" + chlevel, inline=False)
        embed.add_field(name="URL", value=url, inline=False)
        await channel.send(embed=embed)
    # if now == '07:00':
    #     res = requests.get(db_url)
    #     song_db = json.loads(res.text)
    #     print('songdb reloaded')
        
loop.start()

lp = asyncio.get_event_loop()
lp.create_task(bot.start(TOKEN))
lp.create_task(slash_client._ready())
lp.run_forever()



