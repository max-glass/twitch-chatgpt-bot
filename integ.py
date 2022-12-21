
# mxGlass
# twitch.tv/mxglass

import logging
import openai
from twitchio.ext import commands
import key
from gtts import gTTS
import pyglet
import os

# Set up logging
logging.basicConfig(level = logging.INFO)

global music
global responses
responses = []
TTSReady = True

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
        # tts = gTTS(text = response)
        # tts.save("speech.mp3")
        # music = pyglet.resource.media('speech.mp3')
        # music.volume = 0.1
        # music.play()
        # os.remove("speech.mp3")
        # End of bandaid fix

        responses.append(response)
        print("Responses: ")
        print(len(responses))

        # Split the response into chunks of 500 characters (Twitch max message length)
        n = 500
        chunks = [response[i:i+n] for i in range(0, len(response), n)]
        for chunk in chunks:
            await ctx.send(chunk)

    def tts(responses):
        for x in responses:
            tts = gTTS(text = x)
            tts.save("speech.mp3")
            music = pyglet.resource.media('speech.mp3')
            music.volume = 0.1
            music.play()
            os.remove("speech.mp3")
    tts(responses)

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
        await ctx.send(f'Hello {ctx.author.name}!')

    @commands.command()
    async def shutup(self, ctx: commands.Context):
        TTSReady = False
        main(TTSReady)
        

    async def event_message(self, message):
        if message.echo:
            return

        # Print the contents of our message to console...
        print(message.content)

        await self.handle_commands(message)

# bot = Bot()
# bot.run()

def main(TTSReady):
    if TTSReady == False:
        bot = Bot()
        bot.run()
        TTSReady = True

if __name__ == "__main__":
    main(TTSReady)

# while True:
#     if TTSReady == True:
#         if len(responses) > 0:
#             TTSReady = False
#             response = responses.pop()
#             tts = gTTS(text = response)
#             tts.save("speech.mp3")
#             music = pyglet.resource.media('speech.mp3')
#             music.volume = 0.1
#             music.play()
#             TTSReady = True
#             os.remove("speech.mp3")
