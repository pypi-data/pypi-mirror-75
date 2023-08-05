from typing import List, Tuple
from decimal import Decimal

from .models import FreightPricing
from .._internals import as_decimal


def parse(json: List[dict]) -> Tuple[FreightPricing, ...]:
    return tuple(
        parse_freight_pricing_item(i) for i in json
    )


def parse_freight_pricing_item(json: dict) -> FreightPricing:
    return FreightPricing(
        json.get('vesselClass'),
        as_decimal(json.get('cargoQuantity')),
        as_decimal(json.get('rate')),
        as_decimal(json.get('totalFreight'))
    )

