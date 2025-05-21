import speech_recognition as sr
import os
import requests

def speech_recognition():
    while True:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.pause_threshold = 5
            r.phrase_threshold = 5
            audio = r.listen(source)
            try:
                print("Cygen is Recognizing...")
                query = r.recognize_google(audio) # type: ignore
                print(f"You: {query}\n")
                return str(query)
            except Exception as e:
                print("Cygen AI: Say that again please...",e)
                return None

def speak(content: str) -> None:
    print("Cygen Ai: ", content)
    lines = content.split(".")
    voiceID = 'p364'
    text = "mpv --terminal=no --really-quiet"
    for idx,line in enumerate(lines):
        resp = requests.get(f"http://localhost:4000/api/tts?text={line}&speaker_id={voiceID}&style_wav=&language_id=;")
        with open(f"temp_audio{idx}.mp3", "wb") as f:
            f.write(resp.content)
        text += f" temp_audio{idx}.mp3"
    text += "&> /dev/null"

    os.system(text)



if __name__ == "__main__":
    speech_recognition()
