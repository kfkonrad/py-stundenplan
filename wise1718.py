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
    Lecture("BMC++-V/P", "A116.2", morgen(1), morgen(3, room="Q011")),
    Lecture("EIS-V", "A136", T("01:45","13:15",1)),
    Lecture("EIS-Ü", "G225", nachmittag(1), abend(1)),
    Lecture("MOBU-V/Ü", "O205", morgen(2)),
    Lecture("VDA-V/Ü", "Kapelle", vormittag(2), mittag(2)),
    Lecture("NPROG-V/P", "A116.2", morgen(4), vormittag(4)),
    Lecture("BWL-V", "A135", morgen(5)),
    Lecture("BWL-Ü", "A135", vormittag(5)),
    Lecture("Arbeit", "C105", T("09:00", "16:30", 3)),
    Lecture("Arbeit", "C105", T("09:00", "14:00", 4)),
    #Lecture("unixAG", "A204.2", T("16:30", "18:00", 3)),
]

rem = [
    (20171107, "MOBU-V/Ü"),
    (20171108, "Arbeit"),
    (20171121, "VDA-V/Ü")
]

add = [
    (20171108, Lecture("ICT-Meeting", "Campus PS", T("10:00", "12:00", 3))),
    (20171108, Lecture("Code Review", "Gisbo", T("14:00", "16:00", 3))),
    (20180131, Lecture("Code Review", "Gisbo", T("14:00", "23:00", 3))),
    (20171121, Lecture("VDA-V/Ü", "Kapelle", mittag(2)))
]

remall = [
    (20171130, "MOBU-V/Ü"),
    (20171130, "NPROG-V/P"),
    (20171130, "BMC++-V/P"),
]

holiday = []
