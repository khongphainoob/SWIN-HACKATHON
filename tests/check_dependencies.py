"""
check_dependencies.py
Script to verify all required dependencies are installed correctly.

Usage:
    python check_dependencies.py
"""
import sys
from typing import List, Tuple


def check_import(module_name: str, package_name: str = None) -> Tuple[bool, str]:
    """
    Check if a module can be imported.
    
    Args:
        module_name: Name of the module to import
        package_name: Name of the package (if different from module)
    
    Returns:
        (success, message) tuple
    """
    package_name = package_name or module_name
    try:
        __import__(module_name)
        return True, f"✓ {package_name}"
    except ImportError as e:
        return False, f"✗ {package_name} - {str(e)}"


def check_all_dependencies() -> Tuple[int, int]:
    """
    Check all required dependencies.
    
    Returns:
        (passed, total) tuple
    """
    print("=" * 60)
    print("DEPENDENCY CHECK")
    print("=" * 60)
    
    # Core dependencies
    print("\n📦 Core Dependencies:")
    core_deps = [
        ("langchain_core", "langchain-core"),
        ("langgraph", "langgraph"),
        ("pydantic", "pydantic"),
        ("requests", "requests"),
        ("yaml", "PyYAML"),
    ]
    
    passed = 0
    total = 0
    
    for module, package in core_deps:
        total += 1
        success, msg = check_import(module, package)
        print(f"  {msg}")
        if success:
            passed += 1
    
    # Optional dependencies
    print("\n📦 Optional Dependencies:")
    optional_deps = [
        ("yfinance", "yfinance (for market data)"),
    ]
    
    for module, package in optional_deps:
        total += 1
        success, msg = check_import(module, package)
        print(f"  {msg}")
        if success:
            passed += 1
    
    # Testing dependencies
    print("\n🧪 Testing Dependencies:")
    test_deps = [
        ("pytest", "pytest"),
    ]
    
    for module, package in test_deps:
        total += 1
        success, msg = check_import(module, package)
        print(f"  {msg}")
        if success:
            passed += 1
    
    # Optional LLM providers
    print("\n🤖 LLM Providers (Optional):")
    llm_deps = [
        ("google.generativeai", "google-generativeai"),
        ("openai", "openai"),
        ("anthropic", "anthropic"),
    ]
    
    for module, package in llm_deps:
        success, msg = check_import(module, package)
        if success:
            print(f"  {msg}")
        else:
            print(f"  - {package} (not installed)")
    
    # Optional vector stores
    print("\n🗂️  Vector Stores (Optional):")
    vector_deps = [
        ("chromadb", "chromadb"),
        ("faiss", "faiss-cpu"),
        ("sentence_transformers", "sentence-transformers"),
    ]
    
    for module, package in vector_deps:
        success, msg = check_import(module, package)
        if success:
            print(f"  {msg}")
        else:
            print(f"  - {package} (not installed)")
    
    return passed, total


def check_python_version():
    """Check Python version."""
    print("\n🐍 Python Version:")
    version = sys.version_info
    print(f"  {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print("  ⚠️  Warning: Python 3.10+ recommended")
    else:
        print("  ✓ Version OK")


def check_project_structure():
    """Check if key project files exist."""
    import os
    from pathlib import Path
    
    print("\n📁 Project Structure:")
    
    required_dirs = [
        "agents",
        "orchestrators",
        "tools",
        "services",
        "memory",
        "data",
        "tests",
    ]
    
    all_exist = True
    for dir_name in required_dirs:
        if Path(dir_name).exists():
            print(f"  ✓ {dir_name}/")
        else:
            print(f"  ✗ {dir_name}/ (missing)")
            all_exist = False
    
    required_files = [
        "requirements.txt",
        "README.md",
        "Task.md",
    ]
    
    for file_name in required_files:
        if Path(file_name).exists():
            print(f"  ✓ {file_name}")
        else:
            print(f"  ✗ {file_name} (missing)")
            all_exist = False
    
    return all_exist


def check_langchain_core():
    """Check LangChain core functionality."""
    print("\n🔗 LangChain Core Check:")
    
    try:
        from langchain_core.tools import BaseTool
        print("  ✓ BaseTool import OK")
        
        from langchain_core.vectorstores import VectorStore
        print("  ✓ VectorStore import OK")
        
        from langchain_core.documents import Document
        print("  ✓ Document import OK")
        
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def check_langgraph():
    """Check LangGraph functionality."""
    print("\n📊 LangGraph Check:")
    
    try:
        from langgraph.graph import StateGraph, END
        print("  ✓ StateGraph import OK")
        
        from typing import TypedDict
        
        class TestState(TypedDict):
            value: int
        
        def test_node(state):
            return {"value": state.get("value", 0) + 1}
        
        graph = StateGraph(TestState)
        graph.add_node("test", test_node)
        graph.set_entry_point("test")
        graph.add_edge("test", END)
        compiled = graph.compile()
        
        result = compiled.invoke({"value": 0})
        if result.get("value") == 1:
            print("  ✓ Graph execution OK")
        else:
            print("  ✗ Graph execution failed")
        
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def main():
    """Run all checks."""
    print("\n" + "█" * 60)
    print("█" + " " * 58 + "█")
    print("█" + "  SWIN DEPENDENCY CHECKER".center(58) + "█")
    print("█" + " " * 58 + "█")
    print("█" * 60)
    
    # Python version
    check_python_version()
    
    # Project structure
    structure_ok = check_project_structure()
    
    # Dependencies
    passed, total = check_all_dependencies()
    
    # LangChain specific checks
    langchain_ok = check_langchain_core()
    langgraph_ok = check_langgraph()
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Core Dependencies: {passed}/{total} passed")
    print(f"LangChain Core: {'✓ OK' if langchain_ok else '✗ FAILED'}")
    print(f"LangGraph: {'✓ OK' if langgraph_ok else '✗ FAILED'}")
    print(f"Project Structure: {'✓ OK' if structure_ok else '✗ INCOMPLETE'}")
    
    if passed == total and langchain_ok and langgraph_ok:
        print("\n✅ All checks passed! Ready to run.")
        print("\nNext steps:")
        print("  1. Run tests: pytest tests/ -v")
        print("  2. Run demo: python demo_langgraph_workflow.py")
        return 0
    else:
        print("\n⚠️  Some checks failed. Install missing dependencies:")
        print("  pip install -r requirements.txt")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
