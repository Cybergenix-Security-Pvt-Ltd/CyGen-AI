import logging

from features.app_launcher import AppLauncher

app_launcher = AppLauncher()


def google_search(query):
    logging.info(f"google search for {query} ")
    app_launcher.gsearch(query)
    return f"Your search for {query} result is ready on screen"


def youtube_search(query):
    logging.info(f"youtube search for {query} ")
    app_launcher.ytsearch(query)
    return "Your YouTube search result is ready on screen"


def play_music(query):
    logging.info(f"playing music for {query} ")
    app_launcher.play_music(query)
    return f"Playing {query}"
