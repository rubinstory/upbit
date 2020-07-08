import discord as discord
import calculate as upbit

client = discord.Client()


@client.event
async def on_ready():
    print(client.user.id)
    print("ready")
    game = discord.Game("상태메시지")
    await client.change_presence(status=discord.Status.online, activity=game)



@client.event
async def on_message(message):
    if message.content.startswith("!안녕"):
        await message.channel.send("안녕하세요")

    if message.content.startswith("!비트코인"):
        result = upbit.calculate('BTC')
        await message.channel.send(result)
        await message.channel.send(file = discord.File('./graph/BTC.png'))
        
    if message.content.startswith("!비트코인 캐시"):
        result = upbit.calculate('BCH')
        await message.channel.send(result)
    
    if message.content.startswith("!이더리움"):
        result = upbit.calculate('ETH')
        await message.channel.send(result)
    
    if message.content.startswith("!라이트코인"):
        result = upbit.calculate('LTC')
        await message.channel.send(result)
    
    if message.content.startswith("!리플"):
           result = upbit.calculate('XRP')
           await message.channel.send(result)
    
    if message.content.startswith("!에이다"):
           result = upbit.calculate('ADA')
           await message.channel.send(result)
        
    if message.content.startswith("!목록"):
        result = "비트코인 : BTC\n이더리움 : ETH\n비트코인 캐시 : BTC\n라이트코인 : LTC\n리플 : XRP\n에이다코인 : ADA"
        await message.channel.send(result)


client.run("NzMwMjc2MjAwNTI1ODU2ODAw.XwVM8Q.W9YKocBNL92Xmpnv6g7kpWbT0xY")
