# mxGlass

import logging
import openai
from twitchio.ext import commands
import key
from gtts import gTTS
import pyglet
import os

# TODO: Implement image creation and auto upload to Imgur
# TODO: Paste code responses in a Pastebin/Codebin, hard to determine if it's a code response or not

# Set up logging
logging.basicConfig(level = logging.INFO)

responses = []
TTSReady = True

class Bot(commands.Bot):

    def __init__(self):

        super().__init__(token = key.OAUTH_TOKEN, prefix='!', initial_channels = [key.CHANNEL_NAME])

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
        
        global responses
        responses.append(response)

        n = 500
        chunks = [response[i:i+n] for i in range(0, len(response), n)]
        for chunk in chunks:
            await ctx.send(chunk)
        # await ctx.send(response)

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User ID is | {self.user_id}')

    async def event_message(self, message):
        if message.echo:
            return

        # Print the contents of our message to console...
        print(message.content)

        await self.handle_commands(message)

bot = Bot()
bot.run()

while True:
    if TTSReady == True:
        if len(responses) > 0:
            TTSReady = False
            response = responses.pop()
            tts = gTTS(text = response)
            tts.save("speech.mp3")
            music = pyglet.resource.media('speech.mp3')
            music.volume = 0.1
            music.play()
            TTSReady = True
            os.remove("speech.mp3")