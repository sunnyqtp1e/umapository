RETENTION_REWARDS = {
    1: 0,
    2: 35,
    3: 75,
    4: 150,
    5: 225,
    6: 375,
}

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


class TeamTrialsIncome:

    def __init__(self, current_class, today_name, days_ahead):
        self._current_class = current_class
        self._today_name = today_name
        self._days_ahead = days_ahead

    def _mondays_between(self):
        today_index = DAYS.index(self._today_name)
        days_until_monday = (7 - today_index) % 7
        if days_until_monday == 0:
            days_until_monday = 7  # today IS Monday -> next reset is next week

        mondays = 0
        d = days_until_monday
        while d <= self._days_ahead:
            mondays += 1
            d += 7
        return mondays

    def calculate(self):
        weekly_reward = RETENTION_REWARDS.get(self._current_class, 0)
        return weekly_reward * self._mondays_between()
