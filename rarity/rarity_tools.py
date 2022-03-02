from rarity import collections

c = collections.get_all_collections()
top = c.sort_by_seven_day_volume("seven_day_volume")[:10]

for t in top:
    print(t)