from .base import Base

from ollama import chat
from ollama import ChatResponse
from googlesearch import search

class Chat(Base):
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
            answer += f"Title: {i.title}\nDescription: {i.description}\n\n"

        answer += "[end]"
        answer.strip().replace("</s>", "")
        return answer

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
        self.chat_history.append({"role": "system", "content": self.google_search(query)})
        response: ChatResponse = chat(model="llama3.2:1b", messages=sys_prompt + self.chat_history)
        self.chat_history.pop()

        if not response.message.content: return None

        self.chat_history.append(
        
            {
            "role": "assistant",
            "content": response.message.content
            }
        )

        response.message.content = response.message.content.replace("<|start_header_id|>assistant<|end_header_id|>", "").strip()
        return response.message.content


def cli():
    chatbot = Chat('MyName')
    while True:
        query = input("You: ")
        print(chatbot.chat(query))


if __name__ == "__main__":
    cli()

