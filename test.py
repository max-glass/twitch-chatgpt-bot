

import pyglet
import random
import time
import threading
from gtts import gTTS
from twitchio.ext import commands
import key

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

# Twitch chat command that plays an audio file generated from the given string periodically
class Bot(commands.Bot):
    def __init__(self):
        super().__init__(token = key.OAUTH_TOKEN, prefix='!', initial_channels = [key.CHANNEL_NAME])

    # Periodiclly play a random promotional string from a list
    def promo():
        while True:
            # Choose a random string from the potential_responses list
            message = random.choice(potential_responses)
            print("\n" + message + "\n")

            # Convert the string to an audio file
            tts = gTTS(text = message)
            tts.save("string.mp3")

            # Play the audio file using pyglet
            speech = pyglet.media.Player()
            speech.queue(pyglet.media.load("string.mp3", streaming=False))
            speech.volume = 0.1
            speech.play()

            # Sleep for 15 minutes (900 seconds) before playing the audio file again
            time.sleep(900)

    # Start the promo function in a separate thread
    thread = threading.Thread(target=promo)
    thread.start()

    # Event that runs every time the bot goes online
    async def event_ready(self):
        # Notify us when everything is ready!
        print(f'Logged in as | {self.nick}')
        print(f'User ID is | {self.user_id}')