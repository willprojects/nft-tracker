import pandas as pd
from rarity.collections import CollectionsManager

pd.set_option('display.max_columns', None)


c = CollectionsManager()

# collections = c.get_collections_objects()
# top = collections.sort_by_seven_day_volume("seven_day_volume")[:10]
# for t in top:
#     print(t)

# collections = c.get_collections_df()
# print(collections.sort_values('stats.seven_day_volume', ascending=False))
