import copy
import time
from typing import NoReturn, List, Sequence
from lib.lecture_digest import Lecture_digest
from lib.date import Date
from lib.lecture import Lecture
from lib.date import Date
from lib.clock import Clock
import lib.database as database

class Self_correcting_lecture_list:
    _lectures: List[Lecture_digest]
    _date: Date

    def __init__(self, _date) -> NoReturn:
        self._date = copy.deepcopy(_date)
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
        for numeric_date, subject in database.remall:
            if self._date.numeric_date >= numeric_date:
                for i in range(0, len(self._lectures)):
                    if self._lectures[i].subject == subject:
                        self._lectures[i].schedule = ()

    def correct_with_add(self) -> NoReturn:
        for numeric_date, lecture in database.add:  # type int, Lecture
            if self._date.numeric_date == numeric_date:
                self._lectures.append(lecture)

    def keep_only_todays_lectures(self) -> NoReturn:
        new_lectures: List[Lecture_digest] = []
        for fach in self._lectures:
            for i in range(0, len(fach.schedule)):
                if self._date.weekday == fach.schedule[i].weekday:
                    new_lectures.append(Lecture_digest(fach, i))
        self._lectures = new_lectures

    def _maybe_not_implemented(self) -> NoReturn:
        if Lecture in [type(i) for i in self._lectures]:
            raise NotImplementedError('Must run .keep_only_todays_lectures \
                before running .' + inspect.stack()[1][3] + ' on \
                Self_correcting_lecture_list!')

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
    def _sort_helper(lectures: List[Lecture_digest]) -> List[Lecture_digest]:
        if not lectures:
            return []
        else:
            pivot: Lecture_digest = lectures.pop(0)
            lesser: List[Lecture_digest] = \
                Self_correcting_lecture_list._sort_helper(
                [i for i in lectures if i < pivot]
            )
            greater: List[Lecture_digest] = \
                Self_correcting_lecture_list._sort_helper(
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
        for lecture in self._lectures:  # type: Lecture_digest
            if localt in lecture.important_bespan:
                ret = lecture.important_bespan.end
        return ret

    def get_length_of_current_lecture(self) -> int:
        self._maybe_not_implemented()
        ret: int = 0
        localt: Clock = Clock(time.strftime("%H:%M"))
        for lecture in self._lectures:  # type: Lecture_digest
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
        for lecture in self._lectures:  # type: Lecture_digest
            ret += lecture.pprint(lecture.imporant_schedule_index) + '\n'
        return ret[:-1]
