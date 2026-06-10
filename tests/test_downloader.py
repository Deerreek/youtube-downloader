import downloader
from downloader import QUALITY_TO_FORMAT, _append_history, load_history


def test_quality_to_format_has_expected_keys():
    assert set(QUALITY_TO_FORMAT) == {"best", "1080", "720", "480", "360"}
    for fmt in QUALITY_TO_FORMAT.values():
        assert "bestvideo" in fmt and "bestaudio" in fmt


def test_load_history_returns_empty_list_when_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(downloader, "HISTORY_FILE", tmp_path / "history.json")
    assert load_history() == []


def test_append_history_round_trip(tmp_path, monkeypatch):
    monkeypatch.setattr(downloader, "HISTORY_FILE", tmp_path / "history.json")

    _append_history({"title": "First", "mode": "audio"})
    _append_history({"title": "Second", "mode": "video"})

    history = load_history()
    assert len(history) == 2
    # most recent download appears first
    assert history[0]["title"] == "Second"
    assert history[1]["title"] == "First"
