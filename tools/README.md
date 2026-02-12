# Tools Module

## Purpose
`tools/` contains LangChain-compatible tools used by agents and scripts.

Implemented tools:
- `search_tool.py` -> `SearchNewsTool`
- `database_tool.py` -> `DatabaseTool`
- `function_tools/summarize_tool.py` -> `SummarizeTool`

## LangChain Standards
Each tool should:
- Inherit from `tools.base_tool.BaseTool`
- Define `name`, `description`, `args_schema`
- Implement `_run(...)`
- Be executed with `.invoke({...})`

## Output Contract
Return only JSON-serializable values:
- `dict`, `list`, `str`, `int`, `float`, `bool`, `None`

This makes tool outputs safe for:
- Agent tool routing
- Logging/tracing
- Protocol handoff

## Example
```python
from tools.search_tool import SearchNewsTool

tool = SearchNewsTool()
articles = tool.invoke({"query": "MSFT", "limit": 3})
```

## Testing
Add one test file per tool in `tests/`:
- Validate schema and input errors.
- Validate output shape.
- Use dependency injection/mocks for network calls.
