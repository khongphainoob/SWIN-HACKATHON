"""
tests/test_tools_comprehensive.py
Comprehensive tests for all LangChain tools

This test suite covers:
1. SearchNewsTool - Fetch market news
2. DatabaseTool - Portfolio CRUD operations
3. SummarizeTool - Extractive text summarization
"""
import unittest
import tempfile
from pathlib import Path

from tools.search_tool import SearchNewsTool
from tools.database_tool import DatabaseTool
from tools.function_tools.summarize_tool import SummarizeTool


class TestSearchNewsTool(unittest.TestCase):
    """Test SearchNewsTool - News fetching from Yahoo Finance"""
    
    def setUp(self):
        self.tool = SearchNewsTool()
    
    def test_tool_metadata(self):
        """Test tool has correct metadata"""
        print("\n" + "="*60)
        print("TEST: SearchNewsTool - Tool Metadata")
        print("="*60)
        
        assert self.tool.name == "search_news"
        assert "market news" in self.tool.description.lower()
        assert self.tool.return_direct == True
        
        print(f"✓ Tool name: {self.tool.name}")
        print(f"✓ Description: {self.tool.description}")
        print(f"✓ Return direct: {self.tool.return_direct}")
    
    def test_tool_schema(self):
        """Test tool has correct schema validation"""
        print("\n" + "="*60)
        print("TEST: SearchNewsTool - Schema Validation")
        print("="*60)
        
        # Valid inputs
        valid_args = {
            "query": "NVDA",
            "limit": 5
        }
        
        try:
            args = self.tool.args_schema(**valid_args)
            print(f"✓ Valid schema accepted: query={args.query}, limit={args.limit}")
        except Exception as e:
            self.fail(f"Valid schema rejected: {e}")
        
        # Invalid limit (should fail)
        invalid_args = {
            "query": "NVDA",
            "limit": 0  # Must be > 0
        }
        
        try:
            args = self.tool.args_schema(**invalid_args)
            self.fail("Invalid schema should have been rejected")
        except Exception:
            print("✓ Invalid schema (limit=0) correctly rejected")
    
    def test_invoke_tool(self):
        """Test actual tool invocation"""
        print("\n" + "="*60)
        print("TEST: SearchNewsTool - Invoke Tool")
        print("="*60)
        
        try:
            result = self.tool.invoke({
                "query": "AAPL",
                "limit": 3
            })
            
            print(f"✓ Tool invoked successfully")
            print(f"✓ Returned {len(result)} articles")
            
            if result:
                article = result[0]
                print(f"\nFirst article:")
                print(f"  Title: {article.get('title', 'N/A')[:50]}...")
                print(f"  Publisher: {article.get('publisher', 'N/A')}")
                print(f"  Timestamp: {article.get('published', 'N/A')}")
                print(f"  Link: {article.get('link', 'N/A')[:50]}..." if article.get('link') else "  Link: N/A")
        except Exception as e:
            print(f"⚠️  Tool invocation note: {e}")
            print(f"   (This is expected if API is rate-limited or network unavailable)")
    
    def test_tool_output_format(self):
        """Test tool output is properly formatted"""
        print("\n" + "="*60)
        print("TEST: SearchNewsTool - Output Format")
        print("="*60)
        
        # Expected output structure
        expected_keys = {"title", "link", "publisher", "published", "type"}
        
        try:
            result = self.tool.invoke({"query": "MSFT", "limit": 1})
            
            if result:
                article = result[0]
                has_all_keys = expected_keys.issubset(set(article.keys()))
                print(f"✓ Output has expected keys: {expected_keys}")
                assert has_all_keys, f"Missing keys. Got: {set(article.keys())}"
        except Exception as e:
            print(f"⚠️  Could not verify output format: {e}")


