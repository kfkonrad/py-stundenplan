# WiSe 17/18

import lecture_classes
# Leider braucht es für eine Erkennung der Namen mit pyflakes diesen
# syntaktischen Käse, ansonsten tut der Code auch mit einem einfachen
# from lecture_classes import *
Class = lecture_classes.Class
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
faecher = []
rem = []
add = []
holiday = []
remall = []

faecher = [
    Class("BMC++-V/P", "A116.2", morgen(1), morgen(3, room="Q011")),
    Class("EIS-V", "A136", mittag(1)),
    Class("EIS-Ü", "G225", nachmittag(1), abend(1)),
    Class("MOBU-V/Ü", "O205", morgen(2)),
    Class("VDA-V/Ü", "Kapelle", vormittag(2), mittag(2)),
    Class("NPROG-V/P", "A116.2", morgen(4), vormittag(4)),
    Class("BWL-V", "A135", morgen(5)),
    Class("BWL-V", "A135", morgen(5)),
    Class("BWL-Ü", "A135", vormittag(5)),
    Class("Arbeit", "C105", T("09:45", "16:30", 3)),
    Class("Arbeit", "C105", T("11:30", "14:00", 4)),
    Class("unixAG", "A204.2", T("16:30", "18:00", 3)),
]

rem = [(20171107, "MOBU-V/Ü"), (20171108, "Arbeit")]

add = [
    (20171108, Class("ICT-Meeting", "Campus PS", T("10:00", "12:00", 3))),
    (20171108, Class("Code Review", "Gisbo", T("14:00", "16:00", 3))),
]

remall = []

holiday = []
