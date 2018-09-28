# WiSe 17/18

from typing import List, Tuple
import lecture_classes as lc
# Leider braucht es für eine Erkennung der Namen mit pyflakes diesen
# syntaktischen Käse, ansonsten tut der Code auch mit einem einfachen
# from lecture_classes import *
Lecture = lc.Lecture
T = lc.T
morgen = lc.morgen
vormittag = lc.vormittag
mittag = lc.mittag
nachmittag = lc.nachmittag
abend = lc.abend
"""
morgen(weekday)     == T("08:00","09:30",weekday)
vormittag(weekday)  == T("09:45","11:15",weekday)
mittag(weekday)     == T("11:45","13:15",weekday)
nachmittag(weekday) == T("14:00","15:30",weekday)
abend(weekday)      == T("15:45","17:15",weekday)
"""
faecher: List[Lecture] = []
rem: List[Tuple[int, str]] = []
add: List[Tuple[int, Lecture]] = []
holiday: List[Tuple[int, int]] = []
remall: List[Tuple[int, str]] = []

faecher = [
    Lecture("PRAX", "Science Park SB",
            T("08:00", "16:30", 1),
            T("08:00", "16:30", 2),
            T("08:00", "16:30", 3),
            T("08:00", "16:30", 4),
            T("08:00", "16:30", 5)
            ),
    Lecture("unixAG", "A204.2", T("16:30", "17:30", 3)),
]

rem = [
    (20180509, "unixAG"),
]

add = [
    (20180509,
     Lecture("Mitgliederversammlung unixAG",
             "A209.1",
             T("19:00", "20:30", 3)
             )
     ),
]

remall = [
    (20180601, "PRAX"),
]

holiday = [
    (20180510, 20180510),
]
