from decimal import Decimal
from datetime import datetime

convertToText = {
    "string": lambda s : s if s is not None else "",
    "number": lambda number: str(number) if number is not None else "",
    "date": lambda date: date.strftime("%Y-%m-%d") if date is not None else "",
}

convertToInitial = {
    "string": lambda s : s,
    "number": lambda numberStr: Decimal(numberStr) if numberStr != "" else None,
    "date": lambda dateStr: datetime.strptime(dateStr, "%Y-%m-%d") if dateStr != "" else None,
}
