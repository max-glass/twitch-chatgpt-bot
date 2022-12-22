
# mxGlass
# twitch.tv/mxGlass

import logging
import openai
from twitchio.ext import commands
from twitchio.ext import routines
import key
from gtts import gTTS
import pyglet
import os
import threading
import asyncio
from asyncio import sleep
import random
import time

# Set up logging (uncomment following line to enable logging)
# logging.basicConfig(level = logging.INFO)

# Initialize global variables
global potential_responses
global chatGPT_uses

chatGPT_uses = 0

# Create bot class
class Bot(commands.Bot):

    def __init__(self):
        super().__init__(token = key.OAUTH_TOKEN, prefix='!', initial_channels = [key.CHANNEL_NAME])
    

    # Event that runs every time a message is sent in chat
    async def event_message(self, message):
        if message.echo:
            return
    
        # Print the contents of our message to console...
        print(message.content)
        await self.handle_commands(message)


    # Event that runs every time the bot goes online
    async def event_ready(self):
        # Notify us when everything is ready!
        print(f'Logged in as | {self.nick}')
        print(f'User ID is | {self.user_id}')


    # Command that sends a message to the chat using OpenAI's GPT-3 API
    @commands.command()
    async def chatgpt(self, ctx: commands.Context, *, question: str):
        openai.api_key = key.API_KEY
        prompt = (f"{question}\n")

        completions = openai.Completion.create(
            engine = "text-davinci-002",
            prompt = prompt,
            max_tokens = 1024,
            n = 1,
            stop = None,
            temperature = 0.7,
        )

        response = completions.choices[0].text

        # Bandaid fix for the bot not being able to speak (with the stacking of resonses method)
        tts = gTTS(text = response)
        tts.save("speech.mp3")
        speech = pyglet.resource.media('speech.mp3')
        speech.volume = 0.1
        speech.play()
        os.remove("speech.mp3")

        chatGPT_uses += 1
        if chatGPT_uses % 100 == 0:
            promo = random.choice(potential_responses)
            tts = gTTS(text = promo)
            tts.save("promo.mp3")
            speech.queue(pyglet.media.load("promo.mp3", streaming=False))
            os.remove("promo.mp3")

        # Send the response to the chat, split into chunks if it's too long
        n = 500
        chunks = [response[i:i+n] for i in range(0, len(response), n)]
        for chunk in chunks:
            await ctx.send(chunk)


potential_responses = [ "Don't forgot to follow me on Twitch!",
                        "If you enjoy this stream, don't forget to follow me on Twitch! It's free!",
                        "If you want to see more of this, don't forget to follow me on Twitch!",
                        "Interested in the development process for this stream/bot? Check out twitch.tv/mxGlass",
                        "Check out twitch.tv/mxGlass for more content like this!",
                        "Want to be part of our community? Check out twitch.tv/mxGlass",
                        "Thanks for talking with me, chat! Don't forget to follow me on Twitch!",
                        "Want to contribute to the development of this bot? Check out twitch.tv/mxGlass and get involved on GitHub!",
                        "If you enjoy this bot, remember you can always use your Twitch Prime sub on me -- ChatGPT!"
                        "Take money from Jeff Bezos and give it to me! Twitch Prime sub on OpenAIChatGPT!",
                        "If you'd rather support the developer, you can always subscribe or follow him on Twitch! twitch.tv/mxGlass",
                      ]

def run():
    bot = Bot()
    bot.run()
run()