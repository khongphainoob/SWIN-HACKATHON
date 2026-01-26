# agents

Chứa các định nghĩa về chuyên gia AI như Planning Agent, Sentiment Agent, Reasoning Agent. Mỗi agent đảm nhận một vai trò chuyên biệt trong hệ thống.

## Sử dụng class base để kế thừa và phát triển

Nên định nghĩa một class trừu tượng (ví dụ: `BaseAgent`) để các agent chuyên biệt kế thừa và mở rộng.

### Ví dụ kế thừa
```python
from base_agent import BaseAgent

class PlanningAgent(BaseAgent):
	def plan(self, portfolio):
		# Logic lập kế hoạch đầu tư
		pass
```

Tạo file `base_agent.py` để định nghĩa class nền cho các agent.