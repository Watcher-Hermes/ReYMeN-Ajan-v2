"""Test: reymen/kanban.py — kapsamli testler"""
from __future__ import annotations
import os, sys, json, tempfile, time
from pathlib import Path
import pytest

PROJE_KOK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJE_KOK))


@pytest.fixture
def board():
    from reymen.kanban import Board, Column, Card, Priority
    b = Board(name="Test Pano")
    yield b


class TestPriority:
    def test_from_str_name(self):
        from reymen.kanban import Priority
        assert Priority.from_str("HIGH") == Priority.HIGH
        assert Priority.from_str("low") == Priority.LOW

    def test_from_str_int(self):
        from reymen.kanban import Priority
        assert Priority.from_str(0) == Priority.CRITICAL
        assert Priority.from_str(3) == Priority.LOW

    def test_from_str_priority_obj(self):
        from reymen.kanban import Priority
        assert Priority.from_str(Priority.MEDIUM) == Priority.MEDIUM

    def test_from_str_aliases(self):
        from reymen.kanban import Priority
        assert Priority.from_str("URGENT") == Priority.CRITICAL
        assert Priority.from_str("BLOCKER") == Priority.CRITICAL
        assert Priority.from_str("NORMAL") == Priority.MEDIUM
        assert Priority.from_str("TRIVIAL") == Priority.LOW

    def test_from_str_invalid(self):
        from reymen.kanban import Priority
        with pytest.raises(ValueError):
            Priority.from_str("INVALID_PRIORITY")

    def test_str_representation(self):
        from reymen.kanban import Priority
        assert str(Priority.HIGH) == "HIGH"
        assert str(Priority.BACKLOG) == "BACKLOG"


class TestCardStatus:
    def test_gecerli_mi_valid(self):
        from reymen.kanban import CardStatus
        assert CardStatus.gecerli_mi("backlog", "todo") is True
        assert CardStatus.gecerli_mi("in_progress", "blocked") is True
        assert CardStatus.gecerli_mi("review", "done") is True

    def test_gecerli_mi_invalid(self):
        from reymen.kanban import CardStatus
        assert CardStatus.gecerli_mi("backlog", "in_progress") is False
        assert CardStatus.gecerli_mi("done", "todo") is False

    def test_gecerli_mi_unknown_source(self):
        from reymen.kanban import CardStatus
        assert CardStatus.gecerli_mi("unknown", "todo") is False


class TestCard:
    def test_card_defaults(self):
        from reymen.kanban import Card
        c = Card(title="Test Kart")
        assert c.title == "Test Kart"
        assert c.status == "backlog"
        assert len(c.id) == 12

    def test_card_touch(self):
        from reymen.kanban import Card
        c = Card(title="Dokunma Testi")
        old = c.updated_at
        import time; time.sleep(0.01)
        c.touch()
        assert c.updated_at > old

    def test_is_overdue_no_deadline(self):
        from reymen.kanban import Card
        c = Card(title="Surek Yok")
        assert c.is_overdue() is False

    def test_is_overdue_past(self):
        from reymen.kanban import Card
        c = Card(title="Gecikmis", deadline="2020-01-01T00:00:00+00:00")
        assert c.is_overdue() is True

    def test_is_overdue_future(self):
        from reymen.kanban import Card
        c = Card(title="Gelecek", deadline="2099-12-31T23:59:59+00:00")
        assert c.is_overdue() is False

    def test_add_comment(self):
        from reymen.kanban import Card
        c = Card(title="Yorum Testi")
        entry = c.add_comment("worker1", "Bu bir yorum")
        assert entry["author"] == "worker1"
        assert entry["body"] == "Bu bir yorum"
        assert len(c.comment_thread) == 1

    def test_add_heartbeat(self):
        from reymen.kanban import Card
        c = Card(title="Heartbeat Testi")
        hb = c.add_heartbeat("calisiyor", "test mesaji")
        assert hb["status"] == "calisiyor"
        assert hb["message"] == "test mesaji"
        assert len(c.heartbeats) == 1

    def test_start_run(self):
        from reymen.kanban import Card
        c = Card(title="Run Testi")
        run = c.start_run("worker_1")
        assert run.worker == "worker_1"
        assert run.outcome == "running"
        assert len(c.runs) == 1

    def test_end_run(self):
        from reymen.kanban import Card
        c = Card(title="Run Bitis")
        c.start_run("worker_1")
        c.end_run("completed", summary="is bitti")
        assert c.runs[-1].outcome == "completed"
        assert c.runs[-1].summary == "is bitti"
        assert c.summary == "is bitti"

    def test_end_run_no_runs(self):
        from reymen.kanban import Card
        c = Card(title="Runsuz")
        # Should not raise
        c.end_run("completed")

    def test_as_dict(self):
        from reymen.kanban import Card, Priority
        c = Card(title="Dict Testi", priority=Priority.LOW)
        d = c.as_dict()
        assert d["title"] == "Dict Testi"
        assert d["priority"] == 3
        assert d["priority_name"] == "LOW"
        assert "runs" in d

    def test_from_dict(self):
        from reymen.kanban import Card
        d = {
            "title": "From Dict",
            "id": "abc123",
            "priority": 1,
            "status": "in_progress",
            "runs": [],
            "tags": [],
            "parents": [],
            "children": [],
            "heartbeats": [],
            "comment_thread": [],
            "metadata": {},
            "order": 0,
        }
        c = Card.from_dict(d)
        assert c.title == "From Dict"
        assert c.id == "abc123"
        assert c.priority.name == "HIGH"


