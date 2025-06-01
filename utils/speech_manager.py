import os

import requests
import speech_recognition as sr
from elevenlabs import play
from elevenlabs.client import ElevenLabs

client = ElevenLabs(api_key="sk_56d9b4bc64d01bc6c5257803f3158a37e0261992772e6475")


def speech_recognition() -> str | None:
    while True:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.pause_threshold = 1
            r.energy_threshold = 50
            audio = r.listen(source)
            try:
                print("Cygen is Recognizing...")
                query = r.recognize_google(audio)  # type: ignore
                print(f"You: {query}\n")
                return str(query)
            except Exception as e:
                print("Cygen AI: Say that again please...", e)
                return None


def speak(content: str) -> None:
    content = f"ummmm, {content}"
    lines = content.split(".")
    voiceID = "p308"  #'p364'
    text = "mpv --terminal=no --really-quiet"
    for idx, line in enumerate(lines):
        resp = requests.get(
            f"http://localhost:4000/api/tts?text={line}&speaker_id={voiceID}&style_wav=&language_id=;"
        )
        with open(f"temp_audio{idx}.mp3", "wb") as f:
            f.write(resp.content)
        text += f" temp_audio{idx}.mp3"
    text += "&> /dev/null"

    os.system(text)


def speak_v2(content: str) -> None:
    print(content)
    audio = client.generate(
        text=content,
        voice="Adam",  # Choose your preferred voice
        model="eleven_monolingual_v1",
    )
    print("Cygen Ai: ", content)
    play(audio)


if __name__ == "__main__":
    speech_recognition()
