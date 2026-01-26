# services

Kết nối hạ tầng như Gemini API, Vector Store. Đảm nhận việc tích hợp các dịch vụ bên ngoài vào hệ thống.

## Sử dụng class base để kế thừa và phát triển

Nên định nghĩa một class nền (ví dụ: `BaseService`) để các service chuyên biệt kế thừa và mở rộng.

### Ví dụ kế thừa
```python
from base_service import BaseService

class GeminiAPIService(BaseService):
	def connect(self):
		# Logic kết nối API
		pass
```

Tạo file `base_service.py` để định nghĩa class nền cho các service.