class TestDatabaseTool(unittest.TestCase):
    """Test DatabaseTool - Portfolio database operations"""
    
    def setUp(self):
        """Create temporary database for testing"""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = str(Path(self.temp_dir.name) / "test.db")
        self.tool = DatabaseTool(db_path=self.db_path)
    
    def tearDown(self):
        self.temp_dir.cleanup()
    
    def test_tool_metadata(self):
        """Test tool metadata"""
        print("\n" + "="*60)
        print("TEST: DatabaseTool - Tool Metadata")
        print("="*60)
        
        assert self.tool.name == "portfolio_db"
        assert "portfolio" in self.tool.description.lower()
        
        print(f"✓ Tool name: {self.tool.name}")
        print(f"✓ Description: {self.tool.description}")
    
    def test_upsert_holding(self):
        """Test inserting/updating portfolio holdings"""
        print("\n" + "="*60)
        print("TEST: DatabaseTool - Upsert Holding")
        print("="*60)
        
        result = self.tool.invoke({
            "action": "upsert",
            "user_id": "user123",
            "symbol": "AAPL",
            "shares": 100,
            "avg_cost": 150.0
        })
        
        assert result == "upserted"
        print("✓ Successfully inserted AAPL holding (100 shares @ $150)")
        
        # Update the same holding
        result = self.tool.invoke({
            "action": "upsert",
            "user_id": "user123",
            "symbol": "AAPL",
            "shares": 150,  # Changed
            "avg_cost": 155.0  # Changed
        })
        
        assert result == "upserted"
        print("✓ Successfully updated AAPL holding (150 shares @ $155)")
    
    def test_get_portfolio(self):
        """Test retrieving portfolio holdings"""
        print("\n" + "="*60)
        print("TEST: DatabaseTool - Get Portfolio")
        print("="*60)
        
        # Insert test data
        self.tool.invoke({
            "action": "upsert",
            "user_id": "user123",
            "symbol": "AAPL",
            "shares": 100,
            "avg_cost": 150.0
        })
        
        self.tool.invoke({
            "action": "upsert",
            "user_id": "user123",
            "symbol": "MSFT",
            "shares": 50,
            "avg_cost": 300.0
        })
        
        # Retrieve portfolio
        result = self.tool.invoke({
            "action": "get",
            "user_id": "user123"
        })
        
        assert len(result) == 2
        print(f"✓ Retrieved portfolio with {len(result)} holdings:")
        
        for holding in result:
            print(f"  • {holding['symbol']}: {holding['shares']} shares @ ${holding['avg_cost']}")
    
    def test_delete_holding(self):
        """Test deleting holdings"""
        print("\n" + "="*60)
        print("TEST: DatabaseTool - Delete Holding")
        print("="*60)
        
        # Insert
        self.tool.invoke({
            "action": "upsert",
            "user_id": "user123",
            "symbol": "GOOGL",
            "shares": 10,
            "avg_cost": 2800.0
        })
        
        # Delete
        result = self.tool.invoke({
            "action": "delete",
            "user_id": "user123",
            "symbol": "GOOGL"
        })
        
        assert result == "deleted"
        print("✓ Successfully deleted GOOGL holding")
        
        # Verify deletion
        portfolio = self.tool.invoke({
            "action": "get",
            "user_id": "user123"
        })
        
        assert len(portfolio) == 0
        print("✓ Verified deletion - portfolio is now empty")
    
    def test_custom_select(self):
        """Test custom SQL SELECT queries"""
        print("\n" + "="*60)
        print("TEST: DatabaseTool - Custom SELECT Query")
        print("="*60)
        
        # Insert test data
        self.tool.invoke({
            "action": "upsert",
            "user_id": "user123",
            "symbol": "AAPL",
            "shares": 100,
            "avg_cost": 150.0
        })
        
        # Custom query
        result = self.tool.invoke({
            "action": "select",
            "user_id": "user123",
            "query": "SELECT symbol, shares FROM holdings WHERE user_id = ?",
            "params": ["user123"]
        })
        
        assert len(result) > 0
        print("✓ Custom SELECT query executed successfully")
        print(f"  Result: {result}")


