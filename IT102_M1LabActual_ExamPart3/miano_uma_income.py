from abc import ABC, abstractmethod


class IncomeSource(ABC):

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @abstractmethod
    def calculate(self, days):
        pass


class DailyTaskIncome(IncomeSource):

    def __init__(self, per_day=75):
        super().__init__("Daily tasks")
        self._per_day = per_day

    def calculate(self, days):
        return self._per_day * days


class EventIncome(IncomeSource):

    def __init__(self, total_event_carats=0):
        super().__init__("Events")
        self._total = total_event_carats

    def calculate(self, days):
        return self._total  # one-off total, not per-day


class StoryIncome(IncomeSource):

    def __init__(self, story_carats_left=0):
        super().__init__("Story")
        self._story_carats_left = story_carats_left

    def calculate(self, days):
        return self._story_carats_left


class ExistingCarats(IncomeSource):

    def __init__(self, existing=0):
        super().__init__("Existing balance")
        self._existing = existing

    def calculate(self, days):
        return self._existing
