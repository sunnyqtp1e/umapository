from abc import ABC, abstractmethod

PULL_COST = 150
TEN_PULL_COST = 1500
PITY_PULLS = 200
PITY_COST = PITY_PULLS * PULL_COST  # 30,000


class Banner(ABC):

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @abstractmethod
    def get_rates(self):
        pass

    @property
    def featured_rate(self):
        return 0.0075  # rate-up chance, same for both banner types


class CharacterBanner(Banner):

    def __init__(self):
        super().__init__("Character (Horse) Banner")

    def get_rates(self):
        return {
            "3-star (any)": 0.03,
            "2-star": 0.18,
            "1-star": 0.79,
        }


class SupportCardBanner(Banner):

    def __init__(self):
        super().__init__("Support Card Banner")

    def get_rates(self):
        return {
            "SSR (any)": 0.03,
            "SR": 0.18,
            "R": 0.79,
        }
