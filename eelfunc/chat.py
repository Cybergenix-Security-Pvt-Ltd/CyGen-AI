import asyncio
import logging

from brain import classify
from features.app_launcher import AppLauncher
from features.chat import Chat
from features.image_manager import ImageManager
from features.realtime import RealChat
from features.reminder import Reminder
from features.system import System
from main import get_image, sanitize
from utils.speech_manager import speak

username = "Tejas"

rchat = RealChat(username)
chat = Chat(username)
system = System()
app_launcher = AppLauncher()
reminder = Reminder()
image_manager = ImageManager()


def realtime_chat(query: str):
    logging.info(f"realtime chat: {query}")
    return rchat.chat(query)


def llm_chat(query: str):
    logging.info(f"llm chat: {query}")
    return chat.chat(query)


def web_speak(query: str):
    speak(query)


def ask(query: str | None) -> str | None:
    if not query:
        return None
    logging.info(f"main classifier: {query}")
    tags = classify(query)
    if not tags:
        return "Sorry i have no answer for it!"
    logging.info(f"Classified: {tags}")
    for tag in tags:
        stag = sanitize(tag)
        if chat.check_trigger(tag):
            logging.info(f"Thinking for tag: {stag}")
            return chat.chat(stag) or "I have no answer!!"
        elif rchat.check_trigger(tag):
            logging.info(f"Searching on internet for tag: {stag}")
            return rchat.chat(stag) or "I was unable to search on internet"
        elif reminder.check_trigger(tag):
            logging.info(f"Setting reminder for tag: {stag}")
            reminder.set_reminder(stag)
            return f"Reminder added of {stag}"
        elif image_manager.check_trigger(tag):
            if " vision" in tags:
                logging.info(f"Analyzing Image")
                return image_manager.read_img(get_image(), stag)
            else:
                logging.info(f"Generating Image")
                asyncio.run(image_manager.generate_images(stag))
                return "Here are some of the images"

        elif system.check_trigger(tag):
            if " mute" in stag:
                logging.info(f"Muting system")
                system.mute()
                return "System Muted"
            elif " unmute" in stag:
                logging.info(f"Unmuting system")
                system.unmute()
                return "System Unmuted"
            elif (" increase" or "up") in stag:
                logging.info(f"Increasing volume for tag: {stag}")
                system.volume_up()
                return "Increased the volume!!"
            elif (" decrease" or "down") in stag:
                logging.info(f"Decreasing volume for tag: {stag}")
                system.volume_down()
                return "Decreased the volume!!"
            elif (" exit" or " exit" or " quit") in stag:
                logging.info(f"Exiting system")
                exit()

        elif app_launcher.check_trigger(tag):
            if tag.startswith("google search"):
                logging.info(f"Searching on google for tag: {stag}")
                app_launcher.gsearch(stag)
                return f"Your search for {stag} result is ready on screen"
            elif tag.startswith("youtube search"):
                logging.info(f"Searching on youtube for tag: {stag}")
                app_launcher.ytsearch(stag)
                return "Your youtube search result is ready on screen"
            elif tag.startswith("play"):
                logging.info(f"Playing music for tag: {stag}")
                app_launcher.play_music(stag)
                return f"Playing {stag}"
            elif tag.startswith("open"):
                logging.info(f"Opening application for tag: {stag}")
                app_launcher.open(stag)
                return f"Launced {stag}"
            elif tag.startswith("close"):
                logging.info(f"Closing application for tag: {stag}")
                app_launcher.close(stag)
                return f"Closed {stag}"