class TestColumn:
    def test_add_card(self):
        from reymen.kanban import Column, Card
        col = Column(name="backlog")
        c = Card(title="Test")
        col.add(c)
        assert len(col.cards) == 1
        assert col.cards[0].title == "Test"

    def test_add_wip_limit(self):
        from reymen.kanban import Column, Card
        col = Column(name="wip_test", wip_limit=1)
        col.add(Card(title="Ilk"))
        with pytest.raises(ValueError, match="WIP"):
            col.add(Card(title="Ikinci"))

    def test_remove_card(self):
        from reymen.kanban import Column, Card
        col = Column(name="test")
        c = Card(title="Silinecek")
        col.add(c)
        removed = col.remove(c.id)
        assert removed is not None
        assert removed.title == "Silinecek"
        assert len(col.cards) == 0

    def test_remove_nonexistent(self):
        from reymen.kanban import Column
        col = Column(name="test")
        assert col.remove("yok") is None

    def test_get_card(self):
        from reymen.kanban import Column, Card
        col = Column(name="test")
        c = Card(title="Bulunacak")
        col.add(c)
        assert col.get(c.id).title == "Bulunacak"

    def test_get_nonexistent(self):
        from reymen.kanban import Column
        col = Column(name="test")
        assert col.get("yok") is None

    def test_sort_by_priority(self):
        from reymen.kanban import Column, Card, Priority
        col = Column(name="test")
        col.add(Card(title="Dusuk", priority=Priority.LOW))
        col.add(Card(title="Yuksek", priority=Priority.CRITICAL))
        col.add(Card(title="Orta", priority=Priority.MEDIUM))
        col.sort_by_priority()
        assert col.cards[0].title == "Yuksek"
        assert col.cards[1].title == "Orta"
        assert col.cards[2].title == "Dusuk"

    def test_as_dict(self):
        from reymen.kanban import Column, Card
        col = Column(name="test", wip_limit=5)
        col.add(Card(title="Kart 1"))
        d = col.as_dict()
        assert d["name"] == "test"
        assert d["wip_limit"] == 5
        assert len(d["cards"]) == 1


