import logging
import importlib
import pkgutil
from typing import Callable, List, Tuple

import eel

import eelfunc

logger = logging.getLogger(__name__)


class EELInterface:
    def __init__(self) -> None:
        self.functions: List[Tuple[str, Callable]] = []
        for module in pkgutil.walk_packages(eelfunc.__path__, "eelfunc."):
            imported = importlib.import_module(module.name)
            self.functions = self.functions+ [x for x in imported.__dict__.items() if callable(x[1]) and not x[0].startswith('_') and not x[0][0].isupper()]
                    

    def expose(self) -> None:
        for fn in self.functions:
            logger.info(f"{fn[0]} is active")
            eel.expose(fn[1])
