import math
from miano_uma_gacha_rates import PULL_COST, PITY_PULLS, PITY_COST


class PityCalculator:
    def __init__(self, banner):
        self._banner = banner

    def chance_by_pulls(self, num_pulls):
        p = self._banner.featured_rate
        return 1 - (1 - p) ** num_pulls

    def pulls_for_confidence(self, target_probability):
        p = self._banner.featured_rate
        if target_probability >= 1:
            return PITY_PULLS  # pity guarantees it regardless of luck
        pulls = math.log(1 - target_probability) / math.log(1 - p)
        return min(PITY_PULLS, math.ceil(pulls))

    def carats_for_pulls(self, num_pulls):
        return num_pulls * PULL_COST

    def pulls_affordable(self, carats):
        return carats // PULL_COST

    def expected_pulls_for_copies(self, n_copies):
        p = self._banner.featured_rate
        return math.ceil(n_copies / p)

    def pity_summary(self):
        return {
            "pulls_to_guarantee": PITY_PULLS,
            "carats_to_guarantee": PITY_COST,
        }
