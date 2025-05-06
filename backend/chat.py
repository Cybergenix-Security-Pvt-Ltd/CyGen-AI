from ollama import chat
from ollama import ChatResponse
from .base import Base




class Chat(Base):
    def __init__(self, username: str) -> None:
        self.username = username
        self.chat_history = []

    def check_trigger(self, query: str) -> bool:
        if query.startswith("general"):
            return True
        return False

    def chat(self, query: str) -> str | None:
        sys_prompt = [{"role": "system", "content" : f"""Hello, I am {self.username}, You are a very accurate and advanced AI chatbot named Cygen which also has real-time up-to-date information from the internet.
                          *** Do not tell time until I ask, do not talk too much, just answer the question.***
                          *** Reply in only English, even if the question is in Hindi, reply in English.***
                          *** Do not provide notes in the output, just answer the question and never mention your training data. ***
                          """
                          }]
        self.chat_history.append({
            "role": "user",
            "content": query
            })
        response: ChatResponse = chat(model="llama3.2:1b", messages=sys_prompt + self.chat_history)

        if not response.message.content: return None

        self.chat_history.append(
        
            {
            "role": "assistant",
            "content": response.message.content
            }
        )

        return response.message.content


def cli():
    chatbot = Chat('MyName')
    while True:
        query = input("You: ")
        print(chatbot.chat(query))


if __name__ == "__main__":
    cli()
