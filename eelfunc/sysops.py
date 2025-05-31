import logging

from features.system import System
from features.app_launcher import AppLauncher

logger = logging.Logger(__name__)

system = System()
app_launcher = AppLauncher()

def mute_system():
    logging.info("muting system")
    system.mute()
    return "System Muted"

def unmute_system():
    logging.info("unmuting system")
    system.unmute()
    return "System Unmuted"

def set_volume_up():
    logging.info("increasing volume")
    system.volume_up()
    return "Increased the volume!!"

def set_volume_down():
    logging.info("decreasing volume")
    system.volume_down()
    return "Decreased the volume!!"

def close_app(app_name):
    logging.info(f"closing {app_name}")
    app_launcher.close(app_name)
    return f"Closed {app_name}"

def open_app(app_name):
    logging.info(f"opening {app_name}")
    app_launcher.open(app_name)
    return f"Launched {app_name}"