class TestBoard:
    def test_init_default_columns(self):
        from reymen.kanban import Board
        b = Board()
        assert len(b.columns) == 7
        assert b.columns[0].name == "backlog"
        assert b.columns[-1].name == "done"

    def test_add_column(self, board):
        board.add_column("test_kolon", wip_limit=3)
        col = board.get_column("test_kolon")
        assert col is not None
        assert col.wip_limit == 3

    def test_add_column_duplicate(self, board):
        with pytest.raises(ValueError, match="zaten var"):
            board.add_column("backlog")

    def test_remove_column(self, board):
        board.add_column("gecici")
        assert board.remove_column("gecici") is True
        assert board.get_column("gecici") is None

    def test_remove_nonexistent_column(self, board):
        assert board.remove_column("yok") is False

    def test_add_card(self, board):
        from reymen.kanban import Card
        c = Card(title="Yeni Kart")
        board.add(c, "backlog")
        assert board.find(c.id) is not None
        assert c.status == "backlog"

    def test_add_card_invalid_column(self, board):
        from reymen.kanban import Card
        c = Card(title="Hatali")
        with pytest.raises(ValueError, match="bulunamad"):
            board.add(c, "yok_kolon")

    def test_move_card(self, board):
        from reymen.kanban import Card
        c = Card(title="Tasinacak")
        board.add(c, "backlog")
        board.move(c.id, "todo")
        assert board.find(c.id).status == "todo"

    def test_move_same_column(self, board):
        from reymen.kanban import Card
        c = Card(title="Ayni")
        board.add(c, "backlog")
        board.move(c.id, "backlog")
        assert board.find(c.id).status == "backlog"

    def test_move_invalid_transition(self, board):
        from reymen.kanban import Card
        c = Card(title="Gecersiz")
        board.add(c, "backlog")
        with pytest.raises(ValueError, match="Geçersiz durum"):
            board.move(c.id, "in_progress")

    def test_move_nonexistent_card(self, board):
        with pytest.raises(ValueError, match="bulunamad"):
            board.move("yok_id", "todo")

    def test_set_status(self, board):
        from reymen.kanban import Card
        c = Card(title="Durum Testi")
        board.add(c, "backlog")
        board.set_status(c.id, "ready")
        assert board.find(c.id).status == "ready"

    def test_prioritize(self, board):
        from reymen.kanban import Card, Priority
        c = Card(title="Oncelik Testi", priority=Priority.MEDIUM)
        board.add(c, "backlog")
        board.prioritize(c.id, Priority.CRITICAL)
        assert board.find(c.id).priority == Priority.CRITICAL

    def test_prioritize_nonexistent(self, board):
        from reymen.kanban import Priority
        with pytest.raises(ValueError):
            board.prioritize("yok", Priority.HIGH)

    def test_set_deadline(self, board):
        from reymen.kanban import Card
        c = Card(title="Deadline Testi")
        board.add(c, "backlog")
        board.set_deadline(c.id, "2099-12-31")
        assert board.find(c.id).deadline == "2099-12-31"

    def test_set_deadline_nonexistent(self, board):
        with pytest.raises(ValueError):
            board.set_deadline("yok", "2099-01-01")

    def test_find_nonexistent(self, board):
        assert board.find("yok_id") is None

    def test_all_cards(self, board):
        from reymen.kanban import Card
        board.add(Card(title="Kart1"), "backlog")
        board.add(Card(title="Kart2"), "todo")
        board.add(Card(title="Kart3"), "done")
        assert len(board.all_cards()) == 3

    def test_overdue_cards(self, board):
        from reymen.kanban import Card
        board.add(Card(title="Gecikmis", deadline="2020-01-01T00:00:00+00:00"), "backlog")
        board.add(Card(title="Gelecek", deadline="2099-12-31T00:00:00+00:00"), "todo")
        overdue = board.overdue_cards()
        assert len(overdue) == 1
        assert overdue[0].title == "Gecikmis"

    def test_cards_by_assignee(self, board):
        from reymen.kanban import Card
        board.add(Card(title="Ali'nin Karti", assignee="ali"), "in_progress")
        board.add(Card(title="Veli'nin Karti", assignee="veli"), "todo")
        board.add(Card(title="Ali'nin Bittigi", assignee="ali", status="done"), "done")
        ali_cards = board.cards_by_assignee("ali")
        assert len(ali_cards) == 1
        assert ali_cards[0].title == "Ali'nin Karti"

    def test_claim(self, board):
        from reymen.kanban import Card
        c = Card(title="Ustlenilecek")
        board.add(c, "ready")
        board.claim(c.id, "worker_1")
        card = board.find(c.id)
        assert card.assignee == "worker_1"
        assert card.status == "in_progress"

    def test_claim_nonexistent(self, board):
        with pytest.raises(ValueError):
            board.claim("yok", "worker_1")

    def test_claim_already_assigned(self, board):
        from reymen.kanban import Card
        c = Card(title="Zaten Atanmis", assignee="ali")
        board.add(c, "ready")
        with pytest.raises(ValueError, match="zaten"):
            board.claim(c.id, "veli")

    def test_complete(self, board):
        from reymen.kanban import Card
        c = Card(title="Tamamlanacak")
        board.add(c, "in_progress")
        board.complete(c.id, summary="bitti", metadata={"files": ["x.py"]})
        card = board.find(c.id)
        assert card.status == "done"
        assert card.metadata.get("files") == ["x.py"]

    def test_block(self, board):
        from reymen.kanban import Card
        c = Card(title="Bloklanacak")
        board.add(c, "in_progress")
        board.block(c.id, "dis bagimlilik")
        card = board.find(c.id)
        assert card.status == "blocked"
        assert card.metadata.get("block_reason") == "dis bagimlilik"

    def test_unblock(self, board):
        from reymen.kanban import Card
        c = Card(title="Unblock")
        board.add(c, "in_progress")
        board.block(c.id, "sebep")
        board.unblock(c.id)
        assert board.find(c.id).status == "in_progress"

    def test_unblock_not_blocked(self, board):
        from reymen.kanban import Card
        c = Card(title="Bloke Degil")
        board.add(c, "backlog")
        with pytest.raises(ValueError, match="bloke durumunda de"):
            board.unblock(c.id)

    def test_comment(self, board):
        from reymen.kanban import Card
        c = Card(title="Yorum")
        board.add(c, "backlog")
        entry = board.comment(c.id, "worker", "test yorum")
        assert entry["author"] == "worker"

    def test_heartbeat(self, board):
        from reymen.kanban import Card
        c = Card(title="HB")
        board.add(c, "in_progress")
        hb = board.heartbeat(c.id, "worker", "calisiyor")
        assert hb["status"] == "worker"

    def test_link_parent_child(self, board):
        from reymen.kanban import Card
        parent = Card(title="Parent")
        child = Card(title="Child")
        board.add(parent, "backlog")
        board.add(child, "todo")
        board.link(parent.id, child.id)
        assert child.id in parent.children
        assert parent.id in child.parents

    def test_link_nonexistent(self, board):
        from reymen.kanban import Card
        p = Card(title="P")
        board.add(p, "backlog")
        with pytest.raises(ValueError):
            board.link(p.id, "yok_child")

    def test_query_status(self, board):
        from reymen.kanban import Card
        board.add(Card(title="A"), "backlog")
        board.add(Card(title="B"), "done")
        board.add(Card(title="C"), "done")
        done_cards = board.query(status="done")
        assert len(done_cards) == 2

    def test_query_assignee(self, board):
        from reymen.kanban import Card
        board.add(Card(title="A", assignee="ali"), "in_progress")
        board.add(Card(title="B", assignee="veli"), "todo")
        assert len(board.query(assignee="ali")) == 1

    def test_query_tag(self, board):
        from reymen.kanban import Card
        board.add(Card(title="A", tags=["bug"]), "todo")
        board.add(Card(title="B", tags=["feature"]), "todo")
        assert len(board.query(tag="bug")) == 1

    def test_query_overdue(self, board):
        from reymen.kanban import Card
        board.add(Card(title="Gec", deadline="2020-01-01T00:00:00+00:00"), "todo")
        board.add(Card(title="Guncel"), "todo")
        assert len(board.query(overdue=True)) == 1

    def test_summary(self, board):
        from reymen.kanban import Card
        board.add(Card(title="Test"), "backlog")
        s = board.summary()
        assert s["name"] == "Test Pano"
        assert s["total_cards"] == 1
        assert "backlog" in s["columns"]

    def test_as_dict(self, board):
        from reymen.kanban import Card
        board.add(Card(title="Test"), "backlog")
        d = board.as_dict()
        assert d["name"] == "Test Pano"
        assert len(d["columns"]) == 7

    def test_to_json(self, board):
        from reymen.kanban import Card
        board.add(Card(title="Test"), "backlog")
        js = board.to_json()
        parsed = json.loads(js)
        assert parsed["name"] == "Test Pano"

    def test_save_and_load(self, board, tmp_path):
        from reymen.kanban import Card
        board.add(Card(title="Kayit Testi"), "backlog")
        p = tmp_path / "test_board.json"
        board.save(p)
        assert p.exists()
        from reymen.kanban import Board
        loaded = Board.load(p)
        assert loaded.name == "Test Pano"
        assert len(loaded.all_cards()) == 1

    def test_from_dict(self):
        from reymen.kanban import Board
        data = {
            "name": "Yuklenen Pano",
            "columns": [
                {"name": "backlog", "wip_limit": None, "cards": []},
                {"name": "done", "wip_limit": None, "cards": []},
            ]
        }
        b = Board.from_dict(data)
        assert b.name == "Yuklenen Pano"
        assert len(b.columns) == 2

    def test_auto_promote_children(self, board):
        """Kart DONE oldugunda child'lar otomatik ready'e alinmali."""
        from reymen.kanban import Card
        parent = Card(title="Parent")
        child = Card(title="Child")
        board.add(parent, "in_progress")
        board.add(child, "todo")
        board.link(parent.id, child.id)
        board.complete(parent.id, summary="tamam")
        # child should be promoted from todo to ready
        assert board.find(child.id).status == "ready"
