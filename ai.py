from ai_assets import *

import pyttsx3, random
'''pyttsx3 is a python text-to-speech library'''


class AI:
    def __init__(self, name, voice, rate = None):
        self.name = name
        self.voice = voice
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty("voices")

        if rate != None:
            self.engine.setProperty("rate", rate)

    def say(self, words):
        self.engine.setProperty("voice", self.voices[self.voice].id)
        self.engine.say(words)
        self.engine.runAndWait()

    def intro (self):
        greeting = random.choice(GREETINGS)
        greeting = greeting.replace("NAME", self.name)
        self.say(greeting)

DEFAULT = AI("Butler", MALE, 180)