# WiSe 16/17
"""
morgen(weekday)     == T("08:00","09:30",weekday)
vormittag(weekday)  == T("09:45","11:15",weekday)
mittag(weekday)     == T("11:45","13:15",weekday)
nachmittag(weekday) == T("14:00","15:30",weekday)
abend(weekday)      == T("15:45","17:15",weekday)
"""

from typing import List, Tuple
import lecture_classes as lc

Lecture = lc.Lecture
T = lc.T
morgen = lc.morgen
vormittag = lc.vormittag
mittag = lc.mittag
nachmittag = lc.nachmittag
abend = lc.abend

faecher: List[Lecture] = []
rem: List[Tuple[int, str]] = []
add: List[Tuple[int, Lecture]] = []
holiday: List[Tuple[int, int]] = []

faecher = [
    Lecture("DB-V", "A136", T("09:45", "11:15", 1)),
    Lecture("DB-Ü", "A216.2", T("09:45", "11:15", 2)),
    Lecture("LAG-V", "A136", T("11:30", "13:00", 1)),
    Lecture("LAG-Ü", "A135", T("15:45", "17:15", 4)),
    Lecture("PROG2-V", "A125", T("11:45", "13:15", 3)),
    Lecture("PROG2-P", "Q011", T("08:00", "09:30", 2)),
    Lecture("MEDGES", "A135", T("08:00", "09:30", 3)),
    Lecture("MEDGES-Ü", "O213", T("11:45", "13:15", 4)),
    Lecture("SE-V", "Audimax", T("08:00", "09:30", 4), T("09:45", "11:15", 4)),
    Lecture("SE-Ü", "G224", T("09:45", "11:15", 3)),
    Lecture("unixAG", "A204.2", T("14:00", "16:00", 3)),
]

rem = [(20161005, "SE-Ü"), (20161005, "unixAG"), (20161006, "LAG-Ü"),
       (20161006, "MEDGES-Ü"), (20161006, "SE-V"), (20161011, "DB-Ü"),
       (20161012, "SE-Ü"), (20161109, 'PROG2-V'), (20170111, 'SE-Ü'),
       (20170112, 'SE-V'), (20170112, 'LAG-Ü')]

add = [
    (20161006, Lecture("SE-V", "Audimax", T('08:00', "09:39", 4))),
    (20161006, Lecture("SE-V", "Audimax", T('09:45', "12:15", 4))),
    (20161202, Lecture("TTTTTT", "Audimax", T('19:45', "20:15", 5))),
    # addLecture(20161202, "TEST", "A205.2", '20:00', "22:00"),
]

holiday = [(20000101, 20161004), (20170201, 20171231)]
