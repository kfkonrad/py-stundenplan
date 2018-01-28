"""
Version 1.0 (20/04/2016) - now supporting versioning.
  uses clock, span, T, Class objects for easier time-handling.

  Support for parsable output added. Use giveargs=True to add CSV info with
  split as its seperator. Semicolon, tab or comma are usually good seperators.

  Better code alignment: no line exceeds 80 characters.

Version 1.1 (03/10/2016)
  dayinc supports optional number for skipping n days instead of just one day,
  good for testing purposes.

  addClass function added. With addClass the weekday needn't be given in the
  add array, providing a more convenient interface.

  The database is now imported from external files, making maintainance and
  switching semesters/years easy and straightforward. Global variable semester
  is introduced to bring swapping semesters to the beginning of the file.

 Version 1.1.1 (06/10/2016)
    add will work for all days, not just for today
    apparently the julian functions are badly broken
Version 1.2 (13/10/2016)
    julian functions were NOT broken
    all it needed to fix the bug was an index shift
Version 1.3 (30/11/2016)
    Replaced julian dates by manual date format correcting function
    numericdatecorrect. dayinc is now much easier to understand, bugs are
    easier to find (hopefully).
    Fixes a bug concerning adding Classes after the current date.
    Julian functions are not used anymore, the code stays for legacy reasons.
    addClass is still broken, I really don't know how to fix that.
Version 1.4 (21/03/2017)
    Updated semester-data for Sommersemester 2017
    Added covenience feature for faster, more human-readable input of T-objects
        that follow the standard lecture timeframes of HSKL.
    Each of these functions support T's optional room argument.
    B(<1..5>,weekday)
    morgen(weekday)     == B (1,weekday) == T("08:00","09:30",weekday)
    vormittag(weekday)  == B (2,weekday) == T("09:45","11:15",weekday)
    mittag(weekday)     == B (3,weekday) == T("11:45","13:15",weekday)
    nachmittag(weekday) == B (4,weekday) == T("14:00","15:30",weekday)
    abend(weekday)      == B (5,weekday) == T("15:45","17:15",weekday)
Version 1.5 (05/04/2017)
    Added functionality to remove all Classes of a certain subject after a
        given date.
    Added remall to list the remall Classes, it basically works like rem except
        it will remove the Class on the given date and any date greater than
        that date.
    remall might look like this: remall = [ (20170815,"Fach") ]
    This definition would remove all instances of "Fach" that occur from
        20170815 on, including 20170815.
Version 1.6 (08/11/2017)
    Split into library and code.
    Refactored code to follow the pyflakes style guidelines.
    Reshaped semester files to form complete library files and valid python
        programs on their own.
Version 1.7 (28/01/2018)
    Added type hints as proposed in PEP 484 and PEP 526.
    Thus this script is only compatible with Python 3.6 or higher.
    Removed unused legacy functions datetojulian and juliantodate
    Renamed the following classes (oldname -> newname)
        clock -> Clock
        span -> Span
        Class -> Lecture
    Renamed the follwing functions:
        addClass -> add_lecture
    Changed variable names and comments to fit new classnames and PEP
        conventions.
"""

import time
import datetime
from lecture_classes import *
import sys
from typing import Any

from wise1718 import *

giveargs: bool = True
split: str = ";"


def geteom(m: int,
           y: int
           ) -> int:  # Determine end of month
    if m in (1, 3, 5, 7, 8, 10, 12):
        return 31
    elif m == 2:
        if (y % 4 == 0 and y % 100 != 0) or y % 400 == 0:
            return 29
        else:
            return 28
    else:
        return 30


def numericdatecorrect(date: int) -> int:
    # correct date format after increment
    strdate: str = str(date)
    y: int = int(strdate[:4])
    m: int = int(strdate[4:6])
    d: int = int(strdate[6:])
    eom: int = geteom(m, y)
    if d > eom:
        d = 1
        m += 1
        if m > 12:
            m = 1
            y += 1
    if m < 10:
        m = "0" + str(m)
    if d < 10:
        d = "0" + str(d)
    return int(str(y) + str(m) + str(d))


