import discord
import threading
import asyncio
import random
import time
import os

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))
client = MyClient()

schedule = ['Total.png','Mon.png','Tue.png','Wed.png','Thu.png','Fri.png']
DotW = ['월','화','수','목','금']

gamePlayer = []
wordList = [[], []]
usedWord = []
gameChannel = ''
isgameplaying = False
gameCount = 0
f = open('단어.txt', 'r')
words = str(f.readline()).split()
f.close()
cats = ['20200819_222730.jpg', '0074KBdTgy1ghvb6ir2b9j30hg0hg40l.jpg']

async def add_word():
    global wordList
    global usedWord
    global gameCount
    global isgameplaying
    global gamePlayer
    if isgameplaying == True:
        gameCount += 1
        if (gameCount > 10):
            await gameChannel.send('```css\n[' + str(gamePlayer[0].nick) + '] 님과 [' + str(
                gamePlayer[1].nick) + '] 님의 게임 지속시간이 10분이 지났습니다. 무승부로 게임이 종료됩니다.\n[' + str(
                gamePlayer[0].nick) + '] 님의 금칙어:' + str(wordList[0]) + '\n[' + str(
                gamePlayer[1].nick) + '] 님의 금칙어:' + str(wordList[1]) + '```')
            isgameplaying = False

        else:
            detect = random.choice(words)
            while detect in usedWord:
                detect = random.choice(words)
            wordList[0].append(detect)
            usedWord.append(detect)

            detect = random.choice(words)
            while detect in usedWord:
                detect = random.choice(words)
            wordList[1].append(detect)
            usedWord.append(detect)

            await gameChannel.send('```css\n[' + str(gamePlayer[0].nick) + '] 님과 [' + str(gamePlayer[1].nick) + '] 님의 게임 지속시간이' + gameCount + '분이 지났습니다. 금칙어가 추가되었습니다.```')
            await gamePlayer[0].send(
                '```css\n[' + str(gamePlayer[1].nick) + '] 님의 금칙어는' + str(wordList[1]) + '입니다. 해당 단어를 언급하도록 유도하세요```')
            await gamePlayer[1].send(
                '```css\n[' + str(gamePlayer[0].nick) + '] 님의 금칙어는' + str(wordList[0]) + '입니다. 해당 단어를 언급하도록 유도하세요```')
            timer = threading.Timer(60, add_word)
            timer.start()

