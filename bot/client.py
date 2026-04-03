import hashlib
import hmac
import logging
import os
import time
from typing import Any, Dict, Optional
from urllib.parse import urlencode

import requests
from dotenv import load_dotenv

from .logging_config import setup_logging


class BinanceAPIError(Exception):
    def __init__(self, code: Optional[int], message: str):
        super().__init__(message)
        self.code = code
        self.message = message


class BinanceNetworkError(Exception):
    pass


class BinanceClient:
    BASE_URL = "https://testnet.binancefuture.com"

    def __init__(self) -> None:
        load_dotenv()
        self.api_key = os.getenv("BINANCE_API_KEY")
        secret_key = os.getenv("BINANCE_SECRET_KEY")

        if not self.api_key or not secret_key:
            raise BinanceAPIError(None, "Missing BINANCE_API_KEY or BINANCE_SECRET_KEY")

        self.secret_key = secret_key.encode("utf-8")
        self.session = requests.Session()
        self.session.headers.update({"X-MBX-APIKEY": self.api_key})

        setup_logging()
        self.logger = logging.getLogger(self.__class__.__name__)

    def _sign(self, params: Dict[str, Any]) -> Dict[str, Any]:
        params["timestamp"] = int(time.time() * 1000)
        params["recvWindow"] = 5000
        query_string = urlencode(params)
        signature = hmac.new(self.secret_key, query_string.encode("utf-8"), hashlib.sha256)
        params["signature"] = signature.hexdigest()
        return params

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        signed: bool = False,
    ) -> Dict[str, Any]:
        params = params or {}
        if signed:
            params = self._sign(params)

        self.logger.debug("REQUEST %s %s params=%s", method, endpoint, params)

        try:
            if method.upper() == "GET":
                response = self.session.get(
                    f"{self.BASE_URL}{endpoint}", params=params, timeout=10
                )
            else:
                response = self.session.post(
                    f"{self.BASE_URL}{endpoint}", params=params, timeout=10
                )
        except (requests.ConnectionError, requests.Timeout, requests.RequestException) as exc:
            self.logger.exception("Network error during request")
            raise BinanceNetworkError(str(exc)) from exc

        self.logger.debug(
            "RESPONSE status=%s body=%s", response.status_code, response.text[:500]
        )

        if response.status_code != 200:
            try:
                error_payload = response.json()
            except ValueError:
                error_payload = {"code": None, "msg": response.text}

            raise BinanceAPIError(error_payload.get("code"), error_payload.get("msg"))

        return response.json()

    def get_server_time(self) -> int:
        data = self._request("GET", "/fapi/v1/time", signed=False)
        return int(data.get("serverTime"))

    def place_order(self, **kwargs: Any) -> Dict[str, Any]:
        return self._request("POST", "/fapi/v1/order", params=kwargs, signed=True)