# Klassen zu getend

import copy
from typing import List, Optional


class Clock(object):  # Beinhaltet Uhrzeit (h:min)
    stringv: str
    h: int
    m: int
    hash: int

    def __init__(self,
                 timestring: str = "00:00"
                 ) -> None:
        self.stringv = timestring
        self.h = int(self.stringv[0:2])
        self.m = int(self.stringv[3:6])
        self.hash = self.h * 60 + self.m

    def minus(self,
              minuend: 'Clock'
              ) -> None:
        self.h -= minuend.h
        self.m -= minuend.m
        if self.m < 0:
            self.m += 60
            self.h -= 1
        if self.h < 0:
            self.h = 0
            self.m = 0
        if self.h < 10:
            self.stringv = "0"
            self.stringv += str(self.h)
        else:
            self.stringv = str(self.h)
        self.stringv += ":"
        if self.m < 10:
            self.stringv += "0"
            self.stringv += str(self.m)
        else:
            self.stringv += str(self.m)
        self.hash = self.h * 60 + self.m

    def pprint(self) -> str:
        return self.stringv


class Span(object):  # Zeitspanne aus 2 Clock-Objekten
    begin: Clock
    end: Clock

    def __init__(self,
                 begin: Clock,
                 end: Clock
                 ) -> None:
        self.begin = begin
        self.end = end

    def isbetween(self,
                  clock: Clock
                  ) -> bool:
        if self.begin.hash <= clock.hash <= self.end.hash:
            return True
        else:
            return False

    def pprint(self) -> str:
        return self.begin.pprint() + ' - ' + self.end.pprint()

    def length(self) -> int:
        length: Clock = copy.deepcopy(self.end)
        length.minus(self.begin)
        return length.hash


# Klassen zu processor / faecher


class T(object):  # Start-Ende-Uhrzeiten, Wochentag, ggf Raum. Für Lecture

    begin: Clock
    end: Clock
    bespan: Span

    wd: int
    room: str

    def __init__(self,
                 begin: str,
                 end: str,
                 weekday: int,
                 room: Optional[str] = None
                 ) -> None:
        # s --> start, e --> end, h --> hour, m --> minute, wd --> weekday

        self.begin = Clock(begin)
        self.end = Clock(end)
        self.bespan = Span(self.begin, self.end)

        self.wd = weekday
        self.room = room

    def pprint(self) -> str:
        return self.bespan.pprint()


class Lecture(object):  # Vorlesungen/Fächer
    subject: str
    room: str
    schedule: List[T]

    def __init__(self,
                 subject: str,
                 room: str,
                 *schedule: T
                 ) -> None:
        self.subject = subject
        self.room = room
        self.schedule = schedule

    def pprint(self,
               n: int
               ) -> str:
        ret: str = self.schedule[n].pprint() + ": "
        ret += self.subject + " ("
        if self.schedule[n].room is None:
            ret += self.room
        else:
            ret += self.schedule[n].room
        ret += ")"
        return ret


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
