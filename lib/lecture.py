from typing import List, NoReturn
from lib.t import T

class Lecture:  # Vorlesungen/Fächer
    subject: str
    room: str
    schedule: List[T]

    def __init__(self,
                 subject: str,
                 room: str,
                 *schedule: T
                 ) -> NoReturn:
        self.subject = subject
        self.room = room
        self.schedule = schedule

    def pprint(self,
               n: int
               ) -> str:
        ret: str = self.schedule[n].pprint() + ": " + self.subject
        ret += " (" + self.__get_room_for_lecture(n) + ")"
        return ret

    def __get_room_for_lecture(self,
                               n: int) -> str:
        if self.schedule[n].room is None:
            return self.room
        return self.schedule[n].room
