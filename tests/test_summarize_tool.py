import unittest

from tools.function_tools.summarize_tool import SummarizeTool


class SummarizeToolTestCase(unittest.TestCase):
    def test_summary_limits_sentences(self):
        text = (
            "Stocks rallied today after inflation cooled. "
            "Investors cheered the news. "
            "Analysts expect rate cuts soon. "
            "Some remain cautious about earnings."
        )
        tool = SummarizeTool()
        summary = tool.invoke({"text": text, "max_sentences": 2})
        self.assertLessEqual(len(summary.split(". ")), 2)
        self.assertIn("Stocks rallied today", summary)

    def test_short_text_returns_original(self):
        text = "Markets were flat."
        tool = SummarizeTool()
        summary = tool.invoke({"text": text, "max_sentences": 3})
        self.assertEqual(summary, text)


if __name__ == "__main__":
    unittest.main()
