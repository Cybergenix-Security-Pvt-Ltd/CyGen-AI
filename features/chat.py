import os

from groq import Groq
from ollama import ChatResponse, chat

from .base import Base

client = Groq(api_key=os.getenv("GROK"))


class Chat(Base):
    def __init__(self, username: str) -> None:
        self.username = username
        self.chat_history = []

    def check_trigger(self, query: str) -> bool:
        if query.startswith("general"):
            return True
        return False

    def chat_v1(self, query: str) -> str | None:
        sys_prompt = [
            {
                "role": "system",
                "content": f"""Hello, I am {self.username}, You are a very accurate and advanced AI chatbot named Cygen which also has real-time up-to-date information from the internet.
                          *** Do not tell time until I ask, do not talk too much, just answer the question.***
                          *** Reply in only English, even if the question is in Hindi, reply in English.***
                          *** Do not provide notes in the output, just answer the question and never mention your training data. ***
                          """,
            }
        ]
        self.chat_history.append({"role": "user", "content": query})
        response: ChatResponse = chat(
            model="llama3.2", messages=sys_prompt + self.chat_history
        )

        if not response.message.content:
            return None

        self.chat_history.append(
            {"role": "assistant", "content": response.message.content}
        )

        return response.message.content

    def chat(self, query: str):
        sys_prompt = [
            {
                "role": "system",
                "content": f"""Hello, I am {self.username}, You are a very accurate and advanced AI chatbot named Cygen which also has real-time up-to-date information from the internet.
                          *** Do not tell time until I ask, do not talk too much, just answer the question.***
                          *** Reply in only English, even if the question is in Hindi, reply in English.***
                          *** Do not provide notes in the output, just answer the question and never mention your training data. ***
                          """,
            }
        ]
        self.chat_history.append({"role": "user", "content": query})
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=sys_prompt + self.chat_history,
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None,
        )
        answer = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                answer += chunk.choices[0].delta.content
        answer = answer.replace("</s>", "")

        self.chat_history.append({"role": "assistant", "content": answer})
        return answer

    def codegen(self, query: str):
        sys_prompt = [
            {
                "role": "system",
                "content": f"""Hello, I am {self.username}, You are a very accurate and advanced AI chatbot named Cygen which also has real-time up-to-date information from the internet.
                          *** Do not tell time until I ask, do not talk too much, just answer the question.***
                          *** Reply in only English, even if the question is in Hindi, reply in English.***
                          *** Do not provide notes in the output, just answer the question and never mention your training data. ***
                          *** Write minimal code if asked ***
                          """,
            }
        ]
        self.chat_history.append({"role": "user", "content": query})
        response: ChatResponse = chat(
            model="gemma3:4b", messages=sys_prompt + self.chat_history
        )

        if not response.message.content:
            return None

        self.chat_history.append(
            {"role": "assistant", "content": response.message.content}
        )

        return response.message.content


def cli():
    chatbot = Chat("MyName")
    while True:
        query = input("You: ")
        print(chatbot.chat(query))


if __name__ == "__main__":
    cli()
