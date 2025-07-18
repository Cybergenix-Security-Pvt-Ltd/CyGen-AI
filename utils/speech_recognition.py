from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
import mtranslate as mt

inputLanguage = 'en'

html_code = '''<!DOCTYPE html>
<html lang="en">

<head>
    <title>Speech Recognition</title>
</head>

<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>

    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {
            recognition = new webkitSpeechRecognition() || new SpeechRecognition();
            recognition.lang = '';
            recognition.continuous = true;

            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript;
            };

            recognition.onend = function() {
                recognition.start();
            };
            recognition.start();
        }

        function stopRecognition() {
            recognition.stop();
            output.innerHTML = ""
        }
    </script>
</body>

</html>'''

html_code = str(html_code).replace("recognition.lang = '';",f"recognition.lang = '{inputLanguage}';")

with open(r"Data\Voice.html","w") as f:
      f.write(html_code)

current_dir = os.getcwd()
Link = f"{current_dir}\\Data\\Voice.html"
chrome_options = Options()
chrome_options.binary_location = "/home/knownblackhat/dev/cygen_old/chrome/chromedriver-linux64/chromedriver"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36"
chrome_options.add_argument("user-data-dir=.")
chrome_options.add_argument('profile-directory=Profile 2')
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--use-fake-device-for-media-stream")
chrome_options.add_argument("--headless=new")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)


def query_modifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["how", "what", "who", "where", "when", "why", "which", "whose", "whom","can you","what's","where's","how's", "can you"]

    if any(word + " " in new_query for word in question_words):
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"

    else:
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "."
        else:
            new_query += "."

    return new_query.capitalize()

def universal_translator(Text):
    english_translation = mt.translate(Text, "en", "auto")
    return english_translation.capitalize()

def speech_recognition():

    driver.get("file:///" + Link)
    driver.find_element(by=By.ID,value="start").click()

    while True:
        try:
            Text = driver.find_element(by=By.ID,value="output").text
            if Text:
                driver.find_element(by=By.ID,value="end").click()
                if inputLanguage.lower() == "en" or "en" in inputLanguage.lower():
                    return query_modifier(Text)
                else:
                    return query_modifier(universal_translator(Text))
        except:
            pass

if __name__ == "__main__":
    while True:
        print("listening")
        Text = speech_recognition()
        print("processed")
        print(Text)
