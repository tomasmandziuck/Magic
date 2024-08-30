import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response
import logging as logger


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
    
    if is_private:
        user_message = user_message[1:]
    if username.lower() == "agusproche":
        await message.author.send("Se requiere autorizacion del propietario para habilitar servicio")
        return
    
    try:
        response= get_response(user_message,username,logger)
        await message.author.send(response) if is_private else await message.channel.send(response)

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