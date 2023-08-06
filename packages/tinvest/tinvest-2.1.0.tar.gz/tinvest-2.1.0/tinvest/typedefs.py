from datetime import datetime
from typing import Any, Dict, Union

__all__ = 'AnyDict'

AnyDict = Dict[str, Any]

datetime_or_str = Union[datetime, str]
