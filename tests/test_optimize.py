from law_n_nsql_engine.engine import execute_query
from law_n_nsql_engine.adapters.in_memory_adapter import InMemoryNetworkAdapter


def test_optimize_route():
    adapter = InMemoryNetworkAdapter()
    query = """
    OPTIMIZE ROUTE "0xA4C1" TO "0xB7D2"
    PREFER frequency_band = "mid-band-5G"
    MINIMIZE latency;
    """
    result = execute_query(query, adapter)[0]
    assert result["status"] == "ok"
    assert "route" in result
    assert result["route"]["device_from"] == "0xA4C1"
