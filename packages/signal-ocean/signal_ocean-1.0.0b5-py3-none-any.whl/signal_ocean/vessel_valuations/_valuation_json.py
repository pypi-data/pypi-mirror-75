from typing import List, Tuple

from .models import Valuation
from .._internals import parse_datetime, as_decimal


def parse_valuations(json: List[dict]) -> Tuple[Valuation, ...]:
    return tuple(
        parse_valuation(s) for s in json
    )


def parse_valuation(json: dict) -> Valuation:
    return Valuation(
        json.get('imo'),
        parse_datetime(json.get('valueFrom')),
        as_decimal(json.get('valuationPrice')),
        parse_datetime(json.get('updatedDate'))
    )
