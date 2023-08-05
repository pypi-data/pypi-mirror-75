from cort_client import CortClient
import pathlib


HOST = "127.0.0.1"
RECEIVER_PORT = 20425
PROVIDER_PORT = 20426


def test_read_data():
    cli = CortClient(HOST, RECEIVER_PORT)
    dir_path = pathlib.Path(__file__).parent.parent / "cort_client"
    assert cli._read_data(dir_path)
