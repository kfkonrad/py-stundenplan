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
mo = lc.mo
di = lc.di
mi = lc.mi
do = lc.do
fr = lc.fr
sa = lc.sa
so = lc.so
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
    Lecture("CMATH", "A209.2", mittag(mo), morgen(di),mittag(do)),
    Lecture("ABK", "A209.2", vormittag(di), morgen(fr), vormittag(fr)),
    Lecture("SE", "A209.2", nachmittag(di), abend(di), morgen(mi)),
    Lecture("ATFP", "A209.2", morgen(do), vormittag(do)),
    Lecture("SOSK", "A209.2", mittag(fr), nachmittag(fr), abend(fr)),
    Lecture("unixAG", "A204.2", T("16:30", "19:00", mi)),
]

rem = [
    (20181121, "SE"),
]

add = [
    (20181120,
     Lecture("Tuesday Night Club",
             "A209.1",
             T("19:00", "22:00", di)
             )
     ),
]

remall = [
    (20181022, "ATFP"),
]

holiday = [
#    (20180510, 20180510),
]
