import datetime as dt
import json
import tempfile
import unittest
from pathlib import Path
from outlook_cleaner import classify, load_config, sender_matches

NOW = dt.datetime(2026, 11, 8, tzinfo=dt.timezone.utc)

def msg(sender="news@shop.pl", subject="Newsletter promocja", days=20, preview=""):
    return {"subject": subject, "bodyPreview": preview, "receivedDateTime": (NOW - dt.timedelta(days=days)).isoformat(), "from": {"emailAddress": {"address": sender}}}

class RulesTests(unittest.TestCase):
    def setUp(self):
        self.config = {"protected_senders": ["boss@firm.pl"], "protected_domains": ["bank.pl"], "protected_keywords": ["pilne"], "blocked_senders": ["news@shop.pl"], "blocked_domains": ["ads.example.com"], "blocked_keywords": ["oferta dnia"], "min_age_days": 7, "max_moves": 25, "use_default_marketing_rules": True}
    def test_block_sender(self):
        self.assertEqual(classify(msg(subject="Cześć"), self.config, NOW), "wybrany nadawca")
    def test_protect_overrides_block(self):
        self.assertIsNone(classify(msg(subject="Faktura i promocja"), self.config, NOW))
    def test_protect_sender(self):
        self.assertIsNone(classify(msg(sender="boss@firm.pl"), self.config, NOW))
    def test_protect_domain_subdomain(self):
        self.assertIsNone(classify(msg(sender="a@alerts.bank.pl"), self.config, NOW))
    def test_not_fake_domain(self):
        self.assertFalse(sender_matches("a@notbank.pl", [], ["bank.pl"]))
    def test_min_age(self):
        self.assertIsNone(classify(msg(days=2), self.config, NOW))
    def test_keyword(self):
        self.assertEqual(classify(msg(sender="x@other.pl", subject="Oferta dnia"), self.config, NOW), "własne słowo kluczowe")
    def test_missing_date_protected(self):
        m = msg(); del m["receivedDateTime"]
        self.assertIsNone(classify(m, self.config, NOW))
    def test_disable_default(self):
        self.config["use_default_marketing_rules"] = False
        self.assertIsNone(classify(msg(sender="x@other.pl"), self.config, NOW))
    def test_config_validation(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "config.json"
            path.write_text(json.dumps({"blocked_senders": ["a@b.pl"], "min_age_days": 3}), encoding="utf-8")
            self.assertEqual(load_config(path)["min_age_days"], 3)
            path.write_text(json.dumps({"max_moves": -1}), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_config(path)
            path.write_text(json.dumps({"blocked_senders": "any"}), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_config(path)

if __name__ == "__main__":
    unittest.main()
