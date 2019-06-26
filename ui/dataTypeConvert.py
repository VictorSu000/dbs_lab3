from decimal import Decimal
from datetime import datetime
convertToText = {
    "string": lambda s : s,
    "number": lambda number: str(number),
    "date": lambda date: date.strftime("%Y-%m-%d"),
}

convertToInitial = {
    "string": lambda s : s,
    "number": lambda numberStr: Decimal(numberStr),
    "date": lambda dateStr: datetime.strptime(dateStr, "%Y-%m-%d"),
}