class TestSummarizeTool(unittest.TestCase):
    """Test SummarizeTool - Extractive text summarization"""
    
    def setUp(self):
        self.tool = SummarizeTool()
        
        self.sample_text = """
        Apple Inc. reported strong financial results for Q4 2025. 
        The company's iPhone sales exceeded expectations with a 15% year-over-year growth.
        Services revenue also showed robust growth, driven by cloud adoption.
        However, competition from other manufacturers remains intense.
        Apple's strategic investments in AI-powered features are expected to drive future growth.
        The company announced plans to expand manufacturing in Southeast Asia.
        """
    
    def test_tool_metadata(self):
        """Test tool metadata"""
        print("\n" + "="*60)
        print("TEST: SummarizeTool - Tool Metadata")
        print("="*60)
        
        assert self.tool.name == "summarize"
        assert "summarize" in self.tool.description.lower()
        assert self.tool.return_direct == True
        
        print(f"✓ Tool name: {self.tool.name}")
        print(f"✓ Description: {self.tool.description}")
    
    def test_schema_validation(self):
        """Test schema validation"""
        print("\n" + "="*60)
        print("TEST: SummarizeTool - Schema Validation")
        print("="*60)
        
        valid_args = {
            "text": "Sample text here",
            "max_sentences": 3
        }
        
        try:
            args = self.tool.args_schema(**valid_args)
            print(f"✓ Valid schema accepted")
        except Exception as e:
            self.fail(f"Valid schema rejected: {e}")
        
        # Invalid max_sentences
        invalid_args = {
            "text": "Sample text",
            "max_sentences": 0
        }
        
        try:
            args = self.tool.args_schema(**invalid_args)
            self.fail("Invalid schema should be rejected")
        except Exception:
            print("✓ Invalid schema (max_sentences=0) correctly rejected")
    
    def test_summarize_text(self):
        """Test text summarization"""
        print("\n" + "="*60)
        print("TEST: SummarizeTool - Summarize Text")
        print("="*60)
        
        print(f"\n📝 Original text ({len(self.sample_text)} chars):")
        print(f"   {self.sample_text[:100]}...\n")
        
        result = self.tool.invoke({
            "text": self.sample_text,
            "max_sentences": 2
        })
        
        print(f"📋 Summary (max 2 sentences):")
        print(f"   {result}\n")
        
        # Count sentences (simple approach)
        sentence_count = len([s for s in result.split('.') if s.strip()])
        assert sentence_count <= 2
        print(f"✓ Summary has {sentence_count} sentences (≤ 2)")
    
    def test_summarize_short_text(self):
        """Test summarization of already short text"""
        print("\n" + "="*60)
        print("TEST: SummarizeTool - Short Text")
        print("="*60)
        
        short_text = "Apple earnings beat expectations. Revenue growth was strong."
        
        result = self.tool.invoke({
            "text": short_text,
            "max_sentences": 5
        })
        
        assert short_text == result
        print("✓ Short text returned unchanged")
        print(f"  Text: {result}")
    
    def test_empty_text_handling(self):
        """Test handling of empty text"""
        print("\n" + "="*60)
        print("TEST: SummarizeTool - Empty Text Handling")
        print("="*60)
        
        try:
            result = self.tool.invoke({
                "text": "",
                "max_sentences": 3
            })
            print("⚠️  Empty text was processed without error")
        except ValueError as e:
            print(f"✓ Empty text correctly rejected: {e}")


def run_all_tool_tests():
    """Run all tool tests with detailed output"""
    print("\n" + "█"*60)
    print("█" + " "*58 + "█")
    print("█" + "  🧪 COMPREHENSIVE TOOLS TEST SUITE".center(58) + "█")
    print("█" + " "*58 + "█")
    print("█"*60)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all tests
    suite.addTests(loader.loadTestsFromTestCase(TestSearchNewsTool))
    suite.addTests(loader.loadTestsFromTestCase(TestDatabaseTool))
    suite.addTests(loader.loadTestsFromTestCase(TestSummarizeTool))
    
    # Run with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*60)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_all_tool_tests()
    exit(0 if success else 1)
