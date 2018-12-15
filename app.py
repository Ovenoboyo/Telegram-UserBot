# -*- coding: utf-8 -*-
from telethon import TelegramClient, events
from async_generator import aclosing
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.custom import Button
from telethon.tl.types import ChannelBannedRights
from telethon.errors import UserAdminInvalidError
from telethon.errors import ChatAdminRequiredError
from telethon.errors import ChannelInvalidError
from telethon.tl.functions.channels import EditAdminRequest
from telethon.tl.types import ChannelAdminRights
from datetime import datetime, timedelta
from googletrans import Translator
import logging
import sqlite3
import time
import re
import logging
import random, re
import asyncio
import os
from pyfiglet import Figlet
from gtts import gTTS
import time
import hastebin
import sys
import urbandict
import gsearch
import subprocess
from datetime import datetime
from requests import get
import wikipedia
import inspect
import platform
from googletrans import Translator
from random import randint
from zalgo_text import zalgo
logging.basicConfig(level=logging.DEBUG)
api_id=os.environ['API_KEY']
api_hash=os.environ['API_HASH']
text=" "
langi="en-us"
global SPAM
SPAM=False
global USERS
USERS={}
global COUNT_MSG
COUNT_MSG=0
WIDE_MAP = dict((i, i + 0xFEE0) for i in range(0x21, 0x7F))
WIDE_MAP[0x20] = 0x3000
client = TelegramClient('session_name', api_id, api_hash).start()
client.start()
@client.on(events.NewMessage(outgoing=True, pattern='.delmsg'))
async def delmsg(event):
    i=1
    async for message in client.iter_messages(event.chat_id,from_user='me'):
        if i>2:
            break
        i=i+1
        await message.delete()
@client.on(events.NewMessage(outgoing=True, pattern='.term'))
async def terminal_runner(event):
    message=await client.get_messages(event.chat_id)
    command = str(message[0].message)
    list_x=command.split(' ')
    result=subprocess.run(list_x[1:], stdout=subprocess.PIPE)
    result=str(result.stdout.decode())
    await event.edit("**Query: **\n`"+str(command[6:])+'`\n**Output: **\n`'+result+'`')
@client.on(events.NewMessage(outgoing=True, pattern='.purgeme'))
async def purgeme(event):
    message=await client.get_messages(event.chat_id)
    count = int(message[0].message[9:])
    i=1
    async for message in client.iter_messages(event.chat_id,from_user='me'):
        if i>count+1:
            break
        i=i+1
        await message.delete()
    await client.send_message(event.chat_id,"`Purge Complete!` Purged "+str(count)+" messages. **This auto-generated message shall be self destructed in 2 seconds.**")
    await client.send_message(-266765687,"Purge of "+str(count)+" messages done successfully.")
    time.sleep(2)
    i=1
    async for message in client.iter_messages(event.chat_id,from_user='me'):
        if i>1:
            break
        i=i+1
        await message.delete()
@client.on(events.NewMessage(outgoing=True,pattern='.shg'))
async def shrug(event):
    await event.edit("¯\_(ツ)_/¯")
@client.on(events.NewMessage(outgoing=True,pattern='/get userbotfile'))
async def userbot_sender(event):
    file=open(sys.argv[0], 'r')
    await client.send_file(event.chat_id, sys.argv[0], reply_to=event.id, caption='`Here\'s me in a file`')
    file.close()
@client.on(events.NewMessage(outgoing=True,pattern='.rekt'))
async def rekt(event):
    await event.edit("Get Rekt man! ( ͡° ͜ʖ ͡°)")
@client.on(events.NewMessage(outgoing=True , pattern='.google (.*)'))
async def gsearch(event):
        match = event.pattern_match.group(1)
        result_=subprocess.run(['gsearch', match], stdout=subprocess.PIPE)
        result=str(result_.stdout.decode())
        await client.send_message(await client.get_input_entity(event.chat_id), message='**Search Query:**\n`' + match + '`\n\n**Result:**\n' + result, reply_to=event.id, link_preview=False)
        await client.send_message(-266765687,"Google Search query "+match+" was executed successfully by "+str(event.sender_id))
