# SoSe 16

import lecture_classes
# Leider braucht es für eine Erkennung der Namen mit pyflakes diesen
# syntaktischen Käse, ansonsten tut der Code auch mit einem einfachen
# from lecture_classes import *
Class = lecture_classes.Class
T = lecture_classes
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
    Class('AWS-V', 'A136', T('11:45', '13:15', 1), T('11:45', '13:15', 3)),
    Class('PROG1-V', 'A135', T('14:00', '15:30', 1), T('11:45', '13:15', 4)),
    Class('ALDS-V', 'Audimax', T('09:45', '11:15', 2), T('09:45', '11:15', 4)),
    Class('ALDS-Ü', 'G224', T('11:45', '13:15', 2)),
    Class('HCI-Ü', 'O205', T('08:00', '09:30', 3)),
    Class('AWS-Ü', 'A135', T('09:45', '11:15', 3)),
    Class('PROG1-P', 'Q013', T('14:00', '15:30', 4)),
    Class('HCI-V', 'Q106', T('08:00', '09:30', 5)),
    Class('KW-V', 'Q106', T('09:45', '11:15', 5)),
    Class('UnixAG', 'A204.2', T('14:00', '16:00', 5)),
    #
    # Class('Beispiel','A123',T('16:00','19:00',6)),
    # Class('Beispiel 2','A123',T('20:00','22:00',6)),
    # Testcase: Class('HCI-V','Q106',T('3:00','3:45',5)),
    # Testcase: Class('KW-V','Q106',T('3:50','6:15',5)),
    # Testcase: Class('KW-V','Q106',T('7:45','9:15',5))
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
    (20160321, Class("PROG-V", "Q106/107", T('14:00', '15:30', 4))),
    (20160512, Class("ALDS-V", "A134", T('17:30', '19:00', 4))),
    (20160519, Class("ALDS-V", "A134", T('17:30', '19:00', 4))),
    # addClass(20160902, "Test", "Raum", '14:30', "16:20"),
]
