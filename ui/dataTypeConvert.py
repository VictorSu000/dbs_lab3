from decimal import Decimal

convertToText = {
    "string": lambda s : s,
    "number": lambda number: str(number),
}

convertToInitial = {
    "string": lambda s : s,
    "number": lambda numberStr: Decimal(numberStr),
}
