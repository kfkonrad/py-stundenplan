from typing import NoReturn
from lib.clock import Clock

class Span:  # Zeitspanne aus 2 Clock-Objekten
    begin: Clock
    end: Clock
    length: int

    def __init__(self,
                 begin: Clock,
                 end: Clock
                 ) -> NoReturn:
        self.begin = begin
        self.end = end
        self.length = (self.end - self.begin).hash

    def __contains__(self, item: Clock) -> bool:
        return self._isbetween(item)

    def __sub__(self, other) -> int:
        return self.distance(other)

    def distance(self, other):
        return self.end.hash - other.begin.hash

    def _isbetween(self,
                   clock: Clock
                   ) -> bool:
        return self.begin.hash <= clock.hash <= self.end.hash

    def pprint(self) -> str:
        return self.begin.pprint() + ' - ' + self.end.pprint()
