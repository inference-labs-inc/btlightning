import pytest

from btlightning import Lightning

from conftest import MINER_HOTKEY, VALIDATOR_HOTKEY


def test_missing_synapse_type(client_and_axon):
    client, axon = client_and_axon
    with pytest.raises(KeyError, match="synapse_type"):
        client.query_axon(axon, {"data": {"msg": "hello"}})


def test_missing_hotkey(client_and_axon):
    client, _ = client_and_axon
    with pytest.raises(KeyError, match="hotkey"):
        client.query_axon({"ip": "127.0.0.1", "port": 1234}, {"synapse_type": "echo", "data": {}})


def test_missing_ip(client_and_axon):
    client, _ = client_and_axon
    with pytest.raises(KeyError, match="ip"):
        client.query_axon({"hotkey": MINER_HOTKEY, "port": 1234}, {"synapse_type": "echo", "data": {}})


def test_missing_port(client_and_axon):
    client, _ = client_and_axon
    with pytest.raises(KeyError, match="port"):
        client.query_axon({"hotkey": MINER_HOTKEY, "ip": "127.0.0.1"}, {"synapse_type": "echo", "data": {}})


def test_query_without_signer():
    client = Lightning(wallet_hotkey=VALIDATOR_HOTKEY)
    axon = {"hotkey": MINER_HOTKEY, "ip": "127.0.0.1", "port": 9999}
    with pytest.raises(Exception):
        client.query_axon(axon, {"synapse_type": "echo", "data": {}})
    client.close()


def test_invalid_timeout(client_and_axon):
    client, axon = client_and_axon
    with pytest.raises(Exception):
        client.query_axon(axon, {"synapse_type": "echo", "data": {}}, timeout_secs=-1.0)
