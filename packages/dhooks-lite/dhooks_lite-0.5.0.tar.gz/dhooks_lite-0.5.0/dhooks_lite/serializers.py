from datetime import datetime
import json
from typing import Any


class JsonDateTimeEncoder(json.JSONEncoder):
    """Add ability to encode datetime to JSON encoder"""

    def default(self, o: Any) -> Any:
        if isinstance(o, datetime):
            return o.isoformat()
        else:
            return json.JSONEncoder.default(self, o)
