
# mxGlass
# twitch.tv/mxglass

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

# Set up logging
logging.basicConfig(level = logging.INFO)

responses = []
TTSReady = True
global music

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(token = key.OAUTH_TOKEN, prefix='!', initial_channels = [key.CHANNEL_NAME])

    # Command that sends a message to the chat using OpenAI's GPT-3 API
    @commands.command()
    async def chatgpt(self, ctx: commands.Context, *, question: str):
        openai.api_key = key.API_KEY
        prompt = (f"{question}\n")
        completions = openai.Completion.create(
            engine = "text-davinci-002",
            prompt = prompt,
            max_tokens = 2048,
            n = 1,
            stop = None,
            temperature = 0.7,
        )

        response = completions.choices[0].text
        
        # TODO: Remove this bandaid fix
        # Bandaid fix for the bot not being able to speak
        tts = gTTS(text = response)
        tts.save("response.mp3")
        global music
        music = pyglet.media.player('response.mp3')
        music.volume = 0.1
        music.play()

        os.remove("response.mp3")
        # End of bandaid fix
        
        global responses
        responses.append(response)

        # Split the response into chunks of 500 characters (Twitch max message length)
        n = 500
        chunks = [response[i:i+n] for i in range(0, len(response), n)]
        count = 1
        for chunk in chunks:
            await ctx.send(chunk)
            count += 1
        print("Number of chunks: ",count)

    async def stop_music(self):
        music.stop()
        print("Music stopped")

    @commands.command()
    async def shutup(self, ctx: commands.Context):
        await self.stop_music()

        loop = asyncio.new_event_loop()
        asyncio.run_coroutine_threadsafe(self.stop_music(), loop)

        thread = threading.Thread(target = self.stop_music)
        thread.start()


    # Event when the bot goes online and is ready to chat
    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User ID is | {self.user_id}')

    # Basic command that sends a message back to the user
    @commands.command()
    async def hello(self, ctx: commands.Context):
        # Send a hello back!
        await ctx.send(f'Fuck you, {ctx.author.name}!')

    async def event_message(self, message):
        if message.echo:
            return

        # Print the contents of our message to console...
        print(message.content)

        await self.handle_commands(message)

    #     def runTTSpromo():
    #         task = asyncio.create_task(ttsPromo())
    #         while True:
    #             sleep(5)
    #             task
    #     asyncio.run(runTTSpromo())
    # promo()

    @routines.routine(seconds = 5.0)
    async def promo():
        # def ttsPromo():
        potential_responses = ["Don't forgot to follow me on Twitch!",
                                "If you enjoy this stream, don't forget to follow me on Twitch! It's free!",
                                "If you want to see more of this, don't forget to follow me on Twitch!",
                                "Interested in the development process for this stream/bot? Check out twitch.tv/mxGlass",
                                "Check out twitch.tv/mxGlass for more content like this!",
                                "Want to be part of our community? Check out twitch.tv/mxGlass",
                                "Thanks for talking with me, chat! Don't forget to follow me on Twitch!",
                                "Want to contribute to the development of this bot? Check out twitch.tv/mxGlass and get involved on GitHub!",
                                "If you enjoy this bot, remember you can always use your Twitch Prime sub on me -- ChatGPT!"
                                "Take money from Jeff Bezos and give it to me! Twitch Prime sub on OpenAIChatGPT!",
                                "If you'd rather support the developer, you can always subscribe/follow him on Twitch! twitch.tv/mxGlass",
                                ]

        # Randomly select a response from potential_responses
        response = random.choice(potential_responses)
        tts = gTTS(text = response)
        tts.save("prewritten_response.mp3")
        promo_speech = pyglet.media.player("prewritten_response.mp3")
        promo_speech.volume = 0.1
        promo_speech.play()
        pass

def run():
    bot = Bot()
    bot.run()
run()