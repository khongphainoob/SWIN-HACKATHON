# orchestrators

Bộ điều phối luồng tác vụ, ví dụ LangGraph State Machine. Quản lý quá trình phối hợp giữa các agent và công cụ.

## Sử dụng class base để kế thừa và phát triển

Nên định nghĩa một class nền (ví dụ: `BaseOrchestrator`) để các orchestrator chuyên biệt kế thừa và mở rộng.

### Ví dụ kế thừa
```python
from base_orchestrator import BaseOrchestrator

class LangGraphOrchestrator(BaseOrchestrator):
	def orchestrate(self, agents):
		# Logic điều phối
		pass
```

Tạo file `base_orchestrator.py` để định nghĩa class nền cho các orchestrator.