from ollama import chat
from ollama import ChatResponse
from .base import Base




class Chat(Base):
    def __init__(self, username: str, query: str) -> None:
        self.username = username
        self.chat_history = []
        self.raw_query = query
        self.query = query.replace("general", "")

    def check_trigger(self) -> bool:
        if self.raw_query.startswith("general"):
            return True
        return False

    def chat(self) -> str | None:
        sys_prompt = [{"role": "system", "content" : f"""Hello, I am {self.username}, You are a very accurate and advanced AI chatbot named Cygen which also has real-time up-to-date information from the internet.
                          *** Do not tell time until I ask, do not talk too much, just answer the question.***
                          *** Reply in only English, even if the question is in Hindi, reply in English.***
                          *** Do not provide notes in the output, just answer the question and never mention your training data. ***
                          """
                          }]
        usr_prompt = [{
            "role": "user",
            "content": self.query
            }]
        response: ChatResponse = chat(model="llama3.2:1b", messages=sys_prompt + self.chat_history + usr_prompt)

        if not response.message.content: return None

        self.chat_history.append(
        [
            {
            "role": "user",
            "content": self.query
            },

            {
            "role": "ChatBot",
            "content": response.message.content
            }
        ])

        return response.message.content


def cli():
    chatbot = Chat('MyName', 'hi how are you')
    print(chatbot.chat())


if __name__ == "__main__":
    cli()
