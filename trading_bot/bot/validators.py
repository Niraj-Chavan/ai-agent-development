import re
from typing import Optional


def validate_symbol(symbol: str) -> str:
    if not isinstance(symbol, str) or not symbol or not re.fullmatch(r"[A-Z]+", symbol):
        raise ValueError("Symbol must be uppercase letters only, e.g. BTCUSDT")
    return symbol.upper()


def validate_side(side: str) -> str:
    if not isinstance(side, str) or side.upper() not in {"BUY", "SELL"}:
        raise ValueError("Side must be BUY or SELL")
    return side.upper()


def validate_order_type(order_type: str) -> str:
    allowed = {"MARKET", "LIMIT", "STOP_MARKET"}
    if not isinstance(order_type, str) or order_type.upper() not in allowed:
        raise ValueError("Order type must be MARKET, LIMIT, or STOP_MARKET")
    return order_type.upper()


def validate_quantity(quantity) -> float:
    try:
        qty = float(quantity)
    except (TypeError, ValueError):
        raise ValueError("Quantity must be a positive number")
    if qty <= 0:
        raise ValueError("Quantity must be a positive number")
    return qty


def validate_price(price, order_type: str) -> Optional[float]:
    if order_type == "LIMIT":
        if price is None:
            raise ValueError("Price is required for LIMIT orders")
        try:
            price_val = float(price)
        except (TypeError, ValueError):
            raise ValueError("Price is required for LIMIT orders")
        if price_val <= 0:
            raise ValueError("Price is required for LIMIT orders")
        return price_val
    if order_type == "MARKET":
        return None
    return None


def validate_stop_price(stop_price, order_type: str) -> Optional[float]:
    if order_type == "STOP_MARKET":
        if stop_price is None:
            raise ValueError("Stop price is required for STOP_MARKET orders")
        try:
            stop_val = float(stop_price)
        except (TypeError, ValueError):
            raise ValueError("Stop price is required for STOP_MARKET orders")
        if stop_val <= 0:
            raise ValueError("Stop price is required for STOP_MARKET orders")
        return stop_val
    return None