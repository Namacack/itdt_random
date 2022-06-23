import copy
import discord
import json
import random
import requests
import time

from datetime import datetime 
from discord.commands import Option
from discord.ext import tasks
from zoneinfo import ZoneInfo

intents = discord.Intents.default()
intents.members = True

db_url = "https://script.google.com/macros/s/AKfycbyfoaulAWtib6ixAFiqtoBc7LXGkUvZ_D6sEfXNsiMRLXHsvQSGf1Ir/exec"
db_url_sl = "https://script.google.com/macros/s/AKfycbxpDx-9KkQhuFHDbmfR75XtUFHrN_eRWh5PoM_n4mLbNuBrddwfcrkxA7WNcPg2b8_MLA/exec"
db_url_lg = "https://script.google.com/macros/s/AKfycbw5CkdE-CoDZxDH7SJjLz0Pf4HuRU25b5uUOmcoOaPtRfwWu8-MdksWDTZuWApprCTQ/exec"
db_url_st = "https://script.google.com/macros/s/AKfycbw-KA9EsIdYidNePnDzWYbsvpbDwSti3jRvJb0uhU7CZDJBzb229rGFxM1zmMRxKOC6sg/exec"

res = requests.get(db_url)
res_sl = requests.get(db_url_sl)
res_lg = requests.get(db_url_lg)
res_st = requests.get(db_url_st)

song_db = json.loads(res.text)
song_db_sl = json.loads(res_sl.text)
song_db_lg = json.loads(res_lg.text)
song_db_st = json.loads(res_st.text)

TOKEN = 'OTg3MzI2MzY2MTA0MDQ3Njc2.GKXgG9.9ZrZQT__v9c9kgEFq_j8YK_OTamAwo4oOV4YVw'

bot = discord.Bot(intents=intents)

all_levels = ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","99","???","(^^)"]

all_random_options = ["PlaySpeed(Easy)","Reg.Speed","PlaySpeed","JudgeRange","JudgeRange(S-Random)","PlaySpeed(Hard)","JudgeRange(Hard)"]

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
    "Undefined":[21,22,23,24],
    "Unplayable":[99,99,99,99]
}

options = [
    ["Normal","x2 Scroll","Doron","Turn","RedOnly","BlueOnly","PlaySpeed(Easy)"],
    ["x3 Scroll","Shuffle","G.Judge H","Reg.Speed","PlaySpeed","JudgeRange"],
    ["x4 Scroll","Stealth"],
    ["G.Judge A","PlaySpeed(Hard)","JudgeRange(Hard)"]
    ]
    #3:

@bot.slash_command(
    name="random", 
    description="難易度表から1曲ランダムに表示します。"
    )        
async def _slash_random(
    ctx, 
    level: Option(str,"難易度を指定します(空欄で全曲)",required=False)
    ):
    error = False
    fnlevel = None
    if level:
        print('not empty')
        if level not in all_levels:
            print('not defined')
            embed_err=discord.Embed(title="エラー", description="指定された難易度は存在しません。", color=0xff8080)
            await ctx.respond(embed=embed_err)
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
        await ctx.respond(embed=embed)

@bot.slash_command(
    name="random_with_option", 
    description="難易度表から1曲とプレイオプションをランダムに表示します。"
    )        
