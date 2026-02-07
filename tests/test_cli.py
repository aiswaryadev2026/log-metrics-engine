import subprocess
import sys


def test_cli_runs_successfully():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "src.main",
            "sample_logs/access.log",
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "request_count" in result.stdout
