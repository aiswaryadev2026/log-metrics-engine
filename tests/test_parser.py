import tempfile
from src.parser.log_parser import LogParser


def test_log_parser_parses_valid_line():
    content = "2024-09-10T10:15:30Z GET /api/orders 200 123\n"

    with tempfile.NamedTemporaryFile(mode="w+") as f:
        f.write(content)
        f.seek(0)

        parser = LogParser()
        events = list(parser.parse(f.name))

        assert len(events) == 1
        event = events[0]
        assert event.method == "GET"
        assert event.path == "/api/orders"
        assert event.status == 200
        assert event.latency_ms == 123
