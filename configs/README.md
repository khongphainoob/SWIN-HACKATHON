# configs

Chứa các file cấu hình cho Model, Tool, Protocol. Đảm bảo hệ thống hoạt động đúng và bảo mật.

## Sử dụng class base để kế thừa và phát triển

Nên định nghĩa một class nền (ví dụ: `BaseConfig`) để các loại cấu hình chuyên biệt kế thừa và mở rộng.

### Ví dụ kế thừa
```python
from base_config import BaseConfig

class ModelConfig(BaseConfig):
	def load(self):
		# Logic tải cấu hình
		pass
```

Tạo file `base_config.py` để định nghĩa class nền cho các loại cấu hình.