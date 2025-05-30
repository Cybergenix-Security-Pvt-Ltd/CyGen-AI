import subprocess
import os

from features.base import Base


class AppLauncher(Base):

    def check_trigger(self, query: str) -> bool:
        if query.startswith(("google search", "youtube search", "play", "open", "close")):
            return True
        return False

    def gsearch(self, query: str) -> None:
        os.system(
                f"firefox 'https://www.google.com/search?client=firefox-b-e&q={query.replace(" ", "+")}'"
                )

    def ytsearch(self, query: str) -> None:
        os.system(f"firefox 'https://www.youtube.com/results?search_query={query.replace(" ", "+")}'")

    def play_music(self, query: str):
        os.system(f"yt-dlp 'ytsearch:{query}'")

    def close(self, application: str) -> None:
        pid = subprocess.run(f"pgrep {application}", capture_output=True, text=True, shell=True)
        os.system(f"kill {pid}")

    def open(self, application: str) -> None:
        if application.startswith((".com", ".io", ".app", ".net")):
            os.system(f"firefox '{application}'")
        else:
            os.system(application)
