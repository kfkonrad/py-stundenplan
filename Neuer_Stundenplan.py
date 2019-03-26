"""
Version 1.0 (20/04/2016) - now supporting versioning.
  uses clock, span, T, Class objects for easier time-handling.

  Support for parsable output added. Use giveargs=True to add CSV info with
  split as its seperator. Semicolon, tab or comma are usually good seperators.

  Better code alignment: no line exceeds 80 characters.

Version 1.1 (03/10/2016)
  dayinc supports optional number for skipping n days instead of just one day,
  good for testing purposes.

  addClass function added. With addClass the weekday needn't be given in the
  add array, providing a more convenient interface.

  The database is now imported from external files, making maintainance and
  switching semesters/years easy and straightforward. Global variable semester
  is introduced to bring swapping semesters to the beginning of the file.

 Version 1.1.1 (06/10/2016)
    add will work for all days, not just for today
    apparently the julian functions are badly broken
Version 1.2 (13/10/2016)
    julian functions were NOT broken
    all it needed to fix the bug was an index shift
Version 1.3 (30/11/2016)
    Replaced julian dates by manual date format correcting function
    numericdatecorrect. dayinc is now much easier to understand, bugs are
    easier to find (hopefully).
    Fixes a bug concerning adding Classes after the current date.
    Julian functions are not used anymore, the code stays for legacy reasons.
    addClass is still broken, I really don't know how to fix that.
Version 1.4 (21/03/2017)
    Updated semester-data for Sommersemester 2017
    Added covenience feature for faster, more human-readable input of T-objects
        that follow the standard lecture timeframes of HSKL.
    Each of these functions support T's optional room argument.
    B(<1..5>,weekday)
    morgen(weekday)     == B (1,weekday) == T("08:00","09:30",weekday)
    vormittag(weekday)  == B (2,weekday) == T("09:45","11:15",weekday)
    mittag(weekday)     == B (3,weekday) == T("11:45","13:15",weekday)
    nachmittag(weekday) == B (4,weekday) == T("14:00","15:30",weekday)
    abend(weekday)      == B (5,weekday) == T("15:45","17:15",weekday)
Version 1.5 (05/04/2017)
    Added functionality to remove all Classes of a certain subject after a
        given date.
    Added remall to list the remall Classes, it basically works like rem except
        it will remove the Class on the given date and any date greater than
        that date.
    remall might look like this: remall = [ (20170815,"Fach") ]
    This definition would remove all instances of "Fach" that occur from
        20170815 on, including 20170815.
Version 1.6 (08/11/2017)
    Split into library and code.
    Refactored code to follow the pyflakes style guidelines.
    Reshaped semester files to form complete library files and valid python
        programs on their own.
Version 1.7 (28/01/2018)
    Added type hints as proposed in PEP 484 and PEP 526.
    Thus this script is only compatible with Python 3.6 or higher.
    Removed unused legacy functions datetojulian and juliantodate
    Renamed the following classes (oldname -> newname)
        clock -> Clock
        span -> Span
        Class -> Lecture
    Renamed the follwing functions:
        addClass -> add_lecture
    Changed variable names and comments to fit new classnames and PEP
        conventions.
Version 1.8 (30/01/2018) - It's been a while, hasn't it
    Complete restructuring of the entire architecture to be independend from
        global variables and entirely based on custom classes.
    Also @property, @total_ordering, @staticmethod and @classmethod
        decorators are used widely
    No more starred imports
    Every function, method and property has gotten a type annotation
    For now I think, that this project is compliant to the unwritten Clean Code
    Codex (as described in Robert C. Martin's book 'Clean Code')
Version 1.9 (20/11/2018) - Split all the files
    Put all classes into individual files
    Move database import to lib.database. There users can note down the
    specific semester for the script to use 
Version 2.0 (26/3/2019) - a new semester
    Maintenance Release for SoSe '19
    B is extended with a 6th T(ime-frame)
    Function 'nacht' was added to accommodate for the new lecture
        time (17:30-19:00). nacht uses B's 6th time frame for consistency
        with earlier convenience functions.
"""

import time
import copy
import inspect
from typing import NoReturn, Tuple
from lib.clock import Clock
from lib.date import Date
from lib.self_correcting_lecture_list import Self_correcting_lecture_list
import lib.database as database

giveargs: bool = True
split: str = ";"


def processor(_date: Date) -> Tuple[Clock, Clock, int, int]:
    # Gibt Fächerliste für den aktuellen Tag aus. Gibt Ende der aktuellen
    # Stunde, Tages zurück.
    thisfaecher: Self_correcting_lecture_list = Self_correcting_lecture_list(
        _date
    )
    thisfaecher.extend(database.faecher)
    thisfaecher.apply_all_correctives_and_sort()

    if thisfaecher.is_empty():
        print("frei")
        return Clock(), Clock(), 0, 0

    print(thisfaecher.pprint())
    return thisfaecher.get_end_of_current_lecture(), \
        thisfaecher.get_end_of_last_lecture(), \
        thisfaecher.get_length_of_current_lecture(), \
        thisfaecher.get_length_of_day()


def print_remaining_length_of_hour_and_day(end_of_current_lecture: Clock,
                                           end_of_current_day: Clock
                                           ) -> NoReturn:
    # Bestimmt, wie lange die Stunde/der Tag noch geht
    localt: Clock = Clock(time.strftime("%H:%M", time.localtime()))
    end_of_current_lecture -= localt
    end_of_current_day -= localt
    if end_of_current_lecture.hash > 0:
        print("\nDiese Stunde noch:", end_of_current_lecture.pprint())
        print("Heute noch:", end_of_current_day.pprint())
    elif end_of_current_day.hash > 0:
        print("\nHeute noch:", end_of_current_day.pprint())


# Wochentag, Datum
date = Date.today()

print("Heute:")
untilclass: Clock
untilday: Clock
currentlen: int
daylen: int
untilclass, untilday, currentlen, daylen = processor(date)
print("-----")
print("Morgen:")
date.step()
processor(date)
print("-----")
date.step()
print(date.pprint_weekday())
processor(date)
print_remaining_length_of_hour_and_day(untilclass, untilday)
if giveargs:
    print(currentlen, daylen, sep=split, end="")
