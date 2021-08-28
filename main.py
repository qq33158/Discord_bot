import asyncio
import discord
import random
import pvc_list
from keep_alive import keep_alive

client = discord.Client()

@client.event
async def on_ready():
    print('目前登入身份：', client.user)
    game = discord.Game('自訂狀態')
    await client.change_presence(status=discord.Activity, activity=game)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
        
    # 隨機選擇使用者輸入的選項 命令語法: OOO 請選擇 選擇一 選擇二 選擇三 ... 或 請選擇 選擇一 選擇二 選擇三 ...
    x = '請選擇'
    if x in message.content:
        tmp = message.content.split(' ')
        mess_index = tmp.index(x)
        if len(tmp) == 1:
            await message.channel.send('講中文')
        else:
            try:
                ans = random.choice(tmp[mess_index+1:])
                await message.channel.send(ans)
            except:
                await message.channel.send('EEEEERROR!')

    # 查詢巴哈PVC 監控 半天清一次file
    if message.content == '!PVC':
        count = 0
        while True:
            inf = pvc_list.runpvc()
            if inf != 'ERROR' and inf != []:
                for i in inf:
                    if '吉普莉爾' in i:
                        await message.channel.send(f'<@{message.author.id}>'+i)
                    else:
                        await message.channel.send(i)         
            elif inf == []:
                None
            else:
                await message.channel.send('暫無此功能')
                break
            await asyncio.sleep(60)
            count += 1
            if count == 720:
                pvc_list.clear_file()
                count=0
            
keep_alive()
client.run('YourToken')