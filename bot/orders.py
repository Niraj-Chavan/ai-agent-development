import logging
from typing import Any, Dict, Optional

from .client import BinanceClient
from .validators import (
    validate_order_type,
    validate_price,
    validate_quantity,
    validate_side,
    validate_stop_price,
    validate_symbol,
)

logger = logging.getLogger(__name__)


def place_order(
    client: BinanceClient,
    symbol,
    side,
    order_type,
    quantity,
    price: Optional[float] = None,
    stop_price: Optional[float] = None,
) -> Dict[str, Any]:
    try:
        symbol_val = validate_symbol(symbol)
        side_val = validate_side(side)
        order_type_val = validate_order_type(order_type)
        quantity_val = validate_quantity(quantity)
        price_val = validate_price(price, order_type_val)
        stop_price_val = validate_stop_price(stop_price, order_type_val)
    except ValueError as exc:
        raise ValueError(str(exc)) from exc

    params: Dict[str, Any] = {
        "symbol": symbol_val,
        "side": side_val,
        "type": order_type_val,
        "quantity": quantity_val,
    }

    if order_type_val == "LIMIT":
        params["price"] = price_val
        params["timeInForce"] = "GTC"
    elif order_type_val == "STOP_MARKET":
        params["stopPrice"] = stop_price_val

    logger.info(
        "Placing %s %s order for %s %s",
        order_type_val,
        side_val,
        quantity_val,
        symbol_val,
    )

    response = client.place_order(**params)

    result = {
        "orderId": response.get("orderId"),
        "status": response.get("status"),
        "executedQty": response.get("executedQty"),
        "avgPrice": response.get("avgPrice"),
        "symbol": response.get("symbol"),
        "side": response.get("side"),
        "type": response.get("type"),
        "origQty": response.get("origQty"),
    }

    if "timeInForce" in response:
        result["timeInForce"] = response.get("timeInForce")

    logger.info("Order placed successfully. orderId=%s", result.get("orderId"))
    return result