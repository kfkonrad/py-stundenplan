from typing import Optional, NoReturn
from lib.clock import Clock
from lib.span import Span

class T:  # Start-Ende-Uhrzeiten, Wochentag, ggf Raum. Für Lecture
    begin: Clock
    end: Clock
    bespan: Span
    weekday: int
    room: str

    def __init__(self,
                 begin: str,
                 end: str,
                 weekday: int,
                 room: Optional[str] = None
                 ) -> NoReturn:
        self.begin = Clock(begin)
        self.end = Clock(end)
        self.bespan = Span(self.begin, self.end)
        self.weekday = weekday
        self.room = room

    def pprint(self) -> str:
        return self.bespan.pprint()
