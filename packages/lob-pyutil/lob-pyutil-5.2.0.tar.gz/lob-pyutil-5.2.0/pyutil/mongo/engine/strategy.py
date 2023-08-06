import pandas as pd
from mongoengine import *

from pyutil.mongo.engine.symbol import Symbol
from pyutil.performance.drawdown import drawdown
from pyutil.performance.month import monthlytable
from pyutil.performance.return_series import from_nav
from pyutil.strategy.config import ConfigMaster
from pyutil.portfolio.portfolio import Portfolio
from antarctic.PandasFields import SeriesField, ParquetFrameField
from antarctic.Document import XDocument

import os


def strategies(folder):
    for file in os.listdir(folder):
        with open(os.path.join(folder, file), "r") as f:
            source = f.read()
            m = _module(source=source)
            yield m.name, source


def _module(source):
    # We store the source code directly as a string in a mongo database!
    # Using reflection we get back to a module
    from types import ModuleType

    compiled = compile(source, '', 'exec')
    mod = ModuleType("module")
    exec(compiled, mod.__dict__)
    return mod


def configuration(strategy, reader=None):
    return strategy.module.Configuration(reader=reader)


class Strategy(XDocument):
    # active flag, only active strategies are updated
    active = BooleanField(default=True)
    # source code
    source = StringField()
    # type of the strategy (you can use whatever name here)
    type = StringField(max_length=100)

    prices = ParquetFrameField()
    weights = ParquetFrameField()
    nav = SeriesField()
    sector = ParquetFrameField()

    symbols = ListField(ReferenceField(Symbol))

    def configuration(self, reader=None) -> ConfigMaster:
        return self.module.Configuration(reader=reader)

    @property
    def portfolio(self):
        try:
            return Portfolio(prices=self.prices, weights=self.weights)
        except AttributeError:
            return None

    @queryset_manager
    def active_strategies(doc_cls, queryset):
        return queryset.filter(active=True)

    @property
    def module(self):
        return _module(self.source)

    @portfolio.setter
    def portfolio(self, portfolio):
        self.weights = portfolio.weights
        self.prices = portfolio.prices
        self.nav = portfolio.nav

        for symbol in portfolio.assets:
            s = Symbol.objects(name=symbol).get()
            if s not in set(self.symbols):
                self.symbols.append(s)

        symbolmap = {s.name: s.group.name for s in self.symbols}
        frame = self.weights.ffill().groupby(by=symbolmap, axis=1).sum()
        frame["Total"] = frame.sum(axis=1)
        self.sector = frame

    @property
    def drawdown(self):
        return drawdown(self.nav)

    @property
    def assets(self):
        return self.configuration(reader=None).names

    @property
    def last_valid_index(self):
        try:
            return self.prices.last_valid_index()
        except AttributeError:
            return None

    @property
    def monthlytable(self):
        return monthlytable(self.nav.pct_change().dropna())

    def ewm_volatility(self, com=50, min_periods=50, periods=None):
        return from_nav(self.nav).ewm_volatility(com=com, min_periods=min_periods, periods=periods).dropna()

    @classmethod
    def reference_frame(cls, objects=None) -> pd.DataFrame:
        objects = objects or Strategy.objects.only("name", "reference", "source", "type", "active")
        frame = super(Strategy, cls).reference_frame(objects=objects)
        frame["source"] = pd.Series({s.name: s.source for s in objects})
        frame["type"] = pd.Series({s.name: s.type for s in objects})
        frame["active"] = pd.Series({s.name: s.active for s in objects})
        return frame

    @staticmethod
    def portfolios(strategies=None) -> dict:
        s = strategies or Strategy.objects.only("name", "prices", "weights")
        return {strategy.name: strategy.portfolio for strategy in s if strategy.portfolio is not None}

    @staticmethod
    def navs(strategies=None) -> pd.DataFrame:
        strategies = strategies or Strategy.objects.only("name", "nav")
        frame = pd.DataFrame({s.name: s.nav for s in strategies})
        frame.index.name = "Portfolio"
        return frame

    @staticmethod
    def sectors(strategies=None) -> pd.DataFrame:
        s = strategies or Strategy.objects.only("name", "sector")
        frame = pd.DataFrame({strategy.name: strategy.sector.iloc[-1] for strategy in s if strategy.sector is not None})
        frame = frame.transpose()
        frame.index.name = "Portfolio"
        return frame