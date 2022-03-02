from rarity import collections
import pandas as pd

pd.set_option('display.max_columns', None)

# c = collections.get_all_collections()
# top = c.sort_by_seven_day_volume("seven_day_volume")[:10]
# for t in top:
#     print(t)

c = collections.get_collections_df()
print(c.sort_values('stats.seven_day_volume', ascending=False))
