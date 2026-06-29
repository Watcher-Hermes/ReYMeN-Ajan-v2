"""Test: reymen/cost_tracker.py — kapsamli testler"""
from __future__ import annotations
import os, sys, json, tempfile, time
from pathlib import Path
import pytest

PROJE_KOK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJE_KOK))


@pytest.fixture
def tracker(tmp_path):
    from reymen.cost_tracker import CostTracker
    db_path = tmp_path / "test_costs.db"
    t = CostTracker(db_path=db_path)
    yield t


class TestCostRecord:
    def test_as_dict(self):
        from reymen.cost_tracker import CostRecord
        r = CostRecord(model="gpt-4o", prompt_tokens=100, completion_tokens=50, cost_usd=0.005)
        d = r.as_dict()
        assert d["model"] == "gpt-4o"
        assert d["prompt_tokens"] == 100
        assert d["completion_tokens"] == 50


class TestPriceFor:
    def test_exact_model(self, tracker):
        price = tracker._price_for("gpt-4o")
        assert price["prompt"] == 5.0
        assert price["completion"] == 15.0

    def test_prefix_match(self, tracker):
        price = tracker._price_for("gpt-4o-2024-08-06")
        assert price["prompt"] == 5.0

    def test_default_model(self, tracker):
        price = tracker._price_for("unknown-model-v42")
        assert price["prompt"] == 1.0

    def test_custom_price_table(self):
        from reymen.cost_tracker import CostTracker
        custom = {"my-model": {"prompt": 10.0, "completion": 20.0}, "default": {"prompt": 1.0, "completion": 2.0}}
        t = CostTracker(db_path=":memory:", price_table=custom)
        assert t._price_for("my-model")["prompt"] == 10.0
        assert t._price_for("other")["prompt"] == 1.0


class TestComputeCost:
    def test_basic(self, tracker):
        cost = tracker.compute_cost("gpt-4o", 1_000_000, 500_000)
        assert cost == 12.5

    def test_zero_tokens(self, tracker):
        cost = tracker.compute_cost("gpt-4o", 0, 0)
        assert cost == 0.0

    def test_rounding(self, tracker):
        cost = tracker.compute_cost("gpt-4o-mini", 100, 50)
        assert cost == 0.000045


class TestRecord:
    def test_basic_record(self, tracker):
        rec = tracker.record("gpt-4o", 1000, 500)
        assert rec.model == "gpt-4o"
        assert rec.prompt_tokens == 1000
        assert rec.completion_tokens == 500
        assert rec.cost_usd > 0

    def test_record_with_provider(self, tracker):
        rec = tracker.record("gpt-4o", 100, 50, provider="openai", session_id="sess-001",
                              metadata={"test": True})
        assert rec.provider == "openai"
        assert rec.session_id == "sess-001"
        assert rec.metadata["test"] is True

    def test_negative_tokens(self, tracker):
        with pytest.raises(ValueError, match="negatif"):
            tracker.record("gpt-4o", -1, 50)

    def test_multiple_records(self, tracker):
        tracker.record("gpt-4o", 100, 50)
        tracker.record("gpt-4o-mini", 200, 100)
        s = tracker.summary()
        assert s["total_calls"] == 2


class TestSummary:
    def test_empty_summary(self, tracker):
        s = tracker.summary()
        assert s["total_calls"] == 0
        assert s["total_cost_usd"] == 0.0

    def test_summary_with_data(self, tracker):
        tracker.record("gpt-4o", 1_000_000, 500_000)
        s = tracker.summary()
        assert s["total_calls"] == 1
        assert s["total_cost_usd"] == 12.5

    def test_summary_by_model(self, tracker):
        tracker.record("gpt-4o", 100, 50)
        tracker.record("gpt-4o-mini", 200, 100)
        s = tracker.summary()
        assert "gpt-4o" in s["by_model"]
        assert "gpt-4o-mini" in s["by_model"]

    def test_summary_by_provider(self, tracker):
        tracker.record("gpt-4o", 100, 50, provider="openai")
        tracker.record("claude-3-5-sonnet", 200, 100, provider="anthropic")
        s = tracker.summary()
        assert "openai" in s["by_provider"]
        assert "anthropic" in s["by_provider"]


class TestDumpLog:
    def test_dump_empty(self, tracker):
        logs = tracker.dump_log()
        assert logs == []

    def test_dump_with_data(self, tracker):
        tracker.record("gpt-4o", 100, 50, metadata={"test": True})
        logs = tracker.dump_log()
        assert len(logs) == 1
        assert logs[0]["model"] == "gpt-4o"

    def test_dump_limit(self, tracker):
        for i in range(5):
            tracker.record(f"model-{i}", 10, 5)
        logs = tracker.dump_log(limit=2)
        assert len(logs) == 2

    def test_dump_filter_model(self, tracker):
        tracker.record("gpt-4o", 100, 50)
        tracker.record("claude-3-5-sonnet", 200, 100)
        logs = tracker.dump_log(model="gpt-4o")
        assert len(logs) == 1


class TestReset:
    def test_reset(self, tracker):
        tracker.record("gpt-4o", 100, 50)
        tracker.record("gpt-4o-mini", 200, 100)
        deleted = tracker.reset()
        assert deleted == 2
        s = tracker.summary()
        assert s["total_calls"] == 0

    def test_reset_empty(self, tracker):
        deleted = tracker.reset()
        assert deleted == 0


class TestIterRecords:
    def test_iter(self, tracker):
        tracker.record("gpt-4o", 100, 50, metadata={"test": True})
        tracker.record("claude-3-5-sonnet", 200, 100)
        records = list(tracker.iter_records())
        assert len(records) == 2

    def test_iter_empty(self, tracker):
        records = list(tracker.iter_records())
        assert records == []


class TestSetDbPath:
    def test_set_db_path(self, tmp_path):
        from reymen.cost_tracker import set_db_path, _get_tracker
        db_path = tmp_path / "new_costs.db"
        set_db_path(db_path)
        t = _get_tracker()
        assert str(t._db_path) == str(db_path)


class TestSetPriceTable:
    def test_set_price_table(self):
        from reymen.cost_tracker import set_price_table, _get_tracker
        new_table = {"my-model": {"prompt": 99.0, "completion": 199.0}, "default": {"prompt": 1.0, "completion": 2.0}}
        set_price_table(new_table)
        t = _get_tracker()
        assert t._price_for("my-model")["prompt"] == 99.0


class TestModuleFunctions:
    def test_record_usage(self, tmp_path):
        from reymen.cost_tracker import record_usage, set_db_path, summary, reset, dump_log
        db_path = tmp_path / "mod_costs.db"
        set_db_path(db_path)
        rec = record_usage("gpt-4o", 1000, 500, provider="openai", session_id="sess-001")
        assert rec.model == "gpt-4o"
        s = summary()
        assert s["total_calls"] == 1
        logs = dump_log()
        assert len(logs) == 1
        deleted = reset()
        assert deleted == 1