async def _slash_random_with_option(
    ctx, 
    level: Option(str,"難易度を指定します(空欄で全曲)",required=False),
    illegular: Option(int,"数が大きいほどマニアック・高難易度なオプションが出現します。(0~3の範囲で入力 空欄で0)",default=0),
    option_select: Option(
        str,"更にランダム要素のあるオプションを直接設定することができます。(空欄でランダム)",
        required=False,
        autocomplete=discord.utils.basic_autocomplete(all_random_options))
    ):
    error = False
    fnlevel = None
    option_list = copy.copy(options[0])
    if level:
        print('not empty')
        if level not in all_levels:
            print('not defined')
            embed_err=discord.Embed(title="エラー", description="指定された難易度は存在しません。", color=0xff8080)
            await ctx.respond(embed=embed_err)
            error = True
        else:
            while fnlevel != level:
                #print('searching')
                rnd = random.randrange(len(song_db))
                fnlevel = song_db[rnd]['level'] 
    else:
        rnd = random.randrange(len(song_db))
    if not (-1 < illegular < 4):
        embed_err=discord.Embed(title="エラー", description="illegularは0~3の範囲で入力してください。", color=0xff8080)
        await ctx.respond(embed=embed_err)
        error = True
    else:
        if not option_select:
            print(option_list)
            if illegular >= 1:
                option_list.extend(options[1])
                print(option_list)
                if illegular >= 2:
                    option_list.extend(options[2])
                    print(option_list)
                    if illegular == 3:
                        option_list.extend(options[3])
                        print(option_list)
            print(option_list)
            rnd_option = random.randrange(len(option_list))
            tmp_option = option_list[rnd_option]
        else:
            if option_select not in all_random_options:
                embed_err=discord.Embed(title="エラー", description="指定されたオプションは存在しないか、ランダム要素がありません。", color=0xff8080)
                await ctx.respond(embed=embed_err)
                error = True
            else:
                tmp_option = option_select
        if tmp_option == "Reg.Speed" :       tmp_option += (" " + str( 20 + (20 * random.randrange(1,14))))
        if tmp_option == "PlaySpeed(Easy)" : tmp_option += (":" + str(round(random.uniform(0.25, 1),2)))
        if tmp_option == "PlaySpeed" :       tmp_option += (":" + str(round(random.uniform(1, 1.5),2)))
        if tmp_option == "PlaySpeed(Hard)" : tmp_option += (":" + str(round(random.uniform(1.5, 4.0),1)))
        if tmp_option == "JudgeRange":
            tmp_option += (":[" + 
            str(50 +  ( 5  * (random.randrange(1,4)))) + "," + 
            str(100 + ( 10 * (random.randrange(1,4)))) + "," +
            str(200 + ( 20 * (random.randrange(1,4)))) + "]" )
        if tmp_option == "JudgeRange(Hard)":
            tmp_option += (":[" + 
            str(20 +  ( 5  * (random.randrange(1,6)))) + "," + 
            str(40 +  ( 10 * (random.randrange(1,6)))) + "," +
            str(80 +  ( 20 * (random.randrange(1,6)))) + "]" )    
        if tmp_option == "JudgeRange(S-Random)":
            tmp_option += (":[" + 
            str(random.randrange(1,250)) + "," + 
            str(random.randrange(1,500))  + "," +
            str(random.randrange(1,1000))  + "]" )    
    if error != True:
        title = song_db[rnd]['title'].replace('_','\_')
        chlevel = song_db[rnd]['level']
        url = song_db[rnd]['url']
        embed=discord.Embed(title="ランダム選曲(オプション付き)", color=0xff8080)
        embed.add_field(name="曲名", value=title, inline=False)
        embed.add_field(name="難易度", value="★" + chlevel, inline=False)
        embed.add_field(name="URL", value=url, inline=False)
        embed.add_field(name="オプション", value=tmp_option, inline=False)
        await ctx.respond(embed=embed)

@bot.command(
    name="random_range", 
    description="範囲内の難易度から1曲ランダムに表示します。???,(^^)は対象外です。",
    )
async def _slash_random_range(
    ctx, 
    min: Option(int,"最低難易度を指定します(空欄で0)",default=0), 
    max: Option(int,"最高難易度を指定します(空欄で25)",default=25)
    ):
    error = False
    fnlevel = -1
    if min < -1 : min = 0
    if max > 100 : max = 99
    if min>max:
        print('incorrect')
        embed_err=discord.Embed(title="エラー", description="入力形式が正しくありません。", color=0xff8080)
        await ctx.respond(embed=embed_err)
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
        await ctx.respond(embed=embed)

@bot.command(
    name="random_nd", 
    description="指定されたND名を含むの譜面から1曲ランダムに表示します。"
    )

async def _slash_random_nd(
    ctx, 
    nd : Option(str,"ND名を指定します",required=True)
    ):
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
            await ctx.respond(embed=embed_err)
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
        await ctx.respond(embed=embed)

