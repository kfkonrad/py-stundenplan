# SoSe 17
from typing import List, Tuple

import lecture_classes
# Leider braucht es für eine Erkennung der Namen mit pyflakes diesen
# syntaktischen Käse, ansonsten tut der Code auch mit einem einfachen
# from lecture_classes import *
Lecture = lecture_classes.Lecture
T = lecture_classes.T
morgen = lecture_classes.morgen
vormittag = lecture_classes.vormittag
mittag = lecture_classes.mittag
nachmittag = lecture_classes.nachmittag
abend = lecture_classes.abend
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
    Lecture("ITS-V", "A124", nachmittag(1), vormittag(4, room="C112")),
    Lecture("PM-Ü", "A124", abend(1)),
    Lecture("CG-Ü", "O210", vormittag(2)),
    Lecture("PM-V", "C114", mittag(2)),
    Lecture("MUG", "G201", nachmittag(2)),
    Lecture("CG-V", "A125", vormittag(3)),
    Lecture("IPROG-V", "A124", mittag(3)),
    Lecture("LAG-V", "A135", nachmittag(4)),
    Lecture("LAG-Ü", "A135", abend(4)),
    Lecture("IPROG-P", "G224", mittag(5)),
    Lecture("unixAG", "A204.2", T("17:00", "18:00", 3)),
    Lecture("Arbeit", "C105", T("08:00", "15:30", 1)),
    Lecture("Arbeit", "C105", T("14:00", "17:00", 3)),
    Lecture("TEST", "C105", T("20:00", "22:00", 6)),
    Lecture("TEST", "C105", T("23:00", "23:30", 6)),
]

rem = [
    (20170321, "CG-Ü"),
    (20170328, "CG-Ü"),
    (20170324, "IPROG-P"),
    (20170329, "unixAG"),
    (20170405, "unixAG"),
    (20170406, "ITS-V"),
    (20170519, "IPROG-P"),
]

add = [
    (20170321, Lecture("CG-V", "Kapelle", vormittag(2))),
    (20170328, Lecture("CG-V", "Kapelle", vormittag(2))),
    (20170401, Lecture("OC", "Pirmasens", T("10:00", "13:00", 6))),
    (20170405, Lecture("EAE-V", "C112", T("14:00", "17:00", 3))),
    (20170619, Lecture("LDD Meeting", "Campus PS", T("10:00", "12:00", 1))),

    # Lecture("STUA-VS","A124",nachmittag(5)),
    # addLecture(20161202,"TEST","A205.2",'20:00',"22:00"),
]

remall = [(20170411, "ITS-V")]

holiday = [
    (20170413, 20170418),
    (20170801, 20991231),
]
