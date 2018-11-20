from functools import total_ordering
from typing import Any, NoReturn
from lib.lecture import Lecture
from lib.span import Span

@total_ordering
class Lecture_digest(Lecture):
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
