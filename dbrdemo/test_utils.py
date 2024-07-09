import json
from copy import deepcopy
from typing import Any, Dict, List, Optional

import pandas as pd
import pyspark.sql as S
import pyspark.sql.connect.dataframe as CS
from pyspark.sql.types import StructType


def _smart_str(x):
    try:
        return x.as_dict()
    except Exception:
        pass

    try:
        return x.asdict()
    except Exception:
        pass

    try:
        return x.asDict(True)
    except Exception:
        pass

    try:
        return x.asDict()
    except Exception:
        pass

    return str(x)


def _random_str_get_replace_dict(random_str: Optional[str | Dict[str, str]]):
    mapping: Dict[str, str]

    if not random_str:
        mapping = {}
    elif isinstance(random_str, str):
        mapping = {random_str: ''}
    elif isinstance(random_str, dict):
        mapping = deepcopy(random_str)
    else:
        raise RuntimeError(f"invalid parameter: {random_str}")

    # add more mapping rules here related to your testing approach

    return mapping


def strip_random_str(data: str, random_str: Optional[str | Dict[str, str]]):
    mapping = _random_str_get_replace_dict(random_str)

    if not data or not mapping:
        return data

    for find, replace in mapping.items():
        data = data.replace(find, replace)

    return data


def smart_verify(obj: Any,
                 namer=None,
                 order_by: Optional[List[str]] = None,
                 random_str: Optional[str | Dict[str, str]] = None):
    from approvaltests.approvals import verify

    if isinstance(obj, Dict):
        try:
            s = json.dumps(obj, indent=4, default=_smart_str)
        except Exception:
            s = str(obj)

        s = strip_random_str(s, random_str)
        return verify(s, namer=namer)

    if isinstance(obj, StructType):
        return smart_verify(obj.jsonValue(), namer=namer, random_str=random_str)

    if isinstance(obj, pd.DataFrame):
        s = obj.to_markdown()
        assert s
        return verify(s, namer=namer)

    if isinstance(obj, (S.DataFrame, CS.DataFrame)):
        order_by = order_by or [x[0] for x in obj.dtypes if "map" not in x[1] and "array" not in x[1]]
        pdf = obj.orderBy(*order_by).toPandas()
        return smart_verify(pdf, namer=namer, random_str=random_str)

    s = str(obj)
    s = strip_random_str(s, random_str)
    return verify(s, namer=namer)
