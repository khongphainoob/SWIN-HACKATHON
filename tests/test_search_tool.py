import unittest

from tools.search_tool import SearchNewsTool


class SearchNewsToolTestCase(unittest.TestCase):
    def test_execute_with_stub_fetcher(self):
        def stub_fetcher(query, limit):
            return [
                {"title": f"{query} news 1", "link": "http://example.com/1", "publisher": "Stub", "published": 1700000000},
                {"title": f"{query} news 2", "link": "http://example.com/2", "publisher": "Stub", "published": 1700001000},
            ][:limit]

        tool = SearchNewsTool(fetcher=stub_fetcher)
        results = tool.invoke({"query": "AAPL", "limit": 1})
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "AAPL news 1")
        self.assertTrue(results[0]["published"].endswith("Z"))

    def test_invalid_query(self):
        tool = SearchNewsTool(fetcher=lambda q, l: [])
        with self.assertRaises(ValueError):
            tool.invoke({"query": "", "limit": 1})


if __name__ == "__main__":
    unittest.main()
