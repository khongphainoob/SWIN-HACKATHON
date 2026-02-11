import unittest

from services.vector_store_service import TfidfVectorStore


class VectorStoreServiceTestCase(unittest.TestCase):
    def test_add_and_query(self):
        store = TfidfVectorStore()
        texts = [
            "Apple shares rose after strong earnings.",
            "Tesla faces production challenges.",
            "Federal Reserve hints at rate cuts.",
        ]
        store.add_texts(texts, ids=["a", "t", "f"])
        results = store.similarity_search("earnings at Apple", k=1)
        self.assertEqual(results[0].id, "a")

    def test_empty_store_query(self):
        store = TfidfVectorStore()
        self.assertEqual(store.similarity_search("anything"), [])


if __name__ == "__main__":
    unittest.main()