@client.on(events.NewMessage(outgoing=True,pattern=r'.wiki (.*)'))
async def wiki(event):
        match = event.pattern_match.group(1)
        result=wikipedia.summary(match)
        await client.send_message(await client.get_input_entity(event.chat_id), message='**Search:**\n`' + match + '`\n\n**Result:**\n' + result, reply_to=event.id, link_preview=False)
        await client.send_message(-266765687,"Wiki query "+match+" was executed successfully")
@client.on(events.NewMessage(outgoing=True, pattern='.eval'))
async def evaluate(event):
    evaluation = eval(event.text[6:])
    if inspect.isawaitable(evaluation):
       evaluation = await evaluation
    if evaluation:
      await event.edit("**Query: **\n`"+event.text[6:]+'`\n**Result: **\n`'+str(evaluation)+'`')
    else:
      await event.edit("**Query: **\n`"+event.text[6:]+'`\n**Result: **\n`No Result Returned/False`')
    await client.send_message(-266765687,"Eval query "+event.text[6:]+" was executed successfully")
@client.on(events.NewMessage(outgoing=True, pattern=r'.exec (.*)'))
async def run(event):
 code = event.raw_text[5:]
 exec(
  f'async def __ex(event): ' +
  ''.join(f'\n {l}' for l in code.split('\n'))
 )
 result = await locals()['__ex'](event)
 if result:
  await event.edit("**Query: **\n`"+event.text[5:]+'`\n**Result: **\n`'+str(result)+'`')
 else:
  await event.edit("**Query: **\n`"+event.text[5:]+'`\n**Result: **\n`'+'No Result Returned/False'+'`')
 await client.send_message(-266765687,"Exec query "+event.text[5:]+" was executed successfully")
@client.on(events.NewMessage(outgoing=True, pattern='.pingme'))
async def pingme(event):
    start = datetime.now()
    await event.edit('Pong!')
    end = datetime.now()
    ms = (end - start).microseconds/1000
    await event.edit('Pong!\n%sms' % (ms))
@client.on(events.NewMessage(outgoing=True, pattern='.spam'))
async def spammer(event):
    message= await client.get_messages(event.chat_id, from_user='me')
    counter=int(message[0].message[6:8])
    spam_message=str(event.text[8:])
    await asyncio.wait([event.respond(spam_message) for i in range(counter)])
    await event.delete()
    await client.send_message(-266765687,"Spam was executed successfully")
@client.on(events.NewMessage(outgoing=True,pattern='.shutdown'))
async def killdabot(event):
        message=message = await client.get_messages(event.chat_id)
        counter=int(message[0].message[10:])
        await event.reply('`Goodbye (*Windows XP showdown sound*....`')
        time.sleep(2)
        time.sleep(counter)
@client.on(events.NewMessage(outgoing=True, pattern='.help'))
async def help(event):
    await event.reply('https://github.com/baalajimaestro/Telegram-UserBot/blob/master/README.md')
@client.on(events.NewMessage(outgoing=True, pattern='.bigspam'))
async def bigspam(event):
    message = await client.get_messages(event.chat_id, from_user='me')
    counter=int(message[0].message[9:13])
    spam_message=str(event.text[13:])
    for i in range (1,counter):
       await event.respond(spam_message)
       time.sleep(0.4)
    await event.delete()
    await client.send_message(-266765687,"bigspam was executed successfully")
@client.on(events.NewMessage(outgoing=True, pattern='.str'))
async def stretch(event):
    textx=await event.get_reply_message()
    message = await client.get_messages(event.chat_id)
    if textx:
         message = textx
         message = str(message.message)
    else:
        message = str(message[0].message[5:])
    count = random.randint(3, 10)
    reply_text = re.sub(r'([aeiouAEIOUａｅｉｏｕＡＥＩＯＵ])', (r'\1' * count), message)
    await event.edit(reply_text)
@client.on(events.NewMessage(outgoing=True, pattern='.rmfilters'))
async def filters(event):
    message=await event.get_reply_message()
    temp = str(message)
    array = temp.split("\\n - ")
    i = 1
    count = int(len(array))
    last = count -1
    while i < count:
        await client.send_message(event.chat_id,"/stop "+array[i]+"")
        i = i+1
        time.sleep(0.3)
        if i==last:
            temp1 = str(array[last])
            temp2= temp1.split("'")
            await client.send_message(event.chat_id,"/stop "+str(temp2[0])+"")
            break
    time.sleep(2)
    j=1
    async for message in client.iter_messages(event.chat_id,from_user='me'):
        if j>count:
            break
        j=j+1
        await message.delete()
