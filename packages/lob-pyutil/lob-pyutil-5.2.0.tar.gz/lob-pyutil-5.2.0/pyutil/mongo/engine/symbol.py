import pandas as pd

from antarctic.Document import XDocument
from antarctic.PandasFields import SeriesField

from mongoengine import *


class Group(Document):
    name = StringField(required=True, unique=True)


class Symbol(XDocument):
    group = ReferenceField(Group, required=True)
    internal = StringField(max_length=200, required=False)
    webpage = URLField(max_length=200, nullable=True)
    PX_LAST = SeriesField()

    @staticmethod
    def symbolmap(symbols=None):
        symbols = symbols or Symbol.objects
        return {asset.name: asset.group.name for asset in symbols}

    @classmethod
    def reference_frame(cls, objects=None) -> pd.DataFrame:
        objects = objects or Symbol.objects.exclude("PX_LAST")
        frame = super(Symbol, cls).reference_frame(objects)
        frame["Sector"] = pd.Series({symbol.name: symbol.group.name for symbol in objects})
        frame["Internal"] = pd.Series({symbol.name: symbol.internal for symbol in objects})
        return frame

    @classmethod
    def frame(cls, objects=None) -> pd.DataFrame:
        objects = objects or Symbol.objects.only("name", "PX_LAST")
        frame = super(Symbol, cls).frame("PX_LAST", objects=objects)

        #frame = pd.DataFrame(
        #    {name: ts for name, ts in Symbol.apply(lambda x: x.PX_LAST, default=pd.Series({}), products=products)})
        return frame.dropna(axis=1, how="all")
