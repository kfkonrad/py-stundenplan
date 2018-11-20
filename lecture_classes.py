from typing import Optional
from lib.clock import Clock
from lib.span import Span
from lib.t import T
from lib.lecture import Lecture

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

mo = 1
di = 2
mi = 3
do = 4
fr = 5
sa = 6
so = 0
