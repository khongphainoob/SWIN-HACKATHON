"""Unit tests for SQLite portfolio database tool operations."""

import tempfile
import unittest
from pathlib import Path

from tools.database_tool import DatabaseTool


class DatabaseToolTestCase(unittest.TestCase):
    """Validates CRUD behavior exposed by ``DatabaseTool``."""

    def setUp(self):
        """Create an isolated temporary database per test."""
        self.tmpdir = tempfile.TemporaryDirectory()
        db_path = Path(self.tmpdir.name) / "portfolio.db"
        self.tool = DatabaseTool(str(db_path))

    def tearDown(self):
        """Dispose temporary database resources."""
        self.tmpdir.cleanup()

    def test_upsert_and_get(self):
        """Upserted holding should be retrievable for the same user."""
        self.tool.invoke({"action": "upsert", "user_id": "user1", "symbol": "AAPL", "shares": 10, "avg_cost": 150.0})
        holdings = self.tool.invoke({"action": "get", "user_id": "user1"})
        self.assertEqual(len(holdings), 1)
        self.assertEqual(holdings[0]["symbol"], "AAPL")
        self.assertEqual(holdings[0]["shares"], 10)

    def test_delete(self):
        """Deleting a holding should remove it from user portfolio results."""
        self.tool.invoke({"action": "upsert", "user_id": "user1", "symbol": "TSLA", "shares": 5, "avg_cost": 200.0})
        self.tool.invoke({"action": "delete", "user_id": "user1", "symbol": "TSLA"})
        holdings = self.tool.invoke({"action": "get", "user_id": "user1"})
        self.assertEqual(holdings, [])


if __name__ == "__main__":
    unittest.main()
