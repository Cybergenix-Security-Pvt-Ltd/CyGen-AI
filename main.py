from pathlib import Path
from typing import List

import cv2

from brain import classify
from utils.speech_manager import speech_recognition, speak
from features.chat import Chat
from features.system import System
from features.realtime import RealChat
from features.app_launcher import AppLauncher
from features.reminder import Reminder
from features.image_manager import ImageManager

USERNAME = "Tejas"

def listen() -> str:
    data = speech_recognition()
    print(data)
    return data or 'nothing'


def sanitize(query: str) -> str:
    words: List[str] = [
    "exit", "general", "realtime", "open", "close", "play",
    "generate image", "system", "content", "google search",
    "youtube search", "reminder"
    ]

    for word in words:
        if query.startswith(word):
            query =  query.replace(word, '') 
            break

    return query

def get_image() -> Path:
    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        raise IOError("Cannot open webcam")

    result, image = cam.read()

    if result:
        cv2.imshow("Captured Image", image)
        
        cv2.imwrite("captured_image.jpg", image)

        cv2.waitKey(0)
        
        cv2.destroyAllWindows()
    else:
        print("No image detected. Please try again.")

    cam.release()
    return Path('./captured_image.jpg')

def main():
    chat = Chat(USERNAME)
    realchat = RealChat(USERNAME)
    system = System()
    app_launcher = AppLauncher()
    reminder = Reminder()
    image_manager = ImageManager()

    data = listen()
    if tags:=classify(data):
        for tag in tags:
            stag = sanitize(tag)
            chat.chat(stag) if chat.check_trigger(tag) else None
            realchat.chat(stag) if realchat.check_trigger(tag) else None
            reminder.set_reminder(stag) if reminder.check_trigger(tag) else None
            image_manager.check_trigger(stag) if image_manager.read_img(get_image(),tag) else None

            if system.check_trigger(tag):
                if ' mute' in stag:
                    system.mute()
                elif ' unmute' in stag:
                    system.unmute()
                elif ' increase' or 'up' in stag:
                    system.volume_up()
                elif ' decrease' or 'down' in stag:
                    system.volume_down()

            if app_launcher.check_trigger(tag):
                if tag.startswith('google search'):
                    app_launcher.gsearch(stag)
                elif tag.startswith('youtube search'):
                    app_launcher.ytsearch(stag)
                elif tag.startswith('play'):
                    app_launcher.play_music(stag)
                elif tag.startswith('open'):
                    app_launcher.open(stag)
                elif tag.startswith('close'):
                    app_launcher.open(stag)
    speak(data)



if __name__ == "__main__":
    main()
