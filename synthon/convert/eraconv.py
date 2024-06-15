import datetime
from enum import Enum


class JaCal(Enum):
    M = "明治"
    T = "大正"
    S = "昭和"
    H = "平成"
    R = "令和"

class JaCalClass:
    def __init__(self, ja_type: JaCal, start_date: datetime.date) -> None:
        self.name: str = ja_type.value
        self.initial: str = ja_type.name[0]
        self.start_date: datetime.date = start_date

    def conv_year_ad2jp(self, date: datetime.date) -> int:
        return int((date - self.start_date).days / 365) + 1

    def conv_ad2jp(self, date: datetime.date) -> str:
        jp_year = self.conv_year_ad2jp(date)
        # return f"{self.name}{jp_year}年{date.month}月{date.day}日"
        # return f"{self.initial}{jp_year}年{date.month}月{date.day}日"
        return f"{self.name}{jp_year if jp_year != 1 else '元'}年{date.month}月{date.day}日"


class EraConv:
    ja_cal = {
        JaCal.M: JaCalClass(JaCal.M, datetime.date(1868, 1, 25)),
        JaCal.T: JaCalClass(JaCal.T, datetime.date(1912, 7, 30)),
        JaCal.S: JaCalClass(JaCal.S, datetime.date(1926, 12, 25)),
        JaCal.H: JaCalClass(JaCal.H, datetime.date(1989, 1, 8)),
        JaCal.R: JaCalClass(JaCal.R, datetime.date(2019, 5, 1)),
    }

    @classmethod
    def conv_ad2ja(cls, date: datetime.date) -> str:
        ja_type = None
        if cls.ja_cal[JaCal.M].start_date <= date < cls.ja_cal[JaCal.T].start_date:
            ja_type = JaCal.M
        elif cls.ja_cal[JaCal.T].start_date <= date < cls.ja_cal[JaCal.S].start_date:
            ja_type = JaCal.T
        elif cls.ja_cal[JaCal.S].start_date <= date < cls.ja_cal[JaCal.H].start_date:
            ja_type = JaCal.S
        elif cls.ja_cal[JaCal.H].start_date <= date < cls.ja_cal[JaCal.R].start_date:
            ja_type = JaCal.H
        elif cls.ja_cal[JaCal.R].start_date <= date:
            ja_type = JaCal.R
        else:
            raise ValueError(f"西暦対応以前に変換できません")
        return cls.ja_cal[ja_type].conv_ad2jp(date)


if __name__ == "__main__":
    ad_date = datetime.date(2021, 12, 12)
    print(ad_date)
    ja_date = EraConv.conv_ad2ja(datetime.date(2019, 12, 12))
    print(ja_date)
