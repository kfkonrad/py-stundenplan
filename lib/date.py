import time
from typing import NoReturn

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

    def step(self, by: int = 1) -> NoReturn:
        # Erhöht Datum um 1 Tag, erhöht Wochentag zyklisch
        self._weekday = (self._weekday + by) % 7
        self._numeric_date = self._numeric_date + by
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
