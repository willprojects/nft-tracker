# import pandas as pd
# pd.set_option('display.max_columns', None)

from rarity_tools.collections import CollectionsManager


def lambda_handler(event, context):
    c = CollectionsManager()
    c.persist_s3()


# lambda_handler(None, None)

# collections = c.get_collections_objects()
# top = collections.sort_by_seven_day_volume("seven_day_volume")[:10]
# for t in top:
#     print(t)

# collections = c.get_collections_df()
# print(collections.sort_values('stats.seven_day_volume', ascending=False))
