import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response
import logging as logger
import bot_config


logger.basicConfig(filename="magic.log", level=logger.INFO)
#Load token
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

#Setup bot
intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)

#Message func
async def send_message(message,user_message,username,logger):
    if not user_message:
        print("no hay mensage porque probablemente no hay intents")
        return
    is_private = user_message[0] == "?"
    is_general= user_message[0] == "!"
    user_message = user_message[1:]
    command = user_message.split(" ")

    if username.lower() == bot_config.ENEMY_USER:
        await message.author.send("Se requiere autorizacion del propietario para habilitar servicio")
        return
    
    try:
        for input in user_message.split(";"):
            responses= get_response(input,username,command[0],logger)
            #await message.author.send(response) if is_private else await message.channel.send(response)
            for response in responses:
                if is_private:
                    await message.author.send(response)
                elif is_general:
                    await message.channel.send(response)


    except Exception as ex:
        print(ex)

#handle bot startup
@client.event
async def on_ready():
    print (f"{client.user}is now running")

#handle incoming messages
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    username = str(message.author.name)
    user_message = message.content
    channel = str(message.channel)

    print(f"{channel}, {username}:{user_message}")

    await send_message(message, user_message, username,logger)

# def main
def main():
    client.run(token=TOKEN)

if __name__ == "__main__":
    main()