def dayinc(add_days: int = 1) -> None:
    # Erhöht Datum um 1 Tag, erhöht Wochentag zyklisch
    global todaywd, todaydate
    todaywd = (todaywd + add_days) % 7
    # julian=datetojulian(str(todaydate)[0:4],
    #                    str(todaydate)[4:6],
    #                    str(todaydate)[6:8])
    # todaydate=juliantodate(julian+addX+1)
    todaydate = numericdatecorrect(todaydate + add_days)


# Funktionen zu processor


def getend(fach: List[Span]) -> Clock:  # Bestimmt Ende der aktuellen Stunde,
    # sofern vorhanden
    global ctime  # aktuelle end-Zeit
    if 'ctime' not in globals():  # initialisiert ctime einmalig
        ctime = Clock()  # type: Clock
    spanne: Span = fach[-1]
    # localtime-Clock erzeugen
    localt: Clock = Clock(time.strftime("%H:%M"))
    # Testcase: localt=Clock("12:00")
    # gegen localtime testen und ggf ersetzen
    if spanne.isbetween(localt):
        ctime = spanne.end
    return ctime


def getlen(fach: List[Any]) -> int:  # beinhaltet immer int, str, Span.
    # Aufgrund verschiedener Konversionen ist List[Any] der allgemeinste Typ,
    # der fach beschreiben kann.
    # Bestimmt Ende der aktuellen Stunde, sofern vorhanden
    global lentime  # aktuelle end-Zeit
    if 'lentime' not in globals():  # initialisiert lentime einmalig
        lentime = 0  # type: int
    spanne: Span = fach[-1]
    # localtime-Clock erzeugen
    localt: Clock = Clock(time.strftime("%H:%M"))
    # Testcase: localt=Clock("12:00")
    # gegen localtime testen und ggf ersetzen
    if spanne.isbetween(localt):
        lentime = spanne.length()
    return lentime


def qsort(lectures: List[Any]) -> List[Any]:  # Quicksort für Lecture-List
    if not lectures:
        return []
    else:
        pivot: Any = lectures.pop(0)
        lesser: List[Any]
        greater: List[Any]
        lesser = qsort([i for i in lectures if int(i[0]) < int(pivot[0])])
        greater = qsort([i for i in lectures if int(i[0]) >= int(pivot[0])])
        return lesser + [pivot] + greater


def correct(thisfaecher: List[Lecture]) -> List[Lecture]:
    # Korrigens basierend auf holiday, add, rem
    holibool: bool = False
    for arr in holiday:  # Ferien bestimmen
        if arr[0] <= todaydate <= arr[1]:
            holibool = True
            break
    # Bei Fächern, die am aktuellen Tag nicht stattfinden sollen, wird der
    # schedule geflusht. Info stammt aus rem
    for i in range(0, len(thisfaecher)):
        for j in range(0, len(rem)):
            if todaydate == rem[j][0]:  # Datum passt
                if thisfaecher[i].subject == rem[j][1]:  # Fächername passt
                    thisfaecher[i].schedule = ()
    # Bei Fächern, die nicht mehr stattfinden sollen, wird der
    # schedule geflusht. Info stammt aus remall
    for j in range(0, len(remall)):
        if todaydate >= remall[j][0]:  # Datum passt
            for i in range(0, len(thisfaecher)):
                if thisfaecher[i].subject == remall[j][1]:  # Fächername passt
                    thisfaecher[i].schedule = ()
    # Hier werden einmalige Termine hinzugefügt. Info stammt aus add
    for i in range(0, len(add)):
        if todaydate == add[i][0]:
            thisfaecher.append(add[i][1])
            # print(add[i][1].schedule[0].pprint(),end=";")
    if holibool:  # Wenn Ferien sind, dann finden keine Stunden statt :)
        thisfaecher = []
    return thisfaecher


# Funktionen zur main


