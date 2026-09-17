import random
from miano_uma_gacha_rates import PULL_COST


class GachaSimulator:
    def __init__(self, banner):
        self._banner = banner

    def simulate(self, num_pulls):
        rates = self._banner.get_rates()
        tiers = list(rates.keys())
        weights = list(rates.values())
        results = random.choices(tiers, weights=weights, k=num_pulls)
        return {tier: results.count(tier) for tier in tiers}

    def simulate_from_carats(self, carats):
        num_pulls = carats // PULL_COST
        return num_pulls, self.simulate(num_pulls)
