# Klassen zu getend

import copy


class clock(object):  # Beinhaltet Uhrzeit (h:min)
    stringv = "00:00"
    h = 0
    m = 0

    def __init__(self, timestring="00:00"):
        self.stringv = timestring
        self.h = int(self.stringv[0:2])
        self.m = int(self.stringv[3:6])
        self.hash = self.h * 60 + self.m

    def minus(self, minuend):
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

    def pprint(self):
        return self.stringv


class span(object):  # Zeitspanne aus 2 clock-Objekten
    begin = clock()
    end = clock()

    def __init__(self, begin, end):
        self.begin = begin
        self.end = end

    def isbetween(self, clock):
        if self.begin.hash <= clock.hash and self.end.hash >= clock.hash:
            return True
        else:
            return False

    def pprint(self):
        return self.begin.pprint() + ' - ' + self.end.pprint()

    def length(self):
        length = copy.deepcopy(self.end)
        length.minus(self.begin)
        return length.hash


# Klassen zu processor / faecher


class T(object):  # Start-Ende-Uhrzeiten, Wochentag, ggf Raum. Für Class

    begin = clock()
    end = clock()
    bespan = span(begin, end)

    wd = None
    room = None

    def __init__(self, begin, end, weekday, room=None):
        # s --> start, e --> end, h --> hour, m --> minute, wd --> weekday

        self.begin = clock(begin)
        self.end = clock(end)
        self.bespan = span(self.begin, self.end)

        self.wd = weekday
        self.room = room

    def pprint(self):
        return self.bespan.pprint()


class Class(object):  # Vorlesungen/Fächer
    subject = ""
    room = ""
    schedule = ()

    def __init__(self, subject, room, *schedule):
        self.subject = subject
        self.room = room
        self.schedule = schedule

    def pprint(self, n):
        a = self.schedule[n].pprint() + ": "
        a += self.subject + " ("
        if self.schedule[n].room is None:
            a += self.room
        else:
            a += self.schedule[n].room
        a += ")"
        return a


# Komfortfunktionen zur schnellen Eingabe der Zeiten nach den Blöcken der HSKL
def B(time, wd, room=None):
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


def morgen(wd, room=None):
    return B(1, wd, room)


def vormittag(wd, room=None):
    return B(2, wd, room)


def mittag(wd, room=None):
    return B(3, wd, room)


def nachmittag(wd, room=None):
    return B(4, wd, room)


def abend(wd, room=None):
    return B(5, wd, room)
