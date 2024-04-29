from typing import Tuple
import uuid


class Positions:
    def __init__(
        self,
        position_id,
        date,
        assets,
        asset_ratios,
        invested_amounts,
        weights
    ):
        self.position_id = position_id
        self.assets = assets
        self.date=date
        self.asset_ratios = asset_ratios
        self.invested_amounts = invested_amounts
        self.weights = weights

    @classmethod
    def sum_instances(cls, instances, parernt_id):

        all_assets = set()
        for instance in instances:
            all_assets.update(instance.assets)

        summed_values = {asset: 0 for asset in all_assets}
        summed_ratio_values = {asset_ratio: 0 for asset_ratio in all_assets}

        for instance in instances:
            for asset, value in zip(instance.assets, instance.invested_amounts):
                summed_values[asset] += value
            for asset_ratio, value in zip(instance.assets, instance.asset_ratios):
                summed_ratio_values[asset_ratio] += value

        summed_assets = tuple(all_assets)
        summed_values = tuple(summed_values[asset] for asset in summed_assets)
        summed_ratio_values = tuple(
            summed_ratio_values[asset] for asset in summed_assets
        )

        return Positions(
            position_id=parernt_id,
            assets=summed_assets,
            date=None,
            asset_ratios=summed_ratio_values,
            invested_amounts=summed_values,
            weights=None
        )
