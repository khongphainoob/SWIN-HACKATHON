# protocols

Quy tắc giao tiếp chuẩn hóa giữa các Agent, ví dụ MCP (Model Context Protocol), A2A (Agent-to-Agent). Đảm bảo bảo mật và mở rộng.

## Sử dụng class base để kế thừa và phát triển

Nên định nghĩa một class nền (ví dụ: `BaseProtocol`) để các protocol chuyên biệt kế thừa và mở rộng.

### Ví dụ kế thừa
```python
from base_protocol import BaseProtocol

class MCPProtocol(BaseProtocol):
	def communicate(self, message):
		# Logic giao tiếp
		pass
```

Tạo file `base_protocol.py` để định nghĩa class nền cho các protocol.