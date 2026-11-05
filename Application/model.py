from datetime import datetime


class Model:

    def __init__(self):
        self.has_fix: bool = False
        self.fix_datetime: datetime | None = None

    def set_fix(self, fix_datetime: datetime | None) -> None:
        if fix_datetime:
            self.has_fix = True
            self.fix_datetime = fix_datetime
        else:
            self.has_fix = False
            self.fix_datetime = None
