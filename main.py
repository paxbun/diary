# Copyright (c) 2021 Chanjung Kim (paxbun). All rights reserved.

from dataclasses import dataclass, field
from datetime import date, time, datetime, timedelta
from typing import List, Optional, Tuple
from re import compile, Pattern
from sys import argv

@dataclass
class Event:
    begin: time = field(default_factory=time)
    end: time = field(default_factory=time)
    company: List[str] = field(default_factory=list)
    location: List[str] = field(default_factory=str)
    descriptions: List[str] = field(default_factory=list)

    @property
    def duration(self) -> timedelta:
        begin = datetime.combine(date.min, self.begin) - datetime.min
        end = datetime.combine(date.min, self.end) - datetime.min
        if self.begin < self.end:
            return end - begin
        else:
            return end + timedelta(1) - begin


@dataclass
class Day:
    todo: bool
    day: date = field(default_factory=date)
    events: List[Event] = field(default_factory=list)


class Regex:
    def __init__(self, regex):
        self.regex: Pattern = compile(regex)

    def __call__(self, line: str) -> Optional[dict]:
        match = self.regex.match(line)
        if match == None:
            return None

        return match.groupdict()


class DateParser:
    month_dict = {
        month: (idx + 1) for idx, month in enumerate((
            "January",  "February", "March",
            "April",    "May",      "June",
            "July",     "August",   "September",
            "October",  "November", "December"
        ))
    }

    def __init__(self, regex):
        self.regex = Regex(regex)
        self.day_regex = compile("^\d+")

    def __call__(self, line: str) -> Tuple[Optional[date], bool]:
        match = self.regex(line)
        if match == None:
            return None, False

        try:
            todo, year, month, day = (
                match["todo"], match["year"], match["month"], match["day"])
            year = int(year)
            month = int(DateParser.month_dict.get(month, month))
            day = int(self.day_regex.match(day).group())
            return date(year, month, day), todo != None
        except ValueError:
            return None, False


class EventParser:
    def __init__(self, regex):
        self.regex = Regex(regex)

    def __call__(self, line: str) -> Optional[Event]:
        match = self.regex(line)
        if match == None:
            return None

        try:
            begin, end, company, location, desc = (
                match["begin"], match["end"], match["company"], match["location"], match["desc"]
            )
            begin = time(int(begin[:2]), int(begin[2:]))
            end = time(int(end[:2]), int(end[2:]))
            company = [] if company == None else [companion.strip()
                                                  for companion in company.split(",")]
            location = [] if location == None else [l.strip()
                                                    for l in location.split(",")]
            desc = [] if desc == None else [desc]
            return Event(begin, end, company, location, desc)
        except ValueError:
            return None


class DescParser:
    def __init__(self, regex):
        self.regex = Regex(regex)

    def __call__(self, line: str) -> Optional[str]:
        match = self.regex(line)
        if match == None:
            return None
        return match["desc"]


date_parsers = [
    DateParser(
        r"^# +(?P<todo>TODO:)? *(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2}) *$"),
    DateParser(
        r"^# +(?P<todo>TODO:)? *(?P<month>\d{2})-(?P<day>\d{2})-(?P<year>\d{4}) *$"),
    DateParser(
        r"^# +(?P<todo>TODO:)? *(?P<month>January|February|March|April|May|June|July|August|September|October|November|December) (?P<day>(?:[1-3]?(?:1st|2nd|3rd|[04-9]th))|(?:\d{2})),? (?P<year>\d{4}) *$")
]

event_parsers = [
    EventParser(
        r"^\* (?P<begin>\d{4})-(?P<end>\d{4})(?: +with +(?P<company>.+?))?(?: +at +(?P<location>.+?))?(?: *\: *(?P<desc>.+))? *$")
]

desc_parsers = [
    DescParser(r"^ +\* (?P<desc>.+?) *$")
]


def parse_file(lines: List[str]) -> List[Day]:
    days = []
    current_day = None
    current_event = None

    def parse_date(line: str):
        nonlocal current_day, current_event
        for parser in date_parsers:
            date, todo = parser(line)
            if date == None:
                continue
            if current_event != None:
                if current_day != None:
                    current_day.events.append(current_event)
            if current_day != None:
                days.append(current_day)
            current_event = None
            current_day = Day(todo, date, [])
            return True
        return False

    def parse_event(line: str):
        nonlocal current_day, current_event
        for parser in event_parsers:
            event = parser(line)
            if event == None:
                continue
            if current_event != None:
                if current_day != None:
                    current_day.events.append(current_event)
            current_event = event
            return True
        return False

    def parse_desc(line: str):
        nonlocal current_event
        for parser in desc_parsers:
            desc = parser(line)
            if desc == None:
                continue
            if current_event != None:
                current_event.descriptions.append(desc)
            return True
        return False

    for line in lines:
        if parse_date(line):
            continue
        if parse_event(line):
            continue
        if parse_desc(line):
            continue

    if current_event != None:
        if current_day != None:
            current_day.events.append(current_event)

    if current_day != None:
        days.append(current_day)

    return days


if __name__ == "__main__":
    with open(argv[1], encoding="utf-8") as input:
        lines = input.readlines()

    total_duration = timedelta()
    days = parse_file(lines)
    for day in days:
        if day.todo:
            continue

        total_duration_today = timedelta()
        for event in day.events:
            total_duration_today += event.duration

        today_str = day.day.strftime("%Y-%m-%d")
        print(f"{today_str} (worked {total_duration_today})")

        for event in day.events:
            for desc in event.descriptions:
                print(f"* {desc}")
        print()
        total_duration += total_duration_today
    print("Total time worked:", total_duration)