@client.event
async def on_message(message):
    global isgameplaying
    global gamePlayer
    global wordList
    global gameCount
    global gameChannel
    global usedWord
    global words

    print(message.content)
    if message.author.bot == False:

        if message.author in gamePlayer:
            if message.author == gamePlayer[0]:
                for word in wordList[0]:
                    if len(message.content.split(word)) != 1:
                        await gameChannel.send('```css\n[' + str(gamePlayer[1].nick) + '] 님이 우승하셨습니다.\n[' + str(
                            gamePlayer[0].nick) + '] 님의 금칙어:' + str(wordList[0]) + '\n[' + str(
                            gamePlayer[1].nick) + '] 님의 금칙어:' + str(wordList[1]) + '```')
                        isgameplaying = False
                        wordList = [[], []]
                        usedWord = []
                        gamePlayer = []
                        break
            else:
                for word in wordList[1]:
                    if len(message.content.split(word)) != 1:
                        await gameChannel.send('```css\n[' + str(gamePlayer[0].nick) + '] 님이 우승하셨습니다.\n[' + str(
                            gamePlayer[1].nick) + '] 님의 금칙어:' + str(wordList[1]) + '\n[' + str(
                            gamePlayer[0].nick) + '] 님의 금칙어:' + str(wordList[0]) + '```')
                        isgameplaying = False
                        isgameplaying = False
                        wordList = [[], []]
                        usedWord = []
                        gamePlayer = []
                        break

        if message.content.startswith("!금칙어게임 "):
            if isgameplaying == True:
                if len(gamePlayer) == 2:
                    await message.channel.send('```css\n['+ str(gamePlayer[0].nick) + ']님과 [' + str(gamePlayer[1].nick) +']님의 게임이 진행중입니다```')
                else:
                    await message.channel.send('```다른 플레이어의 요청이 진행중입니다```')
            elif len(message.content.split()) == 2 and len(message.mentions) == 1:
                if message.mentions[0].bot == True or message.mentions[0] == message.author:
                    await message.channel.send('적절하지 않은 플레이어 입니다')
                else:
                    isgameplaying = True
                    await message.channel.send('```css\n['+str(message.mentions[0].nick) + '] 님에게 게임 요청을 보냈습니다 (20초 후 초대장 만료)```')
                    apply = await message.mentions[0].send('```css\n['+str(message.author.nick) +']님으로부터 금칙어 게임 신청이 들어왔습니다. 아래 이모지로 응답해주세요. (20초 후 초대장 만료)```')
                    await apply.add_reaction('✅')
                    channel = message.channel
                    def check(reaction, user):
                        return user == message.mentions[0] and str(reaction.emoji) == '✅'

                    try:
                        reaction, user = await client.wait_for('reaction_add', timeout=20.0, check=check)
                    except asyncio.TimeoutError:
                        await message.channel.send('```css\n['+str(message.mentions[0].nick) + ']님이 응답하지 않았습니다. 게임 진행이 취소되었습니다.```')
                        isgameplaying = False
                    else:
                        gamePlayer = [message.author, message.mentions[0]]
                        isgameplaying = True
                        wordList = [[], []]
                        for i in range(10):
                            detect = random.choice(words)
                            while detect in usedWord:
                                detect = random.choice(words)
                            wordList[0].append(detect)
                            usedWord.append(detect)
                        for i in range(10):
                            detect = random.choice(words)
                            while detect in usedWord:
                                detect = random.choice(words)
                            wordList[1].append(detect)
                            usedWord.append(detect)
                        gameChannel = message.channel
                        gameCount = 0
                        await message.channel.send('```css\n['+ str(gamePlayer[0].nick) + '] 님과 ['+str(gamePlayer[1].nick)+'] 님의 금칙어 게임이 시작되었습니다.```')
                        await gamePlayer[0].send('```css\n['+ str(gamePlayer[1].nick) + '] 님의 금칙어는' + str(wordList[1]) + '입니다. 해당 단어를 언급하도록 유도하세요```')
                        await gamePlayer[1].send('```css\n['+ str(gamePlayer[0].nick) + '] 님의 금칙어는' + str(wordList[0]) + '입니다. 해당 단어를 언급하도록 유도하세요```')

                        #threading.Timer(60, add_word).start()
            else:
                await message.channel.send('!금칙어게임 [@같이할_플레이어] 형식으로 사용해주세요')

        if message.content.startswith('!아바타 '):
            if len(message.mentions) != 1:
                await message.channel.send('!아바타 [@플레이어] 형식으로 사용해주세요')
            else:
                await message.channel.send(message.mentions[0].avatar_url)

        if message.content == '!고양이':
            await message.channel.send(file=discord.File(random.choice(cats)))

        if str(message.content) == '!금지추가':
            if str(message.author.id) == '500854374541557771':
                if isgameplaying == False:
                    await message.channel.send('게임 진행중이 아닙니다')
                else:
                    detect = random.choice(words)
                    while detect in usedWord:
                        detect = random.choice(words)
                    wordList[0].append(detect)
                    usedWord.append(detect)

                    detect = random.choice(words)
                    while detect in usedWord:
                        detect = random.choice(words)
                    wordList[1].append(detect)
                    usedWord.append(detect)

                    await gameChannel.send('```css\n[' + str(gamePlayer[0].nick) + '] 님과 [' + str(gamePlayer[1].nick) + '] 님의 게임에 금칙어가 추가되었습니다.```')
                    await gamePlayer[0].send('```css\n[' + str(gamePlayer[1].nick) + '] 님의 금칙어는' + str(wordList[1]) + '입니다. 해당 단어를 언급하도록 유도하세요```')
                    await gamePlayer[1].send('```css\n[' + str(gamePlayer[0].nick) + '] 님의 금칙어는' + str(wordList[0]) + '입니다. 해당 단어를 언급하도록 유도하세요```')
            else:
                await message.channel.send('관리자가 아닙니다')
                
        if message.content.startswith('!단어추가 '):
            if str(message.author.id) == '500854374541557771':
                if message.content.split()[1] in words:
                    await message.channel.send('```css\n[' + str(message.content.split()[1]) + ']는 이미 금칙어 목록에 존재합니다 (현재 금칙어 개수: ' + str(len(words)) + ')```')
                else:
                    f = open('단어.txt', 'a')
                    f.write(' ' + str(message.content.split()[1]))
                    f.close()
                    f = open('단어.txt', 'r')
                    words = f.readline().split()
                    f.close()
                    await message.channel.send('```css\n['+str(message.content.split()[1]) + ']를 금칙어 목록에 추가했습니다 (현재 금칙어 개수: ' + str(len(words))+ ')```')
            else:
                await message.channel.send('관리자가 아닙니다')

        if str(message.content) == '!금칙어목록':
            if str(message.author.id) == '500854374541557771':
                content = ''
                for i in words:
                    content +='[' + i + ']\n'
                await message.channel.send('```css\n-금칙어 목록-\n' + content + '(현재 금칙어 개수: ' + str(len(words)) + ')```')
            else:
                await message.channel.send('관리자가 아닙니다')

        if message.content.startswith('!단어삭제 '):
            if str(message.author.id) == '500854374541557771':
                if message.content.split()[1] in words:
                    f = open('단어.txt', 'r')
                    content = f.readline()
                    f.close()
                    content += ' '
                    content = content.replace(' ' + str(message.content.split()[1]) + ' ', ' ')
                    content = content[0:(len(content) - 1)]
                    f = open('단어.txt', 'w')
                    f.write(content)
                    f.close()
                    f = open('단어.txt', 'r')
                    words = f.readline().split()
                    f.close()
                    await message.channel.send('```css\n[' + str(message.content.split()[1]) + ']를 금칙어 목록에서 삭제했습니다 (현재 금칙어 개수: ' + str(len(words)) + ')```')
                else:
                    await message.channel.send('해당 금칙어가 존재하지 않습니다')
            else:
                await message.channel.send('관리자가 아닙니다')
        if str(message.content) == '!시간표':
            await message.channel.send('__**구암고등학교 1-2 전체시간표**__', file=discord.File(schedule[0]))
        elif str(message.content) == '!오늘시간표':
            today = time.localtime().tm_wday
            if today > 4:
                today = 0

            await message.channel.send('__**구암고등학교 1-2 ' + DotW[today] + '요일시간표**__', file=discord.File(schedule[today + 1]))
        elif str(message.content) == '!내일시간표':
            today = time.localtime().tm_wday
            today += 1
            if today > 4:
                today = 0

            await message.channel.send('__**구암고등학교 1-2 ' + DotW[today] + '요일시간표**__',file=discord.File(schedule[today + 1]))

client.run(os.environ['token'])