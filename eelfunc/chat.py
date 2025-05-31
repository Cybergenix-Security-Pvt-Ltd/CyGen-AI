import logging

from features.chat import Chat
from features.realtime import RealChat

logger = logging.Logger(__name__)

username = "Tejas"

rchat = RealChat(username)
chat = Chat(username)

def realtime_chat(query: str):
    logger.info(f"realtime chat: {query}")
    return rchat.chat(query)

def llm_chat(query: str):
    logger.info(f"llm chat: {query}")
    return chat.chat(query)
