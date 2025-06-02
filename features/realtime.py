import os

from googlesearch import search
from groq import Groq
from ollama import ChatResponse, chat

from features.base import Base

client = Groq(api_key=os.getenv("GROK"))


class RealChat(Base):
    def __init__(self, username: str) -> None:
        self.username = username
        self.chat_history = []

    def check_trigger(self, query: str) -> bool:
        if query.startswith("realtime"):
            return True
        return False

    def google_search(self, query: str) -> str | None:
        results = list(search(query, advanced=True, num_results=5))
        answer = f"The search result for '{query}' are:\n [start]\n"
        for i in results:
            if isinstance(i, str):
                continue
            answer += f"Title: {i.title}\nDescription: {i.description}\n\n"

        answer += "[end]"
        answer.strip().replace("</s>", "")
        return answer

    def chat(self, query: str) -> str | None:
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
        self.chat_history.append(
            {"role": "system", "content": self.google_search(query)}
        )
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

        answer = answer.replace(
            "<|start_header_id|>assistant<|end_header_id|>", ""
        ).strip()
        return answer


def cli():
    chatbot = RealChat("MyName")
    while True:
        query = input("You: ")
        print(chatbot.chat(query))


if __name__ == "__main__":
    cli()
