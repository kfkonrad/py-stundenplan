# SoSe 16
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
    Lecture('AWS-V', 'A136',
            T('11:45', '13:15', 1),
            T('11:45', '13:15', 3)
            ),
    Lecture('PROG1-V', 'A135',
            T('14:00', '15:30', 1),
            T('11:45', '13:15', 4)
            ),
    Lecture('ALDS-V', 'Audimax',
            T('09:45', '11:15', 2),
            T('09:45', '11:15', 4)
            ),
    Lecture('ALDS-Ü', 'G224', T('11:45', '13:15', 2)),
    Lecture('HCI-Ü', 'O205', T('08:00', '09:30', 3)),
    Lecture('AWS-Ü', 'A135', T('09:45', '11:15', 3)),
    Lecture('PROG1-P', 'Q013', T('14:00', '15:30', 4)),
    Lecture('HCI-V', 'Q106', T('08:00', '09:30', 5)),
    Lecture('KW-V', 'Q106', T('09:45', '11:15', 5)),
    Lecture('UnixAG', 'A204.2', T('14:00', '16:00', 5)),
    #
    # Lecture('Beispiel','A123',T('16:00','19:00',6)),
    # Lecture('Beispiel 2','A123',T('20:00','22:00',6)),
    # Testcase: Lecture('HCI-V','Q106',T('3:00','3:45',5)),
    # Testcase: Lecture('KW-V','Q106',T('3:50','6:15',5)),
    # Testcase: Lecture('KW-V','Q106',T('7:45','9:15',5))
]
holiday = [
    (20160101, 20160320),
    (20160324, 20160328),
    (20160505, 20160505),
    # (20160709,20991231)
]
rem = [
    (20160321, "PROG-V"),
    (20160322, "ALDS-V"),
    (20160322, "ALDS-Ü"),
    (20160323, "HCI-Ü"),
    (20160323, "AWS-Ü"),
    (20160324, "ALDS-V"),
    (20160329, "ALDS-V"),
    (20160329, "ALDS-Ü"),
    (20160330, "HCI-Ü"),
    (20160331, "PROG1-P"),
    (20160406, "AWS-V"),
    (20160414, "ALDS-V"),
    (20160420, "HCI-Ü"),
    (20160421, "ALDS-V"),
    (20160504, "HCI-Ü"),
]

add = [
    (20160321, Lecture("PROG-V", "Q106/107", T('14:00', '15:30', 4))),
    (20160512, Lecture("ALDS-V", "A134", T('17:30', '19:00', 4))),
    (20160519, Lecture("ALDS-V", "A134", T('17:30', '19:00', 4))),
    # addLecture(20160902, "Test", "Raum", '14:30', "16:20"),
]
