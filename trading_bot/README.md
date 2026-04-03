# Binance Futures Testnet Trading Bot

## Project Overview

This project is a Python 3.x CLI trading bot for placing MARKET, LIMIT, and STOP_MARKET orders on the Binance Futures Testnet (USDT-M). It uses direct REST calls with HMAC-SHA256 signing, structured logging, and clear validation. The focus is on clean code structure, robustness, and developer-friendly CLI output.

## Setup

### Prerequisites

- Python 3.8+

### Clone / Download

Download or clone this repository into your workspace.

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment

Copy the example environment file and add your testnet keys:

```bash
cp .env.example .env
```

```
BINANCE_API_KEY=your_testnet_api_key_here
BINANCE_SECRET_KEY=your_testnet_secret_key_here
```

### Get Binance Futures Testnet API Keys

Create a testnet account and generate API keys at `https://testnet.binancefuture.com`.

## Usage

Run commands from the `trading_bot/` directory.

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

```bash
python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.01 --price 3500
```

```bash
python cli.py --symbol BTCUSDT --side SELL --type MARKET --quantity 0.001
```

```bash
python cli.py --symbol BTCUSDT --side BUY --type STOP_MARKET --quantity 0.001 --stop-price 60000
```

## Project Structure

```
trading_bot/
  bot/
    __init__.py
    client.py
    orders.py
    validators.py
    logging_config.py
  cli.py
  logs/
  .env
  .env.example
  README.md
  requirements.txt
```

## Logging

- Logs are written to `logs/trading_bot.log`.
- INFO logs capture order summaries and success messages.
- DEBUG logs capture raw API request/response details (truncated for safety).
- ERROR logs include full tracebacks for failures.

## Assumptions

- Testnet only (not for live trading).
- LIMIT order price must be within ~10% of the mark price or Binance rejects it.
- Quantities must meet Binance minimum notional (0.001 BTC minimum on testnet).

## Error Handling

- `ValueError` for validation failures.
- `BinanceAPIError` for API errors returned by Binance.
- `BinanceNetworkError` for connection, timeout, or request failures.
- CLI prints a clean error message and exits with status code 1.