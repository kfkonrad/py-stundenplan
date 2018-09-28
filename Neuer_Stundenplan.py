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
"""

import time
import copy
from functools import total_ordering
from typing import Any, NoReturn, List, Tuple, Sequence
from lecture_classes import Lecture, Span, Clock

import sose18 as database

giveargs: bool = True
split: str = ";"


# Klassen zu processor

@total_ordering
class LectureDigest(Lecture):
    imporant_schedule_index: int

    def __init__(self,
                 lecture: Lecture,
                 imporant_schedule_index: int
                 ) -> NoReturn:
        super().__init__(lecture.subject, lecture.room, *lecture.schedule)
        self.imporant_schedule_index = imporant_schedule_index

    @property
    def important_begin(self) -> int:
        return self.schedule[self.imporant_schedule_index].begin.hash

    @property
    def important_pprint(self) -> str:
        return self.pprint(self.imporant_schedule_index)

    @property
    def important_bespan(self) -> Span:
        return self.schedule[self.imporant_schedule_index].bespan

    @staticmethod
    def _is_valid_operand(other: Any) -> bool:
        return hasattr(other, 'important_begin')

    def __lt__(self, other: Any) -> Any:
        if self._is_valid_operand(other):
            return self.important_begin < other.important_begin
        return NotImplemented

    def __eq__(self, other: Any) -> Any:
        if self._is_valid_operand(other):
            return self.important_begin == other.important_begin
        return NotImplemented


class Date:
    _weekday: int
    _numeric_date: int

    def __init__(self, weekday: int, numeric_date: int) -> NoReturn:
        self._weekday = weekday
        self._numeric_date = numeric_date

    @classmethod
    def today(cls) -> 'Date':
        today_weekday: int = int(time.strftime("%w"))  # type: int
        today_date: int = int(
            time.strftime("%Y")
            + time.strftime("%m")
            + time.strftime("%d")
        )
        return cls(today_weekday, today_date)

    def step(self, add_days: int = 1) -> NoReturn:
        # Erhöht Datum um 1 Tag, erhöht Wochentag zyklisch
        self._weekday = (self._weekday + add_days) % 7
        self._numeric_date = self._numeric_date + add_days
        self._numeric_date_correct()

    @property
    def weekday(self) -> int:
        return self._weekday

    @property
    def numeric_date(self) -> int:
        return self._numeric_date

    def pprint_weekday(self) -> str:
        if self._weekday == 0:
            return "Sonntag:"
        elif self._weekday == 1:
            return "Montag:"
        elif self._weekday == 2:
            return "Dienstag:"
        elif self._weekday == 3:
            return "Mittwoch:"
        elif self._weekday == 4:
            return "Donnerstag:"
        elif self._weekday == 5:
            return "Freitag:"
        elif self._weekday == 6:
            return "Samstag:"
        else:
            raise ValueError('unexpected weekday value in Date instance')

    def _numeric_date_correct(self) -> NoReturn:
        class YMD:
            y: int
            m: int
            d: int

            def __init__(self, _date: int) -> None:
                strdate: str = str(_date)
                self.y = int(strdate[:4])
                self.m = int(strdate[4:6])
                self.d = int(strdate[6:])
                self.__numeric_day_correct()
                self.__numeric_month_correct()

            def end_of_month(self) -> int:
                if self.m in (1, 3, 5, 7, 8, 10, 12):
                    return 31
                elif self.m == 2:
                    if (self.y % 4 == 0 and self.y % 100 != 0) \
                            or self.y % 400 == 0:
                        return 29
                    else:
                        return 28
                else:
                    return 30

            def __numeric_day_correct(self) -> None:
                eom: int = self.end_of_month()
                if self.d > eom:
                    self.d = 1
                    self.m += 1

            def __numeric_month_correct(self) -> None:
                if self.m > 12:
                    self.m = 1
                    self.y += 1

            def __str__(self):
                ret: str = str(self.y)
                if self.m < 10:
                    ret += "0"
                ret += str(self.m)
                if self.d < 10:
                    ret += "0"
                return ret + str(self.d)

            def __int__(self):
                return int(self.__str__())

        self._numeric_date = int(YMD(self._numeric_date))


class SelfCorrectingLectureList:
    _lectures: List[LectureDigest]
    _date: Date

    def __init__(self, _date) -> NoReturn:
        self._date = copy.deepcopy(date)
        self._lectures = []

    def extend(self, _lectures: Sequence[Lecture]) -> NoReturn:
        self._lectures.extend(_lectures)

    def append(self, lecture: Lecture) -> NoReturn:
        self._lectures.append(lecture)

    def correct_with_holiday(self) -> NoReturn:
        for arr in database.holiday:
            if arr[0] <= self._date.numeric_date <= arr[1]:
                self._lectures = []
                break

    def correct_with_rem(self) -> NoReturn:
        for i in range(0, len(self._lectures)):
            for numeric_date, subject in database.rem:
                if self._date.numeric_date == numeric_date and \
                        self._lectures[i].subject == subject:
                    self._lectures[i].schedule = ()

    def correct_with_remall(self) -> NoReturn:
        for numeric_date, subject in database.rem:
            if self._date.numeric_date >= numeric_date:
                for i in range(0, len(self._lectures)):
                    if self._lectures[i].subject == subject:
                        self._lectures[i].schedule = ()

    def correct_with_add(self) -> NoReturn:
        for numeric_date, lecture in database.add:  # type int, Lecture
            if self._date.numeric_date == numeric_date:
                self._lectures.append(lecture)

    def keep_only_todays_lectures(self) -> NoReturn:
        new_lectures: List[LectureDigest] = []
        for fach in self._lectures:
            for i in range(0, len(fach.schedule)):
                if self._date.weekday == fach.schedule[i].weekday:
                    new_lectures.append(LectureDigest(fach, i))
        self._lectures = new_lectures

    def _maybe_not_implemented(self) -> NoReturn:
        if Lecture in [type(i) for i in self._lectures]:
            import inspect
            raise NotImplementedError('Must run .keep_only_todays_lectures \
                before running .' + inspect.stack()[1][3] + ' on \
                SelfCorrectingLectureList!')

    def sort(self) -> NoReturn:
        self._maybe_not_implemented()
        self._lectures = self._sort_helper(self._lectures)

    def apply_all_correctives_and_sort(self) -> NoReturn:
        self.correct_with_holiday()
        self.correct_with_rem()
        self.correct_with_remall()
        self.correct_with_add()
        self.keep_only_todays_lectures()
        self.sort()

    @staticmethod
    def _sort_helper(lectures: List[LectureDigest]) -> List[LectureDigest]:
        if not lectures:
            return []
        else:
            pivot: LectureDigest = lectures.pop(0)
            lesser: List[LectureDigest] = \
                SelfCorrectingLectureList._sort_helper(
                [i for i in lectures if i < pivot]
            )
            greater: List[LectureDigest] = \
                SelfCorrectingLectureList._sort_helper(
                    [i for i in lectures if not i < pivot]
            )
            return lesser + [pivot] + greater

    def get_length_of_day(self) -> int:
        self._maybe_not_implemented()
        return self._lectures[-1].important_bespan - \
            self._lectures[0].important_bespan

    def get_end_of_current_lecture(self) -> Clock:
        self._maybe_not_implemented()
        ret: Clock = Clock()
        localt: Clock = Clock(time.strftime("%H:%M"))
        for lecture in self._lectures:  # type: LectureDigest
            if localt in lecture.important_bespan:
                ret = lecture.important_bespan.end
        return ret

    def get_length_of_current_lecture(self) -> int:
        self._maybe_not_implemented()
        ret: int = 0
        localt: Clock = Clock(time.strftime("%H:%M"))
        for lecture in self._lectures:  # type: LectureDigest
            if localt in lecture.important_bespan:
                ret = lecture.important_bespan.length
        return ret

    def get_end_of_lecture(self, n: int) -> Clock:
        self._maybe_not_implemented()
        return self._lectures[n].important_bespan.end

    def get_end_of_last_lecture(self) -> Clock:
        self._maybe_not_implemented()
        return self.get_end_of_lecture(-1)

    def is_empty(self) -> bool:
        return len(self._lectures) == 0

    def pprint(self) -> str:
        self._maybe_not_implemented()
        ret: str = ''
        for lecture in self._lectures:  # type: LectureDigest
            ret += lecture.pprint(lecture.imporant_schedule_index) + '\n'
        return ret[:-1]


# Funktionen zur main


def processor(_date: Date) -> Tuple[Clock, Clock, int, int]:
    # Gibt Fächerliste für den aktuellen Tag aus. Gibt Ende der aktuellen
    # Stunde, Tages zurück.
    thisfaecher: SelfCorrectingLectureList = SelfCorrectingLectureList(
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
