# -*- coding: utf-8 -*-
import argparse
import logging
import sys
from typing import Any, Dict

from bot.client import BinanceAPIError, BinanceClient, BinanceNetworkError
from bot.orders import place_order


def _print_table(title: str, rows: Dict[str, Any]) -> None:
    labels = list(rows.keys())
    values = ["" if v is None else str(v) for v in rows.values()]

    label_width = max(len(label) for label in labels) if labels else 0
    value_width = max(len(value) for value in values) if values else 0

    total_width = label_width + value_width + 7
    print("┌" + "─" * (total_width - 2) + "┐")
    print(f"│  {title.ljust(total_width - 4)}│")
    print("├" + "─" * (label_width + 2) + "┬" + "─" * (value_width + 2) + "┤")

    for label, value in zip(labels, values):
        print(f"│  {label.ljust(label_width)} │  {value.ljust(value_width)} │")

    print("└" + "─" * (label_width + 2) + "┴" + "─" * (value_width + 2) + "┘")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Binance Futures Testnet Trading Bot")
    parser.add_argument("--symbol", required=True, type=str, help="e.g. BTCUSDT")
    parser.add_argument("--side", required=True, type=str, help="BUY or SELL")
    parser.add_argument(
        "--type",
        required=True,
        type=str,
        help="MARKET, LIMIT, or STOP_MARKET",
    )
    parser.add_argument("--quantity", required=True, type=float, help="e.g. 0.001")
    parser.add_argument("--price", type=float, help="required for LIMIT orders")
    parser.add_argument("--stop-price", type=float, help="required for STOP_MARKET orders")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    logger = logging.getLogger("cli")

    summary = {
        "Symbol": args.symbol,
        "Side": args.side,
        "Type": args.type,
        "Quantity": args.quantity,
    }
    if args.price is not None:
        summary["Price"] = args.price
    if args.stop_price is not None:
        summary["Stop Price"] = args.stop_price

    _print_table("ORDER REQUEST SUMMARY", summary)

    try:
        client = BinanceClient()
        result = place_order(
            client=client,
            symbol=args.symbol,
            side=args.side,
            order_type=args.type,
            quantity=args.quantity,
            price=args.price,
            stop_price=args.stop_price,
        )

        print("✓ Order placed successfully!")
        response_rows = {
            "Order ID": result.get("orderId"),
            "Status": result.get("status"),
            "Exec Qty": result.get("executedQty"),
            "Avg Price": result.get("avgPrice"),
        }
        _print_table("ORDER RESPONSE", response_rows)
    except (ValueError, BinanceAPIError, BinanceNetworkError) as exc:
        logger.exception("Order failed")
        print(f"✗ Error: {exc}", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        logger.exception("Unexpected error")
        print(f"✗ Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()