from unittest.mock import patch
from src.checker import check_website

@patch("src.checker.urllib.request.urlopen")
def test_website_is_healthy(mock_urlopen):
    mock_urlopen.return_value.__enter__.return_value.status = 200
    result = check_website("https://example.com")

    assert result["healthy"] is True
    assert result["status_code"] == 200
    assert result["latency_ms"] >= 0