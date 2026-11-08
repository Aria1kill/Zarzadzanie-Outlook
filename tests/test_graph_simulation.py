"""Offline integration checks: Microsoft Graph is mocked, no mailbox is touched."""
import argparse
import contextlib
import datetime as dt
import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import outlook_cleaner

class GraphSimulationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.config = Path(self.tmp.name) / "config.json"
        self.config.write_text(json.dumps({
            "blocked_senders": ["ads@example.com"], "min_age_days": 7,
            "max_moves": 25, "use_default_marketing_rules": False
        }), encoding="utf-8")
        when = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=20)).isoformat()
        def message(identifier, sender, subject):
            return {"id": identifier, "subject": subject, "bodyPreview": "",
                    "receivedDateTime": when,
                    "from": {"emailAddress": {"address": sender}}}
        self.messages = [message("1", "ads@example.com", "Promocja"),
                         message("2", "ads@example.com", "Faktura"),
                         message("3", "friend@example.com", "Cześć")]
    def args(self, apply=False, yes=False, limit=None):
        return argparse.Namespace(config=str(self.config), max_moves=limit,
                                  apply=apply, yes=yes, demo=False)
    def test_dry_run_never_moves(self):
        with patch.dict(os.environ, {"OUTLOOK_CLIENT_ID": "fake"}), \
             patch.object(outlook_cleaner, "authenticate", return_value="fake"), \
             patch.object(outlook_cleaner, "graph_request", return_value={"value": self.messages}) as request, \
             contextlib.redirect_stdout(io.StringIO()):
            outlook_cleaner.run(self.args())
        self.assertEqual(request.call_count, 1)
        self.assertEqual(request.call_args.args[0], "GET")
    def test_apply_moves_only_matching_message(self):
        calls = []
        def fake_request(method, url, token, **kwargs):
            calls.append((method, url, kwargs))
            if method == "GET":
                return {"value": self.messages}
            return {}
        with patch.dict(os.environ, {"OUTLOOK_CLIENT_ID": "fake"}), \
             patch.object(outlook_cleaner, "authenticate", return_value="fake"), \
             patch.object(outlook_cleaner, "graph_request", side_effect=fake_request), \
             contextlib.redirect_stdout(io.StringIO()):
            outlook_cleaner.run(self.args(apply=True, yes=True))
        posts = [c for c in calls if c[0] == "POST"]
        self.assertEqual(len(posts), 1)
        self.assertTrue(posts[0][1].endswith("/1/move"))
        self.assertEqual(posts[0][2]["json"]["destinationId"], "deleteditems")
    def test_apply_requires_explicit_confirmation(self):
        with self.assertRaises(ValueError):
            outlook_cleaner.run(self.args(apply=True))
    def test_limit_prevents_excessive_moves(self):
        self.messages.insert(0, dict(self.messages[0], id="0"))
        calls = []
        def fake_request(method, url, token, **kwargs):
            calls.append(method)
            return {"value": self.messages} if method == "GET" else {}
        with patch.dict(os.environ, {"OUTLOOK_CLIENT_ID": "fake"}), \
             patch.object(outlook_cleaner, "authenticate", return_value="fake"), \
             patch.object(outlook_cleaner, "graph_request", side_effect=fake_request), \
             contextlib.redirect_stdout(io.StringIO()):
            outlook_cleaner.run(self.args(apply=True, yes=True, limit=1))
        self.assertEqual(calls.count("POST"), 1)

if __name__ == "__main__":
    unittest.main()
