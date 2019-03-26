# SoSe 19

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
nacht = lc.nacht
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
nacht(weekday)      == T("17:30","19:00",weekday)
"""
faecher: List[Lecture] = []
rem: List[Tuple[int, str]] = []
add: List[Tuple[int, Lecture]] = []
holiday: List[Tuple[int, int]] = []
remall: List[Tuple[int, str]] = []

faecher = [
    Lecture("WKOMM", "A134", vormittag(mo), nachmittag(di)),
    Lecture("SSE", "A209.2", abend(mo), nacht(mo)),
    Lecture("DEEP", "A209.2", nachmittag(do), abend(do)),
    Lecture("INTP", "A125", nachmittag(fr), abend(fr)),
    Lecture("unixAG", "A204.2", T("16:30", "19:00", mi)),
]

rem = [
]

add = [
]

remall = [
]

holiday = [
]
