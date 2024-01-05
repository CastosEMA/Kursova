import datetime

class Time:
    def __init__(self):
        time = datetime.datetime.now()
        ctime = time.timetuple()

        # Виправлення: Присвоєння без дужок
        self.year = ctime.tm_year

        self.month = ctime.tm_mon

        self.day = ctime.tm_mday

        self.hour = ctime.tm_hour

        self.min = ctime.tm_min

        self.second = ctime.tm_sec

    def if_early(self, other_time):
        if self.year < other_time.year:
            return True
        elif self.month < other_time.month:
            return True
        elif self.day < other_time.day:
            return True
        elif self.hour < other_time.hour:
            return True
        elif self.min < other_time.min:
            return True
        elif self.second < other_time.second:
            return True
        else:
            return False

    def dict_ret(self):
        time_dict = {
            "year": self.year,
            "month": self.month,
            "day": self.day,
            "hour": self.hour,
            "min": self.min,
            "second": self.second,
        }
        return time_dict


def main():
    print(str(Time().dict_ret()))


if __name__ == "main":
    main()