def processor(wd: int) -> Tuple[Clock, Clock, int, int]:
    # Gibt Fächerliste für den aktuellen Tag aus. Gibt Ende der aktuellen
    # Stunde, Tages zurück.
    todaylectures: List[Any] = []  # beinhaltet immer int, str, Span. Aufgrund
    # verschiedener Konversionen ist List[Any] der allgemeinste Typ, der
    # todaylectures beschreiben kann.
    thisfaecher: List[Lecture] = copy.deepcopy(faecher)
    thisfaecher = correct(thisfaecher)
    # if len(thisfaecher)>0:
    #    print(thisfaecher[-1])
    #    thisfaecher[-1].pprint(0)
    for fach in thisfaecher:
        for i in range(0, len(fach.schedule)):
            # print(wd,fach.schedule[i].wd,fach.subject)
            if wd == fach.schedule[i].wd:  # Wenn Fach heute stattfinded
                todaylectures.append([
                    fach.schedule[i].begin.h,
                    fach.pprint(i), fach.schedule[i].bespan
                ])
    if len(todaylectures) == 0:
        print("frei")
        return Clock(), Clock(), 0, 0
    todaylectures = qsort(todaylectures)
    end: Clock = Clock()
    current_len: int = 0
    day_len: int = todaylectures[-1][-1].end.hash
    day_len -= todaylectures[0][-1].begin.hash
    for fach in todaylectures:
        end = getend(fach)
        current_len = getlen(fach)
        print(fach[1])
    return end, todaylectures[-1][-1].end, current_len, day_len


def wdtostr(wd: int) -> None:  # Gibt numerischen Wochentag menschenlesbar aus
    if wd == 0:
        print("Sonntag:")
    elif wd == 1:
        print("Montag:")
    elif wd == 2:
        print("Dienstag:")
    elif wd == 3:
        print("Mittwoch:")
    elif wd == 4:
        print("Donnerstag:")
    elif wd == 5:
        print("Freitag:")
    elif wd == 6:
        print("Samstag:")
    else:
        print(wd)


def howlong(endtclass: Clock,
            endtday: Clock
            ) -> None:
    # Bestimmt, wie lange die Stunde/der Tag noch geht
    localt: Clock = Clock(time.strftime("%H:%M", time.localtime()))
    # Testcase: localt=Clock("12:00")
    endtclass = copy.deepcopy(endtclass)
    endtday = copy.deepcopy(endtday)
    endtclass.minus(localt)
    endtday.minus(localt)
    if endtclass.hash > 0:
        print()
        print("Diese Stunde noch:", endtclass.pprint())
        print("Heute noch:", endtday.pprint())
    elif endtday.hash > 0:
        print()
        print("Heute noch:", endtday.pprint())


def add_lecture(date: int,
                name: str,
                room: str,
                start: str,
                end: str
                ) -> Tuple[str, Lecture]:
    # julian=datetojulian(str(todaydate)[0:4],
    #                    str(todaydate)[4:6],
    #                    str(todaydate)[6:8])
    # wd=(julian+2)%7
    strdate = str(date)
    wd: int = int(datetime.strptime(strdate, "%Y%m%d").strftime("%w")) - 1

    # print(wd,int(datetime.strptime(str(todaydate),"%Y%m%d").strftime("%w")))
    # print(date,name,wd)
    return strdate, Lecture(name, room, T(start, end, wd))


for elem in ['faecher', 'rem', 'add', 'holiday', 'remall']:
    if elem not in globals():
        setattr(sys.modules[__name__], elem, [])

# Wochentag, Datum
todaywd = int(time.strftime("%w"))  # type: int
# Testcase: todaywd=5
todaydate = int(
    time.strftime("%Y")
    + time.strftime("%m")
    + time.strftime("%d")
)  # type: int

print("Heute:")
untilclass: Clock
untilday: Clock
currentlen: int
daylen: int
untilclass, untilday, currentlen, daylen = processor(todaywd)
print("-----")
print("Morgen:")
dayinc()
processor(todaywd)
print("-----")
dayinc()
wdtostr(todaywd)
processor(todaywd)
howlong(untilclass, untilday)
if giveargs:
    print(currentlen, daylen, sep=split, end="")
