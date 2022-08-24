from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import requests

USER_AGENT = "KrakenSpot/Py"


@dataclass
class KrakenResponse:
    result: Dict = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return len(self.errors) == 0


@dataclass
class HTTPResponse:
    status_code: int
    body: Dict[str, Any]


def http_get(url: str, params: Optional[Dict[str, str]] = None) -> HTTPResponse:
    r = requests.get(url, headers={"User-Agent": USER_AGENT}, params=params)
    return HTTPResponse(
        status_code=r.status_code,
        body=r.json(),
    )


def http_post(
    url: str,
    body: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
) -> HTTPResponse:
    r = requests.post(url, headers=headers, data=body)
    print(url)
    return HTTPResponse(
        status_code=r.status_code,
        body=r.json(),
    )
