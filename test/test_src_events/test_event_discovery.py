from src.events.event_bus import discover_events

def test_discover_events_has_core():
    events = discover_events()
    assert "log_message" in events
    assert "batch_gen_data_truthful" in events
    assert "gen_truthful_summary" in events
