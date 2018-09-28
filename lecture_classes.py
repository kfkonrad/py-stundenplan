# Klassen zu getend

from typing import List, Optional, Tuple, NoReturn


class Clock:  # Beinhaltet Uhrzeit (h:min)
    _stringv: str
    _h: int
    _m: int

    def __init__(self,
                 timestring: str = "00:00",
                 ) -> NoReturn:
        self._stringv = timestring
        self._h = int(self._stringv[0:2])
        self._m = int(self._stringv[3:6])

    def __sub__(self, other: 'Clock') -> 'Clock':
        h: int = self._h - other._h
        m: int = self._m - other._m
        ret: Clock = Clock()
        ret._m = m
        ret._h = h
        ret.__fix_negative_minutes()
        ret.__set_time_to_zero_if_negative()
        ret.__stringv_reconstruct()
        return ret

    def __fix_negative_minutes(self) -> NoReturn:
        if self._m < 0:
            self._m += 60
            self._h -= 1

    def __set_time_to_zero_if_negative(self) -> NoReturn:
        if self._h < 0:
            self._h = 0
            self._m = 0

    def __stringv_reconstruct(self) -> NoReturn:
        if self._h < 10:
            self._stringv = "0"
            self._stringv += str(self._h)
        else:
            self._stringv = str(self._h)
        self._stringv += ":"
        if self._m < 10:
            self._stringv += "0"
            self._stringv += str(self._m)
        else:
            self._stringv += str(self._m)

    @property
    def hash(self) -> int:
        return self.__hash__()

    def __hash__(self) -> int:
        return self._h * 60 + self._m

    def pprint(self) -> str:
        return self._stringv


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


# Komfortfunktionen zur schnellen Eingabe der Zeiten nach den Blöcken der HSKL
def B(time: int,
      wd: int,
      room: Optional[str] = None
      ) -> T:
    if time == 1:
        return T("08:00", "09:30", wd, room)
    elif time == 2:
        return T("09:45", "11:15", wd, room)
    elif time == 3:
        return T("11:45", "13:15", wd, room)
    elif time == 4:
        return T("14:00", "15:30", wd, room)
    elif time == 5:
        return T("15:45", "17:15", wd, room)
    else:
        return T("00:00", "07:59", wd, room)


def morgen(wd: int,
           room: Optional[str] = None
           ) -> B:
    return B(1, wd, room)


def vormittag(wd: int,
              room: Optional[str] = None
              ) -> B:
    return B(2, wd, room)


def mittag(wd: int,
           room: Optional[str] = None
           ) -> B:
    return B(3, wd, room)


def nachmittag(wd: int,
               room: Optional[str] = None
               ) -> B:
    return B(4, wd, room)


def abend(wd: int,
          room: Optional[str] = None
          ) -> B:
    return B(5, wd, room)
