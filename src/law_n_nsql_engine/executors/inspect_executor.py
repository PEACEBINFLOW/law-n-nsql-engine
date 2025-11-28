from typing import Any, Dict

from ..ast import InspectQuery
from ..adapters.in_memory_adapter import BaseNetworkAdapter


def execute_inspect(query: InspectQuery, adapter: BaseNetworkAdapter) -> Dict[str, Any]:
    if query.target_type == "FREQUENCY":
        return adapter.inspect_frequency(query.value)
    if query.target_type == "DEVICE":
        return adapter.inspect_device(query.value)
    if query.target_type == "TOWER":
        return adapter.inspect_tower(query.value)

    return {"status": "error", "reason": "unknown_inspect_target"}
