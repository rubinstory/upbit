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

    if message.content.startswith("!계산"):
        result = upbit.calculate()
        await message.channel.send(result)


client.run("NzMwMjc2MjAwNTI1ODU2ODAw.XwVI_Q.J9P3OtEArpHJb5IrNTHXBw_BvhY ")
