from pathlib import Path
from typing import List

import cv2
import eel

from brain import classify
from utils.speech_manager import speech_recognition, speak
from features.chat import Chat
from features.system import System
from features.realtime import RealChat
from features.app_launcher import AppLauncher
from features.reminder import Reminder
from features.image_manager import ImageManager

USERNAME = "Tejas"

eel.init("web")

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

    import eel

    @eel.expose
    def send_command(command):
        # Process manual commands from UI
        tags = classify(command) or []
        if not tags:
            return "Sorry, I didn't understand that command."
        stag = sanitize(tags[0]) if tags else command
        # Reuse logic from main() for each feature
        # Example for chat:
        if chat.check_trigger(tags[0]):
            return chat.chat(stag) or "I have no answer!!"
        # Add similar checks for other features
        return "Command processed."

    @eel.expose
    def get_response():
        # Return the last spoken response (you may need to store it in a global variable)
        return "Assistant response"

    @eel.expose
    def capture_image():
        try:
            img_path = get_image()
            return image_manager.read_img(img_path, "analyze")
        except Exception as e:
            return f"Error capturing image: {e}"

    @eel.expose
    def mute_system():
        system.mute()
        return "System Muted"

    @eel.expose
    def unmute_system():
        system.unmute()
        return "System Unmuted"

    @eel.expose
    def set_volume_up():
        system.volume_up()
        return "Increased the volume!!"

    @eel.expose
    def set_volume_down():
        system.volume_down()
        return "Decreased the volume!!"

    @eel.expose
    def open_app(app_name):
        app_launcher.open(app_name)
        return f"Launched {app_name}"

    @eel.expose
    def close_app(app_name):
        app_launcher.close(app_name)
        return f"Closed {app_name}"

    @eel.expose
    def google_search(query):
        app_launcher.gsearch(query)
        return f"Your search for {query} result is ready on screen"

    @eel.expose
    def youtube_search(query):
        app_launcher.ytsearch(query)
        return "Your YouTube search result is ready on screen"

    @eel.expose
    def play_music(query):
        app_launcher.play_music(query)
        return f"Playing {query}"

    @eel.expose
    def set_reminder(reminder_text):
        reminder.set_reminder(reminder_text)
        return f"Reminder added of {reminder_text}"
    eel.start("./main.html")
    while True:
        data = listen()
        print(f"Classifying started")
        tags = classify(data)
        if not tags: return None
        print(f"Classified: {tags}")
        for tag in tags:
            stag = sanitize(tag)
            if chat.check_trigger(tag):
                print("Thinking")
                speak(chat.chat(stag) or 'I have no answer!!')
            elif realchat.check_trigger(tag):
                speak("Wait for a while.. i m searching on internet")
                speak(realchat.chat(stag) or "I was unable to search on internet")
            elif reminder.check_trigger(tag):
                reminder.set_reminder(stag)
                speak(f"Reminder added of {stag}")
            elif image_manager.check_trigger(tag):
                speak(f"Analyzing Image")
                speak(image_manager.read_img(get_image(),stag))
                
            elif system.check_trigger(tag):
                if ' mute' in stag:
                    system.mute()
                    speak("System Muted")
                elif ' unmute' in stag:
                    system.unmute()
                    speak("System Unmuted")
                elif (' increase' or 'up') in stag:
                    print(f"increase trigger {stag}")
                    system.volume_up()
                    speak("Increased the volume!!")
                elif (' decrease' or 'down') in stag:
                    print(f"decrease trigger {stag}")
                    system.volume_down()
                    speak("Decreased the volume!!")
                elif (' exit' or ' exit' or ' quit') in stag:
                    speak("I think its time to go now!")
                    break

            elif app_launcher.check_trigger(tag):
                if tag.startswith('google search'):
                    app_launcher.gsearch(stag)
                    speak(f"Your search for {stag} result is ready on screen")
                elif tag.startswith('youtube search'):
                    app_launcher.ytsearch(stag)
                    speak("Your youtube search result is ready on screen")
                elif tag.startswith('play'):
                    app_launcher.play_music(stag)
                    speak(f"Playing {stag}")
                elif tag.startswith('open'):
                    app_launcher.open(stag)
                    speak(f"Launced {stag}")
                elif tag.startswith('close'):
                    app_launcher.open(stag)
                    speak(f"Closed {stag}")



if __name__ == "__main__":
    main()
