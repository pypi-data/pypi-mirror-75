import enum

from dataclasses import dataclass


class Period(str, enum.Enum):
    MINS = '1m'
    MINS_5 = '5m'
    MINS_15 = '15m'
    MINS_30 = '30m'
    HOURS = '1h'
    HOURS_4 = '4h'
    HOURS_6 = '6h'
    HOURS_12 = '12h'
    DAY = '1D'
    WEEK = '7D'
    WEEK_2 = '14D'
    MONTH_1 = '1M'


class OrderSide(str, enum.Enum):
    BUY = 'BUY'
    SELL = 'SELL'


class OrderType(str, enum.Enum):
    LIMIT = 'LIMIT'
    MARKET = 'MARKET'


class OrderStatus(str, enum.Enum):
    ACTIVE = 'ACTIVE'
    FILLED = 'FILLED'
    CANCELED = 'CANCELED'
    REJECTED = 'REJECTED'
    EXPIRED = 'EXPIRED'


class Coin(str, enum.Enum):
    BTC = 'BTC'
    CRO = 'CRO'
    MCO = 'MCO'
    ETH = 'ETH'
    XRP = 'XRP'
    LTC = 'LTC'
    EOS = 'EOS'
    XLM = 'XLM'
    ATOM = 'ATOM'
    LINK = 'LINK'
    XTZ = 'XTZ'
    BCH = 'BCH'
    VET = 'VET'
    ICX = 'ICX'
    ADA = 'ADA'
    ENJ = 'ENJ'
    ALGO = 'ALGO'
    KNC = 'KNC'
    NEO = 'NEO'

    USDT = 'USDT'
    USDC = 'USDC'


class Pair(str, enum.Enum):
    CRO_BTC = 'CRO_BTC'
    MCO_BTC = 'MCO_BTC'
    ETH_BTC = 'ETH_BTC'
    XRP_BTC = 'XRP_BTC'
    LTC_BTC = 'LTC_BTC'
    EOS_BTC = 'EOS_BTC'
    XLM_BTC = 'XLM_BTC'
    ATOM_BTC = 'ATOM_BTC'
    LINK_BTC = 'LINK_BTC'
    XTZ_BTC = 'XTZ_BTC'
    BCH_BTC = 'BCH_BTC'
    VET_BTC = 'VET_BTC'
    ICX_BTC = 'ICX_BTC'
    ADA_BTC = 'ADA_BTC'
    ENJ_BTC = 'ENJ_BTC'
    ALGO_BTC = 'ALGO_BTC'
    KNC_BTC = 'KNC_BTC'
    NEO_BTC = 'NEO_BTC'

    USDC_USDT = 'USDC_USDT'
    BTC_USDT = 'BTC_USDT'
    CRO_USDT = 'CRO_USDT'
    MCO_USDT = 'MCO_USDT'
    ETH_USDT = 'ETH_USDT'
    XRP_USDT = 'XRP_USDT'
    LTC_USDT = 'LTC_USDT'
    EOS_USDT = 'EOS_USDT'
    XLM_USDT = 'XLM_USDT'
    ATOM_USDT = 'ATOM_USDT'
    LINK_USDT = 'LINK_USDT'
    XTZ_USDT = 'XTZ_USDT'
    BCH_USDT = 'BCH_USDT'
    VET_USDT = 'VET_USDT'
    ICX_USDT = 'ICX_USDT'
    ADA_USDT = 'ADA_USDT'
    ENJ_USDT = 'ENJ_USDT'
    ALGO_USDT = 'ALGO_USDT'
    KNC_USDT = 'KNC_USDT'
    NEO_USDT = 'NEO_USDT'

    MCO_CRO = 'MCO_CRO'
    ETH_CRO = 'ETH_CRO'
    XRP_CRO = 'XRP_CRO'
    LTC_CRO = 'LTC_CRO'
    EOS_CRO = 'EOS_CRO'
    XLM_CRO = 'XLM_CRO'
    ATOM_CRO = 'ATOM_CRO'
    LINK_CRO = 'LINK_CRO'
    XTZ_CRO = 'XTZ_CRO'
    BCH_CRO = 'BCH_CRO'
    VET_CRO = 'VET_CRO'
    ICX_CRO = 'ICX_CRO'
    ADA_CRO = 'ADA_CRO'
    ENJ_CRO = 'ENJ_CRO'
    ALGO_CRO = 'ALGO_CRO'
    KNC_CRO = 'KNC_CRO'
    NEO_CRO = 'NEO_CRO'

    CRO_USDC = 'CRO_USDC'


@dataclass
class Candle:
    time: int
    open: float
    high: float
    low: float
    close: float
    volume: float
    pair: Pair


@dataclass
class Trade:
    id: int
    time: int
    price: float
    quantity: float
    side: OrderSide
    pair: Pair
