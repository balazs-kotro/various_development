from typing import Tuple

class Trade:
    def __init__(self, traded_assets: tuple, traded_volumes: tuple):
        self.assets = traded_assets
        self.values = traded_volumes

    @classmethod
    def sum_instances(cls, instances):
              
        all_assets = set()
        for instance in instances:
            all_assets.update(instance.assets)
        
        summed_values = {asset: 0 for asset in all_assets}
        
        for instance in instances:
            for asset, value in zip(instance.assets, instance.values):
                summed_values[asset] += value
        
        summed_assets = tuple(all_assets)
        summed_values = tuple(summed_values[asset] for asset in summed_assets)
        
        return Trade(summed_assets, summed_values)