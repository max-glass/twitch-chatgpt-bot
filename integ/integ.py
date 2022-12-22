
# mxGlass
# twitch.tv/mxGlass

import logging
import openai
from twitchio.ext import commands
from gtts import gTTS
import pyglet
import os
from asyncio import sleep
import random

import key
import dependencies.promotional as promo

# Set up logging
logging.basicConfig(level = logging.INFO)

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

        # Play the response using gTTS and pyglet
        tts = gTTS(text = response)
        tts.save("speech.mp3")
        speech = pyglet.resource.media('speech.mp3')
        speech.volume = 0.1
        speech.play()
        os.remove("speech.mp3")

        # Increment the number of times chatGPT has been used
        chatGPT_uses += 1
        if chatGPT_uses % 100 == 0:
            # Play a random promotional message from the list
            response = random.choice(potential_responses)
            tts = gTTS(text = response)
            tts.save("promo.mp3")
            speech.queue(pyglet.media.load("promo.mp3", streaming=False))
            os.remove("promo.mp3")

        # Send the response to the chat, split into chunks if it's too long
        charLimit = 500
        chunks = [response[i:i+charLimit] for i in range(0, len(response), charLimit)]
        for chunk in chunks:
            await ctx.send(chunk)


    # Command that makes ChatGPT talk to itself
    @commands.command()
    async def argue(self, ctx: commands.Context, *, opening_prompt: str):
        openai.api_key = key.API_KEY
        prompt = (f"{opening_prompt}\n")

        completions = openai.Completion.create(
            engine = "text-davinci-002",
            prompt = prompt,
            max_tokens = 512,
            n = 1,
            stop = None,
            temperature = 0.7,
        )

        response = completions.choices[0].text

        # Send the response to the chat, split into chunks if it's too long
        charLimit = 500
        chunks = [response[i:i+charLimit] for i in range(0, len(response), charLimit)]
        for chunk in chunks:
            await ctx.send(chunk)

        # Make ChatGPT talk to itself by using the response as the new opening prompt
        await self.argue(ctx, opening_prompt=response)

potential_responses = promo.promotional_responses

def run():
    bot = Bot()
    bot.run()
run()