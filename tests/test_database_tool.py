import tempfile
import unittest
from pathlib import Path

from tools.database_tool import DatabaseTool


class DatabaseToolTestCase(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        db_path = Path(self.tmpdir.name) / "portfolio.db"
        self.tool = DatabaseTool(str(db_path))

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_upsert_and_get(self):
        self.tool.invoke({"action": "upsert", "user_id": "user1", "symbol": "AAPL", "shares": 10, "avg_cost": 150.0})
        holdings = self.tool.invoke({"action": "get", "user_id": "user1"})
        self.assertEqual(len(holdings), 1)
        self.assertEqual(holdings[0]["symbol"], "AAPL")
        self.assertEqual(holdings[0]["shares"], 10)

    def test_delete(self):
        self.tool.invoke({"action": "upsert", "user_id": "user1", "symbol": "TSLA", "shares": 5, "avg_cost": 200.0})
        self.tool.invoke({"action": "delete", "user_id": "user1", "symbol": "TSLA"})
        holdings = self.tool.invoke({"action": "get", "user_id": "user1"})
        self.assertEqual(holdings, [])


if __name__ == "__main__":
    unittest.main()
