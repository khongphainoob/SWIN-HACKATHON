# memory

Quản lý ngữ cảnh, bao gồm Short-term Memory, Long-term Memory, và RAG (Retrieval-Augmented Generation).

## Sử dụng các class base để kế thừa và phát triển

Các class base được định nghĩa trong file `base_memory.py`:
- `BaseMemory`: class trừu tượng, định nghĩa các phương thức cơ bản (`store`, `retrieve`, `clear`).
- `ShortTermMemory`, `LongTermMemory`, `RAGMemory`: các class mẫu kế thừa từ `BaseMemory`.

### Ví dụ kế thừa
```python
from base_memory import BaseMemory

class CustomMemory(BaseMemory):
	def __init__(self):
		self.data = []

	def store(self, data):
		self.data.append(data)

	def retrieve(self, query=None):
		# Tùy chỉnh logic truy xuất
		return self.data

	def clear(self):
		self.data.clear()
```

Bạn có thể mở rộng các class này để tích hợp logic phù hợp với hệ thống Agentic AI.