@bot.command(
    name="random_dan", 
    description="指定された段位相当のコースをランダムに生成します。",
)

async def _slash_random_dan(
    ctx, 
    dan: Option(
        str,
        "段位を指定します。(ビギナー,初段～十段,皆伝,Overjoy)",
        required=True,
        autocomplete=discord.utils.basic_autocomplete(["ビギナー","初段","二段","三段","四段","五段","六段","七段","八段","九段","十段","皆伝","Overjoy"]),),
    duplication : Option (bool,"曲被りの有無を指定します。(空欄でTrue(被りあり))",default=True)
    ):
    error = False
    titles = ["","","",""]
    chlevels = [-1,-1,-1,-1]
    urls = ["","","",""]
    chartnum = [0,0,0,0]
    fnlevel = None
    if dan not in ["ビギナー","初段","二段","三段","四段","五段","六段","七段","八段","九段","十段","皆伝","Overjoy","Undefined","Unplayable"]:
            print('not defined')
            embed_err=discord.Embed(title="エラー", description="指定された段位は存在しません。", color=0xff8080)
            await ctx.respond(embed=embed_err)
            error = True
    if  error != True:
        for i in range(4):
            fnlevel = None
            while fnlevel != dan_level[dan][i]:
                rnd = random.randrange(len(song_db))
                if song_db[rnd]['level'] in ["???","(^^)"]:
                    fnlevel = 101
                elif duplication == False and rnd in chartnum:
                    fnlevel = 777
                else:
                    fnlevel = int(song_db[rnd]['level'])
            titles[i] = song_db[rnd]['title'].replace('_','\_')
            chlevels[i] = song_db[rnd]['level']
            urls[i] = song_db[rnd]['url']
            chartnum[i] = rnd
        embed=discord.Embed(title="ランダム段位", color=0xff8080)
        embed.add_field(name="1曲目", value="★" + chlevels[0] + " " + titles[0], inline=False)
        embed.add_field(name="URL", value=urls[0], inline=True)
        embed.add_field(name="2曲目", value="★" + chlevels[1] + " " + titles[1], inline=False)
        embed.add_field(name="URL", value=urls[1], inline=True)
        embed.add_field(name="3曲目", value="★" + chlevels[2] + " " + titles[2], inline=False)
        embed.add_field(name="URL", value=urls[2], inline=True)
        embed.add_field(name="4曲目", value="★" + chlevels[3] + " " + titles[3], inline=False)
        embed.add_field(name="URL", value=urls[3], inline=True)
        await ctx.respond(embed=embed)

#ここから下は特殊難易度表ランダム

@bot.slash_command(
    name="sl_random", 
    description="低速難易度表から1曲ランダムに表示します。"
    )        
async def _slash_sl_random(
    ctx, 
    level: Option(str,"難易度を指定します(空欄で全曲)",required=False)
    ):
    error = False
    fnlevel = None
    if level:
        print('not empty')
        if level not in ["1","2","3","4","5","6","7","9","10"]:
            print('not defined')
            embed_err=discord.Embed(title="エラー", description="指定された難易度は存在しません。", color=0xff8080)
            await ctx.respond(embed=embed_err)
            error = True
        else:
            while fnlevel != level:
                #print('searching')
                rnd = random.randrange(len(song_db_sl))
                fnlevel = song_db_sl[rnd]['level'] 
    else:
        rnd = random.randrange(len(song_db_sl))
    if  error != True:
        title = song_db_sl[rnd]['title'].replace('_','\_')
        chlevel = song_db_sl[rnd]['level']
        url = song_db_sl[rnd]['url']
        embed=discord.Embed(title="ランダム選曲(低速難易度表)", color=0xff8080)
        embed.add_field(name="曲名", value=title, inline=False)
        embed.add_field(name="難易度", value="$" + chlevel, inline=False)
        embed.add_field(name="URL", value=url, inline=False)
        await ctx.respond(embed=embed)

@bot.slash_command(
    name="lg_random", 
    description="長尺・短尺まとめ表から1曲ランダムに表示します。"
    )        