@client.on(events.NewMessage(pattern='.random'))
async def randomevents(event):
    textx=await event.get_reply_message()
    message = await client.get_messages(event.chat_id)
    if textx:
         message = textx
         temp = str(message)
    else:
         temp = str(message[0].message[8:])
    array = temp.split(",")
    count = int(len(array)) -1
    chosen = random.randint(0, count)
    await client.send_message(event.chat_id, "Random event: `"+array[chosen]+"`", reply_to=event.id)
    await client.send_message(-266765687,".random function initiated at ID: `"+str(event.chat_id)+"`, Selected option was `"+array[chosen]+"`")
@client.on(events.NewMessage(outgoing=True, pattern='.cp'))
async def copypasta(event):
    textx=await event.get_reply_message()
    if textx:
         message = textx
         message = str(message.message)
    else:
        message = await client.get_messages(event.chat_id)
        message = str(message[0].message[3:])
    emojis = ["😂", "😂", "👌", "✌", "💞", "👍", "👌", "💯", "🎶", "👀", "😂", "👓", "👏", "👐", "🍕", "💥", "🍴", "💦", "💦", "🍑", "🍆", "😩", "😏", "👉👌", "👀", "👅", "😩", "🚰"]
    reply_text = random.choice(emojis)
    b_char = random.choice(message).lower() # choose a random character in the message to be substituted with 🅱️
    for c in message:
        if c == " ":
            reply_text += random.choice(emojis)
        elif c in emojis:
            reply_text += c
            reply_text += random.choice(emojis)
        elif c.lower() == b_char:
            reply_text += "🅱️"
        else:
            if bool(random.getrandbits(1)):
                reply_text += c.upper()
            else:
                reply_text += c.lower()
    reply_text += random.choice(emojis)
    await event.edit(reply_text)
@client.on(events.NewMessage(outgoing=True, pattern='.vapor'))
async def vapor(event):
    textx=await event.get_reply_message()
    message = await client.get_messages(event.chat_id)
    if textx:
         message = textx
         message = str(message.message)
    else:
        message = str(message[0].message[7:])
    if message:
        data = message
    else:
        data = ''
    reply_text = str(data).translate(WIDE_MAP)
    await event.edit(reply_text)
@client.on(events.NewMessage(outgoing=True, pattern=':/'))
async def dopedance(event):
    uio=['/','\\']
    for i in range (1,30):
        time.sleep(0.3)
        await event.edit(':'+uio[i%2])
@client.on(events.NewMessage(outgoing=True, pattern='-_-'))
async def mutemeow(event):
    await event.delete()
    t = '-_-'
    r = await event.reply(t)
    for j in range(30):
        t = t[:-1] + '_-'
        await r.edit(t)
