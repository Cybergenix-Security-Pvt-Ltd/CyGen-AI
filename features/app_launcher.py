from features.base import Base
import os


class AppLauncher(Base):

    def check_trigger(self) -> bool:
        if self.query.startswith(("google search", "youtube", "play")):
            return True
        return False

    def gsearch(self, query: str) -> None:
        os.system(
                f"firefox https://www.google.com/search?client=firefox-b-e&q={query.replace(" ", "+")}"
                )

    def ytsearch(self, query: str) -> None:
        os.system(f"firefox https://www.youtube.com/results?search_query={query.replace(" ", "+")}")

    def play_music(self, query: str):
        os.system(f"yt-dlp 'ytsearch:{query}'")

    def close(self, application: str) -> None:
        pid = os.system(f"pgrep {application}")
        os.system(f"kill {pid}")

    def open(self, application: str) -> None:
        if application.startswith((".com", ".io", ".app", ".net")):
            os.system(f"firefox '{application}'")
        else:
            os.system(application)

