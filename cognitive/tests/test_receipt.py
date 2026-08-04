"""Tests for the shared receipt emission module."""

import json

from cognitive.config import CONFIDENCE_CAP
from cognitive.receipt import Receipt, emit_receipt


class TestReceipt:
    def test_basic_receipt(self):
        r = emit_receipt(
            module="test",
            operation="test_op",
            data={"key": "value"},
            evidence_type="OBS_CAUSAL",
            confidence=0.85,
            verdict="COMPUTED",
        )
        assert r.module == "test"
        assert r.operation == "test_op"
        assert r.confidence == 0.85
        assert r.receipt_id.startswith("rcpt-")
        assert r.timestamp  # non-empty

    def test_confidence_cap(self):
        r = emit_receipt(
            module="test",
            operation="cap_test",
            data={},
            confidence=0.99,
        )
        assert r.confidence == CONFIDENCE_CAP

    def test_is_capped(self):
        r = emit_receipt(module="t", operation="o", data={}, confidence=0.95)
        assert r.is_capped()
        r2 = emit_receipt(module="t", operation="o", data={}, confidence=0.50)
        assert not r2.is_capped()

    def test_to_json(self):
        r = emit_receipt(module="t", operation="o", data={"x": 1})
        j = r.to_json()
        parsed = json.loads(j)
        assert parsed["module"] == "t"
        assert parsed["data"]["x"] == 1

    def test_to_dict(self):
        r = emit_receipt(module="t", operation="o", data={})
        d = r.to_dict()
        assert isinstance(d, dict)
        assert "receipt_id" in d
        assert "timestamp" in d
