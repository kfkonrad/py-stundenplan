from typing import NoReturn

class Clock:  # Beinhaltet Uhrzeit (h:min)
    _stringv: str
    _h: int
    _m: int

    def __init__(self,
                 timestring: str = "00:00",
                 ) -> NoReturn:
        self._stringv = timestring
        self._h = int(self._stringv[0:2])
        self._m = int(self._stringv[3:6])

    def __sub__(self, other: 'Clock') -> 'Clock':
        h: int = self._h - other._h
        m: int = self._m - other._m
        ret: Clock = Clock()
        ret._m = m
        ret._h = h
        ret.__fix_negative_minutes()
        ret.__set_time_to_zero_if_negative()
        ret.__stringv_reconstruct()
        return ret

    def __fix_negative_minutes(self) -> NoReturn:
        if self._m < 0:
            self._m += 60
            self._h -= 1

    def __set_time_to_zero_if_negative(self) -> NoReturn:
        if self._h < 0:
            self._h = 0
            self._m = 0

    def __stringv_reconstruct(self) -> NoReturn:
        if self._h < 10:
            self._stringv = "0"
            self._stringv += str(self._h)
        else:
            self._stringv = str(self._h)
        self._stringv += ":"
        if self._m < 10:
            self._stringv += "0"
            self._stringv += str(self._m)
        else:
            self._stringv += str(self._m)

    @property
    def hash(self) -> int:
        return self.__hash__()

    def __hash__(self) -> int:
        return self._h * 60 + self._m

    def pprint(self) -> str:
        return self._stringv
