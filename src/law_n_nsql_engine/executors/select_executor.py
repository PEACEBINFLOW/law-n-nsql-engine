from typing import List, Dict, Any

from ..ast import SelectQuery, Condition
from ..adapters.in_memory_adapter import BaseNetworkAdapter


def execute_select(query: SelectQuery, adapter: BaseNetworkAdapter) -> List[Dict[str, Any]]:
    """
    Execute a SELECT query against the given adapter.
    """
    rows = adapter.fetch_table(query.table)
    filtered = [row for row in rows if _matches_all(row, query.conditions)]

    if query.fields == ["*"]:
        return filtered

    projected: List[Dict[str, Any]] = []
    for row in filtered:
        projected.append({field: row.get(field) for field in query.fields})
    return projected


def _matches_all(row: Dict[str, Any], conditions: List[Condition]) -> bool:
    return all(_matches(row, cond) for cond in conditions)


def _matches(row: Dict[str, Any], cond: Condition) -> bool:
    value = row.get(cond.field)

    if cond.op == "MATCHES":
        pattern = cond.value.replace("*", ".*")
        import re
        return re.fullmatch(pattern, str(value) or "") is not None

    if cond.op == "=":
        return value == cond.value
    if cond.op == "!=":
        return value != cond.value
    if cond.op == "<":
        return value < cond.value
    if cond.op == ">":
        return value > cond.value
    if cond.op == "<=":
        return value <= cond.value
    if cond.op == ">=":
        return value >= cond.value

    return False