@client.on(events.NewMessage(outgoing=True, pattern='.react'))
async def react(event):
    reactor=['ʘ‿ʘ','ヾ(-_- )ゞ','(っ˘ڡ˘ς)','(´ж｀ς)','( ಠ ʖ̯ ಠ)','(° ͜ʖ͡°)╭∩╮','(ᵟຶ︵ ᵟຶ)','(งツ)ว','ʚ(•｀','(っ▀¯▀)つ','(◠﹏◠)','( ͡ಠ ʖ̯ ͡ಠ)','( ఠ ͟ʖ ఠ)','(∩｀-´)⊃━☆ﾟ.*･｡ﾟ','(⊃｡•́‿•̀｡)⊃','(._.)','{•̃_•̃}','(ᵔᴥᵔ)','♨_♨','⥀.⥀','ح˚௰˚づ ','(҂◡_◡)','ƪ(ړײ)‎ƪ​​','(っ•́｡•́)♪♬','◖ᵔᴥᵔ◗ ♪ ♫ ','(☞ﾟヮﾟ)☞','[¬º-°]¬','(Ծ‸ Ծ)','(•̀ᴗ•́)و ̑̑','ヾ(´〇`)ﾉ♪♪♪','(ง\'̀-\'́)ง','ლ(•́•́ლ)','ʕ •́؈•̀ ₎','♪♪ ヽ(ˇ∀ˇ )ゞ','щ（ﾟДﾟщ）','( ˇ෴ˇ )','눈_눈','(๑•́ ₃ •̀๑) ','( ˘ ³˘)♥ ','ԅ(≖‿≖ԅ)','♥‿♥','◔_◔','⁽⁽ଘ( ˊᵕˋ )ଓ⁾⁾','乁( ◔ ౪◔)「      ┑(￣Д ￣)┍','( ఠൠఠ )ﾉ','٩(๏_๏)۶','┌(ㆆ㉨ㆆ)ʃ','ఠ_ఠ','(づ｡◕‿‿◕｡)づ','(ノಠ ∩ಠ)ノ彡( \\o°o)\\','“ヽ(´▽｀)ノ”','༼ ༎ຶ ෴ ༎ຶ༽','｡ﾟ( ﾟஇ‸இﾟ)ﾟ｡','(づ￣ ³￣)づ','(⊙.☉)7','ᕕ( ᐛ )ᕗ','t(-_-t)','(ಥ⌣ಥ)','ヽ༼ ಠ益ಠ ༽ﾉ','༼∵༽ ༼⍨༽ ༼⍢༽ ༼⍤༽','ミ●﹏☉ミ','(⊙_◎)','¿ⓧ_ⓧﮌ','ಠ_ಠ','(´･_･`)','ᕦ(ò_óˇ)ᕤ','⊙﹏⊙','(╯°□°）╯︵ ┻━┻','¯\_(⊙︿⊙)_/¯','٩◔̯◔۶','°‿‿°','ᕙ(⇀‸↼‶)ᕗ','⊂(◉‿◉)つ','V•ᴥ•V','q(❂‿❂)p','ಥ_ಥ','ฅ^•ﻌ•^ฅ','ಥ﹏ಥ','（ ^_^）o自自o（^_^ ）','ಠ‿ಠ','ヽ(´▽`)/','ᵒᴥᵒ#','( ͡° ͜ʖ ͡°)','┬─┬﻿ ノ( ゜-゜ノ)','ヽ(´ー｀)ノ','☜(⌒▽⌒)☞','ε=ε=ε=┌(;*´Д`)ﾉ','(╬ ಠ益ಠ)','┬─┬⃰͡ (ᵔᵕᵔ͜ )','┻━┻ ︵ヽ(`Д´)ﾉ︵﻿ ┻━┻','¯\_(ツ)_/¯','ʕᵔᴥᵔʔ','(`･ω･´)','ʕ•ᴥ•ʔ','ლ(｀ー´ლ)','ʕʘ̅͜ʘ̅ʔ','（　ﾟДﾟ）','¯\(°_o)/¯','(｡◕‿◕｡)']
    index=randint(0,len(reactor))
    reply_text=reactor[index]
    await event.edit(reply_text)
@client.on(events.NewMessage(outgoing=True, pattern='.fastpurge'))
async def fastpurge(event):
   chat = await event.get_input_chat()
   msgs = []
   count =0
   async with aclosing(client.iter_messages(chat, min_id=event.reply_to_msg_id)) as h:
    async for m in h:
        msgs.append(m)
        count=count+1
        if len(msgs) == 100:
            await client.delete_messages(chat, msgs)
            msgs = []
   if msgs:
       await client.delete_messages(chat, msgs)
   await client.send_message(event.chat_id,"`Fast Purge Complete!\n`Purged "+str(count)+" messages.")
   await client.send_message(-266765687,"Purge of "+str(count)+" messages done successfully.")
   time.sleep(2)
   i=1
   async for message in client.iter_messages(event.chat_id,from_user='me'):
        if i>1:
            break
        i=i+1
        await message.delete()
@client.on(events.NewMessage(outgoing=True, pattern='.zucc'))
async def zucc(event):
    with open('zucc.txt', 'r') as f:
        content = f.readlines()
    content = content[0].rstrip()
    with open(str(content), 'r') as zucc:
        await event.edit("```Uploading```")
        await client.send_file(event.chat_id, content)
    await client.send_message(-266765687,str(content)+" uploaded to "+str(event.sender_id))
@client.on(events.NewMessage(outgoing=True, pattern='.stop'))
async def stop(event):
    os.execl(sys.executable, sys.executable, *sys.argv)
if len(sys.argv) < 2:
    client.run_until_disconnected()
