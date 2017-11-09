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
        -> TODO: Research correct julian functions
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
Version 1.6 (08/11.2017)
    Split into library and code.
    Refactored code to follow the pyflakes style guidelines.
    Reshaped semester files to form complete library files and valid python
        programs on their own.
"""

import time
from lecture_classes import *
import sys

from wise1718 import *
giveargs = True
split = ";"


def datetojulian(y, m, d):  # Gregorianisches Datum zu julian date
    d = int(d)
    m = int(m)
    y = int(y)
    jd = (1461 * (y + 4800 + (m - 14) / 12)) / 4 + (367 * (m - 2 - 12 * (
        (m - 14) / 12))) / 12 - (3 * ((y + 4900 +
                                       (m - 14) / 12) / 100)) / 4 + d - 32075
    return int(jd)


def juliantodate(jd):  # julian date zu gregorianischem Datum
    h = jd + 68569
    n = (4 * h) // 146097
    h = h - (146097 * n + 3) // 4
    i = (4000 * (h + 1)) // 1461001
    h = h - (1461 * i) // 4 + 31
    j = (80 * h) // 2447
    d = h - (2447 * j) // 80
    h = j // 11
    m = j + 2 - (12 * h)
    y = 100 * (n - 49) + i + h
    if d < 10:
        d = "0" + str(d)
    else:
        d = str(d)
    if m < 10:
        m = "0" + str(m)
    else:
        m = str(m)
    return int(str(y) + m + d)


def geteom(m, y):  # Determine end of month
    if m in (1, 3, 5, 7, 8, 10, 12):
        return 31
    elif m == 2:
        if (y % 4 == 0 and y % 100 != 0) or y % 400 == 0:
            return 29
        else:
            return 28
    else:
        return 30


def numericdatecorrect(date):  # correct date format after increment
    date = str(date)
    y = int(date[:4])
    m = int(date[4:6])
    d = int(date[6:])
    eom = geteom(m, y)
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


def dayinc(addX=1):  # Erhöht Datum um 1 Tag, erhöht Wochentag zyklisch
    global todaywd, todaydate
    todaywd = (todaywd + addX) % 7
    # julian=datetojulian(str(todaydate)[0:4],
    #                    str(todaydate)[4:6],
    #                    str(todaydate)[6:8])
    # todaydate=juliantodate(julian+addX+1)
    todaydate = numericdatecorrect(todaydate + addX)


# Funktionen zu processor


def getend(fach):  # Bestimmt Ende der aktuellen Stunde, sofern vorhanden
    global ctime  # aktuelle end-Zeit
    if 'ctime' not in globals():  # initialisiert ctime einmalig
        ctime = clock()
    spanne = fach[-1]
    # localtime-clock erzeugen
    localt = clock(time.strftime("%H:%M"))
    # Testcase: localt=clock("12:00")
    # gegen localtime testen und ggf ersetzen
    if spanne.isbetween(localt):
        ctime = spanne.end
    return ctime


def getlen(fach):  # Bestimmt Ende der aktuellen Stunde, sofern vorhanden
    global lentime  # aktuelle end-Zeit
    if 'lentime' not in globals():  # initialisiert ctime einmalig
        lentime = 0
    spanne = fach[-1]
    # localtime-clock erzeugen
    localt = clock(time.strftime("%H:%M"))
    # Testcase: localt=clock("12:00")
    # gegen localtime testen und ggf ersetzen
    if spanne.isbetween(localt):
        lentime = spanne.length()
    return lentime


def qsort(classes):  # Quicksort für Class-Array
    if classes == []:
        return []
    else:
        pivot = classes.pop(0)
        lesser = qsort([i for i in classes if int(i[0]) < int(pivot[0])])
        greater = qsort([i for i in classes if int(i[0]) >= int(pivot[0])])
        return lesser + [pivot] + greater


def correct(thisfaecher):  # Korrigens basierend auf holiday, add, rem
    holibool = False
    for arr in holiday:  # Ferien bestimmen
        if todaydate >= arr[0] and todaydate <= arr[1]:
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


def processor(wd):  # Gibt Fächerliste für den aktuellen Tag aus. Gibt Ende der
    # aktuellen Stunde, Tages zurück
    todayClasses = []
    thisfaecher = copy.deepcopy(faecher)
    thisfaecher = correct(thisfaecher)
    # if len(thisfaecher)>0:
    #    print(thisfaecher[-1])
    #    thisfaecher[-1].pprint(0)
    for fach in thisfaecher:
        for i in range(0, len(fach.schedule)):
            # print(wd,fach.schedule[i].wd,fach.subject)
            if wd == fach.schedule[i].wd:  # Wenn Fach heute stattfinded
                todayClasses.append([
                    fach.schedule[i].begin.h,
                    fach.pprint(i), fach.schedule[i].bespan
                ])
    if len(todayClasses) == 0:
        print("frei")
        return clock(), clock(), 0, 0
    todayClasses = qsort(todayClasses)
    end = clock()
    currentlen = 0
    daylen = todayClasses[-1][-1].end.hash - todayClasses[0][-1].begin.hash
    for fach in todayClasses:
        end = getend(fach)
        currentlen = getlen(fach)
        print(fach[1])
    return [end, todayClasses[-1][-1].end, currentlen, daylen]


def wdtostr(wd):  # Gibt numerischen Wochentag menschenlesbar aus
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


def howlong(endTclass, endTday):  # Bestimmt, wie lange die Stunde/der Tag
    #   noch geht
    localt = clock(time.strftime("%H:%M", time.localtime()))
    # Testcase: localt=clock("12:00")
    endTclass = copy.deepcopy(endTclass)
    endTday = copy.deepcopy(endTday)
    endTclass.minus(localt)
    endTday.minus(localt)
    if endTclass.hash > 0:
        print()
        print("Diese Stunde noch:", endTclass.pprint())
        print("Heute noch:", endTday.pprint())
    elif endTday.hash > 0:
        print()
        print("Heute noch:", endTday.pprint())


def addClass(date, name, room, start, end):
    # julian=datetojulian(str(todaydate)[0:4],
    #                    str(todaydate)[4:6],
    #                    str(todaydate)[6:8])
    # wd=(julian+2)%7
    date = str(date)
    wd = int(datetime.strptime(date, "%Y%m%d").strftime("%w")) - 1

    # print(wd,int(datetime.strptime(str(todaydate),"%Y%m%d").strftime("%w")))
    # print(date,name,wd)
    return (date, Class(name, room, T(start, end, 5)))


for elem in ['faecher', 'rem', 'add', 'holiday', 'remall']:
    if elem not in globals():
        setattr(sys.modules[__name__], elem, [])

# Wochentag, Datum
todaywd = int(time.strftime("%w"))
# Testcase: todaywd=5
todaydate = int(
    time.strftime("%Y") + time.strftime("%m") + time.strftime("%d"))

print("Heute:")
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
