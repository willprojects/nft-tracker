import datetime
import inspect
import json
from dataclasses import dataclass, field
from typing import Optional, Dict
import requests
from dataclasses_json import dataclass_json, config as dt_json_config, CatchAll
import pandas as pd

COLLECTIONS_ENDPOINT_URL = "https://collections.rarity.tools/static/collections.json"

"""
https://github.com/Quantumlyy/rarity-tools-scraper-py
"""


@dataclass_json
@dataclass
class ProjectLookup:
    name: str
    added_order: Optional[int] = field(metadata=dt_json_config(field_name="addedOrder"), default=None)
    dynamic: Optional[int] = None
    manual: Optional[bool] = None
    contracts: Optional[list[str]] = None
    cv: Optional[int] = None
    item_name: Optional[str] = field(metadata=dt_json_config(field_name="itemName"), default=None)
    added: Optional[str] = None
    custom_header: Optional[str] = field(metadata=dt_json_config(field_name="customHeader"), default=None)


@dataclass_json
@dataclass
class Projects:
    list: list[str]
    lookup: Dict[str, ProjectLookup]


@dataclass_json
@dataclass
class CollectionStats:
    one_day_volume: Optional[float] = None
    one_day_change: Optional[float] = None
    one_day_sales: Optional[float] = None
    one_day_average_price: Optional[float] = None
    seven_day_volume: Optional[float] = None
    seven_day_change: Optional[float] = None
    seven_day_sales: Optional[float] = None
    seven_day_average_price: Optional[float] = None
    total_volume: Optional[float] = None
    total_sales: Optional[float] = None
    total_supply: Optional[float] = None
    num_owners: Optional[float] = None
    average_price: Optional[float] = None
    market_cap: Optional[float] = None
    floor_price: Optional[float] = None


@dataclass_json
@dataclass
class Collection:
    id: str
    slug: str
    name: str
    description: str
    created_date: Optional[str] = None
    discord_url: Optional[str] = None
    external_url: Optional[str] = None
    image_url: Optional[str] = None
    large_image_url: Optional[str] = None
    banner_image_url: Optional[str] = None
    medium_username: Optional[str] = None
    twitter_username: Optional[str] = None
    instagram_username: Optional[str] = None

    stats: Optional[CollectionStats] = None


@dataclass_json
@dataclass
class Collections:
    collections: list[Collection]
    projects: Projects
    unknown_things: CatchAll = None

    def sort_by_seven_day_volume(self, prop: str) -> list[Collection]:
        prop_list = inspect.getmembers(CollectionStats)[0][1].keys()
        if prop not in prop_list:
            raise ValueError("Stat property options: %r." % prop_list)
        has_stats = [i for i in self.collections if i.stats]
        return sorted(has_stats, key=lambda x: x.stats.__dict__.get(prop), reverse=True)


class CollectionsManager:

    def __init__(self, auto_cache=True, dir_path="../cache"):
        self.dir_path = dir_path
        self.collections = self.fetch_rarity_collections()
        if auto_cache:
            self.cache()

    @staticmethod
    def fetch_rarity_collections() -> dict:
        res = requests.get(COLLECTIONS_ENDPOINT_URL)
        return res.json()

    def get_collections_objects(self) -> Collections:
        collections = Collections.from_dict(self.collections)
        for i in range(len(self.collections["collections"])):
            collections.collections[i] = Collection.from_dict(self.collections["collections"][i])
        return collections

    def get_collections_df(self):
        return pd.json_normalize(self.collections['collections'])

    def cache(self):
        dt = str(datetime.date.today()).replace("-", "")
        with open(f"{self.dir_path}/rarity-{dt}.json", 'w') as f:
            json.dump(self.collections, f)