async def _slash_lg_random(
    ctx, 
    level: Option(str,"難易度を指定します(空欄で全曲)",required=False)
    ):
    error = False
    fnlevel = None
    if level:
        print('not empty')
        if level not in ["__","-5","-4","-3","-2","-1","0","1","2","3","4","5","6","7","8","9","10"]:
            print('not defined')
            embed_err=discord.Embed(title="エラー", description="指定された難易度は存在しません。", color=0xff8080)
            await ctx.respond(embed=embed_err)
            error = True
        else:
            while fnlevel != level:
                #print('searching')
                rnd = random.randrange(len(song_db_lg))
                fnlevel = song_db_lg[rnd]['level'] 
    else:
        rnd = random.randrange(len(song_db_lg))
    if  error != True:
        title = song_db_lg[rnd]['title'].replace('_','\_')
        chlevel = song_db_lg[rnd]['level']
        time = song_db_lg[rnd]['time']
        url = song_db_lg[rnd]['url']
        embed=discord.Embed(title="ランダム選曲(長尺・短尺まとめ表)", color=0xff8080)
        embed.add_field(name="曲名", value=title, inline=False)
        embed.add_field(name="難易度", value="長" + chlevel, inline=False)
        embed.add_field(name="演奏時間", value=time, inline=False)
        embed.add_field(name="URL", value=url, inline=False)
        await ctx.respond(embed=embed)

@bot.slash_command(
    name="st_random", 
    description="長複合難易度表から1曲ランダムに表示します。"
    )        
async def _slash_st_random(
    ctx, 
    level: Option(str,"難易度を指定します(空欄で全曲)",required=False)
    ):
    error = False
    fnlevel = None
    if level:
        print('not empty')
        if level not in ["2","3","4","5","6","7","8","9","11","12","13","14","15","16","17","18","19","20"]:
            print('not defined')
            embed_err=discord.Embed(title="エラー", description="指定された難易度は存在しません。", color=0xff8080)
            await ctx.respond(embed=embed_err)
            error = True
        else:
            while fnlevel != level:
                #print('searching')
                rnd = random.randrange(len(song_db_st))
                fnlevel = song_db_st[rnd]['level'] 
    else:
        rnd = random.randrange(len(song_db_st))
    if  error != True:
        title = song_db_st[rnd]['title'].replace('_','\_')
        chlevel = song_db_st[rnd]['level']
        url = song_db_st[rnd]['url']
        embed=discord.Embed(title="ランダム選曲(長複合難易度表)", color=0xff8080)
        embed.add_field(name="曲名", value=title, inline=False)
        embed.add_field(name="難易度", value="◆" + chlevel, inline=False)
        embed.add_field(name="URL", value=url, inline=False)
        await ctx.respond(embed=embed)

@bot.slash_command(name="kill")
async def _slash_kill(ctx):
  await ctx.respond(f"{ctx.author}は奈落の底へ落ちた")

@bot.slash_command(name="gamerule")
async def _slash_gamerule(
    ctx,
    gamerule: Option(str,required=True),
    value: Option(str,required=True),
    ):
    await ctx.respond(f"ゲームルール {gamerule} が {value} に設定されました")

@bot.slash_command(name="leveljudge")
async def _slash_leveljudge(
    ctx,
    chart: Option(str,required=True)
    ):
    level = all_levels[random.randrange(len(all_levels))]
    await ctx.respond(f"{chart}は★{level}です。")

@bot.event
async def on_ready():
    print('log in')
    loop.start()
    activity = discord.Activity(name='ITDTの譜面', type=discord.ActivityType.playing)
    await bot.change_presence(activity=activity)

@tasks.loop(seconds=60)
async def loop():
    now = datetime.now(ZoneInfo("Asia/Tokyo")).strftime('%H:%M')
    #print(f"loop:{now}")
    if now == '00:00':

        res = requests.get(db_url)
        res_sl = requests.get(db_url_sl)
        res_lg = requests.get(db_url_lg)
        res_st = requests.get(db_url_st)
        song_db = json.loads(res.text)
        song_db_sl = json.loads(res_sl.text)
        song_db_lg = json.loads(res_lg.text)
        song_db_st = json.loads(res_st.text)
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

bot.run(TOKEN)