# tools

Các công cụ thực thi như Search News, DB Query, Yahoo Finance. Được sử dụng bởi các agent để lấy dữ liệu và thực hiện tác vụ.

## Sử dụng class base để kế thừa và phát triển

Nên định nghĩa một class nền (ví dụ: `BaseTool`) để các tool chuyên biệt kế thừa và mở rộng.

### Ví dụ kế thừa
```python
from base_tool import BaseTool

class SearchNewsTool(BaseTool):
	def execute(self, query):
		# Logic tìm kiếm tin tức
		pass
```

Tạo file `base_tool.py` để định nghĩa class nền cho các tool.