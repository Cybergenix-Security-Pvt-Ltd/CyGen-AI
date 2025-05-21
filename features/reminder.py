from typing import Any, Dict, List, Optional
from features.base import Base
import datetime
import json


class Reminder(Base):
    def check_trigger(self) -> bool:
        if self.query.startswith('reminder'):
            return True
        return False

    def set_reminder(self, time: str, reason: Optional[str]=None):
        data = {
                'id': 0,
                'time': datetime.datetime.strptime(time,"%H:%M").time(),
                'reason': reason
                }
        with open("reminder.json", 'rw') as fp:
            fdata: List[Dict[str, Any]] = json.load(fp)
            data['id'] = fdata[-1]['id'] + 1
            fdata.append(data)
            json.dump(data, fp)
