from typing import List
import os

from features.base import Base

class System(Base):

    def check_trigger(self) -> bool:
        if self.query.startswith("system"):
            return True
        return False

    def volume_up(self, amount: int):
        os.system(f"pactl set-sink-volume @DEFAULT_SINK@ +{amount}%")

    def volume_down(self, amount: int):
        os.system(f"pactl set-sink-volume @DEFAULT_SINK@ -{amount}%")

    def mute(self):
        os.system(f"pactl set-sink-mute @DEFAULT_SINK@ 1")

    def unmute(self):
        os.system(f"pactl set-sink-mute @DEFAULT_SINK@ 0")
